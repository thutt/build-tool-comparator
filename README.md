# build-tool-comparator

# Preface

There is a significant amount of discord about build tools.  For example:

  - Scons has perfect dependencies.

  - Bazel is hermetically sealed.

  - Make is old.

Many of the claims made about any particular build tool are often
entirely untrue (two of the three above, for example).  Adding to the
tribalization, it seems no one is interested in writing several build
processes for their software project.  Instead, the normal path is to
choose one and stick with it.  Conversions to another build tool,
even, are rarely done because such work is notoriously difficult.

Irrespective the build tool used, the quality of the result is
directly related to the strength of the team writing and maintaining
it.  However, there are immutable properties that must be accepted
with each tool: overheads, for example.  These overheads can be
measured and compared, allowing a well-informed person to make
reasoned decisions about a build tool, rather than solely relying
on tribalized hype.

The goal of this project is to provide information about the
_out-of-the-box_ experience for each tool.  Simple options that
broadly improve a tools behavior can be included here.  However,
options or additional programs & systems that require a deep
appreciation of the whole of the tool are rejected as decidedly
__not__ _out-of-the-box_.

# What is a Build Tool and Build Process / System?

A _build tool_ is a utility that reads and executes the rules
contained in a _build process_.  These rules in the _build process_
turn product source code into product deliverables.  In general, the
_build tool_ is a third party program.  The _build process_, however,
is written and maintained by the team creating the product.  The
intermediate files produced on the way to making the final
deliverables, and the final deliverables themselves are referred to as
_build artifacts_.

_Build process_ and _build system_ are generally regarded as synonyms.

A build process exists to turn product sources into product artifacts.
It accomplishes this by implicitly defining a directed acyclic graph
(DAG) of the product specification (in Makefiles, for example).  The
product specification associates source files with artifacts (object
files & executables, documentation, etc.), and the commands needed to
transform the former into the latter.  These commands collective are
sometimes called a _rule_.

Once the product specification is read, and the DAG created by the
_build tool_, it is traversed.  During traversal, any source file that
has changed since the last creation of its associated artifact (or if
the artifact doesn't exist) will cause the commands needed to
transform that source into an artifact to be executed.

In the case a C file (source) is newer than its associated object
file, the compiler would be invoked to create an up-to-date object
file (artifact).  In the case of an object file being newer than the
executable containing it, the linker will be invoked to create an
up-to-date executable.

Good build tools have properties sought by all developers, but are
all-too-often not actually achieved in practice.  These properties,
when present, make developers much more productive and happier.  A few
desirable properties are shown below:

 - Simple Invocation

   A tool should be simple to use, since it will be used dozens or
   hundreds of times a day.  It should as little hidden state as
   possible so that each invocation clearly shows how the build was
   produced.  Hidden state includes anything that is not visible at
   the point of invocation, such as default configuration files, shell
   environment variables.  This transparency is worthwhile because it
   reduces the mental load needed to understand the how a produced is
   produced is reduced.

 - Little time spent executing build tool

   The build tool needs to read the product specification, construct a
   DAG and execute rules to turn sources into artifacts.

   Some build tools have additional checking built-in.  This checking
   is the build tool equivalent of a type system in a programming
   language.  Stronger checking up front (when reasonable,
   understandable, errors are produced!) helps to ensure that the
   project is consistent, as specified, at all times.

 - Parallel execution of rules

   When projects have thousands of files, executing them serially will
   cause build times to be glacial.  Executing rules, unrelated to
   each other, in parallel generally reduces product builds.

 - Low resource overhead

   The fewer resources used by the build tool leaves more resources
   available to execute the commands that turn sources into artifacts.

 - Minimal work performed on each invocation.

   A build tool must only perform work necessary to bring out-of-date
   artifacts up-to-date, and nothing more, on each invocation.

   An artifact is out-of-date when it doesn't exist, its sources have
   changed, or its prerequisites have been rebuilt.  _Any_ work
   occurring that is __not__ creating an out-of-date artifact is
   unnecessary is a deficiency in the build process, and, possibly,
   the build tool.

 - Good error reporting

   There are two major classes of errors that can occur.

   1. Errors in the product definition.

      The build tool must be able to precisely report errors in the
      product definition, as appropriate for the tool.  By way of
      example, all build tools must correctly report cycles in the
      DAG.

   2. Errors occurring while building the product

      When an error occurs during the build, the tool should stop and
      faithfully reproduce the error displayed by the invoked tool.
      For example, a compiler error.

      If one of many subordinate processes executing in parallel
      returns a non-zero exit code to the build process, upon exiting
      the build tool should clearly denote the error from the
      subordinate process so that the user does not have to search
      through, possibly, many megabytes of logs to find the error.


This testing system is designed to facilitate objective comparison of
different build tools.  To accomplish this, it generates a set of
'source modules', 'interfaces', and product specifications for a
variety of different build tools.  These specifications can be used
to measure the time it takes to 'build' the described software using a
variety of build tools.

The 'modules' and 'interfaces' generated are not real software, and
nothing is actually 'built' in the traditional sense.  This is a
deliberate design decision undertaken to reduce the time-overhead of
actually invoking compilers or other tools.  Each artifact is brought
up-to-date with a simple application of the 'touch' utility.

# Using This Software

The current version of this software uses environment variables to
communicate information to the utilities.  This must be done using a
Bash shell.

## Configure Shell Environment

To configure your current shell, you must specify the following
information:

1. The _build output directory_ (BOD).  This is where all the build
   output will be placed.

2. The amount of parallelism desired in the builds.

3. The number of _files per directory_.  This controls the number of
   simulated module and interface files that are placed in a directory.

4. The number of simulated modules.

5. The size of the simulated modules.  This size will indirectly
   affect build speed for build tools that use checksums to determine
   if a file is changed.

6. The root location where the simulated modules should be written.

The information is set in the environment with a command like this:

```
cd <directory where this repository is cloned>
source setup \
  --bod /tmp/make/BOD \
  --parallel 4 \
  --files-per-dir 100 \
  --modules 1000 \
  --source /tmp/make/source
```

## Generating Build Processes

Once the environment has been configured (or changed) using with the
```setup``` tool, the build processes and software must be generated.
This is done with:

```
./scripts/generate.sh
```

## Producing The Report

To produce the report of all information stored in the metrics file,
you may execute:

```
./scripts/report.py --metrics ./metrics/metrics.json
```

## Running All Characterizations

To run all the characterizations, simply execute:

```
./scripts/runner.sh
```

If a build tool is not accessible through ${PATH}, it will not be
run.


## Running A Single Characterization

To run a single characterization, execute one of the following:

```
./scripts/build-bash.sh
```
```
./scripts/build-bazel.sh
```
```
./scripts/build-ninja.sh
```
```
./scripts/build-recursive-make.sh
```
```
./scripts/build-scons.sh
```
```
./scripts/build-single-make.sh
```

## Inducing An Incremental Build

To change one of the interface files, thereby inducing an incremental
build when characterizing a single build tool, execute the following:

```
./scripts/modify-most-used-interface.sh
```

Then re-execute the command (see above) to exercise the tool.

This will also collect metrics during the report and add them to the
metrics file.  The information collected will be added to the metrics
files based on the identify of your system (host os, amount of ram,
number of CPUs, etc.).   The data is suitable for inclusion in the
upstream repository, if you'd like to contribute.  It would be
interesting to see results for larger machines, as memory usage will
scale with the amount of parallelism being used.



# Tools Being Measured

## Make

Make is the oldest of the build tools.  The Make dialect used in this
project is Gnu Make.

### Pros
- Easy to start a project.
- Fast.
- Common.
- Simple enough to understand 95% of the tool, but capable enough to
  do everything you need.
- Plays well with other build tools.
- Pretty good documentation.
- Scales well to large projects in terms of build time.
- POSIX standard provides predictable cross platform behavior

### Cons

- Moderately complicated.
- Single global namespace.
- Minimal checking of input files.
- Undefined (eg: misspelled) variables have an empty value.
- Does not handle pathnames with embedded spaces well.
- Hidden state affecting build mostly through environment variables.
- Scales very poorly to large projects in terms of Makefile management.

## Scons

Scons is a build tool written in Python.  Possibly simpler to use
for those with no familiarity at all with Make.

### Pros

- Plays somewhat well with other build tools.
- Uses Python.
- Fairly good documentation.
- Scales well in terms of Scons code.
- Scales well to medium-sized projects in terms of speed.
- Scales moderately well to medium-sized projects in terms of disk usage overhead.

### Cons

- Moderately complicated.
- Hidden state affecting build via automatically used config files.
- Uses Python; people tend to treat it is a general purpose
  programming language, and not a builder of a DAG to build to
  product.  This causes work, that should be done only when
  _out-of-date_, to be done on every startup.
- Large projects have significant administrative overheads in time and disk space.
- Significant use of RAM for large projects.
- Significant use of disk space for large projects.

## Bazel

Bazel is the public version of Google's internal Blaze build tool,
without the secret sauce that makes it work well in their network.
Google made this tool to solve problems they have; you probably do not
have those problems.

Bazel claims to be fast & correct.  Correctness is not addressed by
this project, but speed claims and disk utilization certainly are.

### Pros

- Made by Google.
- Apparently large community.
- Continually being updated & changed; the tool is not abandoned.

### Cons

- Out-of-the-box resource use can make machine nearly unusable while building.
- In the worst case, out-of-the-box resource use can activate OOM killer.
- Extremely complicated.
- Does not play well with other build tools.
- Significant hidden state affecting build via automatically used config files.
- Very large number of command line options (eg: bazel help build|nl -ba)
- Bad, often incomplete or incorrect, documentation.
- Profligate use of disk space and other system resources.
- Not hermetic, though often claimed as such by enthusiasts.
- Continually being updated & changed; change isn't always positive.
- Bazel places all build output into four directories one level above
  the root directory of your sources.
- By default, these four build directories are symlinked to ~/.cache/bazel.


## Ninja

Ninja is a build system created by Google.  It is similar to Make, but
nearly all the useful features of Make have been removed in an effort
to make it fast.

### Pros

- Genuinely fast for many projects.
- Made by Google.

### Cons

- Made by Google.
- Syntax not suited to manual creation.
- Ninja files usually created by one of a coterie of preprocessors, each accepting a different domain specific language (DSL).
- Insignificantly faster than Make.

# Informational Results


The information below was collected by using the tool in this
repository to generate a set of simulated module files, interface
files, and build artifacts.  The build artifacts are dependent on
source files and interface files.  The build artifacts are created
using 'touch'.

The intention here is to be able to measure the overheads of the build
tool without the overhead of running compilers and other tools
normally needed to build software.  Because each tool is doing the
same thing, this gives a representative example of the base overhead
you will see if you use a particular build tool for your project.

## Note on Scons variants:
```
  By default, Scons uses md5sums to determine if files have changed.
  There is a simple option to have it use just timestamps, like make.
```

## Note on Make variants:
```
   Make has a lot of built-in suffix rules, and will automatically
   search them when deciding how a file should be built.  In many
   cases, these legacy-esque rules are not necessary and can be
   disabled, resulting in a faster build.  When these rules are
   disabled, the Makefile maintainer will have to supply the rules (or
   copy them from Make) needed to build the product.
```

# Results

The columns in the reports below are as follows:

```
  kind:  'full' means a full build of all files was produced.
         'incr' means only a few files needed to be re-created.
         'NULL' means no files needed to be re-created.
  secs:  Number of seconds consumed performing the build.
  mem :  The amount of memory used to perform the build.
  BOD :  The amount of disk space consumed by the build.
         Each 'module' produces just a single 0-byte file.
```

## Arm

```
arch        : aarch64
platform    : Linux-6.8.0-1018-raspi-aarch64-with-glibc2.39
version     : #20-Ubuntu SMP PREEMPT_DYNAMIC Fri Jan 17 12:35:36 UTC 2025
cpus        : 4
memory      : 7G
files/dir   : 100
module count: 50
parallelism : 4

  bash  [GNU bash, version 5.2.21(1)-release (aarch64-unknown-linux-gnu)]
    args: <no-args>
        2025/02/08 16:26:17|  kind: full  secs:    0.104  mem:  14M  BOD: 12K
        2025/02/08 16:26:17|  kind: incr  secs:    0.072  mem:  12M  BOD: 12K
        2025/02/08 16:26:17|  kind: NULL  secs:    0.021  mem:  14M  BOD: 12K

  bazel  [bazel 8.0.1]
    args: <no-args>
        2025/02/08 16:26:17|  kind: full  secs:   21.498  mem: 480M  BOD: 310M
        2025/02/08 16:26:43|  kind: incr  secs:    1.551  mem: 348M  BOD: 310M
        2025/02/08 16:26:49|  kind: NULL  secs:    0.792  mem: 503M  BOD: 310M

  recursive-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/08 16:26:54|  kind: full  secs:    0.073  mem:  14M  BOD: 12K
        2025/02/08 16:26:55|  kind: incr  secs:    0.051  mem:  12M  BOD: 12K
        2025/02/08 16:26:55|  kind: NULL  secs:    0.036  mem:  14M  BOD: 12K

  recursive-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/08 16:26:55|  kind: full  secs:    0.047  mem:  13M  BOD: 12K
        2025/02/08 16:26:55|  kind: incr  secs:    0.029  mem:  12M  BOD: 12K
        2025/02/08 16:26:55|  kind: NULL  secs:    0.009  mem:  13M  BOD: 12K

  single-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/08 16:26:55|  kind: full  secs:    0.067  mem:  14M  BOD: 12K
        2025/02/08 16:26:56|  kind: incr  secs:    0.047  mem:  12M  BOD: 12K
        2025/02/08 16:26:56|  kind: NULL  secs:    0.033  mem:  14M  BOD: 12K

  single-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/08 16:26:56|  kind: full  secs:    0.041  mem:  14M  BOD: 12K
        2025/02/08 16:26:56|  kind: incr  secs:    0.027  mem:  12M  BOD: 12K
        2025/02/08 16:26:56|  kind: NULL  secs:    0.006  mem:  14M  BOD: 12K

  scons-md5sum  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/08 16:26:56|  kind: full  secs:    0.392  mem:  27M  BOD: 52K
        2025/02/08 16:26:57|  kind: incr  secs:    0.382  mem:  26M  BOD: 52K
        2025/02/08 16:26:58|  kind: NULL  secs:    0.331  mem:  27M  BOD: 52K

  scons-make  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/08 16:26:58|  kind: full  secs:    0.355  mem:  25M  BOD: 44K
        2025/02/08 16:26:59|  kind: incr  secs:    0.301  mem:  25M  BOD: 44K
        2025/02/08 16:27:00|  kind: NULL  secs:    0.300  mem:  25M  BOD: 44K


arch        : aarch64
platform    : Linux-6.8.0-1018-raspi-aarch64-with-glibc2.39
version     : #20-Ubuntu SMP PREEMPT_DYNAMIC Fri Jan 17 12:35:36 UTC 2025
cpus        : 4
memory      : 7G
files/dir   : 100
module count: 100
parallelism : 4

  bash  [GNU bash, version 5.2.21(1)-release (aarch64-unknown-linux-gnu)]
    args: <no-args>
        2025/02/08 16:27:00|  kind: full  secs:    0.203  mem:  13M  BOD: 12K
        2025/02/08 16:27:01|  kind: incr  secs:    0.128  mem:  12M  BOD: 12K
        2025/02/08 16:27:01|  kind: NULL  secs:    0.041  mem:  13M  BOD: 12K

  bazel  [bazel 8.0.1]
    args: <no-args>
        2025/02/08 16:27:01|  kind: full  secs:   21.575  mem: 506M  BOD: 310M
        2025/02/08 16:27:27|  kind: incr  secs:    1.940  mem: 387M  BOD: 310M
        2025/02/08 16:27:32|  kind: NULL  secs:    0.835  mem: 518M  BOD: 310M

  recursive-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/08 16:27:38|  kind: full  secs:    0.130  mem:  13M  BOD: 12K
        2025/02/08 16:27:38|  kind: incr  secs:    0.098  mem:  12M  BOD: 12K
        2025/02/08 16:27:39|  kind: NULL  secs:    0.070  mem:  13M  BOD: 12K

  recursive-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/08 16:27:39|  kind: full  secs:    0.081  mem:  13M  BOD: 12K
        2025/02/08 16:27:39|  kind: incr  secs:    0.044  mem:  12M  BOD: 12K
        2025/02/08 16:27:39|  kind: NULL  secs:    0.012  mem:  13M  BOD: 12K

  single-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/08 16:27:39|  kind: full  secs:    0.134  mem:  13M  BOD: 12K
        2025/02/08 16:27:40|  kind: incr  secs:    0.097  mem:  12M  BOD: 12K
        2025/02/08 16:27:40|  kind: NULL  secs:    0.066  mem:  13M  BOD: 12K

  single-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/08 16:27:40|  kind: full  secs:    0.076  mem:  13M  BOD: 12K
        2025/02/08 16:27:40|  kind: incr  secs:    0.040  mem:  12M  BOD: 12K
        2025/02/08 16:27:40|  kind: NULL  secs:    0.008  mem:  13M  BOD: 12K

  scons-md5sum  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/08 16:27:41|  kind: full  secs:    0.540  mem:  28M  BOD: 92K
        2025/02/08 16:27:41|  kind: incr  secs:    0.486  mem:  28M  BOD: 92K
        2025/02/08 16:27:42|  kind: NULL  secs:    0.431  mem:  28M  BOD: 92K

  scons-make  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/08 16:27:43|  kind: full  secs:    0.487  mem:  27M  BOD: 80K
        2025/02/08 16:27:44|  kind: incr  secs:    0.397  mem:  27M  BOD: 80K
        2025/02/08 16:27:44|  kind: NULL  secs:    0.372  mem:  27M  BOD: 80K


arch        : aarch64
platform    : Linux-6.8.0-1018-raspi-aarch64-with-glibc2.39
version     : #20-Ubuntu SMP PREEMPT_DYNAMIC Fri Jan 17 12:35:36 UTC 2025
cpus        : 4
memory      : 7G
files/dir   : 100
module count: 1000
parallelism : 4

  bash  [GNU bash, version 5.2.21(1)-release (aarch64-unknown-linux-gnu)]
    args: <no-args>
        2025/02/08 16:27:45|  kind: full  secs:    2.047  mem:  15M  BOD: 48K
        2025/02/08 16:27:48|  kind: incr  secs:    0.680  mem:  12M  BOD: 48K
        2025/02/08 16:27:49|  kind: NULL  secs:    0.467  mem:  15M  BOD: 48K

  bazel  [bazel 8.0.1]
    args: <no-args>
        2025/02/08 16:27:49|  kind: full  secs:   31.739  mem: 537M  BOD: 310M
        2025/02/08 16:28:26|  kind: incr  secs:    3.326  mem: 429M  BOD: 310M
        2025/02/08 16:28:32|  kind: NULL  secs:    1.211  mem: 571M  BOD: 310M

  recursive-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/08 16:28:37|  kind: full  secs:    1.846  mem:  15M  BOD: 48K
        2025/02/08 16:28:41|  kind: incr  secs:    1.081  mem:  12M  BOD: 48K
        2025/02/08 16:28:42|  kind: NULL  secs:    0.994  mem:  15M  BOD: 48K

  recursive-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/08 16:28:43|  kind: full  secs:    0.689  mem:  15M  BOD: 48K
        2025/02/08 16:28:44|  kind: incr  secs:    0.102  mem:  12M  BOD: 48K
        2025/02/08 16:28:45|  kind: NULL  secs:    0.036  mem:  15M  BOD: 48K

  single-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/08 16:28:45|  kind: full  secs:    1.692  mem:  25M  BOD: 48K
        2025/02/08 16:28:47|  kind: incr  secs:    1.090  mem:  21M  BOD: 48K
        2025/02/08 16:28:49|  kind: NULL  secs:    1.007  mem:  25M  BOD: 48K

  single-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/08 16:28:50|  kind: full  secs:    0.711  mem:  15M  BOD: 48K
        2025/02/08 16:28:51|  kind: incr  secs:    0.107  mem:  12M  BOD: 48K
        2025/02/08 16:28:51|  kind: NULL  secs:    0.041  mem:  15M  BOD: 48K

  scons-md5sum  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/08 16:28:52|  kind: full  secs:    3.532  mem:  61M  BOD: 1M
        2025/02/08 16:28:56|  kind: incr  secs:    2.584  mem:  62M  BOD: 1M
        2025/02/08 16:28:59|  kind: NULL  secs:    2.420  mem:  62M  BOD: 1M

  scons-make  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/08 16:29:02|  kind: full  secs:    2.951  mem:  61M  BOD: 1020K
        2025/02/08 16:29:06|  kind: incr  secs:    1.968  mem:  61M  BOD: 1020K
        2025/02/08 16:29:08|  kind: NULL  secs:    1.832  mem:  61M  BOD: 1020K


arch        : aarch64
platform    : Linux-6.8.0-1018-raspi-aarch64-with-glibc2.39
version     : #20-Ubuntu SMP PREEMPT_DYNAMIC Fri Jan 17 12:35:36 UTC 2025
cpus        : 4
memory      : 7G
files/dir   : 100
module count: 5000
parallelism : 4

  bash  [GNU bash, version 5.2.21(1)-release (aarch64-unknown-linux-gnu)]
    args: <no-args>
        2025/02/08 16:29:10|  kind: full  secs:   10.396  mem:  18M  BOD: 208K
        2025/02/08 16:29:24|  kind: incr  secs:    2.799  mem:  12M  BOD: 208K
        2025/02/08 16:29:27|  kind: NULL  secs:    2.502  mem:  18M  BOD: 208K

  bazel  [bazel 8.0.1]
    args: <no-args>
        2025/02/08 16:29:30|  kind: full  secs:   79.474  mem: 738M  BOD: 312M
        2025/02/08 16:30:56|  kind: incr  secs:    6.162  mem: 621M  BOD: 312M
        2025/02/08 16:31:06|  kind: NULL  secs:    1.715  mem: 756M  BOD: 312M

  recursive-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/08 16:31:12|  kind: full  secs:   17.887  mem:  21M  BOD: 208K
        2025/02/08 16:31:34|  kind: incr  secs:   12.443  mem:  21M  BOD: 208K
        2025/02/08 16:31:46|  kind: NULL  secs:   12.487  mem:  21M  BOD: 208K

  recursive-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/08 16:31:59|  kind: full  secs:    3.522  mem:  18M  BOD: 208K
        2025/02/08 16:32:07|  kind: incr  secs:    0.301  mem:  12M  BOD: 208K
        2025/02/08 16:32:07|  kind: NULL  secs:    0.191  mem:  18M  BOD: 208K

  single-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/08 16:32:08|  kind: full  secs:   12.680  mem: 119M  BOD: 208K
        2025/02/08 16:32:25|  kind: incr  secs:    9.311  mem:  96M  BOD: 208K
        2025/02/08 16:32:34|  kind: NULL  secs:    9.088  mem: 119M  BOD: 208K

  single-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/08 16:32:44|  kind: full  secs:    3.628  mem:  36M  BOD: 208K
        2025/02/08 16:32:52|  kind: incr  secs:    0.317  mem:  13M  BOD: 208K
        2025/02/08 16:32:53|  kind: NULL  secs:    0.214  mem:  36M  BOD: 208K

  scons-md5sum  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/08 16:32:53|  kind: full  secs:   18.262  mem: 203M  BOD: 10M
        2025/02/08 16:33:15|  kind: incr  secs:   12.864  mem: 205M  BOD: 10M
        2025/02/08 16:33:29|  kind: NULL  secs:   12.837  mem: 205M  BOD: 10M

  scons-make  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/08 16:33:42|  kind: full  secs:   15.072  mem: 203M  BOD: 7M
        2025/02/08 16:34:01|  kind: incr  secs:    9.843  mem: 202M  BOD: 7M
        2025/02/08 16:34:11|  kind: NULL  secs:    9.504  mem: 203M  BOD: 7M


arch        : aarch64
platform    : Linux-6.8.0-1018-raspi-aarch64-with-glibc2.39
version     : #20-Ubuntu SMP PREEMPT_DYNAMIC Fri Jan 17 12:35:36 UTC 2025
cpus        : 4
memory      : 7G
files/dir   : 100
module count: 10000
parallelism : 4

  bash  [GNU bash, version 5.2.21(1)-release (aarch64-unknown-linux-gnu)]
    args: <no-args>
        2025/02/08 16:34:21|  kind: full  secs:   21.186  mem:  23M  BOD: 408K
        2025/02/08 16:35:05|  kind: incr  secs:    5.582  mem:  12M  BOD: 408K
        2025/02/08 16:35:11|  kind: NULL  secs:    5.058  mem:  23M  BOD: 408K

  bazel  [bazel 8.0.1]
    args: <no-args>
        2025/02/08 16:35:17|  kind: full  secs:  128.591  mem:   1G  BOD: 314M
        2025/02/08 16:37:47|  kind: incr  secs:    7.660  mem: 931M  BOD: 313M
        2025/02/08 16:37:58|  kind: NULL  secs:    2.168  mem:   1G  BOD: 313M

  recursive-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/08 16:38:03|  kind: full  secs:   40.008  mem:  23M  BOD: 408K
        2025/02/08 16:39:02|  kind: incr  secs:   28.987  mem:  23M  BOD: 408K
        2025/02/08 16:39:31|  kind: NULL  secs:   28.901  mem:  23M  BOD: 408K

  recursive-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/08 16:40:00|  kind: full  secs:    7.204  mem:  23M  BOD: 408K
        2025/02/08 16:40:27|  kind: incr  secs:    0.550  mem:  12M  BOD: 408K
        2025/02/08 16:40:28|  kind: NULL  secs:    0.413  mem:  23M  BOD: 408K

  single-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/08 16:40:28|  kind: full  secs:   30.666  mem: 238M  BOD: 408K
        2025/02/08 16:41:18|  kind: incr  secs:   23.592  mem: 191M  BOD: 408K
        2025/02/08 16:41:41|  kind: NULL  secs:   23.268  mem: 238M  BOD: 408K

  single-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/08 16:42:05|  kind: full  secs:    7.519  mem:  72M  BOD: 408K
        2025/02/08 16:42:31|  kind: incr  secs:    0.612  mem:  24M  BOD: 408K
        2025/02/08 16:42:32|  kind: NULL  secs:    0.486  mem:  72M  BOD: 408K

  scons-md5sum  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/08 16:42:33|  kind: full  secs:   38.531  mem: 384M  BOD: 25M
        2025/02/08 16:43:31|  kind: incr  secs:   26.685  mem: 387M  BOD: 25M
        2025/02/08 16:43:58|  kind: NULL  secs:   26.424  mem: 388M  BOD: 25M

  scons-make  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/08 16:44:24|  kind: full  secs:   30.841  mem: 384M  BOD: 17M
        2025/02/08 16:45:14|  kind: incr  secs:   20.758  mem: 381M  BOD: 17M
        2025/02/08 16:45:35|  kind: NULL  secs:   20.289  mem: 384M  BOD: 17M


arch        : aarch64
platform    : Linux-6.8.0-1018-raspi-aarch64-with-glibc2.39
version     : #20-Ubuntu SMP PREEMPT_DYNAMIC Fri Jan 17 12:35:36 UTC 2025
cpus        : 4
memory      : 7G
files/dir   : 100
module count: 50000
parallelism : 4

  bash  [GNU bash, version 5.2.21(1)-release (aarch64-unknown-linux-gnu)]
    args: <no-args>
        2025/02/08 16:45:56|  kind: full  secs:  103.892  mem:  56M  BOD: 1M
        2025/02/08 16:52:00|  kind: incr  secs:   26.748  mem:  12M  BOD: 1M
        2025/02/08 16:52:27|  kind: NULL  secs:   26.050  mem:  56M  BOD: 1M

  bazel  [bazel 8.0.1]
    args: <no-args>
        2025/02/08 16:52:54|  kind: full  secs:  501.612  mem:   1G  BOD: 326M
        2025/02/08 17:05:50|  kind: incr  secs:   36.115  mem:   1G  BOD: 323M
        2025/02/08 17:06:31|  kind: NULL  secs:    9.538  mem:   2G  BOD: 323M

  recursive-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/08 17:06:42|  kind: full  secs:  236.995  mem:  56M  BOD: 1M
        2025/02/08 17:15:03|  kind: incr  secs:  182.038  mem:  27M  BOD: 1M
        2025/02/08 17:18:05|  kind: NULL  secs:  181.508  mem:  56M  BOD: 1M

  recursive-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/08 17:21:07|  kind: full  secs:   36.513  mem:  56M  BOD: 1M
        2025/02/08 17:26:26|  kind: incr  secs:    2.670  mem:  12M  BOD: 1M
        2025/02/08 17:26:29|  kind: NULL  secs:    2.287  mem:  56M  BOD: 1M

  single-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/08 17:26:31|  kind: full  secs:   98.354  mem:   1G  BOD: 1M
        2025/02/08 17:32:33|  kind: incr  secs:   63.125  mem: 936M  BOD: 1M
        2025/02/08 17:33:36|  kind: NULL  secs:   62.166  mem:   1G  BOD: 1M

  single-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/08 17:34:39|  kind: full  secs:   39.351  mem: 363M  BOD: 1M
        2025/02/08 17:40:17|  kind: incr  secs:    4.476  mem: 116M  BOD: 1M
        2025/02/08 17:40:21|  kind: NULL  secs:    3.412  mem: 363M  BOD: 1M

  scons-md5sum  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/08 17:40:25|  kind: full  secs:  301.629  mem:   1G  BOD: 150M
        2025/02/08 17:49:49|  kind: incr  secs:  227.252  mem:   1G  BOD: 150M
        2025/02/08 17:53:36|  kind: NULL  secs:  223.452  mem:   1G  BOD: 150M

  scons-make  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/08 17:57:20|  kind: full  secs:  168.000  mem:   1G  BOD: 105M
        2025/02/08 18:04:32|  kind: incr  secs:  110.946  mem:   1G  BOD: 105M
        2025/02/08 18:06:23|  kind: NULL  secs:  107.545  mem:   1G  BOD: 105M


arch        : aarch64
platform    : Linux-6.8.0-1018-raspi-aarch64-with-glibc2.39
version     : #20-Ubuntu SMP PREEMPT_DYNAMIC Fri Jan 17 12:35:36 UTC 2025
cpus        : 4
memory      : 7G
files/dir   : 100
module count: 100000
parallelism : 4

  bash  [GNU bash, version 5.2.21(1)-release (aarch64-unknown-linux-gnu)]
    args: <no-args>
        2025/02/08 18:08:11|  kind: full  secs:  207.386  mem:  98M  BOD: 3M
        2025/02/08 18:21:40|  kind: incr  secs:   54.473  mem:  12M  BOD: 3M
        2025/02/08 18:22:35|  kind: NULL  secs:   52.695  mem:  98M  BOD: 3M

  bazel  [bazel 8.0.1]
    args: <no-args>
        2025/02/08 18:23:28|  kind: full  secs: 1105.608  mem:   2G  BOD: 341M
        2025/02/08 18:53:37|  kind: incr  secs:  140.940  mem:   2G  BOD: 335M
        2025/02/08 18:56:03|  kind: NULL  secs:   14.877  mem:   2G  BOD: 335M

  recursive-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/08 18:56:24|  kind: full  secs:  502.662  mem:  98M  BOD: 3M
        2025/02/08 19:15:24|  kind: incr  secs:  395.652  mem:  31M  BOD: 3M
        2025/02/08 19:22:00|  kind: NULL  secs:  392.445  mem:  98M  BOD: 3M

  recursive-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/08 19:28:33|  kind: full  secs:   72.391  mem:  98M  BOD: 3M
        2025/02/08 19:40:25|  kind: incr  secs:    5.894  mem:  12M  BOD: 3M
        2025/02/08 19:40:31|  kind: NULL  secs:    5.168  mem:  98M  BOD: 3M

  single-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/08 19:40:37|  kind: full  secs:  205.583  mem:   2G  BOD: 3M
        2025/02/08 19:54:42|  kind: incr  secs:  137.804  mem:   1G  BOD: 3M
        2025/02/08 19:57:00|  kind: NULL  secs:  134.175  mem:   2G  BOD: 3M

  single-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/08 19:59:14|  kind: full  secs:   79.144  mem: 730M  BOD: 3M
        2025/02/08 20:11:28|  kind: incr  secs:   10.126  mem: 230M  BOD: 3M
        2025/02/08 20:11:38|  kind: NULL  secs:    7.781  mem: 730M  BOD: 3M

  scons-md5sum  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/08 20:11:46|  kind: full  secs:  722.993  mem:   3G  BOD: 312M
        2025/02/08 20:34:21|  kind: incr  secs:  562.694  mem:   3G  BOD: 312M
        2025/02/08 20:43:45|  kind: NULL  secs:  594.918  mem:   3G  BOD: 312M

  scons-make  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/08 20:53:40|  kind: full  secs:  329.100  mem:   3G  BOD: 219M
        2025/02/08 21:10:31|  kind: incr  secs:  223.063  mem:   3G  BOD: 219M
        2025/02/08 21:14:14|  kind: NULL  secs:  217.003  mem:   3G  BOD: 219M
```

## x86_64

```


arch        : x86_64
platform    : Linux-6.8.0-48-generic-x86_64-with-glibc2.39
version     : #48~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Mon Oct  7 11:24:13 UTC 2
cpus        : 4
memory      : 7G
files/dir   : 100
module count: 50
parallelism : 4

  bash  [GNU bash, version 5.1.16(1)-release (x86_64-pc-linux-gnu)]
    args: <no-args>
        2025/02/08 21:48:06|  kind: full  secs:    0.155  mem:  15M  BOD: 12K
        2025/02/08 21:48:07|  kind: incr  secs:    0.100  mem:  14M  BOD: 12K
        2025/02/08 21:48:07|  kind: NULL  secs:    0.037  mem:  14M  BOD: 12K

  bazel  [bazel no_version]
    args: <no-args>
        2025/02/08 21:48:07|  kind: full  secs:    9.846  mem: 232M  BOD: 6M
        2025/02/08 21:48:18|  kind: incr  secs:    0.960  mem: 233M  BOD: 10M
        2025/02/08 21:48:23|  kind: NULL  secs:    0.378  mem: 236M  BOD: 9M

  recursive-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/08 21:48:28|  kind: full  secs:    0.115  mem:  15M  BOD: 12K
        2025/02/08 21:48:29|  kind: incr  secs:    0.090  mem:  14M  BOD: 12K
        2025/02/08 21:48:29|  kind: NULL  secs:    0.063  mem:  14M  BOD: 12K

  recursive-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/08 21:48:29|  kind: full  secs:    0.070  mem:  15M  BOD: 12K
        2025/02/08 21:48:30|  kind: incr  secs:    0.043  mem:  14M  BOD: 12K
        2025/02/08 21:48:30|  kind: NULL  secs:    0.014  mem:  14M  BOD: 12K

  single-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/08 21:48:30|  kind: full  secs:    0.114  mem:  15M  BOD: 12K
        2025/02/08 21:48:31|  kind: incr  secs:    0.087  mem:  14M  BOD: 12K
        2025/02/08 21:48:31|  kind: NULL  secs:    0.059  mem:  14M  BOD: 12K

  single-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/08 21:48:31|  kind: full  secs:    0.069  mem:  15M  BOD: 12K
        2025/02/08 21:48:32|  kind: incr  secs:    0.040  mem:  14M  BOD: 12K
        2025/02/08 21:48:32|  kind: NULL  secs:    0.011  mem:  14M  BOD: 12K

  scons-md5sum  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/08 21:48:32|  kind: full  secs:    0.860  mem:  29M  BOD: 52K
        2025/02/08 21:48:34|  kind: incr  secs:    0.770  mem:  29M  BOD: 52K
        2025/02/08 21:48:35|  kind: NULL  secs:    0.710  mem:  29M  BOD: 52K

  scons-make  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/08 21:48:36|  kind: full  secs:    0.769  mem:  28M  BOD: 44K
        2025/02/08 21:48:38|  kind: incr  secs:    0.671  mem:  28M  BOD: 44K
        2025/02/08 21:48:39|  kind: NULL  secs:    0.664  mem:  28M  BOD: 44K


arch        : x86_64
platform    : Linux-6.8.0-48-generic-x86_64-with-glibc2.39
version     : #48~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Mon Oct  7 11:24:13 UTC 2
cpus        : 4
memory      : 7G
files/dir   : 100
module count: 100
parallelism : 4

  bash  [GNU bash, version 5.1.16(1)-release (x86_64-pc-linux-gnu)]
    args: <no-args>
        2025/02/08 21:48:40|  kind: full  secs:    0.274  mem:  15M  BOD: 12K
        2025/02/08 21:48:41|  kind: incr  secs:    0.182  mem:  14M  BOD: 12K
        2025/02/08 21:48:41|  kind: NULL  secs:    0.075  mem:  14M  BOD: 12K

  bazel  [bazel no_version]
    args: <no-args>
        2025/02/08 21:48:42|  kind: full  secs:   10.463  mem: 252M  BOD: 15M
        2025/02/08 21:48:57|  kind: incr  secs:    1.331  mem: 249M  BOD: 21M
        2025/02/08 21:49:03|  kind: NULL  secs:    0.410  mem: 249M  BOD: 20M

  recursive-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/08 21:49:08|  kind: full  secs:    0.232  mem:  15M  BOD: 12K
        2025/02/08 21:49:09|  kind: incr  secs:    0.173  mem:  14M  BOD: 12K
        2025/02/08 21:49:09|  kind: NULL  secs:    0.123  mem:  14M  BOD: 12K

  recursive-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/08 21:49:09|  kind: full  secs:    0.126  mem:  15M  BOD: 12K
        2025/02/08 21:49:10|  kind: incr  secs:    0.076  mem:  14M  BOD: 12K
        2025/02/08 21:49:10|  kind: NULL  secs:    0.019  mem:  14M  BOD: 12K

  single-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/08 21:49:10|  kind: full  secs:    0.231  mem:  15M  BOD: 12K
        2025/02/08 21:49:11|  kind: incr  secs:    0.178  mem:  14M  BOD: 12K
        2025/02/08 21:49:11|  kind: NULL  secs:    0.123  mem:  14M  BOD: 12K

  single-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/08 21:49:12|  kind: full  secs:    0.118  mem:  15M  BOD: 12K
        2025/02/08 21:49:12|  kind: incr  secs:    0.061  mem:  14M  BOD: 12K
        2025/02/08 21:49:13|  kind: NULL  secs:    0.013  mem:  14M  BOD: 12K

  scons-md5sum  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/08 21:49:13|  kind: full  secs:    1.160  mem:  30M  BOD: 92K
        2025/02/08 21:49:15|  kind: incr  secs:    1.039  mem:  30M  BOD: 92K
        2025/02/08 21:49:16|  kind: NULL  secs:    0.940  mem:  30M  BOD: 92K

  scons-make  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/08 21:49:18|  kind: full  secs:    1.063  mem:  30M  BOD: 80K
        2025/02/08 21:49:20|  kind: incr  secs:    0.975  mem:  30M  BOD: 80K
        2025/02/08 21:49:21|  kind: NULL  secs:    0.854  mem:  30M  BOD: 80K


arch        : x86_64
platform    : Linux-6.8.0-48-generic-x86_64-with-glibc2.39
version     : #48~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Mon Oct  7 11:24:13 UTC 2
cpus        : 4
memory      : 7G
files/dir   : 100
module count: 1000
parallelism : 4

  bash  [GNU bash, version 5.1.16(1)-release (x86_64-pc-linux-gnu)]
    args: <no-args>
        2025/02/08 21:49:23|  kind: full  secs:    2.854  mem:  16M  BOD: 48K
        2025/02/08 21:49:27|  kind: incr  secs:    1.108  mem:  14M  BOD: 48K
        2025/02/08 21:49:29|  kind: NULL  secs:    0.868  mem:  14M  BOD: 48K

  bazel  [bazel no_version]
    args: <no-args>
        2025/02/08 21:49:30|  kind: full  secs:   28.168  mem: 298M  BOD: 193M
        2025/02/08 21:50:02|  kind: incr  secs:    2.439  mem: 296M  BOD: 197M
        2025/02/08 21:50:07|  kind: NULL  secs:    0.576  mem: 301M  BOD: 196M

  recursive-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/08 21:50:13|  kind: full  secs:    2.879  mem:  16M  BOD: 48K
        2025/02/08 21:50:19|  kind: incr  secs:    1.947  mem:  14M  BOD: 48K
        2025/02/08 21:50:21|  kind: NULL  secs:    1.867  mem:  14M  BOD: 48K

  recursive-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/08 21:50:23|  kind: full  secs:    0.983  mem:  16M  BOD: 48K
        2025/02/08 21:50:26|  kind: incr  secs:    0.151  mem:  14M  BOD: 48K
        2025/02/08 21:50:26|  kind: NULL  secs:    0.060  mem:  14M  BOD: 48K

  single-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/08 21:50:27|  kind: full  secs:    3.191  mem:  25M  BOD: 48K
        2025/02/08 21:50:32|  kind: incr  secs:    2.250  mem:  22M  BOD: 48K
        2025/02/08 21:50:34|  kind: NULL  secs:    2.105  mem:  21M  BOD: 48K

  single-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/08 21:50:36|  kind: full  secs:    1.089  mem:  16M  BOD: 48K
        2025/02/08 21:50:40|  kind: incr  secs:    0.166  mem:  14M  BOD: 48K
        2025/02/08 21:50:40|  kind: NULL  secs:    0.068  mem:  14M  BOD: 48K

  scons-md5sum  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/08 21:50:40|  kind: full  secs:    7.617  mem:  64M  BOD: 1M
        2025/02/08 21:50:50|  kind: incr  secs:    5.691  mem:  64M  BOD: 1M
        2025/02/08 21:50:56|  kind: NULL  secs:    5.367  mem:  64M  BOD: 1M

  scons-make  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/08 21:51:02|  kind: full  secs:    6.832  mem:  63M  BOD: 1020K
        2025/02/08 21:51:11|  kind: incr  secs:    4.954  mem:  64M  BOD: 1020K
        2025/02/08 21:51:17|  kind: NULL  secs:    4.623  mem:  63M  BOD: 1020K


arch        : x86_64
platform    : Linux-6.8.0-48-generic-x86_64-with-glibc2.39
version     : #48~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Mon Oct  7 11:24:13 UTC 2
cpus        : 4
memory      : 7G
files/dir   : 100
module count: 5000
parallelism : 4

  bash  [GNU bash, version 5.1.16(1)-release (x86_64-pc-linux-gnu)]
    args: <no-args>
        2025/02/08 21:51:22|  kind: full  secs:   13.955  mem:  20M  BOD: 208K
        2025/02/08 21:51:44|  kind: incr  secs:    4.931  mem:  14M  BOD: 208K
        2025/02/08 21:51:49|  kind: NULL  secs:    4.517  mem:  14M  BOD: 208K

  bazel  [bazel no_version]
    args: <no-args>
        2025/02/08 21:51:54|  kind: full  secs:   78.255  mem: 440M  BOD: 1G
        2025/02/08 21:53:29|  kind: incr  secs:    4.325  mem: 436M  BOD: 1G
        2025/02/08 21:53:40|  kind: NULL  secs:    1.126  mem: 438M  BOD: 1G

  recursive-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/08 21:53:45|  kind: full  secs:   29.210  mem:  22M  BOD: 208K
        2025/02/08 21:54:34|  kind: incr  secs:   22.385  mem:  21M  BOD: 208K
        2025/02/08 21:54:57|  kind: NULL  secs:   22.321  mem:  21M  BOD: 208K

  recursive-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/08 21:55:19|  kind: full  secs:    4.887  mem:  20M  BOD: 208K
        2025/02/08 21:55:34|  kind: incr  secs:    0.460  mem:  14M  BOD: 208K
        2025/02/08 21:55:34|  kind: NULL  secs:    0.323  mem:  14M  BOD: 208K

  single-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/08 21:55:35|  kind: full  secs:   29.927  mem: 119M  BOD: 208K
        2025/02/08 21:56:14|  kind: incr  secs:   24.907  mem:  96M  BOD: 208K
        2025/02/08 21:56:39|  kind: NULL  secs:   24.553  mem:  96M  BOD: 208K

  single-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/08 21:57:04|  kind: full  secs:    5.734  mem:  37M  BOD: 208K
        2025/02/08 21:57:18|  kind: incr  secs:    0.571  mem:  14M  BOD: 208K
        2025/02/08 21:57:19|  kind: NULL  secs:    0.418  mem:  14M  BOD: 208K

  scons-md5sum  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/08 21:57:20|  kind: full  secs:   38.519  mem: 206M  BOD: 10M
        2025/02/08 21:58:08|  kind: incr  secs:   28.109  mem: 208M  BOD: 10M
        2025/02/08 21:58:37|  kind: NULL  secs:   27.579  mem: 208M  BOD: 10M

  scons-make  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/08 21:59:05|  kind: full  secs:   34.696  mem: 206M  BOD: 7M
        2025/02/08 21:59:49|  kind: incr  secs:   24.203  mem: 204M  BOD: 7M
        2025/02/08 22:00:14|  kind: NULL  secs:   23.574  mem: 204M  BOD: 7M


arch        : x86_64
platform    : Linux-6.8.0-48-generic-x86_64-with-glibc2.39
version     : #48~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Mon Oct  7 11:24:13 UTC 2
cpus        : 4
memory      : 7G
files/dir   : 100
module count: 10000
parallelism : 4

  bash  [GNU bash, version 5.1.16(1)-release (x86_64-pc-linux-gnu)]
    args: <no-args>
        2025/02/08 22:00:38|  kind: full  secs:   28.043  mem:  24M  BOD: 408K
        2025/02/08 22:01:23|  kind: incr  secs:    9.665  mem:  14M  BOD: 408K
        2025/02/08 22:01:33|  kind: NULL  secs:    9.157  mem:  14M  BOD: 408K

  bazel  [bazel no_version]
    args: <no-args>
        2025/02/08 22:01:43|  kind: full  secs:  136.637  mem: 606M  BOD: 2G
        2025/02/08 22:04:38|  kind: incr  secs:    5.103  mem: 545M  BOD: 2G
        2025/02/08 22:04:54|  kind: NULL  secs:    1.632  mem: 545M  BOD: 2G

  recursive-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/08 22:05:04|  kind: full  secs:   63.980  mem:  24M  BOD: 408K
        2025/02/08 22:06:49|  kind: incr  secs:   51.585  mem:  23M  BOD: 408K
        2025/02/08 22:07:41|  kind: NULL  secs:   51.354  mem:  23M  BOD: 408K

  recursive-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/08 22:08:33|  kind: full  secs:   10.069  mem:  24M  BOD: 408K
        2025/02/08 22:09:01|  kind: incr  secs:    0.846  mem:  14M  BOD: 408K
        2025/02/08 22:09:02|  kind: NULL  secs:    0.679  mem:  14M  BOD: 408K

  single-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/08 22:09:03|  kind: full  secs:   72.376  mem: 239M  BOD: 408K
        2025/02/08 22:10:34|  kind: incr  secs:   61.843  mem: 191M  BOD: 408K
        2025/02/08 22:11:36|  kind: NULL  secs:   61.327  mem: 191M  BOD: 408K

  single-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/08 22:12:38|  kind: full  secs:   11.285  mem:  72M  BOD: 408K
        2025/02/08 22:13:07|  kind: incr  secs:    1.131  mem:  25M  BOD: 408K
        2025/02/08 22:13:09|  kind: NULL  secs:    0.952  mem:  24M  BOD: 408K

  scons-md5sum  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/08 22:13:10|  kind: full  secs:   78.252  mem: 386M  BOD: 25M
        2025/02/08 22:14:47|  kind: incr  secs:   57.336  mem: 390M  BOD: 25M
        2025/02/08 22:15:45|  kind: NULL  secs:   56.835  mem: 390M  BOD: 25M

  scons-make  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/08 22:16:42|  kind: full  secs:   70.239  mem: 386M  BOD: 17M
        2025/02/08 22:18:11|  kind: incr  secs:   49.869  mem: 383M  BOD: 17M
        2025/02/08 22:19:01|  kind: NULL  secs:   48.962  mem: 383M  BOD: 17M


arch        : x86_64
platform    : Linux-6.8.0-48-generic-x86_64-with-glibc2.39
version     : #48~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Mon Oct  7 11:24:13 UTC 2
cpus        : 4
memory      : 7G
files/dir   : 100
module count: 50000
parallelism : 4

  bash  [GNU bash, version 5.1.16(1)-release (x86_64-pc-linux-gnu)]
    args: <no-args>
        2025/02/08 22:19:51|  kind: full  secs:  138.910  mem:  58M  BOD: 1M
        2025/02/08 22:24:49|  kind: incr  secs:   49.675  mem:  14M  BOD: 1M
        2025/02/08 22:25:39|  kind: NULL  secs:   47.133  mem:  14M  BOD: 1M

  bazel  [bazel no_version]
    args: <no-args>
        2025/02/08 22:26:27|  kind: full  secs:  663.045  mem:   1G  BOD: 13G
        2025/02/08 22:49:35|  kind: incr  secs:   20.864  mem:   1G  BOD: 12G
        2025/02/08 22:58:54|  kind: NULL  secs:    6.507  mem:   1G  BOD: 12G

  recursive-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/08 23:07:48|  kind: full  secs:  381.007  mem:  57M  BOD: 1M
        2025/02/08 23:25:42|  kind: incr  secs:  321.164  mem:  28M  BOD: 1M
        2025/02/08 23:31:04|  kind: NULL  secs:  319.092  mem:  28M  BOD: 1M

  recursive-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/08 23:36:23|  kind: full  secs:   50.070  mem:  58M  BOD: 1M
        2025/02/08 23:39:56|  kind: incr  secs:    4.615  mem:  14M  BOD: 1M
        2025/02/08 23:40:01|  kind: NULL  secs:    3.741  mem:  14M  BOD: 1M

  single-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/08 23:40:05|  kind: full  secs:  191.029  mem:   1G  BOD: 1M
        2025/02/08 23:45:57|  kind: incr  secs:  139.150  mem: 936M  BOD: 1M
        2025/02/08 23:48:16|  kind: NULL  secs:  134.708  mem: 936M  BOD: 1M

  single-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/08 23:50:31|  kind: full  secs:   59.074  mem: 364M  BOD: 1M
        2025/02/08 23:54:17|  kind: incr  secs:    8.231  mem: 117M  BOD: 1M
        2025/02/08 23:54:25|  kind: NULL  secs:    6.361  mem: 116M  BOD: 1M

  scons-md5sum  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/08 23:54:32|  kind: full  secs:  463.036  mem:   1G  BOD: 150M
        2025/02/09 00:04:57|  kind: incr  secs:  381.283  mem:   1G  BOD: 150M
        2025/02/09 00:11:19|  kind: NULL  secs:  375.905  mem:   1G  BOD: 150M

  scons-make  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/09 00:17:36|  kind: full  secs:  366.234  mem:   1G  BOD: 105M
        2025/02/09 00:26:28|  kind: incr  secs:  259.813  mem:   1G  BOD: 105M
        2025/02/09 00:30:48|  kind: NULL  secs:  256.492  mem:   1G  BOD: 105M


arch        : x86_64
platform    : Linux-6.8.0-48-generic-x86_64-with-glibc2.39
version     : #48~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Mon Oct  7 11:24:13 UTC 2
cpus        : 4
memory      : 7G
files/dir   : 100
module count: 100000
parallelism : 4

  bash  [GNU bash, version 5.1.16(1)-release (x86_64-pc-linux-gnu)]
    args: <no-args>
        2025/02/09 00:35:05|  kind: full  secs:  278.104  mem:  99M  BOD: 3M
        2025/02/09 00:45:22|  kind: incr  secs:   99.115  mem:  14M  BOD: 3M
        2025/02/09 00:47:02|  kind: NULL  secs:   94.514  mem:  14M  BOD: 3M

  bazel  [bazel no_version]
    args: <no-args>
        2025/02/09 00:48:37|  kind: full  secs: 1372.449  mem:   2G  BOD: 26G
        2025/02/09 01:41:06|  kind: incr  secs:   56.994  mem:   2G  BOD: 25G
        2025/02/09 02:05:22|  kind: NULL  secs:   14.892  mem:   2G  BOD: 25G

  recursive-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/09 02:28:18|  kind: full  secs:  811.857  mem:  99M  BOD: 3M
        2025/02/09 03:08:37|  kind: incr  secs:  692.427  mem:  31M  BOD: 3M
        2025/02/09 03:20:10|  kind: NULL  secs:  687.749  mem:  31M  BOD: 3M

  recursive-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/09 03:31:39|  kind: full  secs:  100.409  mem:  99M  BOD: 3M
        2025/02/09 03:39:09|  kind: incr  secs:    9.418  mem:  14M  BOD: 3M
        2025/02/09 03:39:19|  kind: NULL  secs:    7.782  mem:  14M  BOD: 3M

  single-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/09 03:39:27|  kind: full  secs:  392.734  mem:   2G  BOD: 3M
        2025/02/09 03:51:57|  kind: incr  secs:  293.158  mem:   1G  BOD: 3M
        2025/02/09 03:56:51|  kind: NULL  secs:  284.259  mem:   1G  BOD: 3M

  single-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/09 04:01:36|  kind: full  secs:  119.629  mem: 730M  BOD: 3M
        2025/02/09 04:09:14|  kind: incr  secs:   17.949  mem: 231M  BOD: 3M
        2025/02/09 04:09:33|  kind: NULL  secs:   14.531  mem: 230M  BOD: 3M

  scons-md5sum  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/09 04:09:48|  kind: full  secs:  928.850  mem:   3G  BOD: 312M
        2025/02/09 04:30:57|  kind: incr  secs:  770.966  mem:   3G  BOD: 312M
        2025/02/09 04:43:49|  kind: NULL  secs:  752.977  mem:   3G  BOD: 312M

  scons-make  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/09 04:56:23|  kind: full  secs:  743.461  mem:   3G  BOD: 219M
        2025/02/09 05:14:46|  kind: incr  secs:  527.956  mem:   3G  BOD: 219M
        2025/02/09 05:23:35|  kind: NULL  secs:  518.432  mem:   3G  BOD: 219M


```

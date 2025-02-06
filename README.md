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
  --module-size 30 \
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
arch       : aarch64
platform   : Linux-6.8.0-1018-raspi-aarch64-with-glibc2.39
version    : #20-Ubuntu SMP PREEMPT_DYNAMIC Fri Jan 17 12:35:36 UTC 2025
cpus       : 4
memory     : 7G
files/dir  : 100
module size: 30
num modules: 50
parallelism: 4

  bash  [GNU bash, version 5.2.21(1)-release (aarch64-unknown-linux-gnu)]
    args: <no-args>
        2025/02/05 04:53:51|  kind: full  secs:    0.168  mem:  12M  BOD: 12K
        2025/02/05 04:54:17|  kind: incr  secs:    0.074  mem:  12M  BOD: 12K
        2025/02/05 04:54:17|  kind: NULL  secs:    0.021  mem:  12M  BOD: 12K

  bazel  [bazel 8.0.1]
    args: <no-args>
        2025/02/05 04:54:17|  kind: full  secs:   36.851  mem: 492M  BOD: 311M
        2025/02/05 04:55:01|  kind: incr  secs:    1.646  mem: 361M  BOD: 311M
        2025/02/05 04:55:06|  kind: NULL  secs:    0.776  mem: 507M  BOD: 311M

  recursive-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/05 04:55:12|  kind: full  secs:    0.098  mem:  12M  BOD: 12K
        2025/02/05 04:55:12|  kind: incr  secs:    0.052  mem:  12M  BOD: 12K
        2025/02/05 04:55:12|  kind: NULL  secs:    0.036  mem:  12M  BOD: 12K

  recursive-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/05 04:55:12|  kind: full  secs:    0.046  mem:  12M  BOD: 12K
        2025/02/05 04:55:13|  kind: incr  secs:    0.030  mem:  12M  BOD: 12K
        2025/02/05 04:55:13|  kind: NULL  secs:    0.009  mem:  12M  BOD: 12K

  single-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/05 04:55:13|  kind: full  secs:    0.071  mem:  12M  BOD: 12K
        2025/02/05 04:55:13|  kind: incr  secs:    0.050  mem:  12M  BOD: 12K
        2025/02/05 04:55:13|  kind: NULL  secs:    0.034  mem:  12M  BOD: 12K

  single-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/05 04:55:13|  kind: full  secs:    0.043  mem:  12M  BOD: 12K
        2025/02/05 04:55:14|  kind: incr  secs:    0.026  mem:  12M  BOD: 12K
        2025/02/05 04:55:14|  kind: NULL  secs:    0.006  mem:  12M  BOD: 12K

  scons-md5sum  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/05 04:55:14|  kind: full  secs:    0.411  mem:  26M  BOD: 52K
        2025/02/05 04:55:15|  kind: incr  secs:    0.344  mem:  26M  BOD: 52K
        2025/02/05 04:55:15|  kind: NULL  secs:    0.309  mem:  26M  BOD: 52K

  scons-make  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/05 04:55:16|  kind: full  secs:    0.364  mem:  26M  BOD: 44K
        2025/02/05 04:55:16|  kind: incr  secs:    0.311  mem:  26M  BOD: 44K
        2025/02/05 04:55:17|  kind: NULL  secs:    0.301  mem:  26M  BOD: 44K


arch       : aarch64
platform   : Linux-6.8.0-1018-raspi-aarch64-with-glibc2.39
version    : #20-Ubuntu SMP PREEMPT_DYNAMIC Fri Jan 17 12:35:36 UTC 2025
cpus       : 4
memory     : 7G
files/dir  : 100
module size: 30
num modules: 100
parallelism: 4

  bash  [GNU bash, version 5.2.21(1)-release (aarch64-unknown-linux-gnu)]
    args: <no-args>
        2025/02/05 04:55:18|  kind: full  secs:    0.207  mem:  12M  BOD: 12K
        2025/02/05 04:55:18|  kind: incr  secs:    0.129  mem:  12M  BOD: 12K
        2025/02/05 04:55:18|  kind: NULL  secs:    0.041  mem:  12M  BOD: 12K

  bazel  [bazel 8.0.1]
    args: <no-args>
        2025/02/05 04:55:18|  kind: full  secs:   32.754  mem: 496M  BOD: 311M
        2025/02/05 04:55:54|  kind: incr  secs:    1.951  mem: 372M  BOD: 311M
        2025/02/05 04:56:00|  kind: NULL  secs:    0.798  mem: 521M  BOD: 311M

  recursive-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/05 04:56:05|  kind: full  secs:    0.133  mem:  12M  BOD: 12K
        2025/02/05 04:56:06|  kind: incr  secs:    0.101  mem:  12M  BOD: 12K
        2025/02/05 04:56:06|  kind: NULL  secs:    0.070  mem:  12M  BOD: 12K

  recursive-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/05 04:56:06|  kind: full  secs:    0.083  mem:  12M  BOD: 12K
        2025/02/05 04:56:06|  kind: incr  secs:    0.045  mem:  12M  BOD: 12K
        2025/02/05 04:56:06|  kind: NULL  secs:    0.012  mem:  12M  BOD: 12K

  single-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/05 04:56:06|  kind: full  secs:    0.135  mem:  12M  BOD: 12K
        2025/02/05 04:56:07|  kind: incr  secs:    0.098  mem:  12M  BOD: 12K
        2025/02/05 04:56:07|  kind: NULL  secs:    0.068  mem:  12M  BOD: 12K

  single-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/05 04:56:07|  kind: full  secs:    0.079  mem:  12M  BOD: 12K
        2025/02/05 04:56:07|  kind: incr  secs:    0.042  mem:  12M  BOD: 12K
        2025/02/05 04:56:07|  kind: NULL  secs:    0.008  mem:  12M  BOD: 12K

  scons-md5sum  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/05 04:56:08|  kind: full  secs:    0.503  mem:  28M  BOD: 92K
        2025/02/05 04:56:08|  kind: incr  secs:    0.451  mem:  28M  BOD: 92K
        2025/02/05 04:56:09|  kind: NULL  secs:    0.389  mem:  28M  BOD: 92K

  scons-make  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/05 04:56:10|  kind: full  secs:    0.481  mem:  28M  BOD: 80K
        2025/02/05 04:56:11|  kind: incr  secs:    0.431  mem:  28M  BOD: 80K
        2025/02/05 04:56:11|  kind: NULL  secs:    0.368  mem:  28M  BOD: 80K


arch       : aarch64
platform   : Linux-6.8.0-1018-raspi-aarch64-with-glibc2.39
version    : #20-Ubuntu SMP PREEMPT_DYNAMIC Fri Jan 17 12:35:36 UTC 2025
cpus       : 4
memory     : 7G
files/dir  : 100
module size: 30
num modules: 1000
parallelism: 4

  bash  [GNU bash, version 5.2.21(1)-release (aarch64-unknown-linux-gnu)]
    args: <no-args>
        2025/02/05 04:56:12|  kind: full  secs:    2.066  mem:  13M  BOD: 48K
        2025/02/05 04:56:15|  kind: incr  secs:    0.668  mem:  12M  BOD: 48K
        2025/02/05 04:56:15|  kind: NULL  secs:    0.467  mem:  13M  BOD: 48K

  bazel  [bazel 8.0.1]
    args: <no-args>
        2025/02/05 04:56:16|  kind: full  secs:   44.031  mem: 549M  BOD: 311M
        2025/02/05 04:57:02|  kind: incr  secs:    3.295  mem: 425M  BOD: 311M
        2025/02/05 04:57:08|  kind: NULL  secs:    1.280  mem: 582M  BOD: 311M

  recursive-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/05 04:57:13|  kind: full  secs:    1.840  mem:  13M  BOD: 48K
        2025/02/05 04:57:16|  kind: incr  secs:    1.099  mem:  12M  BOD: 48K
        2025/02/05 04:57:17|  kind: NULL  secs:    1.014  mem:  13M  BOD: 48K

  recursive-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/05 04:57:18|  kind: full  secs:    0.704  mem:  12M  BOD: 48K
        2025/02/05 04:57:19|  kind: incr  secs:    0.104  mem:  12M  BOD: 48K
        2025/02/05 04:57:20|  kind: NULL  secs:    0.037  mem:  12M  BOD: 48K

  single-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/05 04:57:20|  kind: full  secs:    1.711  mem:  25M  BOD: 48K
        2025/02/05 04:57:22|  kind: incr  secs:    1.111  mem:  21M  BOD: 48K
        2025/02/05 04:57:23|  kind: NULL  secs:    1.008  mem:  25M  BOD: 48K

  single-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/05 04:57:24|  kind: full  secs:    0.725  mem:  13M  BOD: 48K
        2025/02/05 04:57:26|  kind: incr  secs:    0.109  mem:  12M  BOD: 48K
        2025/02/05 04:57:26|  kind: NULL  secs:    0.040  mem:  13M  BOD: 48K

  scons-md5sum  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/05 04:57:26|  kind: full  secs:    3.142  mem:  62M  BOD: 1.3M
        2025/02/05 04:57:30|  kind: incr  secs:    2.162  mem:  62M  BOD: 1.3M
        2025/02/05 04:57:32|  kind: NULL  secs:    2.012  mem:  62M  BOD: 1.3M

  scons-make  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/05 04:57:35|  kind: full  secs:    2.952  mem:  61M  BOD: 1012K
        2025/02/05 04:57:38|  kind: incr  secs:    1.972  mem:  61M  BOD: 1012K
        2025/02/05 04:57:41|  kind: NULL  secs:    1.823  mem:  61M  BOD: 1012K


arch       : aarch64
platform   : Linux-6.8.0-1018-raspi-aarch64-with-glibc2.39
version    : #20-Ubuntu SMP PREEMPT_DYNAMIC Fri Jan 17 12:35:36 UTC 2025
cpus       : 4
memory     : 7G
files/dir  : 100
module size: 30
num modules: 5000
parallelism: 4

  bash  [GNU bash, version 5.2.21(1)-release (aarch64-unknown-linux-gnu)]
    args: <no-args>
        2025/02/05 04:57:43|  kind: full  secs:   10.490  mem:  16M  BOD: 208K
        2025/02/05 04:57:56|  kind: incr  secs:    2.832  mem:  12M  BOD: 208K
        2025/02/05 04:57:58|  kind: NULL  secs:    2.480  mem:  16M  BOD: 208K

  bazel  [bazel 8.0.1]
    args: <no-args>
        2025/02/05 04:58:01|  kind: full  secs:   75.401  mem: 788M  BOD: 313M
        2025/02/05 04:59:20|  kind: incr  secs:    6.669  mem: 656M  BOD: 313M
        2025/02/05 04:59:30|  kind: NULL  secs:    1.703  mem: 801M  BOD: 313M

  recursive-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/05 04:59:36|  kind: full  secs:   17.723  mem:  21M  BOD: 208K
        2025/02/05 04:59:56|  kind: incr  secs:   12.903  mem:  21M  BOD: 208K
        2025/02/05 05:00:09|  kind: NULL  secs:   12.402  mem:  21M  BOD: 208K

  recursive-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/05 05:00:22|  kind: full  secs:    3.553  mem:  16M  BOD: 208K
        2025/02/05 05:00:28|  kind: incr  secs:    0.301  mem:  12M  BOD: 208K
        2025/02/05 05:00:28|  kind: NULL  secs:    0.195  mem:  16M  BOD: 208K

  single-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/05 05:00:29|  kind: full  secs:   12.817  mem: 119M  BOD: 208K
        2025/02/05 05:00:44|  kind: incr  secs:    9.259  mem:  96M  BOD: 208K
        2025/02/05 05:00:53|  kind: NULL  secs:    8.965  mem: 119M  BOD: 208K

  single-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/05 05:01:02|  kind: full  secs:    3.876  mem:  36M  BOD: 208K
        2025/02/05 05:01:09|  kind: incr  secs:    0.317  mem:  13M  BOD: 208K
        2025/02/05 05:01:09|  kind: NULL  secs:    0.216  mem:  36M  BOD: 208K

  scons-md5sum  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/05 05:01:10|  kind: full  secs:   16.031  mem: 204M  BOD: 11M
        2025/02/05 05:01:28|  kind: incr  secs:   10.652  mem: 206M  BOD: 11M
        2025/02/05 05:01:39|  kind: NULL  secs:   10.953  mem: 206M  BOD: 11M

  scons-make  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/05 05:01:51|  kind: full  secs:   15.104  mem: 204M  BOD: 7.7M
        2025/02/05 05:02:09|  kind: incr  secs:    9.785  mem: 202M  BOD: 7.7M
        2025/02/05 05:02:19|  kind: NULL  secs:    9.578  mem: 204M  BOD: 7.7M


arch       : aarch64
platform   : Linux-6.8.0-1018-raspi-aarch64-with-glibc2.39
version    : #20-Ubuntu SMP PREEMPT_DYNAMIC Fri Jan 17 12:35:36 UTC 2025
cpus       : 4
memory     : 7G
files/dir  : 100
module size: 30
num modules: 10000
parallelism: 4

  bash  [GNU bash, version 5.2.21(1)-release (aarch64-unknown-linux-gnu)]
    args: <no-args>
        2025/02/05 05:02:28|  kind: full  secs:   20.966  mem:  20M  BOD: 408K
        2025/02/05 05:02:55|  kind: incr  secs:    5.616  mem:  12M  BOD: 408K
        2025/02/05 05:03:01|  kind: NULL  secs:    5.070  mem:  20M  BOD: 408K

  bazel  [bazel 8.0.1]
    args: <no-args>
        2025/02/05 05:03:06|  kind: full  secs:  110.548  mem:   1G  BOD: 314M
        2025/02/05 05:05:04|  kind: incr  secs:    7.979  mem:   1G  BOD: 314M
        2025/02/05 05:05:14|  kind: NULL  secs:    2.499  mem:   1G  BOD: 314M

  recursive-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/05 05:05:20|  kind: full  secs:   39.830  mem:  23M  BOD: 408K
        2025/02/05 05:06:05|  kind: incr  secs:   29.226  mem:  23M  BOD: 408K
        2025/02/05 05:06:35|  kind: NULL  secs:   29.381  mem:  23M  BOD: 408K

  recursive-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/05 05:07:04|  kind: full  secs:    7.386  mem:  20M  BOD: 408K
        2025/02/05 05:07:17|  kind: incr  secs:    0.534  mem:  12M  BOD: 408K
        2025/02/05 05:07:18|  kind: NULL  secs:    0.409  mem:  20M  BOD: 408K

  single-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/05 05:07:18|  kind: full  secs:   30.897  mem: 238M  BOD: 408K
        2025/02/05 05:07:54|  kind: incr  secs:   23.606  mem: 191M  BOD: 408K
        2025/02/05 05:08:18|  kind: NULL  secs:   23.304  mem: 238M  BOD: 408K

  single-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/05 05:08:41|  kind: full  secs:    7.612  mem:  72M  BOD: 408K
        2025/02/05 05:08:54|  kind: incr  secs:    0.606  mem:  24M  BOD: 408K
        2025/02/05 05:08:55|  kind: NULL  secs:    0.491  mem:  72M  BOD: 408K

  scons-md5sum  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/05 05:08:55|  kind: full  secs:   32.884  mem: 384M  BOD: 25M
        2025/02/05 05:09:34|  kind: incr  secs:   22.769  mem: 387M  BOD: 25M
        2025/02/05 05:09:57|  kind: NULL  secs:   22.344  mem: 388M  BOD: 25M

  scons-make  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/05 05:10:19|  kind: full  secs:   30.675  mem: 384M  BOD: 18M
        2025/02/05 05:10:56|  kind: incr  secs:   20.706  mem: 381M  BOD: 18M
        2025/02/05 05:11:17|  kind: NULL  secs:   20.365  mem: 384M  BOD: 18M


arch       : aarch64
platform   : Linux-6.8.0-1018-raspi-aarch64-with-glibc2.39
version    : #20-Ubuntu SMP PREEMPT_DYNAMIC Fri Jan 17 12:35:36 UTC 2025
cpus       : 4
memory     : 7G
files/dir  : 100
module size: 30
num modules: 50000
parallelism: 4

  bash  [GNU bash, version 5.2.21(1)-release (aarch64-unknown-linux-gnu)]
    args: <no-args>
        2025/02/05 05:11:37|  kind: full  secs:  104.609  mem:  53M  BOD: 2.0M
        2025/02/05 05:13:56|  kind: incr  secs:   26.636  mem:  12M  BOD: 2.0M
        2025/02/05 05:14:23|  kind: NULL  secs:   26.084  mem:  53M  BOD: 2.0M

  bazel  [bazel 8.0.1]
    args: <no-args>
        2025/02/05 05:14:49|  kind: full  secs:  379.877  mem:   2G  BOD: 327M
        2025/02/05 05:21:54|  kind: incr  secs:   39.415  mem:   2G  BOD: 324M
        2025/02/05 05:22:34|  kind: NULL  secs:    8.343  mem:   2G  BOD: 324M

  recursive-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/05 05:22:45|  kind: full  secs:  237.002  mem:  53M  BOD: 2.0M
        2025/02/05 05:27:29|  kind: incr  secs:  181.158  mem:  27M  BOD: 2.0M
        2025/02/05 05:30:30|  kind: NULL  secs:  180.897  mem:  53M  BOD: 2.0M

  recursive-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/05 05:33:31|  kind: full  secs:   38.072  mem:  53M  BOD: 2.0M
        2025/02/05 05:34:59|  kind: incr  secs:    4.326  mem:  12M  BOD: 2.0M
        2025/02/05 05:35:03|  kind: NULL  secs:    2.300  mem:  53M  BOD: 2.0M

  single-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/05 05:35:07|  kind: full  secs:   97.493  mem:   1G  BOD: 2.0M
        2025/02/05 05:37:28|  kind: incr  secs:   62.497  mem: 936M  BOD: 2.0M
        2025/02/05 05:38:31|  kind: NULL  secs:   61.392  mem:   1G  BOD: 2.0M

  single-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/05 05:39:32|  kind: full  secs:   39.970  mem: 363M  BOD: 2.0M
        2025/02/05 05:40:56|  kind: incr  secs:    3.597  mem: 116M  BOD: 2.0M
        2025/02/05 05:41:00|  kind: NULL  secs:    3.422  mem: 363M  BOD: 2.0M

  scons-md5sum  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/05 05:41:04|  kind: full  secs:  169.348  mem:   1G  BOD: 150M
        2025/02/05 05:44:34|  kind: incr  secs:  115.367  mem:   1G  BOD: 150M
        2025/02/05 05:46:30|  kind: NULL  secs:  115.666  mem:   1G  BOD: 150M

  scons-make  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/05 05:48:26|  kind: full  secs:  158.107  mem:   1G  BOD: 105M
        2025/02/05 05:51:48|  kind: incr  secs:  106.457  mem:   1G  BOD: 105M
        2025/02/05 05:53:35|  kind: NULL  secs:  105.660  mem:   1G  BOD: 105M


arch       : aarch64
platform   : Linux-6.8.0-1018-raspi-aarch64-with-glibc2.39
version    : #20-Ubuntu SMP PREEMPT_DYNAMIC Fri Jan 17 12:35:36 UTC 2025
cpus       : 4
memory     : 7G
files/dir  : 100
module size: 30
num modules: 100000
parallelism: 4

  bash  [GNU bash, version 5.2.21(1)-release (aarch64-unknown-linux-gnu)]
    args: <no-args>
        2025/02/05 05:55:21|  kind: full  secs:  211.525  mem:  95M  BOD: 4.0M
        2025/02/05 06:00:38|  kind: incr  secs:   53.271  mem:  12M  BOD: 4.0M
        2025/02/05 06:01:32|  kind: NULL  secs:   52.701  mem:  95M  BOD: 4.0M

  bazel  [bazel 8.0.1]
    args: <no-args>
        2025/02/05 06:02:25|  kind: full  secs:  934.466  mem:   2G  BOD: 342M
        2025/02/05 06:27:12|  kind: incr  secs:  115.301  mem:   2G  BOD: 336M
        2025/02/05 06:29:09|  kind: NULL  secs:   15.014  mem:   2G  BOD: 336M

  recursive-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/05 06:29:29|  kind: full  secs:  497.477  mem:  95M  BOD: 4.0M
        2025/02/05 06:40:15|  kind: incr  secs:  390.929  mem:  31M  BOD: 4.0M
        2025/02/05 06:46:46|  kind: NULL  secs:  390.758  mem:  95M  BOD: 4.0M

  recursive-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/05 06:53:17|  kind: full  secs:   74.185  mem:  95M  BOD: 4.0M
        2025/02/05 06:56:31|  kind: incr  secs:    5.840  mem:  12M  BOD: 4.0M
        2025/02/05 06:56:37|  kind: NULL  secs:    4.826  mem:  95M  BOD: 4.0M

  single-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/05 06:56:43|  kind: full  secs:  202.863  mem:   2G  BOD: 4.0M
        2025/02/05 07:06:52|  kind: incr  secs:  133.613  mem:   1G  BOD: 4.0M
        2025/02/05 07:09:06|  kind: NULL  secs:  132.723  mem:   2G  BOD: 4.0M

  single-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/05 07:11:19|  kind: full  secs:   76.478  mem: 730M  BOD: 4.0M
        2025/02/05 07:14:35|  kind: incr  secs:    7.900  mem: 230M  BOD: 4.0M
        2025/02/05 07:14:43|  kind: NULL  secs:    7.620  mem: 730M  BOD: 4.0M

  scons-md5sum  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/05 07:14:51|  kind: full  secs:  919.650  mem:   3G  BOD: 311M
        2025/02/05 07:33:01|  kind: incr  secs:  278.169  mem:   3G  BOD: 311M
        2025/02/05 07:37:40|  kind: NULL  secs:  315.800  mem:   3G  BOD: 311M

  scons-make  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/05 07:42:57|  kind: full  secs:  320.818  mem:   3G  BOD: 217M
        2025/02/05 07:52:33|  kind: incr  secs:  214.800  mem:   3G  BOD: 217M
        2025/02/05 07:56:08|  kind: NULL  secs:  213.875  mem:   3G  BOD: 217M
```

## x86_64

```
arch       : x86_64
platform   : Linux-6.8.0-48-generic-x86_64-with-glibc2.39
version    : #48~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Mon Oct  7 11:24:13 UTC 2
cpus       : 4
memory     : 7G
files/dir  : 100
module size: 30
num modules: 50
parallelism: 4

  bash  [GNU bash, version 5.1.16(1)-release (x86_64-pc-linux-gnu)]
    args: <no-args>
        2025/02/05 21:32:04|  kind: full  secs:    0.147  mem:  14M  BOD: 12K
        2025/02/05 21:32:04|  kind: incr  secs:    0.100  mem:  14M  BOD: 12K
        2025/02/05 21:32:04|  kind: NULL  secs:    0.037  mem:  14M  BOD: 12K

  bazel  [bazel no_version]
    args: <no-args>
        2025/02/05 21:32:05|  kind: full  secs:    9.371  mem: 224M  BOD: 7.0M
        2025/02/05 21:32:15|  kind: incr  secs:    0.983  mem: 231M  BOD: 11M
        2025/02/05 21:32:20|  kind: NULL  secs:    0.368  mem: 233M  BOD: 9.9M

  recursive-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/05 21:32:26|  kind: full  secs:    0.117  mem:  14M  BOD: 12K
        2025/02/05 21:32:26|  kind: incr  secs:    0.093  mem:  14M  BOD: 12K
        2025/02/05 21:32:26|  kind: NULL  secs:    0.062  mem:  14M  BOD: 12K

  recursive-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/05 21:32:27|  kind: full  secs:    0.071  mem:  14M  BOD: 12K
        2025/02/05 21:32:27|  kind: incr  secs:    0.043  mem:  14M  BOD: 12K
        2025/02/05 21:32:27|  kind: NULL  secs:    0.014  mem:  14M  BOD: 12K

  single-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/05 21:32:27|  kind: full  secs:    0.114  mem:  14M  BOD: 12K
        2025/02/05 21:32:28|  kind: incr  secs:    0.088  mem:  14M  BOD: 12K
        2025/02/05 21:32:28|  kind: NULL  secs:    0.058  mem:  14M  BOD: 12K

  single-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/05 21:32:28|  kind: full  secs:    0.089  mem:  14M  BOD: 12K
        2025/02/05 21:32:29|  kind: incr  secs:    0.040  mem:  14M  BOD: 12K
        2025/02/05 21:32:29|  kind: NULL  secs:    0.010  mem:  14M  BOD: 12K

  scons-md5sum  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/05 21:32:29|  kind: full  secs:    0.811  mem:  28M  BOD: 52K
        2025/02/05 21:32:31|  kind: incr  secs:    0.742  mem:  28M  BOD: 52K
        2025/02/05 21:32:32|  kind: NULL  secs:    0.682  mem:  28M  BOD: 52K

  scons-make  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/05 21:32:33|  kind: full  secs:    0.774  mem:  28M  BOD: 44K
        2025/02/05 21:32:35|  kind: incr  secs:    0.743  mem:  28M  BOD: 44K
        2025/02/05 21:32:36|  kind: NULL  secs:    0.666  mem:  28M  BOD: 44K


arch       : x86_64
platform   : Linux-6.8.0-48-generic-x86_64-with-glibc2.39
version    : #48~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Mon Oct  7 11:24:13 UTC 2
cpus       : 4
memory     : 7G
files/dir  : 100
module size: 30
num modules: 100
parallelism: 4

  bash  [GNU bash, version 5.1.16(1)-release (x86_64-pc-linux-gnu)]
    args: <no-args>
        2025/02/05 21:32:37|  kind: full  secs:    0.275  mem:  14M  BOD: 12K
        2025/02/05 21:32:38|  kind: incr  secs:    0.182  mem:  14M  BOD: 12K
        2025/02/05 21:32:38|  kind: NULL  secs:    0.076  mem:  14M  BOD: 12K

  bazel  [bazel no_version]
    args: <no-args>
        2025/02/05 21:32:38|  kind: full  secs:   10.601  mem: 262M  BOD: 16M
        2025/02/05 21:32:54|  kind: incr  secs:    1.281  mem: 245M  BOD: 22M
        2025/02/05 21:32:59|  kind: NULL  secs:    0.406  mem: 249M  BOD: 21M

  recursive-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/05 21:33:05|  kind: full  secs:    0.233  mem:  14M  BOD: 12K
        2025/02/05 21:33:05|  kind: incr  secs:    0.176  mem:  14M  BOD: 12K
        2025/02/05 21:33:06|  kind: NULL  secs:    0.130  mem:  14M  BOD: 12K

  recursive-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/05 21:33:06|  kind: full  secs:    0.127  mem:  14M  BOD: 12K
        2025/02/05 21:33:07|  kind: incr  secs:    0.067  mem:  14M  BOD: 12K
        2025/02/05 21:33:07|  kind: NULL  secs:    0.020  mem:  14M  BOD: 12K

  single-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/05 21:33:07|  kind: full  secs:    0.234  mem:  14M  BOD: 12K
        2025/02/05 21:33:08|  kind: incr  secs:    0.179  mem:  14M  BOD: 12K
        2025/02/05 21:33:08|  kind: NULL  secs:    0.123  mem:  14M  BOD: 12K

  single-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/05 21:33:08|  kind: full  secs:    0.119  mem:  14M  BOD: 12K
        2025/02/05 21:33:09|  kind: incr  secs:    0.063  mem:  14M  BOD: 12K
        2025/02/05 21:33:09|  kind: NULL  secs:    0.013  mem:  14M  BOD: 12K

  scons-md5sum  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/05 21:33:09|  kind: full  secs:    1.124  mem:  30M  BOD: 92K
        2025/02/05 21:33:11|  kind: incr  secs:    1.004  mem:  30M  BOD: 92K
        2025/02/05 21:33:13|  kind: NULL  secs:    0.889  mem:  30M  BOD: 92K

  scons-make  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/05 21:33:14|  kind: full  secs:    1.076  mem:  30M  BOD: 80K
        2025/02/05 21:33:16|  kind: incr  secs:    0.919  mem:  30M  BOD: 80K
        2025/02/05 21:33:17|  kind: NULL  secs:    0.849  mem:  30M  BOD: 80K


arch       : x86_64
platform   : Linux-6.8.0-48-generic-x86_64-with-glibc2.39
version    : #48~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Mon Oct  7 11:24:13 UTC 2
cpus       : 4
memory     : 7G
files/dir  : 100
module size: 30
num modules: 1000
parallelism: 4

  bash  [GNU bash, version 5.1.16(1)-release (x86_64-pc-linux-gnu)]
    args: <no-args>
        2025/02/05 21:33:19|  kind: full  secs:    2.795  mem:  14M  BOD: 48K
        2025/02/05 21:33:23|  kind: incr  secs:    1.122  mem:  14M  BOD: 48K
        2025/02/05 21:33:24|  kind: NULL  secs:    0.866  mem:  14M  BOD: 48K

  bazel  [bazel no_version]
    args: <no-args>
        2025/02/05 21:33:25|  kind: full  secs:   27.025  mem: 330M  BOD: 194M
        2025/02/05 21:33:57|  kind: incr  secs:    2.080  mem: 335M  BOD: 198M
        2025/02/05 21:34:03|  kind: NULL  secs:    0.581  mem: 337M  BOD: 197M

  recursive-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/05 21:34:08|  kind: full  secs:    2.906  mem:  14M  BOD: 48K
        2025/02/05 21:34:14|  kind: incr  secs:    1.953  mem:  14M  BOD: 48K
        2025/02/05 21:34:16|  kind: NULL  secs:    1.831  mem:  14M  BOD: 48K

  recursive-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/05 21:34:18|  kind: full  secs:    0.966  mem:  14M  BOD: 48K
        2025/02/05 21:34:20|  kind: incr  secs:    0.152  mem:  14M  BOD: 48K
        2025/02/05 21:34:21|  kind: NULL  secs:    0.059  mem:  14M  BOD: 48K

  single-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/05 21:34:21|  kind: full  secs:    3.205  mem:  26M  BOD: 48K
        2025/02/05 21:34:26|  kind: incr  secs:    2.269  mem:  22M  BOD: 48K
        2025/02/05 21:34:28|  kind: NULL  secs:    2.111  mem:  21M  BOD: 48K

  single-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/05 21:34:30|  kind: full  secs:    1.090  mem:  14M  BOD: 48K
        2025/02/05 21:34:33|  kind: incr  secs:    0.169  mem:  14M  BOD: 48K
        2025/02/05 21:34:33|  kind: NULL  secs:    0.068  mem:  14M  BOD: 48K

  scons-md5sum  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/05 21:34:33|  kind: full  secs:    7.336  mem:  64M  BOD: 1.3M
        2025/02/05 21:34:43|  kind: incr  secs:    5.236  mem:  64M  BOD: 1.3M
        2025/02/05 21:34:48|  kind: NULL  secs:    4.954  mem:  64M  BOD: 1.3M

  scons-make  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/05 21:34:54|  kind: full  secs:    6.881  mem:  64M  BOD: 1012K
        2025/02/05 21:35:02|  kind: incr  secs:    4.949  mem:  64M  BOD: 1012K
        2025/02/05 21:35:08|  kind: NULL  secs:    4.605  mem:  63M  BOD: 1012K


arch       : x86_64
platform   : Linux-6.8.0-48-generic-x86_64-with-glibc2.39
version    : #48~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Mon Oct  7 11:24:13 UTC 2
cpus       : 4
memory     : 7G
files/dir  : 100
module size: 30
num modules: 5000
parallelism: 4

  bash  [GNU bash, version 5.1.16(1)-release (x86_64-pc-linux-gnu)]
    args: <no-args>
        2025/02/05 21:35:13|  kind: full  secs:   13.936  mem:  17M  BOD: 208K
        2025/02/05 21:35:33|  kind: incr  secs:    4.926  mem:  14M  BOD: 208K
        2025/02/05 21:35:38|  kind: NULL  secs:    4.539  mem:  14M  BOD: 208K

  bazel  [bazel no_version]
    args: <no-args>
        2025/02/05 21:35:43|  kind: full  secs:   79.736  mem: 444M  BOD: 1.2G
        2025/02/05 21:37:15|  kind: incr  secs:    4.062  mem: 426M  BOD: 1.1G
        2025/02/05 21:37:25|  kind: NULL  secs:    1.173  mem: 427M  BOD: 1.1G

  recursive-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/05 21:37:31|  kind: full  secs:   28.687  mem:  21M  BOD: 208K
        2025/02/05 21:38:18|  kind: incr  secs:   22.581  mem:  21M  BOD: 208K
        2025/02/05 21:38:41|  kind: NULL  secs:   22.819  mem:  21M  BOD: 208K

  recursive-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/05 21:39:04|  kind: full  secs:    4.902  mem:  17M  BOD: 208K
        2025/02/05 21:39:16|  kind: incr  secs:    0.466  mem:  14M  BOD: 208K
        2025/02/05 21:39:16|  kind: NULL  secs:    0.358  mem:  14M  BOD: 208K

  single-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/05 21:39:17|  kind: full  secs:   29.609  mem: 119M  BOD: 208K
        2025/02/05 21:39:53|  kind: incr  secs:   24.588  mem:  96M  BOD: 208K
        2025/02/05 21:40:18|  kind: NULL  secs:   24.219  mem:  96M  BOD: 208K

  single-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/05 21:40:42|  kind: full  secs:    5.642  mem:  37M  BOD: 208K
        2025/02/05 21:40:54|  kind: incr  secs:    0.565  mem:  14M  BOD: 208K
        2025/02/05 21:40:55|  kind: NULL  secs:    0.414  mem:  14M  BOD: 208K

  scons-md5sum  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/05 21:40:55|  kind: full  secs:   36.800  mem: 206M  BOD: 11M
        2025/02/05 21:41:39|  kind: incr  secs:   25.840  mem: 207M  BOD: 11M
        2025/02/05 21:42:05|  kind: NULL  secs:   26.879  mem: 207M  BOD: 11M

  scons-make  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/05 21:42:33|  kind: full  secs:   34.869  mem: 206M  BOD: 7.7M
        2025/02/05 21:43:14|  kind: incr  secs:   24.095  mem: 204M  BOD: 7.7M
        2025/02/05 21:43:39|  kind: NULL  secs:   23.475  mem: 204M  BOD: 7.7M


arch       : x86_64
platform   : Linux-6.8.0-48-generic-x86_64-with-glibc2.39
version    : #48~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Mon Oct  7 11:24:13 UTC 2
cpus       : 4
memory     : 7G
files/dir  : 100
module size: 30
num modules: 10000
parallelism: 4

  bash  [GNU bash, version 5.1.16(1)-release (x86_64-pc-linux-gnu)]
    args: <no-args>
        2025/02/05 21:44:03|  kind: full  secs:   27.403  mem:  21M  BOD: 408K
        2025/02/05 21:44:42|  kind: incr  secs:    9.621  mem:  14M  BOD: 408K
        2025/02/05 21:44:52|  kind: NULL  secs:    9.135  mem:  14M  BOD: 408K

  bazel  [bazel no_version]
    args: <no-args>
        2025/02/05 21:45:01|  kind: full  secs:  134.239  mem: 624M  BOD: 2.5G
        2025/02/05 21:47:46|  kind: incr  secs:    5.932  mem: 580M  BOD: 2.4G
        2025/02/05 21:48:06|  kind: NULL  secs:    1.626  mem: 567M  BOD: 2.4G

  recursive-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/05 21:48:17|  kind: full  secs:   63.894  mem:  24M  BOD: 408K
        2025/02/05 21:50:00|  kind: incr  secs:   52.068  mem:  23M  BOD: 408K
        2025/02/05 21:50:52|  kind: NULL  secs:   51.851  mem:  23M  BOD: 408K

  recursive-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/05 21:51:44|  kind: full  secs:    9.982  mem:  21M  BOD: 408K
        2025/02/05 21:52:07|  kind: incr  secs:    0.848  mem:  14M  BOD: 408K
        2025/02/05 21:52:08|  kind: NULL  secs:    0.680  mem:  14M  BOD: 408K

  single-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/05 21:52:09|  kind: full  secs:   71.969  mem: 239M  BOD: 408K
        2025/02/05 21:53:34|  kind: incr  secs:   61.867  mem: 191M  BOD: 408K
        2025/02/05 21:54:36|  kind: NULL  secs:   61.295  mem: 191M  BOD: 408K

  single-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/05 21:55:37|  kind: full  secs:   11.202  mem:  72M  BOD: 408K
        2025/02/05 21:56:01|  kind: incr  secs:    1.114  mem:  25M  BOD: 408K
        2025/02/05 21:56:03|  kind: NULL  secs:    0.937  mem:  24M  BOD: 408K

  scons-md5sum  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/05 21:56:04|  kind: full  secs:   74.876  mem: 386M  BOD: 25M
        2025/02/05 21:57:31|  kind: incr  secs:   52.915  mem: 389M  BOD: 25M
        2025/02/05 21:58:25|  kind: NULL  secs:   52.077  mem: 390M  BOD: 25M

  scons-make  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/05 21:59:18|  kind: full  secs:   70.287  mem: 386M  BOD: 18M
        2025/02/05 22:00:41|  kind: incr  secs:   49.476  mem: 382M  BOD: 18M
        2025/02/05 22:01:31|  kind: NULL  secs:   48.894  mem: 382M  BOD: 18M


arch       : x86_64
platform   : Linux-6.8.0-48-generic-x86_64-with-glibc2.39
version    : #48~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Mon Oct  7 11:24:13 UTC 2
cpus       : 4
memory     : 7G
files/dir  : 100
module size: 30
num modules: 50000
parallelism: 4

  bash  [GNU bash, version 5.1.16(1)-release (x86_64-pc-linux-gnu)]
    args: <no-args>
        2025/02/05 22:02:21|  kind: full  secs:  138.971  mem:  55M  BOD: 2.0M
        2025/02/05 22:05:41|  kind: incr  secs:   47.420  mem:  14M  BOD: 2.0M
        2025/02/05 22:06:29|  kind: NULL  secs:   46.730  mem:  14M  BOD: 2.0M

  bazel  [bazel no_version]
    args: <no-args>
        2025/02/05 22:07:16|  kind: full  secs:  710.739  mem:   1G  BOD: 14G
        2025/02/05 22:29:33|  kind: incr  secs:   19.319  mem:   1G  BOD: 13G
        2025/02/05 22:36:52|  kind: NULL  secs:    7.060  mem:   1G  BOD: 13G

  recursive-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/05 22:43:50|  kind: full  secs:  380.785  mem:  55M  BOD: 2.0M
        2025/02/05 22:59:14|  kind: incr  secs:  323.231  mem:  28M  BOD: 2.0M
        2025/02/05 23:04:38|  kind: NULL  secs:  321.291  mem:  28M  BOD: 2.0M

  recursive-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/05 23:10:00|  kind: full  secs:   49.376  mem:  55M  BOD: 2.0M
        2025/02/05 23:11:59|  kind: incr  secs:    3.951  mem:  14M  BOD: 2.0M
        2025/02/05 23:12:03|  kind: NULL  secs:    3.726  mem:  14M  BOD: 2.0M

  single-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/05 23:12:07|  kind: full  secs:  190.733  mem:   1G  BOD: 2.0M
        2025/02/05 23:16:56|  kind: incr  secs:  135.669  mem: 936M  BOD: 2.0M
        2025/02/05 23:19:12|  kind: NULL  secs:  135.290  mem: 936M  BOD: 2.0M

  single-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/05 23:21:28|  kind: full  secs:   58.028  mem: 364M  BOD: 2.0M
        2025/02/05 23:23:43|  kind: incr  secs:    6.515  mem: 116M  BOD: 2.0M
        2025/02/05 23:23:49|  kind: NULL  secs:    6.280  mem: 116M  BOD: 2.0M

  scons-md5sum  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/05 23:23:56|  kind: full  secs:  421.035  mem:   1G  BOD: 150M
        2025/02/05 23:32:41|  kind: incr  secs:  327.503  mem:   1G  BOD: 150M
        2025/02/05 23:38:09|  kind: NULL  secs:  317.157  mem:   1G  BOD: 150M

  scons-make  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/05 23:43:27|  kind: full  secs:  365.518  mem:   1G  BOD: 105M
        2025/02/05 23:50:40|  kind: incr  secs:  256.416  mem:   1G  BOD: 105M
        2025/02/05 23:54:57|  kind: NULL  secs:  255.538  mem:   1G  BOD: 105M


arch       : x86_64
platform   : Linux-6.8.0-48-generic-x86_64-with-glibc2.39
version    : #48~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Mon Oct  7 11:24:13 UTC 2
cpus       : 4
memory     : 7G
files/dir  : 100
module size: 30
num modules: 100000
parallelism: 4

  bash  [GNU bash, version 5.1.16(1)-release (x86_64-pc-linux-gnu)]
    args: <no-args>
        2025/02/05 23:59:13|  kind: full  secs:  278.126  mem:  97M  BOD: 4.0M
        2025/02/06 00:06:05|  kind: incr  secs:   94.758  mem:  14M  BOD: 4.0M
        2025/02/06 00:07:40|  kind: NULL  secs:   94.024  mem:  14M  BOD: 4.0M

  bazel  [bazel no_version]
    args: <no-args>
        2025/02/06 00:09:15|  kind: full  secs: 1275.600  mem:   3G  BOD: 27G
        2025/02/06 00:57:12|  kind: incr  secs:   55.467  mem:   1G  BOD: 26G
        2025/02/06 01:20:38|  kind: NULL  secs:   25.985  mem:   1G  BOD: 26G

  recursive-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/06 01:43:23|  kind: full  secs:  811.231  mem:  97M  BOD: 4.0M
        2025/02/06 02:19:38|  kind: incr  secs:  695.176  mem:  31M  BOD: 4.0M
        2025/02/06 02:31:14|  kind: NULL  secs:  691.322  mem:  31M  BOD: 4.0M

  recursive-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/06 02:42:46|  kind: full  secs:   99.329  mem:  97M  BOD: 4.0M
        2025/02/06 02:46:53|  kind: incr  secs:    7.938  mem:  14M  BOD: 4.0M
        2025/02/06 02:47:01|  kind: NULL  secs:    7.777  mem:  14M  BOD: 4.0M

  single-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/06 02:47:09|  kind: full  secs:  394.478  mem:   2G  BOD: 4.0M
        2025/02/06 02:56:52|  kind: incr  secs:  289.963  mem:   1G  BOD: 4.0M
        2025/02/06 03:01:42|  kind: NULL  secs:  280.610  mem:   1G  BOD: 4.0M

  single-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/06 03:06:23|  kind: full  secs:  117.915  mem: 730M  BOD: 4.0M
        2025/02/06 03:11:01|  kind: incr  secs:   14.351  mem: 231M  BOD: 4.0M
        2025/02/06 03:11:16|  kind: NULL  secs:   14.137  mem: 230M  BOD: 4.0M

  scons-md5sum  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/06 03:11:31|  kind: full  secs:  854.483  mem:   3G  BOD: 311M
        2025/02/06 03:28:57|  kind: incr  secs:  647.178  mem:   3G  BOD: 311M
        2025/02/06 03:39:45|  kind: NULL  secs:  615.987  mem:   3G  BOD: 311M
```

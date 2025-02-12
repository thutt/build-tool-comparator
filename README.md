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

## Bash

Bash is not a build tool, but it can used to conveniently create a
shell script that emulates the unoptimized operations of creating an
artifact if any of its prerequisite are changed.  It represents a
naive low bound for the time needed to create artifacts.

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

## Arm: 50 Simulated Modules
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
        2025/02/10 15:02:39|  kind: full  secs:    0.108  mem:  13M  BOD: 12K
        2025/02/10 15:02:39|  kind: incr  secs:    0.071  mem:  12M  BOD: 12K
        2025/02/10 15:02:39|  kind: NULL  secs:    0.021  mem:  13M  BOD: 12K

  ninja  [1.11.1]
    args: <no-args>
        2025/02/10 15:02:39|  kind: full  secs:    0.041  mem:  13M  BOD: 12K
        2025/02/10 15:02:40|  kind: incr  secs:    0.028  mem:  12M  BOD: 12K
        2025/02/10 15:02:40|  kind: NULL  secs:    0.006  mem:  13M  BOD: 12K

  bazel  [bazel 8.0.1]
    args: <no-args>
        2025/02/10 15:02:40|  kind: full  secs:   20.683  mem: 500M  BOD: 310M
        2025/02/10 15:03:06|  kind: incr  secs:    1.537  mem: 351M  BOD: 310M
        2025/02/10 15:03:12|  kind: NULL  secs:    0.744  mem: 495M  BOD: 310M

  recursive-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/10 15:03:17|  kind: full  secs:    0.066  mem:  13M  BOD: 12K
        2025/02/10 15:03:18|  kind: incr  secs:    0.052  mem:  12M  BOD: 12K
        2025/02/10 15:03:18|  kind: NULL  secs:    0.037  mem:  13M  BOD: 12K

  recursive-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/10 15:03:18|  kind: full  secs:    0.046  mem:  13M  BOD: 12K
        2025/02/10 15:03:18|  kind: incr  secs:    0.028  mem:  12M  BOD: 12K
        2025/02/10 15:03:18|  kind: NULL  secs:    0.008  mem:  13M  BOD: 12K

  single-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/10 15:03:18|  kind: full  secs:    0.068  mem:  13M  BOD: 12K
        2025/02/10 15:03:19|  kind: incr  secs:    0.050  mem:  12M  BOD: 12K
        2025/02/10 15:03:19|  kind: NULL  secs:    0.033  mem:  13M  BOD: 12K

  single-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/10 15:03:19|  kind: full  secs:    0.044  mem:  13M  BOD: 12K
        2025/02/10 15:03:19|  kind: incr  secs:    0.026  mem:  12M  BOD: 12K
        2025/02/10 15:03:19|  kind: NULL  secs:    0.006  mem:  13M  BOD: 12K

  scons-md5sum  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/10 15:03:19|  kind: full  secs:    0.389  mem:  26M  BOD: 52K
        2025/02/10 15:03:20|  kind: incr  secs:    0.367  mem:  26M  BOD: 52K
        2025/02/10 15:03:21|  kind: NULL  secs:    0.333  mem:  26M  BOD: 52K

  scons-make  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/10 15:03:21|  kind: full  secs:    0.353  mem:  25M  BOD: 44K
        2025/02/10 15:03:22|  kind: incr  secs:    0.302  mem:  25M  BOD: 44K
        2025/02/10 15:03:22|  kind: NULL  secs:    0.302  mem:  25M  BOD: 44K
```

## Arm: 100 Simulated Modules

```
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
        2025/02/10 15:03:23|  kind: full  secs:    0.205  mem:  13M  BOD: 12K
        2025/02/10 15:03:23|  kind: incr  secs:    0.130  mem:  12M  BOD: 12K
        2025/02/10 15:03:24|  kind: NULL  secs:    0.041  mem:  13M  BOD: 12K

  ninja  [1.11.1]
    args: <no-args>
        2025/02/10 15:03:24|  kind: full  secs:    0.076  mem:  13M  BOD: 12K
        2025/02/10 15:03:24|  kind: incr  secs:    0.043  mem:  12M  BOD: 12K
        2025/02/10 15:03:24|  kind: NULL  secs:    0.006  mem:  13M  BOD: 12K

  bazel  [bazel 8.0.1]
    args: <no-args>
        2025/02/10 15:03:24|  kind: full  secs:   21.582  mem: 523M  BOD: 310M
        2025/02/10 15:03:50|  kind: incr  secs:    1.938  mem: 376M  BOD: 310M
        2025/02/10 15:03:56|  kind: NULL  secs:    0.826  mem: 524M  BOD: 310M

  recursive-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/10 15:04:01|  kind: full  secs:    0.132  mem:  13M  BOD: 12K
        2025/02/10 15:04:02|  kind: incr  secs:    0.097  mem:  12M  BOD: 12K
        2025/02/10 15:04:02|  kind: NULL  secs:    0.070  mem:  13M  BOD: 12K

  recursive-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/10 15:04:02|  kind: full  secs:    0.082  mem:  13M  BOD: 12K
        2025/02/10 15:04:02|  kind: incr  secs:    0.044  mem:  12M  BOD: 12K
        2025/02/10 15:04:03|  kind: NULL  secs:    0.012  mem:  13M  BOD: 12K

  single-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/10 15:04:03|  kind: full  secs:    0.134  mem:  13M  BOD: 12K
        2025/02/10 15:04:03|  kind: incr  secs:    0.097  mem:  12M  BOD: 12K
        2025/02/10 15:04:03|  kind: NULL  secs:    0.067  mem:  13M  BOD: 12K

  single-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/10 15:04:03|  kind: full  secs:    0.078  mem:  13M  BOD: 12K
        2025/02/10 15:04:04|  kind: incr  secs:    0.041  mem:  12M  BOD: 12K
        2025/02/10 15:04:04|  kind: NULL  secs:    0.007  mem:  13M  BOD: 12K

  scons-md5sum  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/10 15:04:04|  kind: full  secs:    0.538  mem:  28M  BOD: 92K
        2025/02/10 15:04:05|  kind: incr  secs:    0.488  mem:  28M  BOD: 92K
        2025/02/10 15:04:06|  kind: NULL  secs:    0.430  mem:  28M  BOD: 92K

  scons-make  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/10 15:04:06|  kind: full  secs:    0.478  mem:  27M  BOD: 80K
        2025/02/10 15:04:07|  kind: incr  secs:    0.368  mem:  27M  BOD: 80K
        2025/02/10 15:04:08|  kind: NULL  secs:    0.370  mem:  27M  BOD: 80K
```

## Arm: 1000 Simulated Modules

```
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
        2025/02/10 15:04:08|  kind: full  secs:    2.044  mem:  15M  BOD: 48K
        2025/02/10 15:04:11|  kind: incr  secs:    0.661  mem:  12M  BOD: 48K
        2025/02/10 15:04:12|  kind: NULL  secs:    0.467  mem:  15M  BOD: 48K

  ninja  [1.11.1]
    args: <no-args>
        2025/02/10 15:04:13|  kind: full  secs:    0.710  mem:  15M  BOD: 48K
        2025/02/10 15:04:14|  kind: incr  secs:    0.101  mem:  12M  BOD: 48K
        2025/02/10 15:04:14|  kind: NULL  secs:    0.031  mem:  15M  BOD: 48K

  bazel  [bazel 8.0.1]
    args: <no-args>
        2025/02/10 15:04:15|  kind: full  secs:   31.774  mem: 531M  BOD: 310M
        2025/02/10 15:04:51|  kind: incr  secs:    3.128  mem: 424M  BOD: 310M
        2025/02/10 15:04:57|  kind: NULL  secs:    1.131  mem: 569M  BOD: 310M

  recursive-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/10 15:05:03|  kind: full  secs:    1.849  mem:  15M  BOD: 48K
        2025/02/10 15:05:05|  kind: incr  secs:    1.106  mem:  12M  BOD: 48K
        2025/02/10 15:05:07|  kind: NULL  secs:    1.004  mem:  15M  BOD: 48K

  recursive-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/10 15:05:08|  kind: full  secs:    0.688  mem:  15M  BOD: 48K
        2025/02/10 15:05:09|  kind: incr  secs:    0.106  mem:  12M  BOD: 48K
        2025/02/10 15:05:10|  kind: NULL  secs:    0.036  mem:  15M  BOD: 48K

  single-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/10 15:05:10|  kind: full  secs:    1.700  mem:  25M  BOD: 48K
        2025/02/10 15:05:12|  kind: incr  secs:    1.092  mem:  21M  BOD: 48K
        2025/02/10 15:05:13|  kind: NULL  secs:    1.008  mem:  25M  BOD: 48K

  single-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/10 15:05:15|  kind: full  secs:    0.705  mem:  15M  BOD: 48K
        2025/02/10 15:05:16|  kind: incr  secs:    0.104  mem:  12M  BOD: 48K
        2025/02/10 15:05:16|  kind: NULL  secs:    0.041  mem:  15M  BOD: 48K

  scons-md5sum  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/10 15:05:16|  kind: full  secs:    3.511  mem:  61M  BOD: 1M
        2025/02/10 15:05:21|  kind: incr  secs:    2.577  mem:  61M  BOD: 1M
        2025/02/10 15:05:24|  kind: NULL  secs:    2.442  mem:  62M  BOD: 1M

  scons-make  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/10 15:05:27|  kind: full  secs:    2.954  mem:  61M  BOD: 1020K
        2025/02/10 15:05:31|  kind: incr  secs:    1.982  mem:  61M  BOD: 1020K
        2025/02/10 15:05:33|  kind: NULL  secs:    1.829  mem:  61M  BOD: 1020K
```

## Arm: 5000 Simulated Modules

```
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
        2025/02/10 15:05:35|  kind: full  secs:   10.370  mem:  18M  BOD: 208K
        2025/02/10 15:05:49|  kind: incr  secs:    2.799  mem:  12M  BOD: 208K
        2025/02/10 15:05:52|  kind: NULL  secs:    2.484  mem:  18M  BOD: 208K

  ninja  [1.11.1]
    args: <no-args>
        2025/02/10 15:05:55|  kind: full  secs:    3.918  mem:  18M  BOD: 208K
        2025/02/10 15:06:03|  kind: incr  secs:    0.255  mem:  17M  BOD: 208K
        2025/02/10 15:06:04|  kind: NULL  secs:    0.142  mem:  18M  BOD: 208K

  bazel  [bazel 8.0.1]
    args: <no-args>
        2025/02/10 15:06:04|  kind: full  secs:   71.107  mem: 721M  BOD: 312M
        2025/02/10 15:07:24|  kind: incr  secs:    6.316  mem: 600M  BOD: 312M
        2025/02/10 15:07:35|  kind: NULL  secs:    1.479  mem: 743M  BOD: 312M

  recursive-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/10 15:07:41|  kind: full  secs:   17.860  mem:  21M  BOD: 208K
        2025/02/10 15:08:03|  kind: incr  secs:   12.842  mem:  21M  BOD: 208K
        2025/02/10 15:08:16|  kind: NULL  secs:   12.529  mem:  21M  BOD: 208K

  recursive-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/10 15:08:28|  kind: full  secs:    3.593  mem:  18M  BOD: 208K
        2025/02/10 15:08:36|  kind: incr  secs:    0.304  mem:  12M  BOD: 208K
        2025/02/10 15:08:37|  kind: NULL  secs:    0.194  mem:  18M  BOD: 208K

  single-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/10 15:08:37|  kind: full  secs:   12.677  mem: 119M  BOD: 208K
        2025/02/10 15:08:54|  kind: incr  secs:    9.214  mem:  96M  BOD: 208K
        2025/02/10 15:09:04|  kind: NULL  secs:    8.861  mem: 119M  BOD: 208K

  single-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/10 15:09:13|  kind: full  secs:    3.637  mem:  36M  BOD: 208K
        2025/02/10 15:09:21|  kind: incr  secs:    0.469  mem:  13M  BOD: 208K
        2025/02/10 15:09:22|  kind: NULL  secs:    0.213  mem:  36M  BOD: 208K

  scons-md5sum  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/10 15:09:22|  kind: full  secs:   18.206  mem: 203M  BOD: 10M
        2025/02/10 15:09:45|  kind: incr  secs:   13.043  mem: 205M  BOD: 10M
        2025/02/10 15:09:58|  kind: NULL  secs:   12.551  mem: 205M  BOD: 10M

  scons-make  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/10 15:10:11|  kind: full  secs:   15.096  mem: 203M  BOD: 7M
        2025/02/10 15:10:31|  kind: incr  secs:    9.880  mem: 202M  BOD: 7M
        2025/02/10 15:10:41|  kind: NULL  secs:    9.531  mem: 203M  BOD: 7M
```


## Arm: 10000 Simulated Modules
```
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
        2025/02/10 15:10:51|  kind: full  secs:   20.976  mem:  23M  BOD: 408K
        2025/02/10 15:11:29|  kind: incr  secs:    5.404  mem:  12M  BOD: 408K
        2025/02/10 15:11:34|  kind: NULL  secs:    5.046  mem:  23M  BOD: 408K

  ninja  [1.11.1]
    args: <no-args>
        2025/02/10 15:11:40|  kind: full  secs:    8.889  mem:  31M  BOD: 408K
        2025/02/10 15:12:07|  kind: incr  secs:    0.440  mem:  31M  BOD: 408K
        2025/02/10 15:12:08|  kind: NULL  secs:    0.308  mem:  31M  BOD: 408K

  bazel  [bazel 8.0.1]
    args: <no-args>
        2025/02/10 15:12:09|  kind: full  secs:  132.899  mem: 862M  BOD: 313M
        2025/02/10 15:14:43|  kind: incr  secs:    8.952  mem: 738M  BOD: 313M
        2025/02/10 15:14:54|  kind: NULL  secs:    2.596  mem:   1G  BOD: 313M

  recursive-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/10 15:15:00|  kind: full  secs:   40.025  mem:  23M  BOD: 408K
        2025/02/10 15:15:58|  kind: incr  secs:   29.255  mem:  23M  BOD: 408K
        2025/02/10 15:16:27|  kind: NULL  secs:   29.157  mem:  23M  BOD: 408K

  recursive-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/10 15:16:57|  kind: full  secs:    7.627  mem:  22M  BOD: 408K
        2025/02/10 15:17:25|  kind: incr  secs:    0.537  mem:  12M  BOD: 408K
        2025/02/10 15:17:26|  kind: NULL  secs:    0.408  mem:  22M  BOD: 408K

  single-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/10 15:17:26|  kind: full  secs:   30.306  mem: 238M  BOD: 408K
        2025/02/10 15:18:19|  kind: incr  secs:   23.285  mem: 191M  BOD: 408K
        2025/02/10 15:18:42|  kind: NULL  secs:   23.008  mem: 238M  BOD: 408K

  single-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/10 15:19:05|  kind: full  secs:    7.578  mem:  71M  BOD: 408K
        2025/02/10 15:19:31|  kind: incr  secs:    0.606  mem:  24M  BOD: 408K
        2025/02/10 15:19:32|  kind: NULL  secs:    0.485  mem:  71M  BOD: 408K

  scons-md5sum  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/10 15:19:33|  kind: full  secs:   37.958  mem: 383M  BOD: 25M
        2025/02/10 15:20:31|  kind: incr  secs:   26.630  mem: 387M  BOD: 25M
        2025/02/10 15:20:58|  kind: NULL  secs:   26.353  mem: 388M  BOD: 25M

  scons-make  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/10 15:21:24|  kind: full  secs:   31.990  mem: 383M  BOD: 17M
        2025/02/10 15:22:16|  kind: incr  secs:   20.795  mem: 380M  BOD: 17M
        2025/02/10 15:22:37|  kind: NULL  secs:   20.427  mem: 383M  BOD: 17M
```


## Arm: 50000 Simulated Modules
```
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
        2025/02/10 15:22:57|  kind: full  secs:  104.314  mem:  56M  BOD: 1M
        2025/02/10 15:28:48|  kind: incr  secs:   26.718  mem:  12M  BOD: 1M
        2025/02/10 15:29:15|  kind: NULL  secs:   26.027  mem:  56M  BOD: 1M

  ninja  [1.11.1]
    args: <no-args>
        2025/02/10 15:29:41|  kind: full  secs:   67.807  mem: 148M  BOD: 1M
        2025/02/10 15:35:08|  kind: incr  secs:    3.014  mem: 148M  BOD: 1M
        2025/02/10 15:35:12|  kind: NULL  secs:    1.841  mem: 148M  BOD: 1M

  bazel  [bazel 8.0.1]
    args: <no-args>
        2025/02/10 15:35:14|  kind: full  secs:  488.375  mem:   1G  BOD: 326M
        2025/02/10 15:48:08|  kind: incr  secs:   36.098  mem:   1G  BOD: 323M
        2025/02/10 15:48:50|  kind: NULL  secs:    8.430  mem:   1G  BOD: 323M

  recursive-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/10 15:49:00|  kind: full  secs:  236.040  mem:  56M  BOD: 1M
        2025/02/10 15:57:24|  kind: incr  secs:  182.009  mem:  27M  BOD: 1M
        2025/02/10 16:00:27|  kind: NULL  secs:  181.286  mem:  56M  BOD: 1M

  recursive-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/10 16:03:28|  kind: full  secs:   36.569  mem:  56M  BOD: 1M
        2025/02/10 16:08:44|  kind: incr  secs:    2.634  mem:  12M  BOD: 1M
        2025/02/10 16:08:47|  kind: NULL  secs:    2.294  mem:  56M  BOD: 1M

  single-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/10 16:08:50|  kind: full  secs:   98.032  mem:   1G  BOD: 1M
        2025/02/10 16:14:50|  kind: incr  secs:   63.288  mem: 936M  BOD: 1M
        2025/02/10 16:15:54|  kind: NULL  secs:   61.804  mem:   1G  BOD: 1M

  single-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/10 16:16:56|  kind: full  secs:   38.742  mem: 363M  BOD: 1M
        2025/02/10 16:22:01|  kind: incr  secs:    4.044  mem: 116M  BOD: 1M
        2025/02/10 16:22:05|  kind: NULL  secs:    3.406  mem: 363M  BOD: 1M

  scons-md5sum  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/10 16:22:09|  kind: full  secs:  289.706  mem:   1G  BOD: 150M
        2025/02/10 16:31:26|  kind: incr  secs:  226.066  mem:   1G  BOD: 150M
        2025/02/10 16:35:12|  kind: NULL  secs:  225.140  mem:   1G  BOD: 150M

  scons-make  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/10 16:38:58|  kind: full  secs:  161.812  mem:   1G  BOD: 105M
        2025/02/10 16:46:00|  kind: incr  secs:  111.307  mem:   1G  BOD: 105M
        2025/02/10 16:47:52|  kind: NULL  secs:  108.260  mem:   1G  BOD: 105M
```


## Arm: 100000 Simulated Modules
```
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
        2025/02/10 16:49:41|  kind: full  secs:  207.359  mem:  99M  BOD: 3M
        2025/02/10 17:03:11|  kind: incr  secs:   54.407  mem:  12M  BOD: 3M
        2025/02/10 17:04:06|  kind: NULL  secs:   52.561  mem:  99M  BOD: 3M

  ninja  [1.11.1]
    args: <no-args>
        2025/02/10 17:04:59|  kind: full  secs:  200.055  mem: 295M  BOD: 3M
        2025/02/10 17:18:47|  kind: incr  secs:    6.896  mem: 295M  BOD: 3M
        2025/02/10 17:18:54|  kind: NULL  secs:    3.961  mem: 295M  BOD: 3M

  bazel  [bazel 8.0.1]
    args: <no-args>
        2025/02/10 17:18:58|  kind: full  secs: 1112.989  mem:   2G  BOD: 341M
        2025/02/10 17:49:21|  kind: incr  secs:  133.383  mem:   2G  BOD: 335M
        2025/02/10 17:51:38|  kind: NULL  secs:   16.195  mem:   2G  BOD: 335M

  recursive-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/10 17:51:59|  kind: full  secs:  501.151  mem:  99M  BOD: 3M
        2025/02/10 18:11:01|  kind: incr  secs:  394.558  mem:  31M  BOD: 3M
        2025/02/10 18:17:36|  kind: NULL  secs:  392.345  mem:  99M  BOD: 3M

  recursive-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/10 18:24:09|  kind: full  secs:   73.399  mem:  99M  BOD: 3M
        2025/02/10 18:36:20|  kind: incr  secs:    5.870  mem:  12M  BOD: 3M
        2025/02/10 18:36:26|  kind: NULL  secs:    4.799  mem:  99M  BOD: 3M

  single-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/10 18:36:31|  kind: full  secs:  205.397  mem:   2G  BOD: 3M
        2025/02/10 18:50:45|  kind: incr  secs:  137.945  mem:   1G  BOD: 3M
        2025/02/10 18:53:04|  kind: NULL  secs:  134.082  mem:   2G  BOD: 3M

  single-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/10 18:55:18|  kind: full  secs:   79.391  mem: 729M  BOD: 3M
        2025/02/10 19:07:10|  kind: incr  secs:   10.180  mem: 230M  BOD: 3M
        2025/02/10 19:07:20|  kind: NULL  secs:    7.781  mem: 729M  BOD: 3M

  scons-md5sum  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/10 19:07:28|  kind: full  secs:  725.886  mem:   3G  BOD: 312M
        2025/02/10 19:30:21|  kind: incr  secs:  579.658  mem:   3G  BOD: 312M
        2025/02/10 19:40:01|  kind: NULL  secs:  607.005  mem:   3G  BOD: 312M

  scons-make  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/10 19:50:09|  kind: full  secs:  330.348  mem:   3G  BOD: 219M
        2025/02/10 20:07:07|  kind: incr  secs:  223.586  mem:   3G  BOD: 219M
        2025/02/10 20:10:51|  kind: NULL  secs:  217.787  mem:   3G  BOD: 219M
```

## x86_64: 50 Simulated Modules
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
        2025/02/11 05:00:02|  kind: full  secs:    0.162  mem:  15M  BOD: 12K
        2025/02/11 05:00:03|  kind: incr  secs:    0.102  mem:  14M  BOD: 12K
        2025/02/11 05:00:03|  kind: NULL  secs:    0.037  mem:  14M  BOD: 12K

  ninja  [1.11.1]
    args: <no-args>
        2025/02/11 05:00:03|  kind: full  secs:    0.071  mem:  15M  BOD: 12K
        2025/02/11 05:00:04|  kind: incr  secs:    0.043  mem:  14M  BOD: 12K
        2025/02/11 05:00:04|  kind: NULL  secs:    0.010  mem:  14M  BOD: 12K

  bazel  [bazel no_version]
    args: <no-args>
        2025/02/11 05:00:04|  kind: full  secs:    9.979  mem: 244M  BOD: 6M
        2025/02/11 05:00:15|  kind: incr  secs:    0.864  mem: 250M  BOD: 10M
        2025/02/11 05:00:20|  kind: NULL  secs:    0.385  mem: 251M  BOD: 9M

  recursive-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/11 05:00:25|  kind: full  secs:    0.118  mem:  15M  BOD: 12K
        2025/02/11 05:00:26|  kind: incr  secs:    0.091  mem:  14M  BOD: 12K
        2025/02/11 05:00:26|  kind: NULL  secs:    0.061  mem:  14M  BOD: 12K

  recursive-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/11 05:00:26|  kind: full  secs:    0.072  mem:  15M  BOD: 12K
        2025/02/11 05:00:27|  kind: incr  secs:    0.045  mem:  14M  BOD: 12K
        2025/02/11 05:00:27|  kind: NULL  secs:    0.015  mem:  14M  BOD: 12K

  single-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/11 05:00:27|  kind: full  secs:    0.114  mem:  15M  BOD: 12K
        2025/02/11 05:00:28|  kind: incr  secs:    0.089  mem:  14M  BOD: 12K
        2025/02/11 05:00:28|  kind: NULL  secs:    0.060  mem:  14M  BOD: 12K

  single-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/11 05:00:28|  kind: full  secs:    0.069  mem:  15M  BOD: 12K
        2025/02/11 05:00:29|  kind: incr  secs:    0.040  mem:  14M  BOD: 12K
        2025/02/11 05:00:29|  kind: NULL  secs:    0.011  mem:  14M  BOD: 12K

  scons-md5sum  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/11 05:00:29|  kind: full  secs:    0.871  mem:  29M  BOD: 52K
        2025/02/11 05:00:31|  kind: incr  secs:    0.769  mem:  29M  BOD: 52K
        2025/02/11 05:00:32|  kind: NULL  secs:    0.709  mem:  29M  BOD: 52K

  scons-make  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/11 05:00:33|  kind: full  secs:    0.786  mem:  28M  BOD: 44K
        2025/02/11 05:00:35|  kind: incr  secs:    0.664  mem:  28M  BOD: 44K
        2025/02/11 05:00:36|  kind: NULL  secs:    0.667  mem:  28M  BOD: 44K
```


## x86_64: 100 Simulated Modules
```
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
        2025/02/11 05:00:37|  kind: full  secs:    0.303  mem:  15M  BOD: 12K
        2025/02/11 05:00:38|  kind: incr  secs:    0.200  mem:  14M  BOD: 12K
        2025/02/11 05:00:39|  kind: NULL  secs:    0.075  mem:  14M  BOD: 12K

  ninja  [1.11.1]
    args: <no-args>
        2025/02/11 05:00:39|  kind: full  secs:    0.124  mem:  15M  BOD: 12K
        2025/02/11 05:00:39|  kind: incr  secs:    0.067  mem:  14M  BOD: 12K
        2025/02/11 05:00:40|  kind: NULL  secs:    0.012  mem:  14M  BOD: 12K

  bazel  [bazel no_version]
    args: <no-args>
        2025/02/11 05:00:40|  kind: full  secs:   10.400  mem: 242M  BOD: 15M
        2025/02/11 05:00:56|  kind: incr  secs:    1.407  mem: 243M  BOD: 21M
        2025/02/11 05:01:01|  kind: NULL  secs:    0.394  mem: 245M  BOD: 20M

  recursive-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/11 05:01:06|  kind: full  secs:    0.230  mem:  15M  BOD: 12K
        2025/02/11 05:01:07|  kind: incr  secs:    0.175  mem:  14M  BOD: 12K
        2025/02/11 05:01:07|  kind: NULL  secs:    0.125  mem:  14M  BOD: 12K

  recursive-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/11 05:01:08|  kind: full  secs:    0.131  mem:  15M  BOD: 12K
        2025/02/11 05:01:08|  kind: incr  secs:    0.070  mem:  14M  BOD: 12K
        2025/02/11 05:01:08|  kind: NULL  secs:    0.020  mem:  14M  BOD: 12K

  single-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/11 05:01:09|  kind: full  secs:    0.232  mem:  15M  BOD: 12K
        2025/02/11 05:01:09|  kind: incr  secs:    0.176  mem:  14M  BOD: 12K
        2025/02/11 05:01:10|  kind: NULL  secs:    0.125  mem:  14M  BOD: 12K

  single-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/11 05:01:10|  kind: full  secs:    0.120  mem:  15M  BOD: 12K
        2025/02/11 05:01:11|  kind: incr  secs:    0.064  mem:  14M  BOD: 12K
        2025/02/11 05:01:11|  kind: NULL  secs:    0.013  mem:  14M  BOD: 12K

  scons-md5sum  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/11 05:01:11|  kind: full  secs:    1.166  mem:  30M  BOD: 92K
        2025/02/11 05:01:13|  kind: incr  secs:    1.042  mem:  30M  BOD: 92K
        2025/02/11 05:01:15|  kind: NULL  secs:    0.934  mem:  30M  BOD: 92K

  scons-make  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/11 05:01:16|  kind: full  secs:    1.073  mem:  30M  BOD: 80K
        2025/02/11 05:01:18|  kind: incr  secs:    0.945  mem:  30M  BOD: 80K
        2025/02/11 05:01:19|  kind: NULL  secs:    0.852  mem:  30M  BOD: 80K
```


## x86_64: 1000 Simulated Modules
```
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
        2025/02/11 05:01:21|  kind: full  secs:    2.837  mem:  17M  BOD: 48K
        2025/02/11 05:01:25|  kind: incr  secs:    1.110  mem:  14M  BOD: 48K
        2025/02/11 05:01:27|  kind: NULL  secs:    0.864  mem:  14M  BOD: 48K

  ninja  [1.11.1]
    args: <no-args>
        2025/02/11 05:01:28|  kind: full  secs:    1.120  mem:  16M  BOD: 48K
        2025/02/11 05:01:31|  kind: incr  secs:    0.157  mem:  14M  BOD: 48K
        2025/02/11 05:01:31|  kind: NULL  secs:    0.047  mem:  14M  BOD: 48K

  bazel  [bazel no_version]
    args: <no-args>
        2025/02/11 05:01:31|  kind: full  secs:   27.226  mem: 300M  BOD: 193M
        2025/02/11 05:02:04|  kind: incr  secs:    2.348  mem: 301M  BOD: 197M
        2025/02/11 05:02:09|  kind: NULL  secs:    0.605  mem: 312M  BOD: 196M

  recursive-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/11 05:02:15|  kind: full  secs:    2.894  mem:  16M  BOD: 48K
        2025/02/11 05:02:21|  kind: incr  secs:    1.912  mem:  14M  BOD: 48K
        2025/02/11 05:02:23|  kind: NULL  secs:    1.816  mem:  14M  BOD: 48K

  recursive-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/11 05:02:25|  kind: full  secs:    1.018  mem:  17M  BOD: 48K
        2025/02/11 05:02:28|  kind: incr  secs:    0.156  mem:  14M  BOD: 48K
        2025/02/11 05:02:28|  kind: NULL  secs:    0.059  mem:  14M  BOD: 48K

  single-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/11 05:02:29|  kind: full  secs:    3.217  mem:  25M  BOD: 48K
        2025/02/11 05:02:34|  kind: incr  secs:    2.262  mem:  22M  BOD: 48K
        2025/02/11 05:02:36|  kind: NULL  secs:    2.122  mem:  21M  BOD: 48K

  single-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/11 05:02:39|  kind: full  secs:    1.113  mem:  17M  BOD: 48K
        2025/02/11 05:02:42|  kind: incr  secs:    0.172  mem:  14M  BOD: 48K
        2025/02/11 05:02:42|  kind: NULL  secs:    0.067  mem:  14M  BOD: 48K

  scons-md5sum  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/11 05:02:42|  kind: full  secs:    7.710  mem:  64M  BOD: 1M
        2025/02/11 05:02:52|  kind: incr  secs:    5.662  mem:  64M  BOD: 1M
        2025/02/11 05:02:59|  kind: NULL  secs:    5.428  mem:  64M  BOD: 1M

  scons-make  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/11 05:03:05|  kind: full  secs:    6.857  mem:  63M  BOD: 1020K
        2025/02/11 05:03:14|  kind: incr  secs:    4.930  mem:  64M  BOD: 1020K
        2025/02/11 05:03:19|  kind: NULL  secs:    4.651  mem:  63M  BOD: 1020K
```


## x86_64: 5000 Simulated Modules
```
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
        2025/02/11 05:03:24|  kind: full  secs:   14.035  mem:  20M  BOD: 208K
        2025/02/11 05:03:47|  kind: incr  secs:    4.955  mem:  14M  BOD: 208K
        2025/02/11 05:03:52|  kind: NULL  secs:    4.538  mem:  14M  BOD: 208K

  ninja  [1.11.1]
    args: <no-args>
        2025/02/11 05:03:57|  kind: full  secs:    6.079  mem:  20M  BOD: 208K
        2025/02/11 05:04:12|  kind: incr  secs:    0.427  mem:  17M  BOD: 208K
        2025/02/11 05:04:13|  kind: NULL  secs:    0.254  mem:  17M  BOD: 208K

  bazel  [bazel no_version]
    args: <no-args>
        2025/02/11 05:04:13|  kind: full  secs:   82.779  mem: 447M  BOD: 1G
        2025/02/11 05:05:54|  kind: incr  secs:    4.040  mem: 432M  BOD: 1G
        2025/02/11 05:06:04|  kind: NULL  secs:    1.091  mem: 437M  BOD: 1G

  recursive-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/11 05:06:09|  kind: full  secs:   28.723  mem:  21M  BOD: 208K
        2025/02/11 05:06:58|  kind: incr  secs:   22.408  mem:  21M  BOD: 208K
        2025/02/11 05:07:21|  kind: NULL  secs:   22.236  mem:  21M  BOD: 208K

  recursive-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/11 05:07:43|  kind: full  secs:    5.322  mem:  20M  BOD: 208K
        2025/02/11 05:07:58|  kind: incr  secs:    0.467  mem:  14M  BOD: 208K
        2025/02/11 05:07:58|  kind: NULL  secs:    0.319  mem:  14M  BOD: 208K

  single-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/11 05:07:59|  kind: full  secs:   30.030  mem: 119M  BOD: 208K
        2025/02/11 05:08:38|  kind: incr  secs:   24.813  mem:  96M  BOD: 208K
        2025/02/11 05:09:03|  kind: NULL  secs:   24.473  mem:  96M  BOD: 208K

  single-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/11 05:09:28|  kind: full  secs:    5.687  mem:  37M  BOD: 208K
        2025/02/11 05:09:43|  kind: incr  secs:    0.569  mem:  14M  BOD: 208K
        2025/02/11 05:09:44|  kind: NULL  secs:    0.417  mem:  14M  BOD: 208K

  scons-md5sum  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/11 05:09:44|  kind: full  secs:   38.602  mem: 206M  BOD: 10M
        2025/02/11 05:10:32|  kind: incr  secs:   28.222  mem: 208M  BOD: 10M
        2025/02/11 05:11:01|  kind: NULL  secs:   27.707  mem: 208M  BOD: 10M

  scons-make  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/11 05:11:29|  kind: full  secs:   34.891  mem: 206M  BOD: 7M
        2025/02/11 05:12:14|  kind: incr  secs:   24.335  mem: 204M  BOD: 7M
        2025/02/11 05:12:39|  kind: NULL  secs:   23.652  mem: 204M  BOD: 7M
```


## x86_64: 10000 Simulated Modules
```
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
        2025/02/11 05:13:03|  kind: full  secs:   28.340  mem:  24M  BOD: 408K
        2025/02/11 05:13:49|  kind: incr  secs:    9.651  mem:  14M  BOD: 408K
        2025/02/11 05:13:59|  kind: NULL  secs:    9.125  mem:  14M  BOD: 408K

  ninja  [1.11.1]
    args: <no-args>
        2025/02/11 05:14:08|  kind: full  secs:   13.282  mem:  31M  BOD: 408K
        2025/02/11 05:14:39|  kind: incr  secs:    0.762  mem:  31M  BOD: 408K
        2025/02/11 05:14:40|  kind: NULL  secs:    0.551  mem:  31M  BOD: 408K

  bazel  [bazel no_version]
    args: <no-args>
        2025/02/11 05:14:41|  kind: full  secs:  153.257  mem: 599M  BOD: 2G
        2025/02/11 05:18:06|  kind: incr  secs:    5.341  mem: 534M  BOD: 2G
        2025/02/11 05:18:32|  kind: NULL  secs:    1.677  mem: 533M  BOD: 2G

  recursive-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/11 05:18:42|  kind: full  secs:   65.597  mem:  24M  BOD: 408K
        2025/02/11 05:20:31|  kind: incr  secs:   51.895  mem:  23M  BOD: 408K
        2025/02/11 05:21:23|  kind: NULL  secs:   51.756  mem:  23M  BOD: 408K

  recursive-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/11 05:22:15|  kind: full  secs:   10.131  mem:  24M  BOD: 408K
        2025/02/11 05:22:43|  kind: incr  secs:    0.855  mem:  14M  BOD: 408K
        2025/02/11 05:22:44|  kind: NULL  secs:    0.678  mem:  14M  BOD: 408K

  single-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/11 05:22:45|  kind: full  secs:   72.458  mem: 239M  BOD: 408K
        2025/02/11 05:24:16|  kind: incr  secs:   61.861  mem: 191M  BOD: 408K
        2025/02/11 05:25:18|  kind: NULL  secs:   61.556  mem: 191M  BOD: 408K

  single-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/11 05:26:20|  kind: full  secs:   11.604  mem:  72M  BOD: 408K
        2025/02/11 05:26:50|  kind: incr  secs:    1.126  mem:  25M  BOD: 408K
        2025/02/11 05:26:51|  kind: NULL  secs:    0.938  mem:  24M  BOD: 408K

  scons-md5sum  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/11 05:26:52|  kind: full  secs:   78.830  mem: 386M  BOD: 25M
        2025/02/11 05:28:30|  kind: incr  secs:   57.915  mem: 390M  BOD: 25M
        2025/02/11 05:29:28|  kind: NULL  secs:   56.758  mem: 390M  BOD: 25M

  scons-make  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/11 05:30:26|  kind: full  secs:   70.844  mem: 386M  BOD: 17M
        2025/02/11 05:31:55|  kind: incr  secs:   50.010  mem: 383M  BOD: 17M
        2025/02/11 05:32:46|  kind: NULL  secs:   48.977  mem: 383M  BOD: 17M
```


## x86_64: 50000 Simulated Modules
```
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
        2025/02/11 05:33:36|  kind: full  secs:  141.801  mem:  58M  BOD: 1M
        2025/02/11 05:38:34|  kind: incr  secs:   49.586  mem:  14M  BOD: 1M
        2025/02/11 05:39:24|  kind: NULL  secs:   47.079  mem:  14M  BOD: 1M

  ninja  [1.11.1]
    args: <no-args>
        2025/02/11 05:40:12|  kind: full  secs:  122.187  mem: 149M  BOD: 1M
        2025/02/11 05:44:53|  kind: incr  secs:    4.964  mem: 149M  BOD: 1M
        2025/02/11 05:44:58|  kind: NULL  secs:    3.364  mem: 149M  BOD: 1M

  bazel  [bazel no_version]
    args: <no-args>
        2025/02/11 05:45:02|  kind: full  secs:  694.389  mem:   1G  BOD: 13G
        2025/02/11 06:09:12|  kind: incr  secs:   16.908  mem:   1G  BOD: 12G
        2025/02/11 06:17:36|  kind: NULL  secs:    6.821  mem:   1G  BOD: 12G

  recursive-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/11 06:26:36|  kind: full  secs:  383.581  mem:  58M  BOD: 1M
        2025/02/11 06:44:28|  kind: incr  secs:  321.401  mem:  28M  BOD: 1M
        2025/02/11 06:49:50|  kind: NULL  secs:  319.003  mem:  28M  BOD: 1M

  recursive-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/11 06:55:09|  kind: full  secs:   51.577  mem:  58M  BOD: 1M
        2025/02/11 06:58:40|  kind: incr  secs:    4.701  mem:  14M  BOD: 1M
        2025/02/11 06:58:45|  kind: NULL  secs:    3.780  mem:  14M  BOD: 1M

  single-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/11 06:58:49|  kind: full  secs:  192.059  mem:   1G  BOD: 1M
        2025/02/11 07:04:39|  kind: incr  secs:  139.175  mem: 936M  BOD: 1M
        2025/02/11 07:06:58|  kind: NULL  secs:  136.516  mem: 936M  BOD: 1M

  single-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/11 07:09:15|  kind: full  secs:   60.244  mem: 364M  BOD: 1M
        2025/02/11 07:12:52|  kind: incr  secs:    8.085  mem: 116M  BOD: 1M
        2025/02/11 07:13:00|  kind: NULL  secs:    6.295  mem: 116M  BOD: 1M

  scons-md5sum  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/11 07:13:07|  kind: full  secs:  465.725  mem:   1G  BOD: 150M
        2025/02/11 07:23:34|  kind: incr  secs:  379.641  mem:   1G  BOD: 150M
        2025/02/11 07:29:55|  kind: NULL  secs:  374.851  mem:   1G  BOD: 150M

  scons-make  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/11 07:36:10|  kind: full  secs:  365.600  mem:   1G  BOD: 105M
        2025/02/11 07:45:02|  kind: incr  secs:  262.734  mem:   1G  BOD: 105M
        2025/02/11 07:49:26|  kind: NULL  secs:  255.490  mem:   1G  BOD: 105M
```


## x86_64: 100000 Simulated Modules
```
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
        2025/02/11 07:53:42|  kind: full  secs:  283.809  mem: 100M  BOD: 3M
        2025/02/11 08:04:06|  kind: incr  secs:   99.422  mem:  14M  BOD: 3M
        2025/02/11 08:05:46|  kind: NULL  secs:   94.851  mem:  14M  BOD: 3M

  ninja  [1.11.1]
    args: <no-args>
        2025/02/11 08:07:22|  kind: full  secs:  407.131  mem: 296M  BOD: 3M
        2025/02/11 08:19:53|  kind: incr  secs:   10.358  mem: 296M  BOD: 3M
        2025/02/11 08:20:04|  kind: NULL  secs:    7.073  mem: 296M  BOD: 3M

  bazel  [bazel no_version]
    args: <no-args>
        2025/02/11 08:20:12|  kind: full  secs: 1381.402  mem:   4G  BOD: 26G
        2025/02/11 09:13:45|  kind: incr  secs:   61.911  mem:   2G  BOD: 25G
        2025/02/11 09:37:11|  kind: NULL  secs:   20.193  mem:   1G  BOD: 25G

  recursive-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/11 09:59:31|  kind: full  secs:  818.571  mem: 101M  BOD: 3M
        2025/02/11 10:39:16|  kind: incr  secs:  692.201  mem:  31M  BOD: 3M
        2025/02/11 10:50:49|  kind: NULL  secs:  688.101  mem:  31M  BOD: 3M

  recursive-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/11 11:02:17|  kind: full  secs:  103.786  mem: 101M  BOD: 3M
        2025/02/11 11:09:49|  kind: incr  secs:    9.486  mem:  14M  BOD: 3M
        2025/02/11 11:09:59|  kind: NULL  secs:    7.816  mem:  14M  BOD: 3M

  single-make  [GNU Make 4.3]
    args: <no-args>
        2025/02/11 11:10:07|  kind: full  secs:  396.181  mem:   2G  BOD: 3M
        2025/02/11 11:22:34|  kind: incr  secs:  292.019  mem:   1G  BOD: 3M
        2025/02/11 11:27:27|  kind: NULL  secs:  285.583  mem:   1G  BOD: 3M

  single-make  [GNU Make 4.3]
    args: --no-builtin-rules --no-builtin-variables
        2025/02/11 11:32:13|  kind: full  secs:  122.269  mem: 730M  BOD: 3M
        2025/02/11 11:40:00|  kind: incr  secs:   17.799  mem: 230M  BOD: 3M
        2025/02/11 11:40:18|  kind: NULL  secs:   14.232  mem: 230M  BOD: 3M

  scons-md5sum  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/11 11:40:33|  kind: full  secs:  935.801  mem:   3G  BOD: 312M
        2025/02/11 12:02:06|  kind: incr  secs:  761.875  mem:   3G  BOD: 312M
        2025/02/11 12:14:49|  kind: NULL  secs:  747.380  mem:   3G  BOD: 312M

  scons-make  [SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021]
    args: <no-args>
        2025/02/11 12:27:18|  kind: full  secs:  740.372  mem:   3G  BOD: 219M
        2025/02/11 12:45:36|  kind: incr  secs:  530.447  mem:   3G  BOD: 219M
        2025/02/11 12:54:27|  kind: NULL  secs:  520.466  mem:   3G  BOD: 219M
```

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

## Bash (5.2.21)

```
tool: bash  | version: GNU bash, version 5.2.21(1)-release (aarch64-unknown-linux-gnu)
  aarch64
   Linux-6.8.0-1018-raspi-aarch64-with-glibc2.39
   #20-Ubuntu SMP PREEMPT_DYNAMIC Fri Jan 17 12:35:36 UTC 2025
   CPU count    : 4
   Memory       : 7G
     Module Count : 50
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 17:50:16|  kind: full  secs:    0.113  mem:  12M  BOD: 12K
        2025/02/01 17:50:29|  kind: incr  secs:    0.072  mem:  12M  BOD: 12K
        2025/02/01 17:50:29|  kind: NULL  secs:    0.022  mem:  12M  BOD: 12K

     Module Count : 100
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 17:51:22|  kind: full  secs:    0.210  mem:  12M  BOD: 12K
        2025/02/01 17:51:23|  kind: incr  secs:    0.132  mem:  12M  BOD: 12K
        2025/02/01 17:51:23|  kind: NULL  secs:    0.042  mem:  12M  BOD: 12K

     Module Count : 1000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 17:52:17|  kind: full  secs:    2.065  mem:  12M  BOD: 48K
        2025/02/01 17:52:19|  kind: incr  secs:    0.672  mem:  12M  BOD: 48K
        2025/02/01 17:52:20|  kind: NULL  secs:    0.474  mem:  12M  BOD: 48K

     Module Count : 5000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 17:53:47|  kind: full  secs:   10.419  mem:  16M  BOD: 208K
        2025/02/01 17:54:00|  kind: incr  secs:    2.786  mem:  12M  BOD: 208K
        2025/02/01 17:54:03|  kind: NULL  secs:    2.478  mem:  16M  BOD: 208K

     Module Count : 10000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 17:58:38|  kind: full  secs:   20.983  mem:  20M  BOD: 408K
        2025/02/01 17:59:03|  kind: incr  secs:    5.429  mem:  12M  BOD: 408K
        2025/02/01 17:59:09|  kind: NULL  secs:    5.039  mem:  20M  BOD: 408K

     Module Count : 50000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 18:07:52|  kind: full  secs:  104.391  mem:  53M  BOD: 2.0M
        2025/02/01 18:10:10|  kind: incr  secs:   26.828  mem:  12M  BOD: 2.0M
        2025/02/01 18:10:37|  kind: NULL  secs:   26.013  mem:  53M  BOD: 2.0M

     Module Count : 100000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 18:51:58|  kind: full  secs:  210.139  mem:  95M  BOD: 4.0M
        2025/02/01 18:57:11|  kind: incr  secs:   53.245  mem:  12M  BOD: 4.0M
        2025/02/01 18:58:05|  kind: NULL  secs:   52.750  mem:  95M  BOD: 4.0M
```



## Bash (5.1.16)

```
tool: bash  | version: GNU bash, version 5.1.16(1)-release (x86_64-pc-linux-gnu)
  x86_64
   Linux-6.8.0-48-generic-x86_64-with-glibc2.39
   #48~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Mon Oct  7 11:24:13 UTC 2
   CPU count    : 4
   Memory       : 7G
     Module Count : 50
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 21:15:47|  kind: full  secs:    0.143  mem:  14M  BOD: 12K
        2025/02/01 21:15:47|  kind: incr  secs:    0.099  mem:  14M  BOD: 12K
        2025/02/01 21:15:47|  kind: NULL  secs:    0.037  mem:  14M  BOD: 12K

     Module Count : 100
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 21:16:20|  kind: full  secs:    0.293  mem:  14M  BOD: 12K
        2025/02/01 21:16:21|  kind: incr  secs:    0.182  mem:  14M  BOD: 12K
        2025/02/01 21:16:21|  kind: NULL  secs:    0.077  mem:  14M  BOD: 12K

     Module Count : 1000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 21:17:02|  kind: full  secs:    2.765  mem:  14M  BOD: 48K
        2025/02/01 21:17:06|  kind: incr  secs:    1.107  mem:  14M  BOD: 48K
        2025/02/01 21:17:08|  kind: NULL  secs:    0.873  mem:  14M  BOD: 48K

     Module Count : 5000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 21:18:57|  kind: full  secs:   13.713  mem:  17M  BOD: 208K
        2025/02/01 21:19:17|  kind: incr  secs:    4.973  mem:  14M  BOD: 208K
        2025/02/01 21:19:22|  kind: NULL  secs:    4.582  mem:  14M  BOD: 208K

     Module Count : 10000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 21:27:57|  kind: full  secs:   27.548  mem:  21M  BOD: 408K
        2025/02/01 21:28:37|  kind: incr  secs:    9.725  mem:  14M  BOD: 408K
        2025/02/01 21:28:47|  kind: NULL  secs:    9.291  mem:  14M  BOD: 408K

     Module Count : 50000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 21:46:18|  kind: full  secs:  138.719  mem:  55M  BOD: 2.0M
        2025/02/01 21:49:38|  kind: incr  secs:   47.720  mem:  14M  BOD: 2.0M
        2025/02/01 21:50:26|  kind: NULL  secs:   47.117  mem:  14M  BOD: 2.0M

     Module Count : 100000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 23:51:10|  kind: full  secs:  278.484  mem:  97M  BOD: 4.0M
        2025/02/01 23:57:59|  kind: incr  secs:   95.449  mem:  14M  BOD: 4.0M
        2025/02/01 23:59:35|  kind: NULL  secs:   94.876  mem:  14M  BOD: 4.0M
```



## Bazel (8.0.1)

```
tool: bazel  | version: bazel 8.0.1
  aarch64
   Linux-6.8.0-1018-raspi-aarch64-with-glibc2.39
   #20-Ubuntu SMP PREEMPT_DYNAMIC Fri Jan 17 12:35:36 UTC 2025
   CPU count    : 4
   Memory       : 7G
     Module Count : 50
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 17:50:29|  kind: full  secs:   34.534  mem: 506M  BOD: 311M
        2025/02/01 17:51:06|  kind: incr  secs:    1.567  mem: 379M  BOD: 311M
        2025/02/01 17:51:11|  kind: NULL  secs:    0.755  mem: 524M  BOD: 311M

     Module Count : 100
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 17:51:23|  kind: full  secs:   33.053  mem: 510M  BOD: 311M
        2025/02/01 17:51:59|  kind: incr  secs:    1.910  mem: 378M  BOD: 311M
        2025/02/01 17:52:04|  kind: NULL  secs:    0.778  mem: 527M  BOD: 311M

     Module Count : 1000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 17:52:21|  kind: full  secs:   43.711  mem: 554M  BOD: 311M
        2025/02/01 17:53:07|  kind: incr  secs:    3.423  mem: 438M  BOD: 311M
        2025/02/01 17:53:12|  kind: NULL  secs:    1.108  mem: 575M  BOD: 311M

     Module Count : 5000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 17:54:05|  kind: full  secs:   76.591  mem: 718M  BOD: 313M
        2025/02/01 17:55:29|  kind: incr  secs:    6.486  mem: 593M  BOD: 313M
        2025/02/01 17:55:40|  kind: NULL  secs:    1.383  mem: 734M  BOD: 313M

     Module Count : 10000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 17:59:14|  kind: full  secs:  114.382  mem: 813M  BOD: 314M
        2025/02/01 18:01:17|  kind: incr  secs:    9.399  mem: 767M  BOD: 314M
        2025/02/01 18:01:27|  kind: NULL  secs:    2.367  mem:   1G  BOD: 314M

     Module Count : 50000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 18:11:03|  kind: full  secs:  416.174  mem:   2G  BOD: 327M
        2025/02/01 18:18:43|  kind: incr  secs:   39.375  mem:   2G  BOD: 324M
        2025/02/01 18:19:24|  kind: NULL  secs:    8.258  mem:   2G  BOD: 324M

     Module Count : 100000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 18:58:58|  kind: full  secs:  926.528  mem:   2G  BOD: 342M
        2025/02/01 19:23:07|  kind: incr  secs:  127.350  mem:   2G  BOD: 336M
        2025/02/01 19:25:19|  kind: NULL  secs:   16.667  mem:   2G  BOD: 336M
```



## Bazel (no_version)
```
tool: bazel  | version: bazel no_version
  x86_64
   Linux-6.8.0-48-generic-x86_64-with-glibc2.39
   #48~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Mon Oct  7 11:24:13 UTC 2
   CPU count    : 4
   Memory       : 7G
     Module Count : 50
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 21:15:48|  kind: full  secs:    9.140  mem: 234M  BOD: 7.0M
        2025/02/01 21:15:58|  kind: incr  secs:    0.898  mem: 235M  BOD: 11M
        2025/02/01 21:16:03|  kind: NULL  secs:    0.376  mem: 237M  BOD: 9.9M

     Module Count : 100
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 21:16:22|  kind: full  secs:   10.575  mem: 253M  BOD: 16M
        2025/02/01 21:16:37|  kind: incr  secs:    1.364  mem: 261M  BOD: 22M
        2025/02/01 21:16:43|  kind: NULL  secs:    0.418  mem: 263M  BOD: 21M

     Module Count : 1000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 21:17:09|  kind: full  secs:   28.215  mem: 297M  BOD: 194M
        2025/02/01 21:17:41|  kind: incr  secs:    2.300  mem: 294M  BOD: 198M
        2025/02/01 21:17:46|  kind: NULL  secs:    0.562  mem: 297M  BOD: 197M

     Module Count : 5000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 21:19:27|  kind: full  secs:   81.639  mem: 459M  BOD: 1.2G
        2025/02/01 21:21:04|  kind: incr  secs:    4.230  mem: 442M  BOD: 1.1G
        2025/02/01 21:21:15|  kind: NULL  secs:    1.057  mem: 449M  BOD: 1.1G

     Module Count : 10000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 21:28:56|  kind: full  secs:  141.639  mem: 625M  BOD: 2.5G
        2025/02/01 21:31:41|  kind: incr  secs:    5.969  mem: 579M  BOD: 2.4G
        2025/02/01 21:31:57|  kind: NULL  secs:    1.677  mem: 573M  BOD: 2.4G

     Module Count : 50000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 21:51:14|  kind: full  secs:  677.024  mem:   1G  BOD: 14G
        2025/02/01 22:14:46|  kind: incr  secs:   18.823  mem:   1G  BOD: 13G
        2025/02/01 22:24:46|  kind: NULL  secs:   24.997  mem:   1G  BOD: 13G

     Module Count : 100000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/02 00:01:10|  kind: full  secs: 1452.776  mem:   2G  BOD: 27G
        2025/02/02 00:54:43|  kind: incr  secs:   51.783  mem:   2G  BOD: 26G
        2025/02/02 01:16:58|  kind: NULL  secs:   12.719  mem:   2G  BOD: 26G
```



## Gnu Make (4.3, recursive Makefile)
```
tool: recursive-make  | version: GNU Make 4.3
  aarch64
   Linux-6.8.0-1018-raspi-aarch64-with-glibc2.39
   #20-Ubuntu SMP PREEMPT_DYNAMIC Fri Jan 17 12:35:36 UTC 2025
   CPU count    : 4
   Memory       : 7G
     Module Count : 50
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 17:51:16|  kind: full  secs:    0.073  mem:  12M  BOD: 12K
        2025/02/01 17:51:17|  kind: incr  secs:    0.051  mem:  12M  BOD: 12K
        2025/02/01 17:51:17|  kind: NULL  secs:    0.037  mem:  12M  BOD: 12K

     Module Count : 100
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 17:52:10|  kind: full  secs:    0.132  mem:  12M  BOD: 12K
        2025/02/01 17:52:10|  kind: incr  secs:    0.099  mem:  12M  BOD: 12K
        2025/02/01 17:52:10|  kind: NULL  secs:    0.070  mem:  12M  BOD: 12K

     Module Count : 1000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 17:53:18|  kind: full  secs:    1.840  mem:  12M  BOD: 48K
        2025/02/01 17:53:20|  kind: incr  secs:    1.109  mem:  12M  BOD: 48K
        2025/02/01 17:53:21|  kind: NULL  secs:    1.015  mem:  12M  BOD: 48K

     Module Count : 5000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 17:55:45|  kind: full  secs:   17.668  mem:  21M  BOD: 208K
        2025/02/01 17:56:05|  kind: incr  secs:   12.663  mem:  20M  BOD: 208K
        2025/02/01 17:56:18|  kind: NULL  secs:   12.490  mem:  21M  BOD: 208K

     Module Count : 10000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 18:01:33|  kind: full  secs:   40.217  mem:  23M  BOD: 408K
        2025/02/01 18:02:18|  kind: incr  secs:   29.133  mem:  23M  BOD: 408K
        2025/02/01 18:02:48|  kind: NULL  secs:   29.099  mem:  23M  BOD: 408K

     Module Count : 50000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 18:19:34|  kind: full  secs:  237.013  mem:  53M  BOD: 2.0M
        2025/02/01 18:24:19|  kind: incr  secs:  181.387  mem:  27M  BOD: 2.0M
        2025/02/01 18:27:21|  kind: NULL  secs:  181.093  mem:  53M  BOD: 2.0M

     Module Count : 100000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 19:25:39|  kind: full  secs:  499.480  mem:  95M  BOD: 4.0M
        2025/02/01 19:36:09|  kind: incr  secs:  390.895  mem:  31M  BOD: 4.0M
        2025/02/01 19:42:40|  kind: NULL  secs:  391.004  mem:  95M  BOD: 4.0M

     Module Count : 50
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : --no-builtin-rules --no-builtin-variables

        2025/02/01 17:51:17|  kind: full  secs:    0.047  mem:  12M  BOD: 12K
        2025/02/01 17:51:17|  kind: incr  secs:    0.030  mem:  12M  BOD: 12K
        2025/02/01 17:51:18|  kind: NULL  secs:    0.009  mem:  12M  BOD: 12K

     Module Count : 100
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : --no-builtin-rules --no-builtin-variables

        2025/02/01 17:52:11|  kind: full  secs:    0.083  mem:  12M  BOD: 12K
        2025/02/01 17:52:11|  kind: incr  secs:    0.045  mem:  12M  BOD: 12K
        2025/02/01 17:52:11|  kind: NULL  secs:    0.011  mem:  12M  BOD: 12K

     Module Count : 1000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : --no-builtin-rules --no-builtin-variables

        2025/02/01 17:53:23|  kind: full  secs:    0.703  mem:  12M  BOD: 48K
        2025/02/01 17:53:24|  kind: incr  secs:    0.100  mem:  12M  BOD: 48K
        2025/02/01 17:53:24|  kind: NULL  secs:    0.036  mem:  12M  BOD: 48K

     Module Count : 5000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : --no-builtin-rules --no-builtin-variables

        2025/02/01 17:56:31|  kind: full  secs:    3.558  mem:  16M  BOD: 208K
        2025/02/01 17:56:37|  kind: incr  secs:    0.300  mem:  12M  BOD: 208K
        2025/02/01 17:56:37|  kind: NULL  secs:    0.193  mem:  16M  BOD: 208K

     Module Count : 10000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : --no-builtin-rules --no-builtin-variables

        2025/02/01 18:03:17|  kind: full  secs:    7.229  mem:  20M  BOD: 408K
        2025/02/01 18:03:29|  kind: incr  secs:    0.560  mem:  12M  BOD: 408K
        2025/02/01 18:03:30|  kind: NULL  secs:    0.425  mem:  20M  BOD: 408K

     Module Count : 50000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : --no-builtin-rules --no-builtin-variables

        2025/02/01 18:30:22|  kind: full  secs:   37.172  mem:  53M  BOD: 2.0M
        2025/02/01 18:31:43|  kind: incr  secs:    2.459  mem:  12M  BOD: 2.0M
        2025/02/01 18:31:46|  kind: NULL  secs:    2.301  mem:  53M  BOD: 2.0M

     Module Count : 100000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : --no-builtin-rules --no-builtin-variables

        2025/02/01 19:49:12|  kind: full  secs:   73.162  mem:  95M  BOD: 4.0M
        2025/02/01 19:52:20|  kind: incr  secs:    5.038  mem:  12M  BOD: 4.0M
        2025/02/01 19:52:26|  kind: NULL  secs:    4.792  mem:  95M  BOD: 4.0M

  x86_64
   Linux-6.8.0-48-generic-x86_64-with-glibc2.39
   #48~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Mon Oct  7 11:24:13 UTC 2
   CPU count    : 4
   Memory       : 7G
     Module Count : 50
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 21:16:09|  kind: full  secs:    0.132  mem:  14M  BOD: 12K
        2025/02/01 21:16:09|  kind: incr  secs:    0.091  mem:  14M  BOD: 12K
        2025/02/01 21:16:10|  kind: NULL  secs:    0.061  mem:  14M  BOD: 12K

     Module Count : 100
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 21:16:48|  kind: full  secs:    0.234  mem:  14M  BOD: 12K
        2025/02/01 21:16:49|  kind: incr  secs:    0.179  mem:  14M  BOD: 12K
        2025/02/01 21:16:49|  kind: NULL  secs:    0.129  mem:  14M  BOD: 12K

     Module Count : 1000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 21:17:51|  kind: full  secs:    2.981  mem:  14M  BOD: 48K
        2025/02/01 21:17:57|  kind: incr  secs:    1.969  mem:  14M  BOD: 48K
        2025/02/01 21:18:00|  kind: NULL  secs:    1.956  mem:  14M  BOD: 48K

     Module Count : 5000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 21:21:20|  kind: full  secs:   29.704  mem:  21M  BOD: 208K
        2025/02/01 21:22:09|  kind: incr  secs:   23.439  mem:  21M  BOD: 208K
        2025/02/01 21:22:32|  kind: NULL  secs:   22.885  mem:  21M  BOD: 208K

     Module Count : 10000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 21:32:12|  kind: full  secs:   64.502  mem:  24M  BOD: 408K
        2025/02/01 21:33:56|  kind: incr  secs:   52.175  mem:  23M  BOD: 408K
        2025/02/01 21:34:49|  kind: NULL  secs:   52.295  mem:  23M  BOD: 408K

     Module Count : 50000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 22:34:36|  kind: full  secs:  385.007  mem:  55M  BOD: 2.0M
        2025/02/01 22:51:15|  kind: incr  secs:  326.528  mem:  28M  BOD: 2.0M
        2025/02/01 22:56:42|  kind: NULL  secs:  323.719  mem:  28M  BOD: 2.0M

     Module Count : 100000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/02 01:39:34|  kind: full  secs:  820.231  mem:  97M  BOD: 4.0M
        2025/02/02 02:17:39|  kind: incr  secs:  702.444  mem:  31M  BOD: 4.0M
        2025/02/02 02:29:22|  kind: NULL  secs:  698.523  mem:  31M  BOD: 4.0M

     Module Count : 50
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : --no-builtin-rules --no-builtin-variables

        2025/02/01 21:16:10|  kind: full  secs:    0.073  mem:  14M  BOD: 12K
        2025/02/01 21:16:10|  kind: incr  secs:    0.044  mem:  14M  BOD: 12K
        2025/02/01 21:16:10|  kind: NULL  secs:    0.015  mem:  14M  BOD: 12K

     Module Count : 100
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : --no-builtin-rules --no-builtin-variables

        2025/02/01 21:16:49|  kind: full  secs:    0.130  mem:  14M  BOD: 12K
        2025/02/01 21:16:50|  kind: incr  secs:    0.079  mem:  14M  BOD: 12K
        2025/02/01 21:16:50|  kind: NULL  secs:    0.019  mem:  14M  BOD: 12K

     Module Count : 1000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : --no-builtin-rules --no-builtin-variables

        2025/02/01 21:18:02|  kind: full  secs:    1.016  mem:  14M  BOD: 48K
        2025/02/01 21:18:04|  kind: incr  secs:    0.193  mem:  14M  BOD: 48K
        2025/02/01 21:18:05|  kind: NULL  secs:    0.061  mem:  14M  BOD: 48K

     Module Count : 5000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : --no-builtin-rules --no-builtin-variables

        2025/02/01 21:22:55|  kind: full  secs:    5.073  mem:  17M  BOD: 208K
        2025/02/01 21:23:07|  kind: incr  secs:    0.495  mem:  14M  BOD: 208K
        2025/02/01 21:23:08|  kind: NULL  secs:    0.324  mem:  14M  BOD: 208K

     Module Count : 10000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : --no-builtin-rules --no-builtin-variables

        2025/02/01 21:35:41|  kind: full  secs:    9.920  mem:  21M  BOD: 408K
        2025/02/01 21:36:04|  kind: incr  secs:    0.842  mem:  14M  BOD: 408K
        2025/02/01 21:36:05|  kind: NULL  secs:    0.682  mem:  14M  BOD: 408K

     Module Count : 50000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : --no-builtin-rules --no-builtin-variables

        2025/02/01 23:02:06|  kind: full  secs:   50.193  mem:  55M  BOD: 2.0M
        2025/02/01 23:04:16|  kind: incr  secs:    4.104  mem:  14M  BOD: 2.0M
        2025/02/01 23:04:20|  kind: NULL  secs:    3.779  mem:  14M  BOD: 2.0M

     Module Count : 100000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : --no-builtin-rules --no-builtin-variables

        2025/02/02 02:41:01|  kind: full  secs:  101.691  mem:  97M  BOD: 4.0M
        2025/02/02 02:45:59|  kind: incr  secs:    9.329  mem:  14M  BOD: 4.0M
        2025/02/02 02:46:09|  kind: NULL  secs:    7.888  mem:  14M  BOD: 4.0M
```



## Gnu Make (4.3, single Makefile)
```
tool: single-make  | version: GNU Make 4.3
  aarch64
   Linux-6.8.0-1018-raspi-aarch64-with-glibc2.39
   #20-Ubuntu SMP PREEMPT_DYNAMIC Fri Jan 17 12:35:36 UTC 2025
   CPU count    : 4
   Memory       : 7G
     Module Count : 50
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 17:51:18|  kind: full  secs:    0.091  mem:  12M  BOD: 12K
        2025/02/01 17:51:18|  kind: incr  secs:    0.051  mem:  12M  BOD: 12K
        2025/02/01 17:51:18|  kind: NULL  secs:    0.034  mem:  12M  BOD: 12K

     Module Count : 100
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 17:52:11|  kind: full  secs:    0.137  mem:  12M  BOD: 12K
        2025/02/01 17:52:11|  kind: incr  secs:    0.099  mem:  12M  BOD: 12K
        2025/02/01 17:52:12|  kind: NULL  secs:    0.068  mem:  12M  BOD: 12K

     Module Count : 1000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 17:53:24|  kind: full  secs:    1.706  mem:  25M  BOD: 48K
        2025/02/01 17:53:27|  kind: incr  secs:    1.109  mem:  21M  BOD: 48K
        2025/02/01 17:53:28|  kind: NULL  secs:    1.003  mem:  25M  BOD: 48K

     Module Count : 5000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 17:56:38|  kind: full  secs:   12.701  mem: 119M  BOD: 208K
        2025/02/01 17:56:53|  kind: incr  secs:    9.331  mem:  96M  BOD: 208K
        2025/02/01 17:57:02|  kind: NULL  secs:    9.256  mem: 119M  BOD: 208K

     Module Count : 10000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 18:03:31|  kind: full  secs:   31.042  mem: 238M  BOD: 408K
        2025/02/01 18:04:08|  kind: incr  secs:   23.934  mem: 191M  BOD: 408K
        2025/02/01 18:04:32|  kind: NULL  secs:   23.401  mem: 238M  BOD: 408K

     Module Count : 50000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 18:31:48|  kind: full  secs:   97.628  mem:   1G  BOD: 2.0M
        2025/02/01 18:34:07|  kind: incr  secs:   61.995  mem: 936M  BOD: 2.0M
        2025/02/01 18:35:09|  kind: NULL  secs:   61.387  mem:   1G  BOD: 2.0M

     Module Count : 100000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 19:52:31|  kind: full  secs:  202.950  mem:   2G  BOD: 4.0M
        2025/02/01 20:01:49|  kind: incr  secs:  132.652  mem:   1G  BOD: 4.0M
        2025/02/01 20:04:02|  kind: NULL  secs:  133.126  mem:   2G  BOD: 4.0M

     Module Count : 50
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : --no-builtin-rules --no-builtin-variables

        2025/02/01 17:51:18|  kind: full  secs:    0.042  mem:  12M  BOD: 12K
        2025/02/01 17:51:18|  kind: incr  secs:    0.027  mem:  12M  BOD: 12K
        2025/02/01 17:51:18|  kind: NULL  secs:    0.006  mem:  12M  BOD: 12K

     Module Count : 100
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : --no-builtin-rules --no-builtin-variables

        2025/02/01 17:52:12|  kind: full  secs:    0.078  mem:  12M  BOD: 12K
        2025/02/01 17:52:12|  kind: incr  secs:    0.042  mem:  12M  BOD: 12K
        2025/02/01 17:52:12|  kind: NULL  secs:    0.007  mem:  12M  BOD: 12K

     Module Count : 1000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : --no-builtin-rules --no-builtin-variables

        2025/02/01 17:53:29|  kind: full  secs:    0.718  mem:  12M  BOD: 48K
        2025/02/01 17:53:30|  kind: incr  secs:    0.107  mem:  12M  BOD: 48K
        2025/02/01 17:53:30|  kind: NULL  secs:    0.041  mem:  12M  BOD: 48K

     Module Count : 5000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : --no-builtin-rules --no-builtin-variables

        2025/02/01 17:57:12|  kind: full  secs:    3.720  mem:  36M  BOD: 208K
        2025/02/01 17:57:18|  kind: incr  secs:    0.314  mem:  13M  BOD: 208K
        2025/02/01 17:57:18|  kind: NULL  secs:    0.219  mem:  36M  BOD: 208K

     Module Count : 10000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : --no-builtin-rules --no-builtin-variables

        2025/02/01 18:04:55|  kind: full  secs:    7.544  mem:  72M  BOD: 408K
        2025/02/01 18:05:08|  kind: incr  secs:    0.611  mem:  24M  BOD: 408K
        2025/02/01 18:05:09|  kind: NULL  secs:    0.486  mem:  72M  BOD: 408K

     Module Count : 50000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : --no-builtin-rules --no-builtin-variables

        2025/02/01 18:36:11|  kind: full  secs:   41.865  mem: 363M  BOD: 2.0M
        2025/02/01 18:37:37|  kind: incr  secs:    3.585  mem: 116M  BOD: 2.0M
        2025/02/01 18:37:40|  kind: NULL  secs:    3.456  mem: 363M  BOD: 2.0M

     Module Count : 100000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : --no-builtin-rules --no-builtin-variables

        2025/02/01 20:06:15|  kind: full  secs:   76.435  mem: 730M  BOD: 4.0M
        2025/02/01 20:09:31|  kind: incr  secs:    8.779  mem: 230M  BOD: 4.0M
        2025/02/01 20:09:40|  kind: NULL  secs:    7.633  mem: 730M  BOD: 4.0M

  x86_64
   Linux-6.8.0-48-generic-x86_64-with-glibc2.39
   #48~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Mon Oct  7 11:24:13 UTC 2
   CPU count    : 4
   Memory       : 7G
     Module Count : 50
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 21:16:11|  kind: full  secs:    0.117  mem:  14M  BOD: 12K
        2025/02/01 21:16:11|  kind: incr  secs:    0.090  mem:  14M  BOD: 12K
        2025/02/01 21:16:11|  kind: NULL  secs:    0.059  mem:  14M  BOD: 12K

     Module Count : 100
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 21:16:50|  kind: full  secs:    0.249  mem:  14M  BOD: 12K
        2025/02/01 21:16:51|  kind: incr  secs:    0.183  mem:  14M  BOD: 12K
        2025/02/01 21:16:51|  kind: NULL  secs:    0.126  mem:  14M  BOD: 12K

     Module Count : 1000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 21:18:05|  kind: full  secs:    3.244  mem:  25M  BOD: 48K
        2025/02/01 21:18:10|  kind: incr  secs:    2.271  mem:  22M  BOD: 48K
        2025/02/01 21:18:12|  kind: NULL  secs:    2.148  mem:  21M  BOD: 48K

     Module Count : 5000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 21:23:08|  kind: full  secs:   30.169  mem: 119M  BOD: 208K
        2025/02/01 21:23:45|  kind: incr  secs:   24.869  mem:  96M  BOD: 208K
        2025/02/01 21:24:10|  kind: NULL  secs:   24.528  mem:  96M  BOD: 208K

     Module Count : 10000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 21:36:06|  kind: full  secs:   72.399  mem: 239M  BOD: 408K
        2025/02/01 21:37:30|  kind: incr  secs:   62.244  mem: 191M  BOD: 408K
        2025/02/01 21:38:33|  kind: NULL  secs:   61.585  mem: 190M  BOD: 408K

     Module Count : 50000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 23:04:24|  kind: full  secs:  191.026  mem:   1G  BOD: 2.0M
        2025/02/01 23:09:16|  kind: incr  secs:  137.480  mem: 936M  BOD: 2.0M
        2025/02/01 23:11:34|  kind: NULL  secs:  134.860  mem: 936M  BOD: 2.0M

     Module Count : 100000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/02 02:46:17|  kind: full  secs:  395.776  mem:   2G  BOD: 4.0M
        2025/02/02 02:56:29|  kind: incr  secs:  293.855  mem:   1G  BOD: 4.0M
        2025/02/02 03:01:24|  kind: NULL  secs:  286.084  mem:   1G  BOD: 4.0M

     Module Count : 50
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : --no-builtin-rules --no-builtin-variables

        2025/02/01 21:16:12|  kind: full  secs:    0.067  mem:  14M  BOD: 12K
        2025/02/01 21:16:12|  kind: incr  secs:    0.042  mem:  14M  BOD: 12K
        2025/02/01 21:16:12|  kind: NULL  secs:    0.011  mem:  14M  BOD: 12K

     Module Count : 100
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : --no-builtin-rules --no-builtin-variables

        2025/02/01 21:16:52|  kind: full  secs:    0.122  mem:  14M  BOD: 12K
        2025/02/01 21:16:52|  kind: incr  secs:    0.068  mem:  14M  BOD: 12K
        2025/02/01 21:16:52|  kind: NULL  secs:    0.013  mem:  14M  BOD: 12K

     Module Count : 1000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : --no-builtin-rules --no-builtin-variables

        2025/02/01 21:18:14|  kind: full  secs:    1.144  mem:  14M  BOD: 48K
        2025/02/01 21:18:17|  kind: incr  secs:    0.165  mem:  14M  BOD: 48K
        2025/02/01 21:18:17|  kind: NULL  secs:    0.070  mem:  14M  BOD: 48K

     Module Count : 5000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : --no-builtin-rules --no-builtin-variables

        2025/02/01 21:24:35|  kind: full  secs:    5.827  mem:  37M  BOD: 208K
        2025/02/01 21:24:47|  kind: incr  secs:    0.566  mem:  14M  BOD: 208K
        2025/02/01 21:24:48|  kind: NULL  secs:    0.418  mem:  14M  BOD: 208K

     Module Count : 10000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : --no-builtin-rules --no-builtin-variables

        2025/02/01 21:39:35|  kind: full  secs:   11.316  mem:  72M  BOD: 408K
        2025/02/01 21:39:59|  kind: incr  secs:    1.118  mem:  25M  BOD: 408K
        2025/02/01 21:40:00|  kind: NULL  secs:    0.951  mem:  24M  BOD: 408K

     Module Count : 50000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : --no-builtin-rules --no-builtin-variables

        2025/02/01 23:13:49|  kind: full  secs:   58.745  mem: 364M  BOD: 2.0M
        2025/02/01 23:16:15|  kind: incr  secs:    6.533  mem: 116M  BOD: 2.0M
        2025/02/01 23:16:22|  kind: NULL  secs:    6.267  mem: 116M  BOD: 2.0M

     Module Count : 100000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : --no-builtin-rules --no-builtin-variables

        2025/02/02 03:06:11|  kind: full  secs:  118.161  mem: 730M  BOD: 4.0M
        2025/02/02 03:10:37|  kind: incr  secs:   14.428  mem: 231M  BOD: 4.0M
        2025/02/02 03:10:52|  kind: NULL  secs:   14.217  mem: 230M  BOD: 4.0M
```

## Scons (md5sum)

```
tool: scons-md5sum  | version: SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021
  aarch64
   Linux-6.8.0-1018-raspi-aarch64-with-glibc2.39
   #20-Ubuntu SMP PREEMPT_DYNAMIC Fri Jan 17 12:35:36 UTC 2025
   CPU count    : 4
   Memory       : 7G
     Module Count : 50
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 17:51:19|  kind: full  secs:    0.374  mem:  25M  BOD: 52K
        2025/02/01 17:51:19|  kind: incr  secs:    0.347  mem:  25M  BOD: 52K
        2025/02/01 17:51:20|  kind: NULL  secs:    0.311  mem:  25M  BOD: 52K

     Module Count : 100
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 17:52:12|  kind: full  secs:    0.504  mem:  27M  BOD: 92K
        2025/02/01 17:52:13|  kind: incr  secs:    0.473  mem:  27M  BOD: 92K
        2025/02/01 17:52:14|  kind: NULL  secs:    0.388  mem:  27M  BOD: 92K

     Module Count : 1000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 17:53:30|  kind: full  secs:    3.111  mem:  61M  BOD: 1.3M
        2025/02/01 17:53:34|  kind: incr  secs:    2.159  mem:  62M  BOD: 1.3M
        2025/02/01 17:53:37|  kind: NULL  secs:    2.017  mem:  62M  BOD: 1.3M

     Module Count : 5000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 17:57:19|  kind: full  secs:   15.934  mem: 203M  BOD: 11M
        2025/02/01 17:57:37|  kind: incr  secs:   10.689  mem: 205M  BOD: 11M
        2025/02/01 17:57:48|  kind: NULL  secs:   10.609  mem: 205M  BOD: 11M

     Module Count : 10000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 18:05:10|  kind: full  secs:   32.934  mem: 383M  BOD: 25M
        2025/02/01 18:05:48|  kind: incr  secs:   22.669  mem: 386M  BOD: 25M
        2025/02/01 18:06:11|  kind: NULL  secs:   22.510  mem: 387M  BOD: 25M

     Module Count : 50000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 18:37:44|  kind: full  secs:  168.790  mem:   1G  BOD: 150M
        2025/02/01 18:41:12|  kind: incr  secs:  116.767  mem:   1G  BOD: 150M
        2025/02/01 18:43:09|  kind: NULL  secs:  115.422  mem:   1G  BOD: 150M

     Module Count : 100000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 20:09:48|  kind: full  secs:  977.967  mem:   3G  BOD: 311M
        2025/02/01 20:28:52|  kind: incr  secs:  277.910  mem:   3G  BOD: 311M
        2025/02/01 20:33:30|  kind: NULL  secs:  333.184  mem:   3G  BOD: 311M

  x86_64
   Linux-6.8.0-48-generic-x86_64-with-glibc2.39
   #48~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Mon Oct  7 11:24:13 UTC 2
   CPU count    : 4
   Memory       : 7G
     Module Count : 50
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 21:16:12|  kind: full  secs:    0.801  mem:  28M  BOD: 52K
        2025/02/01 21:16:14|  kind: incr  secs:    0.748  mem:  28M  BOD: 52K
        2025/02/01 21:16:15|  kind: NULL  secs:    0.686  mem:  28M  BOD: 52K

     Module Count : 100
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 21:16:53|  kind: full  secs:    1.136  mem:  30M  BOD: 92K
        2025/02/01 21:16:55|  kind: incr  secs:    1.010  mem:  30M  BOD: 92K
        2025/02/01 21:16:56|  kind: NULL  secs:    0.899  mem:  30M  BOD: 92K

     Module Count : 1000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 21:18:17|  kind: full  secs:    7.378  mem:  64M  BOD: 1.3M
        2025/02/01 21:18:27|  kind: incr  secs:    5.261  mem:  64M  BOD: 1.3M
        2025/02/01 21:18:32|  kind: NULL  secs:    5.038  mem:  64M  BOD: 1.3M

     Module Count : 5000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 21:24:48|  kind: full  secs:   37.358  mem: 206M  BOD: 11M
        2025/02/01 21:25:32|  kind: incr  secs:   26.247  mem: 207M  BOD: 11M
        2025/02/01 21:25:59|  kind: NULL  secs:   25.550  mem: 207M  BOD: 11M

     Module Count : 10000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 21:40:01|  kind: full  secs:   74.958  mem: 386M  BOD: 25M
        2025/02/01 21:41:29|  kind: incr  secs:   52.825  mem: 389M  BOD: 25M
        2025/02/01 21:42:22|  kind: NULL  secs:   52.006  mem: 389M  BOD: 25M

     Module Count : 50000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 23:16:28|  kind: full  secs:  423.898  mem:   1G  BOD: 150M
        2025/02/01 23:25:00|  kind: incr  secs:  313.816  mem:   1G  BOD: 150M
        2025/02/01 23:30:15|  kind: NULL  secs:  306.407  mem:   1G  BOD: 150M

     Module Count : 100000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/02 03:11:07|  kind: full  secs:  856.723  mem:   3G  BOD: 311M
        2025/02/02 03:28:22|  kind: incr  secs:  624.359  mem:   3G  BOD: 311M
        2025/02/02 03:38:48|  kind: NULL  secs:  619.959  mem:   3G  BOD: 311M


## Scons (make)

```
tool: scons-make  | version: SCons: v4.5.2.120fd4f633e9ef3cafbc0fec35306d7555ffd1db, Tue, 21 Mar 2023 12:11:27 -0400, by bdbaddog on M1DOG2021
  aarch64
   Linux-6.8.0-1018-raspi-aarch64-with-glibc2.39
   #20-Ubuntu SMP PREEMPT_DYNAMIC Fri Jan 17 12:35:36 UTC 2025
   CPU count    : 4
   Memory       : 7G
     Module Count : 50
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 17:51:20|  kind: full  secs:    0.357  mem:  25M  BOD: 44K
        2025/02/01 17:51:21|  kind: incr  secs:    0.304  mem:  25M  BOD: 44K
        2025/02/01 17:51:22|  kind: NULL  secs:    0.301  mem:  25M  BOD: 44K

     Module Count : 100
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 17:52:14|  kind: full  secs:    0.492  mem:  27M  BOD: 80K
        2025/02/01 17:52:15|  kind: incr  secs:    0.369  mem:  27M  BOD: 80K
        2025/02/01 17:52:16|  kind: NULL  secs:    0.370  mem:  27M  BOD: 80K

     Module Count : 1000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 17:53:39|  kind: full  secs:    2.943  mem:  61M  BOD: 1012K
        2025/02/01 17:53:43|  kind: incr  secs:    1.990  mem:  61M  BOD: 1012K
        2025/02/01 17:53:45|  kind: NULL  secs:    1.824  mem:  61M  BOD: 1012K

     Module Count : 5000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 17:57:59|  kind: full  secs:   15.280  mem: 203M  BOD: 7.7M
        2025/02/01 17:58:18|  kind: incr  secs:    9.869  mem: 201M  BOD: 7.7M
        2025/02/01 17:58:28|  kind: NULL  secs:    9.661  mem: 203M  BOD: 7.7M

     Module Count : 10000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 18:06:34|  kind: full  secs:   30.854  mem: 383M  BOD: 18M
        2025/02/01 18:07:10|  kind: incr  secs:   20.704  mem: 380M  BOD: 18M
        2025/02/01 18:07:31|  kind: NULL  secs:   20.380  mem: 383M  BOD: 18M

     Module Count : 50000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 18:45:04|  kind: full  secs:  158.515  mem:   1G  BOD: 105M
        2025/02/01 18:48:24|  kind: incr  secs:  107.118  mem:   1G  BOD: 105M
        2025/02/01 18:50:12|  kind: NULL  secs:  105.895  mem:   1G  BOD: 105M

     Module Count : 100000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 20:39:04|  kind: full  secs:  320.551  mem:   3G  BOD: 217M
        2025/02/01 20:48:36|  kind: incr  secs:  215.585  mem:   3G  BOD: 217M
        2025/02/01 20:52:13|  kind: NULL  secs:  214.283  mem:   3G  BOD: 217M

  x86_64
   Linux-6.8.0-48-generic-x86_64-with-glibc2.39
   #48~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Mon Oct  7 11:24:13 UTC 2
   CPU count    : 4
   Memory       : 7G
     Module Count : 50
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 21:16:16|  kind: full  secs:    0.778  mem:  28M  BOD: 44K
        2025/02/01 21:16:18|  kind: incr  secs:    0.672  mem:  28M  BOD: 44K
        2025/02/01 21:16:19|  kind: NULL  secs:    0.668  mem:  28M  BOD: 44K

     Module Count : 100
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 21:16:58|  kind: full  secs:    1.094  mem:  30M  BOD: 80K
        2025/02/01 21:16:59|  kind: incr  secs:    0.857  mem:  30M  BOD: 80K
        2025/02/01 21:17:01|  kind: NULL  secs:    0.860  mem:  30M  BOD: 80K

     Module Count : 1000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 21:18:38|  kind: full  secs:    6.879  mem:  63M  BOD: 1012K
        2025/02/01 21:18:47|  kind: incr  secs:    4.977  mem:  63M  BOD: 1012K
        2025/02/01 21:18:52|  kind: NULL  secs:    4.657  mem:  63M  BOD: 1012K

     Module Count : 5000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 21:26:25|  kind: full  secs:   35.118  mem: 206M  BOD: 7.7M
        2025/02/01 21:27:07|  kind: incr  secs:   24.563  mem: 204M  BOD: 7.7M
        2025/02/01 21:27:32|  kind: NULL  secs:   23.902  mem: 204M  BOD: 7.7M

     Module Count : 10000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 21:43:15|  kind: full  secs:   70.434  mem: 386M  BOD: 18M
        2025/02/01 21:44:38|  kind: incr  secs:   49.600  mem: 383M  BOD: 18M
        2025/02/01 21:45:29|  kind: NULL  secs:   48.752  mem: 382M  BOD: 18M

     Module Count : 50000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/01 23:35:22|  kind: full  secs:  365.770  mem:   1G  BOD: 105M
        2025/02/01 23:42:35|  kind: incr  secs:  257.425  mem:   1G  BOD: 105M
        2025/02/01 23:46:54|  kind: NULL  secs:  255.813  mem:   1G  BOD: 105M

     Module Count : 100000
     Files per dir: 100
     Module Size  : 30
     Parallelism  : 4
     Add'l args   : <no-args>

        2025/02/02 03:49:09|  kind: full  secs:  739.783  mem:   3G  BOD: 217M
        2025/02/02 04:04:31|  kind: incr  secs:  521.631  mem:   3G  BOD: 217M
        2025/02/02 04:13:13|  kind: NULL  secs:  515.623  mem:   3G  BOD: 217M
```

# build-tool-comparator

# Preface

There is a significant amount of discord about build tools:

  - Scons has perfect dependencies.

  - Bazel is hermetically sealed.

  - Make is old.

Many of the claims made about any particular build tool are often
untrue (two of the three above, for example).  Adding to the
tribalization, it seems no one is interested in writing several build
systems for their software project.  Instead, the normal path is to
choose one and stick with it.  Conversions to another system, even,
are rarely done because such work is notoriously difficult.

Irrespective the build tool used, the quality of the result is
directly related to the strength of the team writing and maintaining
it.  However, there are immutable properties that must be accepted
with each tool: overheads, for example.  These overheads can be
measured and compared, allowing a well-informed person to make
reasoned decisions about a build system, rather than solely relying on
tribalized hype.

# Lay of the Land

## Make

Make is the oldest of the build tools.  The Make dialect used in this
project is Gnu Make.

### Pros
- Easy to start a project
- Fast
- Common
- Simple enough to understand 95% of the tool, but capable enough to
  do everything you need.
- Plays well with other build systems
- Pretty good documentation.
- Scales well to large projects in terms of build time.

### Cons

- Moderately complicated.
- Single global namespace.
- Minimal checking of input files.
- Undefined (eg: misspelled) variables have an empty value.
- Does not handle pathnames with embedded spaces well.
- Hidden state affecting build mostly through environment variables.
- Scales very poorly to large projects in terms of source code.

## Scons

Scons is a build system written in Python.  Possibly simpler to use
for those with no familiarity at all with Make.

### Pros

- Plays somewhat well with other build systems.
- Uses Python.
- Fairly good documentation.
- Scales well in terms of source code.
- Scales well to medium-sized projects in terms of speed.

### Cons

- Moderately complicated.
- Hidden state affecting build via automatically used config files.
- Uses Python; people tend to treat it is a general purpose
  programming language, and not a builder of a DAG to build to product.
- Large projects have significant administrative overheads in time and disk space.
- Significant use of RAM for large projects.
- Significant use of disk space for large projects.

## Bazel

Bazel is the public version of Google's internal Blaze build system,
without all the secret sauce that makes it work well in their network.

Bazel claims to be fast & correct.  Correctness is not answered by
this project, but speed and disk utilization certainly are.

### Pros

- Made by Google.
- Apparently large community.
- Continually being updated & changed.

### Cons

- Out-of-the-box resource use makes machine nearly unsuable while building.
- Extremely complicated.
- Does not play well with other build systems.
- Significant hidden state affecting build via automatically used config files.
- Ridiculous number of command line options (eg: bazel help build|nl -ba)
- Bad, often incomplete or incorrect, documentation.
- Profligate use of disk space and other system resources.
- Not as hermetic as claimed.
- Continually being updated & changed.

# Rationale

A build system exists to turn product sources into product artifacts.
It accomplishes this by creating a directed acyclic graph (DAG) of the
product specification (Makefiles, for example).  The product
specification associates source files with artifacts (object files &
executables, documentation, etc.), and the rules needed to transform
the former into the latter.  Once the DAG is created, it is traversed,
and any source file that has been changed since the last creation of
its associated artifact (or if the artifact doesn't exist) will cause
the rule needed to transform that source into an artifact to be
re-executed.

In the case of a C file (source), the compiler would be invoked to
create an up-to-date object file (artifact).  In the case of an object
file, the linker will be invoked to create an up-to-date executable.

Good build tools have many properties sought by developers, but
all-too-often not achieved in practice.  These properties, when
present, make developers much more productive and happier.  A few
desirable properties are shown below:

 - Simple Model Invocation

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

   When projects have thousands of files, executing them serially can
   make the time to build the project seem glacial.  Executing
   unrelated rules at the same time speeds product builds.

 - Low resource overhead

   The fewer resources used by the build tool means more resources are
   available to execute rules.

 - Minimal work performed on each invocation.

   A build tool should only execute rules needed to bring out-of-date
   artifacts up-to-date.  An artifact is out-of-date when it doesn't
   exist, its sources have changed, or its prerequisites have been
   rebuilt.  Any work that occurs to create an artifact when it is not
   out-of-date is unnecessary, a deficiency in the build process, and,
   possibly, the build tool.

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
different build systems.  To accomplish this, it generates a set of
'source modules', 'interfaces', and product specifications for a
variety of different build systems.  These specifications can be used
to measure the time it takes to 'build' the described software using a
variety of build systems.

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

```
Note on Scons variants:

  Scons uses md5sums to determine if files have changed.  There is a
  simple option to have it use just timestamps, like make.
```

```
Note on Make variants:

   Make has a lot of built-in suffix rules, and will automatically
   search them when deciding how a file should be built.  In many
   cases, these legacy-esque rules are not necessary and can be
   disabled, resulting in a faster build.  When these rules are
   disabled, the Makefile maintainer will have to supply the rules (or
   copy them from Make) needed to build the product.
```

```
The columns below are as follows:

  kind:  'full' means a full build of all files was produced.
         'incr' means only a few files needed to be re-created.
         'NULL' means no files needed to be re-created.
  secs:  Number of seconds consumed performing the build.
  mem :  The amount of memory used to perform the build.
  BOD :  The amount of disk space consumed by the build.
         Each 'module' produces just a single 0-byte file.
```


## 50 simulated modules

```
BOD          : /tmp/make/BOD
Files Per Dir: 100
Modules      : 50
Parallel     : 4
Source       : /tmp/make/source

Bash
                bash: kind: full  secs:    0.144  mem:  14M  BOD:  12K
                bash: kind: incr  secs:    0.101  mem:  13M  BOD:  12K
                bash: kind: NULL  secs:    0.037  mem:  13M  BOD:  12K

Bazel
               bazel: kind: full  secs:    8.632  mem: 230M  BOD: 7.0M
               bazel: kind: incr  secs:    0.852  mem: 235M  BOD:  11M
               bazel: kind: NULL  secs:    0.356  mem: 241M  BOD: 9.9M

Recursive Make
      recursive-make: kind: full  secs:    0.113  mem:  14M  BOD:  12K
      recursive-make: kind: incr  secs:    0.091  mem:  13M  BOD:  12K
      recursive-make: kind: NULL  secs:    0.062  mem:  13M  BOD:  12K

Recursive Make + --no-builtin-rules --no-builtin-variables
      recursive-make: kind: full  secs:    0.069  mem:  14M  BOD:  12K
      recursive-make: kind: incr  secs:    0.044  mem:  13M  BOD:  12K
      recursive-make: kind: NULL  secs:    0.015  mem:  13M  BOD:  12K

Scons: md5sum
               scons: kind: full  secs:    0.802  mem:  28M  BOD:  52K
               scons: kind: incr  secs:    0.746  mem:  28M  BOD:  52K
               scons: kind: NULL  secs:    0.674  mem:  28M  BOD:  52K

Scons: make
               scons: kind: full  secs:    0.789  mem:  28M  BOD:  44K
               scons: kind: incr  secs:    0.706  mem:  28M  BOD:  44K
               scons: kind: NULL  secs:    0.662  mem:  28M  BOD:  44K

Single Make
         single-make: kind: full  secs:    0.111  mem:  14M  BOD:  12K
         single-make: kind: incr  secs:    0.088  mem:  13M  BOD:  12K
         single-make: kind: NULL  secs:    0.059  mem:  12M  BOD:  12K

Single Make + --no-builtin-rules --no-builtin-variables
         single-make: kind: full  secs:    0.067  mem:  14M  BOD:  12K
         single-make: kind: incr  secs:    0.039  mem:  13M  BOD:  12K
         single-make: kind: NULL  secs:    0.010  mem:  13M  BOD:  12K
```


## 100 simulated modules

```
BOD          : /tmp/make/BOD
Files Per Dir: 100
Modules      : 100
Parallel     : 4
Source       : /tmp/make/source

Bash
                bash: kind: full  secs:    0.276  mem:  14M  BOD:  12K
                bash: kind: incr  secs:    0.185  mem:  13M  BOD:  12K
                bash: kind: NULL  secs:    0.073  mem:  13M  BOD:  12K

Bazel
               bazel: kind: full  secs:   10.271  mem: 251M  BOD:  16M
               bazel: kind: incr  secs:    1.363  mem: 262M  BOD:  22M
               bazel: kind: NULL  secs:    0.397  mem: 263M  BOD:  21M

Recursive Make
      recursive-make: kind: full  secs:    0.226  mem:  13M  BOD:  12K
      recursive-make: kind: incr  secs:    0.177  mem:  13M  BOD:  12K
      recursive-make: kind: NULL  secs:    0.123  mem:  13M  BOD:  12K

Recursive Make + --no-builtin-rules --no-builtin-variables
      recursive-make: kind: full  secs:    0.126  mem:  14M  BOD:  12K
      recursive-make: kind: incr  secs:    0.066  mem:  13M  BOD:  12K
      recursive-make: kind: NULL  secs:    0.020  mem:  13M  BOD:  12K

Scons: md5sum
               scons: kind: full  secs:    1.113  mem:  30M  BOD:  92K
               scons: kind: incr  secs:    0.998  mem:  30M  BOD:  92K
               scons: kind: NULL  secs:    0.874  mem:  30M  BOD:  92K

Scons: make
               scons: kind: full  secs:    1.063  mem:  30M  BOD:  80K
               scons: kind: incr  secs:    0.974  mem:  30M  BOD:  80K
               scons: kind: NULL  secs:    0.845  mem:  30M  BOD:  80K

Single Make
         single-make: kind: full  secs:    0.237  mem:  14M  BOD:  12K
         single-make: kind: incr  secs:    0.178  mem:  13M  BOD:  12K
         single-make: kind: NULL  secs:    0.121  mem:  13M  BOD:  12K

Single Make + --no-builtin-rules --no-builtin-variables
         single-make: kind: full  secs:    0.119  mem:  13M  BOD:  12K
         single-make: kind: incr  secs:    0.061  mem:  13M  BOD:  12K
         single-make: kind: NULL  secs:    0.013  mem:  13M  BOD:  12K
```


## 1000 simulated modules

```
BOD          : /tmp/make/BOD
Files Per Dir: 100
Modules      : 1000
Parallel     : 4
Source       : /tmp/make/source

Bash
                bash: kind: full  secs:    2.778  mem:  14M  BOD:  48K
                bash: kind: incr  secs:    1.130  mem:  13M  BOD:  48K
                bash: kind: NULL  secs:    0.852  mem:  13M  BOD:  48K

Bazel
               bazel: kind: full  secs:   26.068  mem: 304M  BOD: 194M
               bazel: kind: incr  secs:    2.154  mem: 305M  BOD: 198M
               bazel: kind: NULL  secs:    0.560  mem: 307M  BOD: 197M

Recursive Make
      recursive-make: kind: full  secs:    2.944  mem:  14M  BOD:  48K
      recursive-make: kind: incr  secs:    1.937  mem:  13M  BOD:  48K
      recursive-make: kind: NULL  secs:    1.819  mem:  13M  BOD:  48K

Recursive Make + --no-builtin-rules --no-builtin-variables
      recursive-make: kind: full  secs:    0.983  mem:  14M  BOD:  48K
      recursive-make: kind: incr  secs:    0.151  mem:  13M  BOD:  48K
      recursive-make: kind: NULL  secs:    0.059  mem:  13M  BOD:  48K

Scons: md5sum
               scons: kind: full  secs:    7.251  mem:  63M  BOD: 1.3M
               scons: kind: incr  secs:    5.229  mem:  64M  BOD: 1.3M
               scons: kind: NULL  secs:    4.907  mem:  64M  BOD: 1.3M

Scons: make
               scons: kind: full  secs:    6.811  mem:  64M  BOD: 1012K
               scons: kind: incr  secs:    4.912  mem:  63M  BOD: 1012K
               scons: kind: NULL  secs:    4.540  mem:  63M  BOD: 1012K

Single Make
         single-make: kind: full  secs:    3.191  mem:  26M  BOD:  48K
         single-make: kind: incr  secs:    2.249  mem:  22M  BOD:  48K
         single-make: kind: NULL  secs:    2.091  mem:  21M  BOD:  48K

Single Make + --no-builtin-rules --no-builtin-variables
         single-make: kind: full  secs:    1.085  mem:  14M  BOD:  48K
         single-make: kind: incr  secs:    0.167  mem:  13M  BOD:  48K
         single-make: kind: NULL  secs:    0.068  mem:  13M  BOD:  48K
```


## 5000 simulated modules

```
BOD          : /tmp/make/BOD
Files Per Dir: 100
Modules      : 5000
Parallel     : 4
Source       : /tmp/make/source

Bash
                bash: kind: full  secs:   14.283  mem:  17M  BOD: 208K
                bash: kind: incr  secs:    5.032  mem:  13M  BOD: 208K
                bash: kind: NULL  secs:    4.568  mem:  13M  BOD: 208K

Bazel
               bazel: kind: full  secs:   82.142  mem: 460M  BOD: 1.2G
               bazel: kind: incr  secs:    4.760  mem: 448M  BOD: 1.1G
               bazel: kind: NULL  secs:    1.406  mem: 446M  BOD: 1.1G

Recursive Make
      recursive-make: kind: full  secs:   30.881  mem:  21M  BOD: 208K
      recursive-make: kind: incr  secs:   24.819  mem:  21M  BOD: 208K
      recursive-make: kind: NULL  secs:   28.424  mem:  21M  BOD: 208K

Recursive Make + --no-builtin-rules --no-builtin-variables
      recursive-make: kind: full  secs:    6.220  mem:  17M  BOD: 208K
      recursive-make: kind: incr  secs:    0.463  mem:  13M  BOD: 208K
      recursive-make: kind: NULL  secs:    0.323  mem:  13M  BOD: 208K

Scons: md5sum
               scons: kind: full  secs:   37.637  mem: 206M  BOD:  11M
               scons: kind: incr  secs:   26.435  mem: 207M  BOD:  11M
               scons: kind: NULL  secs:   25.413  mem: 207M  BOD:  11M

Scons: make
               scons: kind: full  secs:   45.696  mem: 206M  BOD: 7.7M
               scons: kind: incr  secs:   32.987  mem: 204M  BOD: 7.7M
               scons: kind: NULL  secs:   35.154  mem: 203M  BOD: 7.7M

Single Make
         single-make: kind: full  secs:   36.091  mem: 119M  BOD: 208K
         single-make: kind: incr  secs:   25.917  mem:  96M  BOD: 208K
         single-make: kind: NULL  secs:   24.561  mem:  96M  BOD: 208K

Single Make + --no-builtin-rules --no-builtin-variables
         single-make: kind: full  secs:    5.707  mem:  37M  BOD: 208K
         single-make: kind: incr  secs:    0.581  mem:  14M  BOD: 208K
         single-make: kind: NULL  secs:    0.421  mem:  13M  BOD: 208K
```

## 10000 simulated modules

```
BOD          : /tmp/make/BOD
Files Per Dir: 100
Modules      : 10000
Parallel     : 4
Source       : /tmp/make/source

Bash
                bash: kind: full  secs:   27.901  mem:  21M  BOD: 408K
                bash: kind: incr  secs:    9.635  mem:  13M  BOD: 408K
                bash: kind: NULL  secs:    9.148  mem:  13M  BOD: 408K

Bazel
               bazel: kind: full  secs:  137.192  mem: 705M  BOD: 2.5G
               bazel: kind: incr  secs:    5.095  mem: 582M  BOD: 2.4G
               bazel: kind: NULL  secs:    1.506  mem: 582M  BOD: 2.4G

Recursive Make
      recursive-make: kind: full  secs:   64.640  mem:  24M  BOD: 408K
      recursive-make: kind: incr  secs:   52.416  mem:  23M  BOD: 408K
      recursive-make: kind: NULL  secs:   51.977  mem:  23M  BOD: 408K

Recursive Make + --no-builtin-rules --no-builtin-variables
      recursive-make: kind: full  secs:   10.380  mem:  21M  BOD: 408K
      recursive-make: kind: incr  secs:    0.847  mem:  13M  BOD: 408K
      recursive-make: kind: NULL  secs:    0.685  mem:  13M  BOD: 408K

Scons: md5sum
               scons: kind: full  secs:   75.071  mem: 386M  BOD:  25M
               scons: kind: incr  secs:   52.683  mem: 389M  BOD:  25M
               scons: kind: NULL  secs:   51.852  mem: 389M  BOD:  25M

Scons: make
               scons: kind: full  secs:   70.825  mem: 386M  BOD:  18M
               scons: kind: incr  secs:   49.691  mem: 383M  BOD:  18M
               scons: kind: NULL  secs:   48.680  mem: 382M  BOD:  18M

Single Make
         single-make: kind: full  secs:   72.519  mem: 238M  BOD: 408K
         single-make: kind: incr  secs:   61.973  mem: 191M  BOD: 408K
         single-make: kind: NULL  secs:   61.525  mem: 190M  BOD: 408K

Single Make + --no-builtin-rules --no-builtin-variables
         single-make: kind: full  secs:   11.589  mem:  72M  BOD: 408K
         single-make: kind: incr  secs:    1.143  mem:  25M  BOD: 408K
         single-make: kind: NULL  secs:    0.948  mem:  24M  BOD: 408K
```


## 50000 simulated modules

```
BOD          : /tmp/make/BOD
Files Per Dir: 100
Modules      : 50000
Parallel     : 4
Source       : /tmp/make/source

Bash
                bash: kind: full  secs:  149.888  mem:  55M  BOD: 2.0M
                bash: kind: incr  secs:   52.989  mem:  13M  BOD: 2.0M
                bash: kind: NULL  secs:   47.051  mem:  13M  BOD: 2.0M

Bazel
               bazel: kind: full  secs:  661.977  mem:   1G  BOD:  14G
               bazel: kind: incr  secs:   18.457  mem:   1G  BOD:  13G
               bazel: kind: NULL  secs:    7.165  mem:   1G  BOD:  13G

Recursive Make
      recursive-make: kind: full  secs:  390.795  mem:  55M  BOD: 2.0M
      recursive-make: kind: incr  secs:  325.651  mem:  28M  BOD: 2.0M
      recursive-make: kind: NULL  secs:  322.823  mem:  28M  BOD: 2.0M

Recursive Make + --no-builtin-rules --no-builtin-variables
      recursive-make: kind: full  secs:   51.259  mem:  55M  BOD: 2.0M
      recursive-make: kind: incr  secs:    4.351  mem:  13M  BOD: 2.0M
      recursive-make: kind: NULL  secs:    3.775  mem:  13M  BOD: 2.0M

Scons: md5sum
               scons: kind: full  secs:  440.138  mem:   1G  BOD: 150M
               scons: kind: incr  secs:  295.302  mem:   1G  BOD: 150M
               scons: kind: NULL  secs:  288.051  mem:   1G  BOD: 150M

Scons: make
               scons: kind: full  secs:  396.699  mem:   1G  BOD: 105M
               scons: kind: incr  secs:  259.472  mem:   1G  BOD: 105M
               scons: kind: NULL  secs:  257.144  mem:   1G  BOD: 105M

Single Make
         single-make: kind: full  secs:  191.576  mem:   1G  BOD: 2.0M
         single-make: kind: incr  secs:  136.677  mem: 936M  BOD: 2.0M
         single-make: kind: NULL  secs:  135.415  mem: 936M  BOD: 2.0M

Single Make + --no-builtin-rules --no-builtin-variables
         single-make: kind: full  secs:   60.228  mem: 364M  BOD: 2.0M
         single-make: kind: incr  secs:    6.588  mem: 116M  BOD: 2.0M
         single-make: kind: NULL  secs:    6.445  mem: 116M  BOD: 2.0M
```


## 100000 simulated modules

```
BOD          : /tmp/make/BOD
Files Per Dir: 100
Modules      : 100000
Parallel     : 4
Source       : /tmp/make/source

Bash
                bash: kind: full  secs:  280.902  mem:  97M  BOD: 4.0M
                bash: kind: incr  secs:   95.337  mem:  13M  BOD: 4.0M
                bash: kind: NULL  secs:   94.720  mem:  13M  BOD: 4.0M

Bazel
               bazel: kind: full  secs: 2057.709  mem:   3G  BOD:  27G
               bazel: kind: incr  secs:   57.452  mem:   2G  BOD:  26G
               bazel: kind: NULL  secs:   13.527  mem:   2G  BOD:  26G

Recursive Make
      recursive-make: kind: full  secs:  805.441  mem:  97M  BOD: 4.0M
      recursive-make: kind: incr  secs:  687.163  mem:  31M  BOD: 4.0M
      recursive-make: kind: NULL  secs:  681.766  mem:  31M  BOD: 4.0M

Recursive Make + --no-builtin-rules --no-builtin-variables
      recursive-make: kind: full  secs:  100.026  mem:  97M  BOD: 4.0M
      recursive-make: kind: incr  secs:    9.316  mem:  13M  BOD: 4.0M
      recursive-make: kind: NULL  secs:    7.739  mem:  13M  BOD: 4.0M

Scons: md5sum
               scons: kind: full  secs:  854.764  mem:   3G  BOD: 311M
               scons: kind: incr  secs:  645.269  mem:   3G  BOD: 311M
               scons: kind: NULL  secs:  607.749  mem:   3G  BOD: 311M

Scons: make
               scons: kind: full  secs:  732.709  mem:   3G  BOD: 217M
               scons: kind: incr  secs:  515.686  mem:   3G  BOD: 217M
               scons: kind: NULL  secs:  511.016  mem:   3G  BOD: 217M

Single Make
         single-make: kind: full  secs:  387.505  mem:   2G  BOD: 4.0M
         single-make: kind: incr  secs:  279.338  mem:   1G  BOD: 4.0M
         single-make: kind: NULL  secs:  280.445  mem:   1G  BOD: 4.0M

Single Make + --no-builtin-rules --no-builtin-variables
         single-make: kind: full  secs:  117.151  mem: 730M  BOD: 4.0M
         single-make: kind: incr  secs:   14.425  mem: 231M  BOD: 4.0M
         single-make: kind: NULL  secs:   14.122  mem: 230M  BOD: 4.0M
```


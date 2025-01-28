# build-tool-comparator

# Preface

There is a significant amount of discord about build tools:

  Scons has perfect dependencies.

  Bazel is hermetically sealed.

  Make is old.

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

- Extremely complicated.
- Does not play well with other build systems.
- Significant hidden state affecting build via automatically used config files.
- Ridiculous number of command line options (eg: bazel help build|nl -ba)
- Bad, often incomplete or incorrect, documentation.
- Profligate use of disk space and other system resources.
- Not as hermetic as fans claim.
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

  full:  When 'true', every file is built. When false, a NULL build is performed.
  secs:  Number of seconds consumed performing the build.
  mem :  The amount of memory used to perform the build.
  BOD :  The amount of disk space consumed by the build.  Each 'module' produces just a single 0-byte file.
```


## 50 simulated modules

```
BOD          : /tmp/make/BOD
Files Per Dir: 100
Modules      : 50
Parallel     : 4
Source       : /tmp/make/source

Bash
                bash: full:  True  secs:    0.155  mem:  13M  BOD:  12K
                bash: full: False  secs:    0.037  mem:  12M  BOD:  12K

Bazel
               bazel: full:  True  secs:    8.942  mem: 236M  BOD: 7.0M
               bazel: full: False  secs:    0.506  mem: 237M  BOD: 6.3M

Recursive Make
      recursive-make: full:  True  secs:    0.116  mem:  13M  BOD:  12K
      recursive-make: full: False  secs:    0.063  mem:  12M  BOD:  12K

Recursive Make + --no-builtin-rules --no-builtin-variables
      recursive-make: full:  True  secs:    0.072  mem:  13M  BOD:  12K
      recursive-make: full: False  secs:    0.015  mem:  12M  BOD:  12K

Scons: md5sum
               scons: full:  True  secs:    0.856  mem:  28M  BOD:  52K
               scons: full: False  secs:    0.690  mem:  28M  BOD:  52K

Scons: make
               scons: full:  True  secs:    0.772  mem:  28M  BOD:  44K
               scons: full: False  secs:    0.661  mem:  28M  BOD:  44K

Single Make
         single-make: full:  True  secs:    0.113  mem:  13M  BOD:  12K
         single-make: full: False  secs:    0.057  mem:  12M  BOD:  12K

Single Make + --no-builtin-rules --no-builtin-variables
         single-make: full:  True  secs:    0.066  mem:  13M  BOD:  12K
         single-make: full: False  secs:    0.011  mem:  12M  BOD:  12K
```


## 100 simulated modules

```
BOD          : /tmp/make/BOD
Files Per Dir: 100
Modules      : 100
Parallel     : 4
Source       : /tmp/make/source

Bash
                bash: full:  True  secs:    0.290  mem:  13M  BOD:  12K
                bash: full: False  secs:    0.074  mem:  12M  BOD:  12K

Bazel
               bazel: full:  True  secs:   10.619  mem: 243M  BOD:  16M
               bazel: full: False  secs:    0.545  mem: 250M  BOD:  14M

Recursive Make
      recursive-make: full:  True  secs:    0.230  mem:  13M  BOD:  12K
      recursive-make: full: False  secs:    0.126  mem:  12M  BOD:  12K

Recursive Make + --no-builtin-rules --no-builtin-variables
      recursive-make: full:  True  secs:    0.126  mem:  13M  BOD:  12K
      recursive-make: full: False  secs:    0.020  mem:  12M  BOD:  12K

Scons: md5sum
               scons: full:  True  secs:    1.118  mem:  30M  BOD:  92K
               scons: full: False  secs:    0.890  mem:  30M  BOD:  92K

Scons: make
               scons: full:  True  secs:    1.072  mem:  30M  BOD:  80K
               scons: full: False  secs:    0.850  mem:  30M  BOD:  80K

Single Make
         single-make: full:  True  secs:    0.234  mem:  13M  BOD:  12K
         single-make: full: False  secs:    0.121  mem:  12M  BOD:  12K

Single Make + --no-builtin-rules --no-builtin-variables
         single-make: full:  True  secs:    0.118  mem:  13M  BOD:  12K
         single-make: full: False  secs:    0.013  mem:  12M  BOD:  12K
```


## 1000 simulated modules

```
BOD          : /tmp/make/BOD
Files Per Dir: 100
Modules      : 1000
Parallel     : 4
Source       : /tmp/make/source

Bash
                bash: full:  True  secs:    2.763  mem:  14M  BOD:  48K
                bash: full: False  secs:    0.858  mem:  12M  BOD:  48K

Bazel
               bazel: full:  True  secs:   26.895  mem: 288M  BOD: 194M
               bazel: full: False  secs:    0.896  mem: 298M  BOD: 180M

Recursive Make
      recursive-make: full:  True  secs:    2.899  mem:  14M  BOD:  48K
      recursive-make: full: False  secs:    1.817  mem:  12M  BOD:  48K

Recursive Make + --no-builtin-rules --no-builtin-variables
      recursive-make: full:  True  secs:    1.004  mem:  14M  BOD:  48K
      recursive-make: full: False  secs:    0.062  mem:  12M  BOD:  48K

Scons: md5sum
               scons: full:  True  secs:    7.274  mem:  64M  BOD: 1.3M
               scons: full: False  secs:    4.934  mem:  64M  BOD: 1.3M

Scons: make
               scons: full:  True  secs:    6.809  mem:  64M  BOD: 1012K
               scons: full: False  secs:    4.549  mem:  63M  BOD: 1012K

Single Make
         single-make: full:  True  secs:    3.186  mem:  25M  BOD:  48K
         single-make: full: False  secs:    2.106  mem:  21M  BOD:  48K

Single Make + --no-builtin-rules --no-builtin-variables
         single-make: full:  True  secs:    1.093  mem:  14M  BOD:  48K
         single-make: full: False  secs:    0.068  mem:  12M  BOD:  48K
```


## 5000 simulated modules

```
BOD          : /tmp/make/BOD
Files Per Dir: 100
Modules      : 5000
Parallel     : 4
Source       : /tmp/make/source

Bash
                bash: full:  True  secs:   13.993  mem:  17M  BOD: 208K
                bash: full: False  secs:    4.507  mem:  12M  BOD: 208K

Bazel
               bazel: full:  True  secs:   78.216  mem: 436M  BOD: 1.2G
               bazel: full: False  secs:    2.290  mem: 420M  BOD: 1.1G

Recursive Make
      recursive-make: full:  True  secs:   28.659  mem:  21M  BOD: 208K
      recursive-make: full: False  secs:   29.556  mem:  21M  BOD: 208K

Recursive Make + --no-builtin-rules --no-builtin-variables
      recursive-make: full:  True  secs:    4.886  mem:  17M  BOD: 208K
      recursive-make: full: False  secs:    0.316  mem:  12M  BOD: 208K

Scons: md5sum
               scons: full:  True  secs:   36.722  mem: 205M  BOD:  11M
               scons: full: False  secs:   24.936  mem: 207M  BOD:  11M

Scons: make
               scons: full:  True  secs:   34.319  mem: 205M  BOD: 7.7M
               scons: full: False  secs:   23.151  mem: 203M  BOD: 7.7M

Single Make
         single-make: full:  True  secs:   29.506  mem: 119M  BOD: 208K
         single-make: full: False  secs:   24.140  mem:  96M  BOD: 208K

Single Make + --no-builtin-rules --no-builtin-variables
         single-make: full:  True  secs:    5.523  mem:  37M  BOD: 208K
         single-make: full: False  secs:    0.411  mem:  13M  BOD: 208K
```

## 10000 simulated modules

```
BOD          : /tmp/make/BOD
Files Per Dir: 100
Modules      : 10000
Parallel     : 4
Source       : /tmp/make/source

Bash
                bash: full:  True  secs:   27.591  mem:  21M  BOD: 408K
                bash: full: False  secs:    9.033  mem:  12M  BOD: 408K

Bazel
               bazel: full:  True  secs:  130.787  mem: 603M  BOD: 2.5G
               bazel: full: False  secs:    3.354  mem: 550M  BOD: 2.3G

Recursive Make
      recursive-make: full:  True  secs:   63.457  mem:  24M  BOD: 408K
      recursive-make: full: False  secs:   51.116  mem:  23M  BOD: 408K

Recursive Make + --no-builtin-rules --no-builtin-variables
      recursive-make: full:  True  secs:    9.722  mem:  21M  BOD: 408K
      recursive-make: full: False  secs:    0.680  mem:  12M  BOD: 408K

Scons: md5sum
               scons: full:  True  secs:   74.561  mem: 385M  BOD:  25M
               scons: full: False  secs:   51.453  mem: 390M  BOD:  25M

Scons: make
               scons: full:  True  secs:   70.341  mem: 386M  BOD:  18M
               scons: full: False  secs:   48.215  mem: 382M  BOD:  18M

Single Make
         single-make: full:  True  secs:   71.645  mem: 239M  BOD: 408K
         single-make: full: False  secs:   61.355  mem: 191M  BOD: 408K

Single Make + --no-builtin-rules --no-builtin-variables
         single-make: full:  True  secs:   11.298  mem:  72M  BOD: 408K
         single-make: full: False  secs:    0.932  mem:  24M  BOD: 408K
```


## 50000 simulated modules

```
BOD          : /tmp/make/BOD
Files Per Dir: 100
Modules      : 50000
Parallel     : 4
Source       : /tmp/make/source

Bash
                bash: full:  True  secs:  138.671  mem:  55M  BOD: 2.0M
                bash: full: False  secs:   46.526  mem:  12M  BOD: 2.0M

Bazel
               bazel: full:  True  secs:  647.644  mem:   1G  BOD:  14G
               bazel: full: False  secs:   17.173  mem:   1G  BOD:  13G

Recursive Make
      recursive-make: full:  True  secs:  502.948  mem:  55M  BOD: 2.0M
      recursive-make: full: False  secs:  402.447  mem:  28M  BOD: 2.0M

Recursive Make + --no-builtin-rules --no-builtin-variables
      recursive-make: full:  True  secs:   51.647  mem:  55M  BOD: 2.0M
      recursive-make: full: False  secs:    3.748  mem:  12M  BOD: 2.0M

Scons: md5sum
               scons: full:  True  secs:  487.910  mem:   1G  BOD: 150M
               scons: full: False  secs:  411.543  mem:   1G  BOD: 150M

Scons: make
               scons: full:  True  secs:  387.646  mem:   1G  BOD: 105M
               scons: full: False  secs:  254.737  mem:   1G  BOD: 105M

Single Make
         single-make: full:  True  secs:  192.407  mem:   1G  BOD: 2.0M
         single-make: full: False  secs:  134.121  mem: 935M  BOD: 2.0M

Single Make + --no-builtin-rules --no-builtin-variables
         single-make: full:  True  secs:   58.381  mem: 364M  BOD: 2.0M
         single-make: full: False  secs:    6.211  mem: 116M  BOD: 2.0M
```


## 100000 simulated modules

```
BOD          : /tmp/make/BOD
Files Per Dir: 100
Modules      : 50000
Parallel     : 4
Source       : /tmp/make/source

Bash
                bash: full:  True  secs:  138.671  mem:  55M  BOD: 2.0M
                bash: full: False  secs:   46.526  mem:  12M  BOD: 2.0M

Bazel
               bazel: full:  True  secs:  647.644  mem:   1G  BOD:  14G
               bazel: full: False  secs:   17.173  mem:   1G  BOD:  13G

Recursive Make
      recursive-make: full:  True  secs:  502.948  mem:  55M  BOD: 2.0M
      recursive-make: full: False  secs:  402.447  mem:  28M  BOD: 2.0M

Recursive Make + --no-builtin-rules --no-builtin-variables
      recursive-make: full:  True  secs:   51.647  mem:  55M  BOD: 2.0M
      recursive-make: full: False  secs:    3.748  mem:  12M  BOD: 2.0M

Scons: md5sum
               scons: full:  True  secs:  487.910  mem:   1G  BOD: 150M
               scons: full: False  secs:  411.543  mem:   1G  BOD: 150M

Scons: make
               scons: full:  True  secs:  387.646  mem:   1G  BOD: 105M
               scons: full: False  secs:  254.737  mem:   1G  BOD: 105M

Single Make
         single-make: full:  True  secs:  192.407  mem:   1G  BOD: 2.0M
         single-make: full: False  secs:  134.121  mem: 935M  BOD: 2.0M

Single Make + --no-builtin-rules --no-builtin-variables
         single-make: full:  True  secs:   58.381  mem: 364M  BOD: 2.0M
         single-make: full: False  secs:    6.211  mem: 116M  BOD: 2.0M
```

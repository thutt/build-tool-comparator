# build-tool-comparator

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

 o Simple Model Invocation

   A tool should be simple to use, since it will be used dozens or
   hundreds of times a day.  It should as little hidden state as
   possible so that each invocation clearly shows how the build was
   produced.  Hidden state includes anything that is not visible at
   the point of invocation, such as default configuration files, shell
   environment variables.  This transparency is worthwhile because it
   reduces the mental load needed to understand the how a produced is
   produced is reduced.

 o Little time spent executing build tool

   The build tool needs to read the product specification, construct a
   DAG and execute rules to turn sources into artifacts.

   Some build tools have additional checking built-in.  This checking
   is the build tool equivalent of a type system in a programming
   language.  Stronger checking up front (when reasonable,
   understandable, errors are produced!) helps to ensure that the
   project is consistent, as specified, at all times.

 o Parallel execution of rules

   When projects have thousands of files, executing them serially can
   make the time to build the project seem glacial.  Executing
   unrelated rules at the same time speeds product builds.

 o Low resource overhead

   The fewer resources used by the build tool means more resources are
   available to execute rules.

 o Minimal work performed on each invocation.

   A build tool should only execute rules needed to bring out-of-date
   artifacts up-to-date.  An artifact is out-of-date when it doesn't
   exist, its sources have changed, or its prerequisites have been
   rebuilt.  Any work that occurs to create an artifact when it is not
   out-of-date is unnecessary, a deficiency in the build process, and,
   possibly, the build tool.

 o Good error reporting

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

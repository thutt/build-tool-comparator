# build-tool-comparator

A build system exists to turn product sources into product artifacts.
It accomplishes this by creating a directed acyclic graph (DAG) of the
product specification.  The product specification associates source
files with artifacts, and the rules needed to transform the source
into the artifact.  Once the DAG is created, it is traversed, and any
source file that has been changed since the last creation of the
associated artifact (or if the artifact doesn't exist) will cause the
rule needed to transform the source to artifact to be reexecuted.

In the case of a C file, the compiler would be invoked to create an
up-to-date object file.  In the case of an object file, the linker
will be invoked to create an up-to-date executable.

The hallmarks of a good build tool are as follows:

 o Little time spent executing build tool

   The build tool needs to read the product describe, construct a DAG
   and execute rules to turn sources into artifacts.

   Some build tools have additional checking built-in.  This checking
   is the build tool equivalent of a type system in a programming
   language.  Stronger checking up front (when reasonable,
   understanable, errors are produced!) helps to ensure that the
   project is consistent, as specified, at all times.

 o Parallel execution of rules

   When projects have thousands of files, executing them serially can
   make the time to build the project seem glacial.  Executing
   unrelated rules at the same time speeds product builds.

 o Low resource overhead

   The fewer resources used by the build tool means that more
   resources are available to execute rules.

 o Minimal work performed on each invocation.

   A build tool should only execute rules that are needed to bring
   out-of-date artifacts up-to-date.  An artifact is out-of-date when
   it doesn't exist, or any of the sources used to create it have
   changed.  Any work that occurs without being triggered by a
   difference in the source and artifacts is unnecessary, and a
   deficiency in the build process, and possibly in the build tool.


<INCOMPLETE>

This readme file will be updated as the overall system gains more
capabilities.

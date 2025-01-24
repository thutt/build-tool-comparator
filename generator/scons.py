# Copyright (c) 2025 Logic Magicians Software.
# All Rights Reserved.
# Licensed under Gnu GPL V3.

import os

import buildtool
import utility

class SConstruct(buildtool.BuildTool):
    def __init__(self, src_root, n_modules, files_per_dir):
        super(SConstruct, self).__init__()
        self.pathname_          = os.path.join(src_root, "SConstruct")
        self.rela_artifact_dir_ = None
        self.src_root_          = src_root
        self.bod_               = os.environ["BPC_BOD"]

    def set_rela_artifact_dir(self, rela_dir):
        self.rela_artifact_dir_ = rela_dir

    def epilog(self, fp):
        fp.write("env.Alias(\"all\",[\n")
        for m in self.modules_:
            fp.write("          \"%s/%s\",\n" % (self.bod_, m.artifact_))
        fp.write("          ])\n")

    def prolog(self, fp):
        fp.write("import os\n\n")
        fp.write("arti = Builder(action='touch $TARGET')\n"
                 "env  = Environment(BUILDERS={'CreateArtifact': arti})\n"
                 "SetOption('silent', True)\n"
                 "\n")
        fp.write("if os.getenv(\"SCONS_MAKE\", None) is not None:\n"
                 "    Decider('make')\n\n")

    def write(self):
        utility.mkdir(os.path.dirname(self.pathname_))
        with open(self.pathname_, "w") as fp:
            self.prolog(fp)

            for m in self.modules_:
                fp.write("env.CreateArtifact(\"%s/%s\",\n"
                         "                   [\"%s\",\n" % (self.bod_,
                                                            m.artifact_,
                                                            m.source_))
                for i in m.imports_:
                    fp.write("                    \"%s\",\n" % (i.interface_))

                fp.write("                   ])\n\n")

            self.epilog(fp)

def create(verbose, src_root, files_per_dir, modules):
    assert(isinstance(verbose, bool))

    n_modules  = len(modules)
    sconstruct = SConstruct(src_root, n_modules, files_per_dir)

    for m in modules:
        sconstruct.add_module(m)

    return sconstruct

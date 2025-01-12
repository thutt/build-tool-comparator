# Copyright (c) 2025 Logic Magicians Software.
# All Rights Reserved.
# Licensed under Gnu GPL V3.

import os

import buildtool
import utility

class Makefile(buildtool.BuildTool):
    def __init__(self, src_root):
        super(Makefile, self).__init__()
        self.pathname_          = os.path.join(src_root, "Makefile.single")
        self.rela_artifact_dir_ = None
        self.src_root_          = src_root

    def atsign(self):
        return "$(if $(VERBOSE),,@)"

    def set_rela_artifact_dir(self, rela_dir):
        self.rela_artifact_dir_ = rela_dir

    def write(self):
        utility.mkdir(os.path.dirname(self.pathname_))
        with open(self.pathname_, "w") as fp:
            fp.write("SOURCE\t:=\t\t\\\n")
            first = True
            for m in self.modules_:
                if not first:
                    fp.write("\t\t\\\n")
                fp.write("\t$(subst $(BPC_SOURCE)/,,%s)" % (m.source_))
                first = False
            fp.write("\n\n"
                     "ARTIFACT\t= $(addprefix $(BOD)/,$(SOURCE:.source=.artifact))\n\n")

            # Set all import files as prerequisites.
            for m in self.modules_:
                fp.write("$(BOD)/%s: %s" % (m.artifact_, m.source_))
                for imp in m.imports_:
                    fp.write(" %s" % (imp.interface_))
                fp.write("\n\t%stouch $@;\n\n" % (self.atsign()))


class RootMakefile(Makefile):
    def __init__(self, src_root, n_modules, files_per_dir):
        super(RootMakefile, self).__init__(src_root)
        self.files_per_dir_ = files_per_dir
        self.subordinates_  = [ ]

    def add_subordinate(self, makefile):
        assert(isinstance(makefile, Makefile))
        self.subordinates_.append(makefile)

    def create_subordinate_directories(self, fp):
        # Create rules for creating build output directories for subordinate
        # Makefiles.
        fp.write("$(addprefix $(BOD)/,")
        first = True
        for sub in self.subordinates_:
            if not first:
                fp.write(" ")
            fp.write("%s" % (sub.rela_artifact_dir_))
            first = False
        fp.write("):\n")
        fp.write("\t%secho \"Creating build directory '$@'\"; \\\n"
                 "\tmkdir --parents $@;\n\n" % (self.atsign()))

        fp.write("create-build-directories:\t\\\n\t|")
        first = True
        for sub in self.subordinates_:
            if not first:
                fp.write("\t ")
            fp.write(" $(addprefix $(BOD)/,%s)\t\\\n" % (sub.rela_artifact_dir_))
            first = False
        fp.write("\n\n")

    def prolog(self, fp):
        fp.write("$(if $(BOD),,$(error BOD "
                 "must be set to build output location. "
                 "It must not be in the source tree))\n"
                 "$(if $(wildcard $(BOD)),,$(error $(BOD) "
                 "directory does not exist))\n\n"
                 "SPACE\t:=\n"
                 "SPACE\t:= $(SPACE) $(SPACE)\n"
                 ".DEFAULT_GOAL\t:=\tbuild\n\n"
                 "clean:\n\trm -rf $(BOD);\n\n")

    def default_goal(self, fp):
        fp.write(".PHONY:\tbuild\n\n")
        fp.write("build:\t")
        fp.write("\n\t%secho \"All targets up-to-date.\";\n" % self.atsign())
        fp.write("\n")

    def generate_subordinate(self, fp, sub):
        sub.write()
        fp.write("include %s\n" % (sub.pathname_))
        fp.write("$(ARTIFACT):\t| $(BOD)/%s\n" % (sub.rela_artifact_dir_))
        fp.write("build: $(ARTIFACT)\n\n")

    def write(self):
        utility.mkdir(os.path.dirname(self.pathname_))
        with open(self.pathname_, "w") as fp:
            self.prolog(fp)
            self.create_subordinate_directories(fp)

            for sub in self.subordinates_:
                self.generate_subordinate(fp, sub)

            self.default_goal(fp)

def create(verbose, src_root, files_per_dir, modules):
    assert(isinstance(verbose, bool))

    n_modules     = len(modules)
    root_makefile = RootMakefile(src_root, n_modules, files_per_dir)

    for m in modules:
        mf_index = m.module_num_ // files_per_dir

        # Add a subordinate Makefile snippet for this set of modules.
        if len(root_makefile.subordinates_) <= mf_index:
            module_dir = os.path.dirname(m.source_)
            mf = Makefile(module_dir)
            mf.set_rela_artifact_dir(m.rela_artifact_dir_)
            root_makefile.add_subordinate(mf)

        root_makefile.subordinates_[mf_index].add_module(m)

    return root_makefile

# Copyright (c) 2025 Logic Magicians Software.
# All Rights Reserved.
# Licensed under Gnu GPL V3.

import os

import buildtool
import utility

class Makefile(buildtool.BuildTool):
    def __init__(self, src_root):
        super(Makefile, self).__init__()
        self.pathname_          = os.path.join(src_root, "Makefile.recursive")
        self.rela_artifact_dir_ = None
        self.src_root_          = src_root

    def atsign(self):
        return "$(if $(VERBOSE),,@)"

    def set_rela_artifact_dir(self, rela_dir):
        self.rela_artifact_dir_ = rela_dir

    def write(self):
        utility.mkdir(os.path.dirname(self.pathname_))
        with open(self.pathname_, "w") as fp:
            # Pattern rule to turn sources into artifacts.
            fp.write("%%.artifact:\t%%.source\n"
                     "\t%stouch $@;\n\n" % (self.atsign()))

            fp.write("SOURCE\t:=\t\t\\\n")
            first = True
            for m in self.modules_:
                if not first:
                    fp.write("\t\t\\\n")
                fp.write("\t%s" % (os.path.basename(m.source_)))
                first = False
            fp.write("\n\n"
                     "ARTIFACT\t= $(SOURCE:.source=.artifact)\n\n")

            # Set all import files as prerequisites.
            for m in self.modules_:
                for imp in m.imports_:
                    fp.write("%s: %s\n" % (os.path.basename(m.artifact_),
                                           imp.interface_))
            fp.write("\nsubdirectory__: $(ARTIFACT)\n\n")


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
        fp.write("\t%smkdir --parents $@; "
                 "$(if $(VERBOSE),echo \"Creating build directory '$@'\";)"
                 "\n\n" % (self.atsign()))

        fp.write("create-build-directories:\t\\\n\t|")
        first = True
        for sub in self.subordinates_:
            if not first:
                fp.write("\t ")
            fp.write(" $(addprefix $(BOD)/,%s)\t\\\n" % (sub.rela_artifact_dir_))
            first = False
        fp.write("\n\n")

    def invoke_subordinate_make(self, fp):
        silent = ""
        for sub in self.subordinates_:
            fp.write("%s " % (sub.rela_artifact_dir_))
        fp.write(":\tcreate-build-directories\n"
                 "\t%s$(MAKE)\t\t\t\\\n"
                 "\t    $(if $(VERBOSE),,--silent)\t\\\n"
                 "\t    --no-print-directory\t\\\n"
                 "\t    BOD=$(BOD)/$@\t\t\\\n"
                 "\t    VPATH=%s/$@\t\t\\\n"
                 "\t    -C $(BOD)/$@\t\t\\\n"
                 "\t    -f %s/$@/Makefile.recursive\t\t\\\n"
                 "\t    subdirectory__\n" % (self.atsign(),
                                             self.src_root_, self.src_root_))
        fp.write("\n\n")

    def subordinate_rules(self, fp):
        self.create_subordinate_directories(fp)
        self.invoke_subordinate_make(fp)

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
        for sub in self.subordinates_:
            fp.write("\t%s" % (sub.rela_artifact_dir_))
        fp.write("\n\t%secho \"All targets up-to-date.\";\n" % self.atsign())
        fp.write("\n")

    def write(self):
        utility.mkdir(os.path.dirname(self.pathname_))
        with open(self.pathname_, "w") as fp:
            self.prolog(fp)
            self.subordinate_rules(fp)
            self.default_goal(fp)

        for sub in self.subordinates_:
            sub.write()


def create(verbose, src_root, files_per_dir, modules):
    assert(isinstance(verbose, bool))

    n_modules     = len(modules)
    root_makefile = RootMakefile(src_root, n_modules, files_per_dir)

    # Compute number of recursively invoked Makefiles.
    n_makefiles = n_modules // files_per_dir + 1
    makefiles   = [ ]

    for m in modules:
        mf_index = m.module_num_ // files_per_dir

        # Add a subordinate Makefile for this set of modules.

        if len(root_makefile.subordinates_) <= mf_index:
            module_dir = os.path.dirname(m.source_)
            mf = Makefile(module_dir)
            mf.set_rela_artifact_dir(m.rela_artifact_dir_)
            root_makefile.add_subordinate(mf)

        root_makefile.subordinates_[mf_index].add_module(m)

    return root_makefile

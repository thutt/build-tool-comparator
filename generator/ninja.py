# Copyright (c) 2025 Logic Magicians Software.
# All Rights Reserved.
# Licensed under Gnu GPL V3.

import os

import buildtool
import utility

class Ninja(buildtool.BuildTool):
    def __init__(self, src_root):
        super(Ninja, self).__init__()
        self.pathname_          = os.path.join(src_root, "build.ninja")
        self.rela_artifact_dir_ = None
        self.src_root_          = src_root
        self.bod_               = os.environ["BPC_BOD"]
        assert(self.bod_ is not None)

    def set_rela_artifact_dir(self, rela_dir):
        self.rela_artifact_dir_ = rela_dir

    def write(self, fp):
        for m in self.modules_:
            fp.write("build %s/%s: touch %s " % (self.bod_,
                                                 m.artifact_, m.source_))
            for imp in m.imports_:
                fp.write("$\n  %s " % (imp.interface_))
            fp.write("\n\n")


class RootNinja(Ninja):
    def __init__(self, src_root, n_modules, files_per_dir):
        super(RootNinja, self).__init__(src_root)
        self.files_per_dir_ = files_per_dir
        self.subordinates_  = [ ]

    def add_subordinate(self, ninja):
        assert(isinstance(ninja, Ninja))
        self.subordinates_.append(ninja)

    def prolog(self, fp):
        fp.write("rule touch\n"
                 "  command = touch $out\n"
                 "\n")

    def write(self):
        utility.mkdir(os.path.dirname(self.pathname_))
        with open(self.pathname_, "w") as fp:
            self.prolog(fp)

            for sub in self.subordinates_:
                sub.write(fp)

            fp.write("build all: touch ")
            for sub in self.subordinates_:
                for m in sub.modules_:
                    fp.write("$\n"
                             "  %s/%s " % (self.bod_, m.artifact_))
            fp.write("\n")


def create(verbose, src_root, files_per_dir, modules):
    assert(isinstance(verbose, bool))

    n_modules = len(modules)
    ninja     = RootNinja(src_root, n_modules, files_per_dir)

    for m in modules:
        mf_index = m.module_num_ // files_per_dir

        if len(ninja.subordinates_) <= mf_index:
            module_dir = os.path.dirname(m.source_)
            mf = Ninja(module_dir)
            mf.set_rela_artifact_dir(m.rela_artifact_dir_)
            ninja.add_subordinate(mf)

        ninja.subordinates_[mf_index].add_module(m)

    return ninja

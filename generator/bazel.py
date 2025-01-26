# Copyright (c) 2025 Logic Magicians Software.
# All Rights Reserved.
# Licensed under Gnu GPL V3.

import os

import buildtool
import utility

class Builder(buildtool.BuildTool):
    def __init__(self, src_root, n_modules, files_per_dir):
        super(Builder, self).__init__()
        self.rela_artifact_dir_ = None
        self.n_modules_         = n_modules
        self.files_per_dir_     = files_per_dir
        self.src_root_          = src_root
        self.bod_               = os.environ["BPC_BOD"]

    # def set_rela_artifact_dir(self, rela_dir):
    #     self.rela_artifact_dir_ = rela_dir

    def write_workspace(self):
        workspace = os.path.join(self.src_root_, "WORKSPACE")
        with open(workspace, "w") as fp:
            fp.write("\n")

    def write_artifact_bzl(self):
        artifact = os.path.join(self.src_root_, "artifact.bzl")
        with open(artifact, "w") as fp:
            fp.write("""
def artifact(name, srcs, **kwargs):
    native.genrule(
        name = name,
        srcs = srcs,
        outs = [name + ".artifact"],
        cmd = "touch $@",
        **kwargs
    )""")

        # For 'Bazel reasons', there needs to be BUILD.bazel file
        # here, too.  It's for the bzl file.  It doesn't need anything
        # in it, however.

        build = os.path.join(self.src_root_, "BUILD.bazel")
        with open(build, "w") as fp:
            fp.write("\n")

    def write_interface_empty(self):
        artifact = os.path.join(self.src_root_, "interface", "BUILD.bazel")
        with open(artifact, "w") as fp:
            fp.write("\n")

    def get_interface_export_pathname(self, dir_num):
        return os.path.join(self.src_root_, "interface",
                            str(dir_num), "BUILD.bazel")

    def write_exports_files(self, fp, residual, start_index, n_files):
        fp.write("# residual: %s  start: %d  n_files: %d\n" %
                 (str(residual), start_index, n_files))

        fp.write("exports_files([\n")
        for j in range(0, n_files):
            fp.write("   \"m%d.interface\",\n" % (start_index + j))
        fp.write("])")

    def write_interface_exports(self):
        # Each interface file in the corresponding directory.
        for i in range(0, self.n_modules_, self.files_per_dir_):
            fname = self.get_interface_export_pathname(i // self.files_per_dir_)
            with open(fname, "w") as fp:
                self.write_exports_files(fp, False, i, self.files_per_dir_)
        # Get residual files in last directory.
        n_residual = self.n_modules_ % self.files_per_dir_
        if n_residual == 0:
            # Last directory is full, not partially full.
            n_residual = self.files_per_dir_
        fname = self.get_interface_export_pathname(i // self.files_per_dir_)
        with open(fname, "w") as fp:
            self.write_exports_files(fp, True, i, n_residual)


    def write_file_rules(self):
        # Each source file in the corresponding directory.
        # artifact(<source-name>, [prerequi-list])
        for m in self.modules_:
            fname = os.path.join(os.path.dirname(m.source_), "BUILD.bazel")
            if not os.path.exists(fname):
                # Load the 'artifact' file
                with open(fname, "a") as fp:
                    fp.write("load(\"//:artifact.bzl\", \"artifact\")\n\n")

            with open(fname, "a") as fp:
                fp.write("artifact(\"m%s\",\n"
                         "         [ \"%s\",\n" %
                         (str(m.module_num_),
                          os.path.basename(m.source_)))
                for imp in m.imports_:
                    dir_name = os.path.dirname(imp.interface_)
                    dir_num  = os.path.basename(dir_name)
                    fp.write("           \"//interface/%s:%s\",\n" %
                             (dir_num, os.path.basename(imp.interface_)))
                fp.write("         ])\n")

    def write(self):
        self.write_workspace()
        self.write_artifact_bzl()
        self.write_interface_empty()
        self.write_interface_exports()
        self.write_file_rules()

def create(verbose, src_root, files_per_dir, modules):
    assert(isinstance(verbose, bool))

    n_modules  = len(modules)
    builder = Builder(src_root, n_modules, files_per_dir)

    for m in modules:
        builder.add_module(m)

    return builder

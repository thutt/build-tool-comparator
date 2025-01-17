# Copyright (c) 2025 Logic Magicians Software.
# All Rights Reserved.
# Licensed under Gnu GPL V3.

import os

import buildtool
import stat
import utility

class Script(buildtool.BuildTool):
    def __init__(self, src_root, n_modules, files_per_dir):
        super(Script, self).__init__()
        self.pathname_          = os.path.join(src_root, "build.sh")
        self.bash_dir_          = os.path.join(src_root, "bash")
        self.rela_artifact_dir_ = None
        self.src_root_          = src_root
        self.n_modules_         = n_modules
        self.files_per_dir_     = files_per_dir

    def set_rela_artifact_dir(self, rela_dir):
        self.rela_artifact_dir_ = rela_dir

    def set_execute(self, pathname):
        os.chmod(pathname, (stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR |
                            stat.S_IRGRP | stat.S_IXGRP |
                            stat.S_IROTH | stat.S_IXOTH))

    def prolog(self, fp):
        fp.write("#!/bin/bash\n"
                 "set -o nounset;\n"
                 "\n\n")

        fp.write("BOD=${BPC_BOD:?\"BPC_BOD is not set.\"};\n"
                 "if [ ! -z ${BPC_VERBOSE:-\"\"} ] ; then\n"
                 "    VERBOSE=t;\n"
                 "fi;\n\n")

    def artifact_script(self, file_num):
        assert(isinstance(file_num, int));
        return os.path.join(self.bash_dir_, "artifacts_%d.sh" % (file_num))

    def chain_script(self, fp, file_number):
        fp.write("\nexec \"%s\";\n" % self.artifact_script(file_number))

    def create_directories(self, pathname, artifact_file_number):
        # Gather directories of all artifacts into a set to remove
        # duplicates.
        artifact_dir = set()
        for m in self.modules_:
            artifact_dir.add(os.path.dirname(m.artifact_))

        with open(pathname, "w") as fp:
            # Make all the directories, iff they are not already present.
            self.prolog(fp)
            fp.write("# Create artifact directories.\n")
            for ad in sorted(artifact_dir):
                ad = "${BOD}/%s" % (ad)
                fp.write("[ -d \"%s\" ] || mkdir --parents \"%s\";\n" % (ad, ad))

            fp.write("\n")

            self.chain_script(fp, artifact_file_number)

            self.set_execute(pathname)

    def create_artifact(self, fp, m):
        fp.write("\n"
                 "[ ! -f \"${BOD}/%s\" ] \\\n"
                 "|| [ \"${BOD}/%s\" -ot \"%s\" ] \\\n"
                 "|| [ \"${BOD}/%s\" -ot \"%s\" ] \\" %
                 (m.artifact_,
                  m.artifact_, m.source_,
                  m.artifact_, m.interface_))
        for imp in m.imports_:
            fp.write("\n"
                     "|| [ \"${BOD}/%s\" -ot \"%s\" ] \\" % (m.artifact_,
                                                             imp.interface_))
        fp.write("\n&& builtin echo "" >\"${BOD}/%s\" \\"
                 "\n&& [ ! -z \"${VERBOSE:-}\" ] \\"
                 "\n&& builtin echo \"Creating '${BOD}/%s'\";\n" %
                 (m.artifact_, m.artifact_))

    def create_artifacts(self, fp):
        n_files_per_snippet = 100
        for script_idx  in range(0, len(self.modules_), n_files_per_snippet):
            pathname = self.artifact_script(script_idx)
            with open(pathname, "w") as fp:
                self.prolog(fp)
                offset = 0;
                while (offset < 100 and
                       script_idx + offset < len(self.modules_)):
                    m = self.modules_[script_idx + offset]
                    self.create_artifact(fp, m)
                    offset = offset + 1
                if script_idx + n_files_per_snippet < len(self.modules_):
                    self.chain_script(fp, script_idx + n_files_per_snippet)
                self.set_execute(pathname)

    def write(self):
        utility.mkdir(os.path.dirname(self.pathname_))
        utility.mkdir(self.bash_dir_)

        with open(self.pathname_, "w") as fp:
            self.prolog(fp)
            pathname = os.path.join(self.bash_dir_, "create_directories.sh")
            fp.write("exec \"%s\"" % (pathname))
            self.create_directories(pathname, 0)
            self.create_artifacts(fp)
            fp.write("\n");
            self.set_execute(self.pathname_)


def create(verbose, src_root, files_per_dir, modules):
    assert(isinstance(verbose, bool))

    n_modules     = len(modules)
    script = Script(src_root, n_modules, files_per_dir)
    for m in modules:
        script.add_module(m)

    return script

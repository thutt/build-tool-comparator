#!/usr/bin/python3 -B
# Copyright (c) 2025  Logic Magicians Software.
# All Rights Reserved.
# Licensed under Gnu GPL V3.

import argparse
import json
import os
import resource
import subprocess
import sys
import time

class build_system(object):
    def __init__(self, name, full):
        self.full_        = full
        self.disk_space_  = None
        self.name_        = name
        self.stdout_      = None
        self.stderr_      = None
        self.rc_          = None
        self.rusage_      = None
        self.root_        = os.path.realpath(os.path.join(os.path.dirname(sys.argv[0]),
                                                          ".."))
        self.generate_    = os.path.join(self.root_, "scripts", "generate.sh")
        self.builder_     = os.path.join(self.root_, "scripts",
                                         "build-%s.sh" % (name))

    def generate(self):
        (stdout, stderr, rc, rusage) = execute_process([ self.generate_ ])
        assert(rc == 0)

    def get_directory_space(self, directory):
        cmd = [ "/usr/bin/du", "-Dsh", directory ]
        (stdout,
         stderr,
         rc,
         rusage) = execute_process(cmd)
        fields = stdout[0].split("\t")
        return fields[0]

    def set_build_disk_space(self):
        self.disk_space_ = self.get_directory_space(os.environ.get("BPC_BOD"))

    def run(self):
        start = time.time()
        (self.stdout_,
         self.stderr_,
         self.rc_,
         self.rusage_) = execute_process([ self.builder_ ])
        end = time.time()
        self.elapsed_ = end - start
        self.set_build_disk_space()

    def dictionary(self):
        return {
            "full"   : self.full_,
            "stdout" : self.stdout_,
            "stderr" : self.stderr_,
            "rc"     : self.rc_,
            "seconds": elapsed,
            "maxrss" : self.rusage_.ru_maxrss,
            "ixxrss" : self.rusage_.ru_ixrss,
            "idxrss" : self.rusage_.ru_idrss,
            "disk"   : self.disk_space_,
            }

    def scale(self, n_bytes):
        Kb = 1024
        Mb = Kb * 1024
        Gb = Mb * 1024
        if n_bytes > Gb:
            return "%dG" % (n_bytes // Gb)
        elif n_bytes > Mb:
            return "%dM" % (n_bytes // Mb)
        elif n_bytes > Kb:
            return "%dK" % (n_bytes // Kb)
        else:
            return "%d " % (n_bytes)


    def display(self):
        print("%20s: full: %5s  secs: %8.3f  mem: %4s  BOD: %4s" %
              (self.name_, str(self.full_),
               self.elapsed_,
               self.scale(self.rusage_.ru_maxrss * 1024),
               self.disk_space_))

class bazel(build_system):
    def __init__(self, name, full):
        super(bazel, self).__init__(name, full)

    def set_build_disk_space(self):
        # Bazel writes to these directories.  They are one directory
        # above the root of the source tree.  But, by default, they
        # are symlinked into ~/.cache/bazel.
        #
        # For out-of-the-box comparisons, this system will remove
        # ~/.cache/bazel (to ensure it's empty, and no cheating with
        # pre-existing data, so instead of following these symlinks,
        # the full ~/.cache/bazel size is measured.
        #
        #   root = os.path.join(os.environ.get("BPC_SOURCE"))
        #   os.path.abspath(os.path.join(root, "bazel-bin")),
        #   os.path.abspath(os.path.join(root, "bazel-out")),
        #   os.path.abspath(os.path.join(root, "bazel-source")),
        #   os.path.abspath(os.path.join(root, "bazel-testlogs"))
        #
        cache_dir = os.path.expanduser("~/.cache/bazel")
        size = self.get_directory_space(cache_dir)
        self.disk_space_ = size


def configure_parser():
    description = ("""
  Return Code:
    0       : success
    non-zero: failure
""")

    formatter = argparse.RawDescriptionHelpFormatter
    parser    = argparse.ArgumentParser(usage           = None,
                                        formatter_class = formatter,
                                        description     = description,
                                        prog            = "generate.py")

    parser.add_argument("arg_tail",
                        help    = "Command line arguments.",
                        nargs = "*")

    return parser


def execute_process(cmd):
    assert(isinstance(cmd, list))
    assert(os.path.exists(cmd[0]))
    p = subprocess.Popen(cmd,
                         universal_newlines = False,
                         shell  = False,
                         encoding = "utf-8",
                         stdin  = subprocess.PIPE,
                         stdout = subprocess.PIPE,
                         stderr = subprocess.PIPE)
    (stdout, stderr) = p.communicate(None)

    # None is returned when no pipe is attached to stdout/stderr.
    if stdout is None:
        stdout = ''
    if stderr is None:
        stderr = ''
    rc = p.returncode

    rusage = resource.getrusage(resource.RUSAGE_CHILDREN)

    # stdout block becomes a list of lines.  For Windows, delete
    # carriage-return so that regexes will match '$' correctly.
    #
    return (stdout.replace("\r", "").split("\n"),
            stderr.replace("\r", "").split("\n"),
            rc, rusage)


def configure_parser():
    description = ("""
  Return Code:
    0       : success
    non-zero: failure
""")

    formatter = argparse.RawDescriptionHelpFormatter
    parser    = argparse.ArgumentParser(usage           = None,
                                        formatter_class = formatter,
                                        description     = description,
                                        prog            = "generate.py")

    parser.add_argument("--name",
                        help     = ("Name of build process to exercise."),
                        required = True,
                        action   = "store",
                        dest     = "arg_name")

    parser.add_argument("--full",
                        help     = ("Max number of files that can be "
                                    "written to a directory.  If this "
                                    "number is too large, the OS will spend "
                                    "more time searching for files in the "
                                    "filesystem [default: %(default)s files]."),
                        required = False,
                        default  = False,
                        action   = "store_true",
                        dest     = "arg_full")

    parser.add_argument("arg_tail",
                        help    = "Command tail.",
                        nargs = "*")

    return parser


def get_options():
    parser  = configure_parser()
    options = parser.parse_args()

    return options


def create_build_data(name, full):
    if name == "bazel":
        # Bazel doesn't play well with others, and therefore does
        # things its own way.  Extracting the necessary information to
        # make a report about build system overheads requires
        # specialization for Bazel.
        return [ bazel(name, full) ]
    else:
        return [ build_system(name, full) ]


def main():
    try:
        options           = get_options()
        build_systems     = create_build_data(options.arg_name,
                                              options.arg_full)
        for bs in build_systems:
            # The 'runner' shell script must execute a full build
            # FIRST, followed by all incremental and NULL builds.
            if options.arg_full:
                bs.generate()
            bs.run()

        for bs in build_systems:
            bs.display()

    except KeyboardInterrupt as exc:
        print("Ctrl-C interrupt")
        sys.exit(10)

    except Exception as exc:
        print("Unhandled exception '%s'" % (str(exc)))
        raise exc

    return 0

if __name__ == "__main__":
    main()

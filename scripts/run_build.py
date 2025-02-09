#!/usr/bin/python3 -B
# Copyright (c) 2025  Logic Magicians Software.
# All Rights Reserved.
# Licensed under Gnu GPL V3.

import argparse
import datetime
import json
import multiprocessing
import os
import platform
import resource
import subprocess
import sys
import threading
import time

class Metrics(object):
    def __init__(self, metrics_file, tool_name, tool_label):
        now                 = datetime.datetime.now()
        self.tool_name_     = tool_name
        self.tool_label_    = tool_label
        self.tool_version_  = self.get_tool_version(tool_name)
        self.json_path_     = metrics_file
        self.json_          = None
        self.host_os_       = platform.system()
        self.host_arch_     = platform.machine()
        self.host_cpus_     = str(multiprocessing.cpu_count())
        self.host_memory_   = str((os.sysconf('SC_PAGE_SIZE') *
                                   os.sysconf('SC_PHYS_PAGES')))
        self.host_platform_ = platform.platform()
        self.host_version_  = platform.version()
        self.now_date_      = now.strftime("%Y/%m/%d")    # Date script run.
        self.now_time_      = now.strftime("%H:%M:%S.%f") # Time script run.
        self.addl_args_     = self.get_additional_args()
        self.n_modules_     = self.get_n_modules()
        self.files_per_dir_ = self.get_files_per_dir()
        self.parallelism_   = self.get_parallelism()

        self.host_dict_ =  {
            "arch"         : self.host_arch_,
            "platform"     : self.host_platform_,
            "version"      : self.host_version_,
            "cpus"         : int(self.host_cpus_),
            "memory-bytes" : int(self.host_memory_),
        }

        self.geometry_dict_ = {
            "files-per-dir"    : int(self.files_per_dir_),
            "num-modules"      : int(self.n_modules_),
            "parallelism"      : int(self.parallelism_),
            }

        self.tool_dict_ = {
            "label"    : self.tool_label_,
            "version"  : self.tool_version_,
            "args"     : self.addl_args_,
            "runs"     : [ ]
        }

        self.geometry_ = {
            "tool"     : self.tool_dict_,
            "host"     : self.host_dict_,
            "geometry" : self.geometry_dict_,
        }

        if os.path.exists(self.json_path_):
            with open(self.json_path_, "r") as fp:
                self.json_ = json.load(fp)
        else:
            self.json_ = [ ]
        self.add_geometry(self.geometry_) # Possibly updates self.geometry_

    def get_parallelism(self):
        j = os.environ.get("BPC_PARALLEL")
        if j is None:
            return "<unknown>"
        else:
            return str(j)

    def get_n_modules(self):
        n_modules = os.environ.get("BPC_MODULES")
        if n_modules is not None:
            return str(n_modules)
        else:
            return "<M: internal error>"

    def get_files_per_dir(self):
        fpd = os.environ.get("BPC_FILES_PER_DIR")
        if fpd is not None:
            return str(fpd)
        else:
            return "<FPD: internal error>"

    def get_additional_args(self):
        baa = os.environ.get("BPC_BUILD_ADDITIONAL_ARGS")
        if baa is not None:
            if len(baa) > 0:
                return baa

        return "<no-args>"

    def add_geometry(self, geometry):
        # Find the test host, geometry & tool info that matchs the
        # current one, and set the current geometry to it.  This makes
        # all test runs on the same machine & geometry be in the same
        # dictionary.
        #
        # If the current host & geometry do not exist, add it to the
        # main json representation.
        for g in self.json_:
            if (g["host"] == geometry["host"] and
                g["geometry"] == geometry["geometry"]):
                # Ignore the 'runs' field of the 'tool' for this
                # comparison.
                if (g["tool"]["label"]   == geometry["tool"]["label"]   and
                    g["tool"]["version"] == geometry["tool"]["version"] and
                    g["tool"]["args"]    == geometry["tool"]["args"]):
                    self.geometry_  = g
                    self.tool_dict_ = g["tool"]
                    return
        self.json_.append(geometry)

    def save(self):
        with open(self.json_path_, "w") as fp:
            json.dump(self.json_, fp, indent = 2)

    def get_version(self, cmd):
        (stdout,
         stderr,
         rc,
         rusage) = execute_process(cmd)
        assert(rc == 0)
        return stdout

    def get_tool_version(self, tool_name):
        if tool_name == "bash":
            stdout = self.get_version(["/usr/bin/bash", "--version"])
            return stdout[0]
        elif tool_name == "bazel":
            stdout = self.get_version(["/usr/bin/bazel", "--version"])
            return stdout[0]
        elif tool_name == "make":
            stdout = self.get_version(["/usr/bin/make", "--version"])
            return stdout[0]
        else:
            assert(tool_name == "scons")
            stdout = self.get_version(["/usr/bin/scons", "--version"])
            return stdout[1][1:] # Delete tab at beginning.

    def add_metrics(self, tm):
        # Include the metrics for this build system's run.
        run = {
            "date" : self.now_date_,
            "time" : self.now_time_,
        }
        run.update(tm)
        self.tool_dict_["runs"].append(run)


class build_system(object):
    def __init__(self, name, kind):
        self.kind_        = kind
        self.disk_space_  = None # Disk space used for BOD.
        self.rsz_         = 0    # Resident memory size.
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
        # Produces number of Kb.
        cmd = [ "/usr/bin/du", "--block-size", "1024", "-Ds", directory ]
        (stdout,
         stderr,
         rc,
         rusage) = execute_process(cmd)
        fields = stdout[0].split("\t")
        return int(fields[0]) * 1024 # Returns number of bytes.

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
        self.rsz_ = self.rusage_.ru_maxrss * 1024 # Resident size, in bytes.
        self.set_build_disk_space()


    def metrics(self):
        return {
            "bod-size-bytes" : self.disk_space_,
            "kind"           : self.kind_,
            "memory-bytes"   : self.rsz_,
            "seconds"        : self.elapsed_,
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
        print("%20s: kind: %4s  secs: %8.3f  mem: %4s  BOD: %4s" %
              (self.name_, self.kind_[0:4],
               self.elapsed_,
               self.scale(self.rsz_),
               self.scale(self.disk_space_)))


class bazel(build_system):
    def __init__(self, name, kind):
        super(bazel, self).__init__(name, kind)
        self.build_complete_  = False
        self.thread_stopped_  = True
        self.java_daemon_rsz_ = 0

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

    def get_pid(self, cmd):
        (stdout,
         stderr,
         rc,
         rusage) = execute_process([ "/usr/bin/pidof", cmd ])

        if rc == 0:
            return stdout[0]
        else:
            return -1           # Invalid PID

    def get_resident_size(self, pid):
        while not self.build_complete_:
            time.sleep(5)       # Gather daemon size every 5 seconds.

            pid = self.get_pid("bazel(source)")
            if pid != -1:
                # A valid PID found.
                (stdout,
                 stderr,
                 rc,
                 rusage) = execute_process([ "/usr/bin/ps",
                                             "-o", "rsz",
                                             "-p", pid ])
                if rc == 0:
                    self.java_daemon_rsz_ = max(self.java_daemon_rsz_,
                                                int(stdout[1]) * 1024)

            else:
                # No applicable Java process found, so no need to add
                # daemon memory consumption.
                pass



    def run(self):
        self.build_complete_ = False
        thread = threading.Thread(name="java-rsz",
                                  target=self.get_resident_size,
                                  args=[self])
        thread.start()
        super(bazel, self).run()
        self.build_complete_ = True
        thread.join()
        self.rsz_ += self.java_daemon_rsz_


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
                        help     = ("Name of build process script "
                                    "to exercise."),
                        required = True,
                        action   = "store",
                        dest     = "arg_name")

    parser.add_argument("--tool",
                        help     = ("Name of build tool being used  "
                                    "(for determining version)."),
                        required = True,
                        choices  = [ 'bash', 'bazel', 'make', 'scons' ],
                        action   = "store",
                        dest     = "arg_tool")

    parser.add_argument("--kind",
                        help     = ("Kind of build: full, incremental, NULL."),
                        required = True,
                        choices  = [ 'incremental', 'full', 'NULL' ],
                        action   = "store",
                        dest     = "arg_kind")

    parser.add_argument("--tool-label",
                        help     = ("Name of build tool being used for "
                                    "use in reports.  "
                                    "If not supplied, '--name' value used."),
                        required = False,
                        default  = None,
                        action   = "store",
                        dest     = "arg_tool_label")

    parser.add_argument("--metrics",
                        help     = ("Name of Json file where "
                                    "collected data should be stored."),
                        required = True,
                        action   = "store",
                        dest     = "arg_metrics")

    parser.add_argument("arg_tail",
                        help    = "Command tail.",
                        nargs = "*")

    return parser


def get_options():
    parser  = configure_parser()
    options = parser.parse_args()

    if options.arg_tool_label is None:
        options.arg_tool_label = options.arg_tool

    return options


def create_build_data(name, kind):
    if name == "bazel":
        # Bazel doesn't play well with others, and therefore does
        # things its own way.  Extracting the necessary information to
        # make a report about build system overheads requires
        # specialization for Bazel.
        return [ bazel(name, kind) ]
    else:
        return [ build_system(name, kind) ]


def main():
    try:
        options       = get_options()
        build_systems = create_build_data(options.arg_name,
                                          options.arg_kind)
        metrics       = Metrics(options.arg_metrics,
                                options.arg_tool,
                                options.arg_tool_label)

        for bs in build_systems:
            # The 'runner' Bash script must execute a full build
            # FIRST, followed by all incremental and NULL builds.
            if options.arg_kind == "full":
                bs.generate()
            bs.run()
            metrics.add_metrics(bs.metrics())
            metrics.save()

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

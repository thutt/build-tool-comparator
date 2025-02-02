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
    def __init__(self, metrics_file, tool_name, tool_process_name):
        now                 = datetime.datetime.now()
        self.tool_name_     = tool_name
        self.process_name_  = tool_process_name
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
        self.module_size_   = self.get_module_size()
        self.files_per_dir_ = self.get_files_per_dir()
        self.parallelism_   = self.get_parallelism()

        if os.path.exists(self.json_path_):
            with open(self.json_path_, "r") as fp:
                self.json_ = json.load(fp)

            self.initialize_fields()
        else:
            self.json_ = { }
            self.initialize_fields()

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

    def get_module_size(self):
        ms = os.environ.get("BPC_MODULE_SIZE")
        if ms is not None:
            return str(ms)
        else:
            return "<MS: internal error>"

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

    def initialize_fields(self):
        if self.process_name_ not in self.json_:
            self.json_[self.process_name_] = { }

        if self.tool_version_ not in self.json_[self.process_name_]:
            self.json_[self.process_name_] \
                      [self.tool_version_] = { }

        if self.host_arch_ not in self.json_[self.process_name_] \
                                            [self.tool_version_]:
            self.json_[self.process_name_] \
                      [self.tool_version_] \
                      [self.host_arch_]    = { }

        if self.host_platform_ not in self.json_[self.process_name_] \
                                                [self.tool_version_] \
                                                [self.host_arch_]:
            self.json_[self.process_name_]  \
                      [self.tool_version_]  \
                      [self.host_arch_]     \
                      [self.host_platform_] = { }


        if self.host_version_ not in self.json_[self.process_name_]   \
                                               [self.tool_version_]   \
                                               [self.host_arch_]      \
                                               [self.host_platform_]:
            self.json_[self.process_name_]  \
                      [self.tool_version_]  \
                      [self.host_arch_]     \
                      [self.host_platform_] \
                      [self.host_version_]  = { }

        if self.host_cpus_ not in self.json_[self.process_name_]  \
                                            [self.tool_version_]  \
                                            [self.host_arch_]     \
                                            [self.host_platform_] \
                                            [self.host_version_]:
            self.json_[self.process_name_]  \
                      [self.tool_version_]  \
                      [self.host_arch_]     \
                      [self.host_platform_] \
                      [self.host_version_]  \
                      [self.host_cpus_]     = { }

        if self.host_memory_ not in self.json_[self.process_name_]  \
                                              [self.tool_version_]  \
                                              [self.host_arch_]     \
                                              [self.host_platform_] \
                                              [self.host_version_]  \
                                              [self.host_cpus_]:
            self.json_[self.process_name_]  \
                      [self.tool_version_]  \
                      [self.host_arch_]     \
                      [self.host_platform_] \
                      [self.host_version_]  \
                      [self.host_cpus_]     \
                      [self.host_memory_]   = { }

        if self.addl_args_ not in self.json_[self.process_name_]  \
                                            [self.tool_version_]  \
                                            [self.host_arch_]     \
                                            [self.host_platform_] \
                                            [self.host_version_]  \
                                            [self.host_cpus_]     \
                                            [self.host_memory_]:
            self.json_[self.process_name_]  \
                      [self.tool_version_]  \
                      [self.host_arch_]     \
                      [self.host_platform_] \
                      [self.host_version_]  \
                      [self.host_cpus_]     \
                      [self.host_memory_]   \
                      [self.addl_args_]     = { }


        if self.files_per_dir_ not in self.json_[self.process_name_]  \
                                                [self.tool_version_]  \
                                                [self.host_arch_]     \
                                                [self.host_platform_] \
                                                [self.host_version_]  \
                                                [self.host_cpus_]     \
                                                [self.host_memory_]   \
                                                [self.addl_args_]:
            self.json_[self.process_name_]  \
                      [self.tool_version_]  \
                      [self.host_arch_]     \
                      [self.host_platform_] \
                      [self.host_version_]  \
                      [self.host_cpus_]     \
                      [self.host_memory_]   \
                      [self.addl_args_]     \
                      [self.files_per_dir_] = { }

        if self.module_size_ not in self.json_[self.process_name_]  \
                                              [self.tool_version_]  \
                                              [self.host_arch_]     \
                                              [self.host_platform_] \
                                              [self.host_version_]  \
                                              [self.host_cpus_]     \
                                              [self.host_memory_]   \
                                              [self.addl_args_]     \
                                              [self.files_per_dir_]:
            self.json_[self.process_name_]  \
                      [self.tool_version_]  \
                      [self.host_arch_]     \
                      [self.host_platform_] \
                      [self.host_version_]  \
                      [self.host_cpus_]     \
                      [self.host_memory_]   \
                      [self.addl_args_]     \
                      [self.files_per_dir_] \
                      [self.module_size_]   = { }

        if self.n_modules_ not in self.json_[self.process_name_]  \
                                            [self.tool_version_]  \
                                            [self.host_arch_]     \
                                            [self.host_platform_] \
                                            [self.host_version_]  \
                                            [self.host_cpus_]     \
                                            [self.host_memory_]   \
                                            [self.addl_args_]     \
                                            [self.files_per_dir_] \
                                            [self.module_size_]:
            self.json_[self.process_name_]  \
                      [self.tool_version_]  \
                      [self.host_arch_]     \
                      [self.host_platform_] \
                      [self.host_version_]  \
                      [self.host_cpus_]     \
                      [self.host_memory_]   \
                      [self.addl_args_]     \
                      [self.files_per_dir_] \
                      [self.module_size_]   \
                      [self.n_modules_]     = { }

        if self.parallelism_ not in self.json_[self.process_name_]  \
                                              [self.tool_version_]  \
                                              [self.host_arch_]     \
                                              [self.host_platform_] \
                                              [self.host_version_]  \
                                              [self.host_cpus_]     \
                                              [self.host_memory_]   \
                                              [self.addl_args_]     \
                                              [self.files_per_dir_] \
                                              [self.module_size_]   \
                                              [self.n_modules_]:
            self.json_[self.process_name_]  \
                      [self.tool_version_]  \
                      [self.host_arch_]     \
                      [self.host_platform_] \
                      [self.host_version_]  \
                      [self.host_cpus_]     \
                      [self.host_memory_]   \
                      [self.addl_args_]     \
                      [self.files_per_dir_] \
                      [self.module_size_]   \
                      [self.n_modules_]     \
                      [self.parallelism_]   = {
                          "run": [ ]
                      }

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
        self.json_[self.process_name_]       \
                  [self.tool_version_]       \
                  [self.host_arch_]          \
                  [self.host_platform_]      \
                  [self.host_version_]       \
                  [self.host_cpus_]          \
                  [self.host_memory_]        \
                  [self.addl_args_]          \
                  [self.files_per_dir_]      \
                  [self.module_size_]        \
                  [self.n_modules_]          \
                  [self.parallelism_]        \
                  ["run"].append(run)

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
        self.rsz_ = self.rusage_.ru_maxrss * 1024 # Resident size, in bytes.
        self.set_build_disk_space()


    def metrics(self):
        return {
            "bod-size"        : self.disk_space_,
            "kind"            : self.kind_,
            "memory-size-b"   : self.rsz_,
            "seconds"         : self.elapsed_,
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
               self.disk_space_))


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

    parser.add_argument("--metrics",
                        help     = ("Name of JSON file containing "
                                    "build data."),
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

    return options


def scale(n_bytes):
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

def report_runs(m):
    for r in m["run"]:
        print("        %s %s|  kind: %s  secs: %8.3f  mem: %4s  BOD: %s" %
              (r["date"],
               r["time"][0:8],
               r["kind"][0:4],
               r["seconds"],
               scale(r["memory-size-b"]),
               r["bod-size"]))
    print("")

def report_by_test_config(m):
    for aa in m:                                 # Additional arguments.
        for fpd in m[aa]:                        # Files per directory.
            for ms in m[aa][fpd]:                # Module size.
                for nm in m[aa][fpd][ms]:        # Module count.
                    for p in m[aa][fpd][ms][nm]: # Parallelism.
                        print("     Module Count : %s\n"
                              "     Files per dir: %s\n"
                              "     Module Size  : %s\n"
                              "     Parallelism  : %s\n"
                              "     Add'l args   : %s\n" % (nm, fpd, ms, p, aa))
                        report_runs(m[aa][fpd][ms][nm][p])

def report_by_machine_config(m):
    for nc in m:                # Number of CPUs.
        for mb in m[nc]:        # Memory, in bytes.
            print("   CPU count    : %s\n"
                  "   Memory       : %s" % (nc, scale(int(mb))))
            report_by_test_config(m[nc][mb])

def report_by_architecture(ha, m):
    print("  %s" % (ha))
    for hp in m:         # Host platform.
        for hv in m[hp]: # Host version.
            print("   %s\n"
                  "   %s" % (hp, hv))
            report_by_machine_config(m[hp][hv])


def report_by_tool(tn, tv, m):
    print("tool: %s  | version: %s" %
          (tn, tv))

    for ha in m:         # Host architecture.
        report_by_architecture(ha, m[ha])


def report(metrics):
    for tn in metrics:          # Tool Name
        for tv in metrics[tn]:  # Tool Version
            report_by_tool(tn, tv, metrics[tn][tv])
            print("\n")

def main():
    try:
        options = get_options()

        with open(options.arg_metrics, "r") as fp:
            metrics = json.load(fp)

        report(metrics)


    except KeyboardInterrupt as exc:
        print("Ctrl-C interrupt")
        sys.exit(10)

    except Exception as exc:
        print("Unhandled exception '%s'" % (str(exc)))
        raise exc

    return 0

if __name__ == "__main__":
    main()

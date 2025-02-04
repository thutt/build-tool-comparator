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

        if os.path.exists(options.arg_metrics):
            with open(options.arg_metrics, "r") as fp:
                metrics = json.load(fp)

            report(metrics)
        else:
            print("'%s' does not exist." % (options.arg_metrics))
            sys.exit(1)

    except KeyboardInterrupt as exc:
        print("Ctrl-C interrupt")
        sys.exit(10)

    except Exception as exc:
        print("Unhandled exception '%s'" % (str(exc)))
        raise exc

    return 0

if __name__ == "__main__":
    main()

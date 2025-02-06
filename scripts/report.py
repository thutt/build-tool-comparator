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


def same_geometry(l, r):
    return (l["host"]     == r ["host"] and
            l["geometry"] == r ["geometry"])


def print_geometry(m):
    host = m["host"]
    geom = m["geometry"]

    memory = scale(int(host["memory"]))
    print("arch       : %s\n"
          "platform   : %s\n"
          "version    : %s\n"
          "cpus       : %s\n"
          "memory     : %s" % (host["arch"],
                               host["platform"],
                               host["version"],
                               host["cpus"],
                               memory))
    print("files/dir  : %s\n"
          "module size: %s\n"
          "num modules: %s\n"
          "parallelism: %s\n" % (geom["files-per-dir"],
                                 geom["module-size-kb"],
                                 geom["num-modules"],
                                 geom["parallelism"]))


def print_runs(runs):
    for r in runs:
        print("        %s %s|  kind: %s  secs: %8.3f  mem: %4s  BOD: %s" %
              (r["date"],
               r["time"][0:8],
               r["kind"][0:4],
               r["seconds"],
               scale(r["memory-bytes"]),
               r["bod-size"]))
    print("")


def print_element(elem):
    tool = elem["tool"]
    print("  %s  [%s]" % (tool["label"], tool["version"]))
    print("    args: %s" % (tool["args"]))
    print_runs(tool["runs"])


def print_elements(metrics, elements):
    print_geometry(metrics[list(elements)[0]])

    for elem in elements:
        print_element(metrics[elem])

    print("")


def report(metrics):
    for o_idx in range(0, len(metrics)):
        o_data = metrics[o_idx]
        if "processed" not in o_data:
            # This is an unprocessed element in the JSON data.  Gather
            # indices to all elements that were run on the same
            # hardware, and had the same runtime geometry.

            o_data["processed"] = True
            elements = set()
            elements.add(o_idx)

            for i_idx in range(o_idx + 1, len(metrics)):
                i_data = metrics[i_idx]
                if "processed" not in i_data and same_geometry(o_data, i_data):
                    i_data["processed"] = True
                    elements.add(i_idx)

            print_elements(metrics, elements)


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

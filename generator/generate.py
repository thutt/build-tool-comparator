#!/usr/bin/python3 -B
# Copyright (c) 2025  Logic Magicians Software.
# All Rights Reserved.
# Licensed under Gnu GPL V3.

import argparse
import os
import random
import sys

import module
import utility

# Build process creators.
import bash                     # Bash shell script.
import bazel                    # Bazel files.
import rmakefile                # Recursive Makefile.
import scons                    # Scons
import smakefile                # Single Makefile.


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

    parser.add_argument("--files-per-dir",
                        help     = ("Max number of files that can be "
                                    "written to a directory.  If this "
                                    "number is too large, the OS will spend "
                                    "more time searching for files in the "
                                    "filesystem [default: %(default)s files]."),
                        required = False,
                        default  = 100,
                        action   = "store",
                        type     = int,
                        dest     = "arg_n_files_per_dir")

    parser.add_argument("--modules",
                        help     = ("Number of modules that should be "
                                    "created [default: %(default)s modules]."),
                        required = False,
                        default  = 100,
                        action   = "store",
                        type     = int,
                        dest     = "arg_n_modules")

    parser.add_argument("--root",
                        help     = ("Root where source files will be created."),
                        required = True,
                        default  = None,
                        action   = "store",
                        dest     = "arg_root")

    parser.add_argument("--seed",
                        help     = ("Random seed."),
                        required = False,
                        default  = 0x19671116,
                        action   = "store",
                        dest     = "arg_seed")

    parser.add_argument("--verbose",
                        help     = ("Cause build process to not be silent."),
                        required = False,
                        default  = False,
                        action   = "store_true",
                        dest     = "arg_verbose")

    parser.add_argument("arg_tail",
                        help    = "Command tail.",
                        nargs = "*")

    return parser


def get_options():
    parser  = configure_parser()
    options = parser.parse_args()

    options.interface_    = os.path.join(options.arg_root, "interface")
    options.source_       = os.path.join(options.arg_root, "source")
    options.max_imports   = 25
    options.build_systems = [ ]

    return options


def recursive_make(options, modules):
    m = rmakefile.create(options.arg_verbose, options.arg_root,
                         options.arg_n_files_per_dir, modules)
    assert(isinstance(m, rmakefile.RootMakefile))
    return m


def single_make(options, modules):
    m = smakefile.create(options.arg_verbose, options.arg_root,
                         options.arg_n_files_per_dir, modules)
    assert(isinstance(m, smakefile.RootMakefile))
    return m


def bash_script(options, modules):
    m = bash.create(options.arg_verbose, options.arg_root,
                    options.arg_n_files_per_dir, modules)
    assert(isinstance(m, bash.Script))
    return m


def scons_script(options, modules):
    m = scons.create(options.arg_verbose, options.arg_root,
                    options.arg_n_files_per_dir, modules)
    assert(isinstance(m, scons.SConstruct))
    return m


def bazel_script(options, modules):
    m = bazel.create(options.arg_verbose, options.arg_root,
                    options.arg_n_files_per_dir, modules)
    assert(isinstance(m, bazel.Builder))
    return m


def main():
    try:
        options = get_options()
        random.seed(options.arg_seed)

        print("Creating %d source modules, max %d files per directory." %
              (options.arg_n_modules, options.arg_n_files_per_dir))
        modules   = module.create(options.arg_verbose,
                                  options.source_, options.interface_,
                                  options.arg_n_files_per_dir,
                                  options.arg_n_modules, options.max_imports)
        assert(isinstance(modules, list))

        options.build_systems.append(recursive_make(options, modules))
        options.build_systems.append(single_make(options, modules))
        options.build_systems.append(bash_script(options, modules))
        options.build_systems.append(scons_script(options, modules))
        options.build_systems.append(bazel_script(options, modules))

        print("Writing %d source modules." % (options.arg_n_modules))
        for m in modules:
            m.create()

        for bs in options.build_systems:
            print("Writing build system: %s" % (bs.__class__))
            bs.write()

    except KeyboardInterrupt as exc:
        print("Ctrl-C interrupt")
        sys.exit(10)

    except Exception as exc:
        print("Unhandled exception '%s'" % (str(exc)))
        raise exc

    return 0

if __name__ == "__main__":
    main()

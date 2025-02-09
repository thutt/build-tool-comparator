# Copyright (c) 2025 Logic Magicians Software.
# All Rights Reserved.
# Licensed under Gnu GPL V3.
import os
import random

import utility

class Module(object):
    def __init__(self, n):
        self.module_num_    = n
        self.imports_       = []
        self.source_        = None
        self.artifact_      = None
        self.interface_     = None

    def set_file_locations(self, src_dir, incl_dir, dir_num):
        mname        = self.module_name()
        cfname       = "%s.source"    % (mname)
        ofname       = "%s.artifact"  % (mname)
        ifname       = "%s.interface" % (mname)
        self.source_ = os.path.join(src_dir, str(dir_num), cfname)

        self.rela_artifact_dir_ = os.path.join(os.path.basename(src_dir),
                                               str(dir_num))

        # self.artifact_ is relative so build output can be in a
        # different location than sources.
        self.artifact_ = os.path.join(self.rela_artifact_dir_, ofname)
        self.interface_ = os.path.join(incl_dir, str(dir_num), ifname)

    def import_module(self, module):
        assert(isinstance(module, Module))
        if module not in self.imports_:
            # Import iff the randomly selected module is not imported.
            self.imports_.append(module)

    def module_name(self):
        return "m%s" % (self.module_num_)

    def random_interface_length(self):
        minimum_size = 1        # In Kb.
        percent = random.random()

        if percent < 0.60:
            # 60% of results.
            return random_select(minimum_size,  10)
        elif percent < 0.85:
            # 25% of results.
            return random_select(10, 25)
        elif percent < 0.97:
            # 12% of results.
            return random_select(25, 50)
        elif percent < 0.99:
            # 2% of results.
            return random_select(50, 150)
        else:
            # 1% of results.
            return random_select(150, 300)

    def write_public_interface(self):
        utility.mkdir(os.path.dirname(self.interface_))
        mname = self.module_name()
        with open(self.interface_, "w") as fp:
            fp.write("# Module '%s' interface.\n" % (mname))
            length_in_kb = self.random_interface_length()
            # Fill the file with '0' to the randomly selected size.
            fp.write("0" * 1024 * length_in_kb)

    def write_import(self, fp):
        fp.write("import \"%s\"\n" % (os.path.basename(self.interface_)))

    def include_directory(self):
        return os.path.dirname(self.interface_)

    def object_path(self):
        return self.artifact_

    def random_file_length(self):
        minimum_size = 30       # In Kb.
        percent = random.random()

        if percent < 0.60:
            # 60% of results.
            return random_select(minimum_size,  100)
        elif percent < 0.85:
            # 25% of results.
            return random_select(100, 250)
        elif percent < 0.97:
            # 12% of results.
            return random_select(250, 500)
        else:
            # 3% of results.
            return random_select(500, 1024)

    def write_source(self):
        utility.mkdir(os.path.dirname(self.source_))
        with open(self.source_, "w") as fp:
            mname = self.module_name()
            for imp in self.imports_:
                imp.write_import(fp)

            length_in_kb = self.random_file_length()
            # Fill the file with '0' to the randomly selected size.
            fp.write("0" * 1024 * length_in_kb)

    def create(self):
        self.write_public_interface()
        self.write_source()

    def get_make_line(self):
        return "%s: %s" % (self.artifact_, self.source_)


def random_select(lo, hi):
    return random.randint(lo, hi)


def create(verbose, src_dir, incl_dir, n_file_per_dir, n_modules, max_imports):
    modules = [ ]
    for i in range(0, n_modules):
        dir_number = i // n_file_per_dir
        n_imports  = min(max_imports, i - 1)

        if verbose and (i % 1000 == 0):
            print("%d: Creating source module" % (i))
        m = Module(i)
        m.set_file_locations(src_dir, incl_dir, dir_number)
        modules.append(m)
        for j in range(0, n_imports):
            m.import_module(modules[random_select(0, i - 1)])

    return modules


    

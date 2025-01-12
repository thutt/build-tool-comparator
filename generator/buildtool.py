# Copyright (c) 2025 Logic Magicians Software.
# All Rights Reserved.
# Licensed under Gnu GPL V3.

import inspect

import module

class BuildTool(object):
    def _fatal(self, msg):
        raise Exception(msg)

    def _get_function_name(self):
        this_name   = inspect.stack()[0][3]
        caller_name = inspect.stack()[1][3]
        return caller_name

    def __init__(self):
        self.modules_   = [ ]

    def add_module(self, m):
        assert(isinstance(m, module.Module))
        self.modules_.append(m)

    def write(self):
        self._fatal("%s.%s must be implemented" % (type(self),
                                                   self._get_function_name()))

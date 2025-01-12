# Copyright (c) 2025 Logic Magicians Software.
# All Rights Reserved.
# Licensed under Gnu GPL V3.
import os
import sys

def fatal(msg):
    print("fatal: %s" % (msg))
    sys.exit(1)


def mkdir(path):
    if os.path.exists(path):
        if not os.path.isdir(path):
            fatal("'%s' is not a directory" % (path))
    else:
        os.makedirs(path)

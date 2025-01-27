#!/bin/bash
# Copyright (c) 2025  Logic Magicians Software.
# All Rights Reserved.
# Licensed under Gnu GPL V3.
#
#  This script invokes Bazel on the generated recursive Bazel files.
#
set -o pipefail;
set -o nounset;
set -o errexit;

function main ()
{
    local SRC="${BPC_SOURCE:?Use setup.sh to configure environment.}";
    local BOD="${BPC_BOD:?:?Use setup.sh to configure environment.}";

    cd ${SRC};
    exec bazel build //source/...
}

main;

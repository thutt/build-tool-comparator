#!/bin/bash
# Copyright (c) 2025  Logic Magicians Software.
# All Rights Reserved.
# Licensed under Gnu GPL V3.
#
#  This script invokes the Bash script to create all the build artifacts.
#
set -o pipefail;
set -o nounset;
set -o errexit;

function main ()
{
    local SRC="${BPC_SOURCE:?Use setup.sh to configure environment.}";
    local BOD="${BPC_BOD:?:?Use setup.sh to configure environment.}";

    exec ${SRC}/build.sh;
}

main;

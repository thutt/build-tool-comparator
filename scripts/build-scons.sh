#!/bin/bash
# Copyright (c) 2025  Logic Magicians Software.
# All Rights Reserved.
# Licensed under Gnu GPL V3.
#
#  This script invokes Gnu Make on the generated recursive Makefiles.
#
set -o pipefail;
set -o nounset;
set -o errexit;

function main ()
{
    local SRC="${BPC_SOURCE:?Use setup.sh to configure environment.}";
    export BOD="${BPC_BOD:?:?Use setup.sh to configure environment.}";

    cd ${BOD};
    exec scons -Q --file ${SRC}/SConstruct -j ${BPC_PARALLEL} all
}

main;

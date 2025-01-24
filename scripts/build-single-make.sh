#!/bin/bash
# Copyright (c) 2025  Logic Magicians Software.
# All Rights Reserved.
# Licensed under Gnu GPL V3.
#
#  This script invokes Gnu Make on the generated single Makefile.
#
set -o pipefail;
set -o nounset;
set -o errexit;

function main ()
{
    local SRC="${BPC_SOURCE:?Use setup.sh to configure environment.}";
    local BOD="${BPC_BOD:?:?Use setup.sh to configure environment.}";
    local PARALLEL="${BPC_PARALLEL:?:?Use setup.sh to configure environment.}";
    local SILENT="--silent --no-print-directory";
    local VERBOSE=" ";          # False, for Gnu Make.

    if [ ! -z "${BPC_VERBOSE:-}" ]; then
        # When BPC_VERBOSE is set, SILENT is disabled & VERBOSE enabled.
        SILENT="";
        VERBOSE="t";            # True, for Gnu Make
    fi;

    exec make BOD=${BOD}                        \
         ${SILENT}                              \
         ${MAKE_ADDITIONAL_OPTIONS}             \
         -C ${BOD}                              \
         -j ${PARALLEL}                         \
         -f ${SRC}/Makefile.single              \
         VPATH=${SRC}                           \
         VERBOSE="${VERBOSE}";
}

main;

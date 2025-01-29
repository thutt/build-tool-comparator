#!/bin/bash
# Copyright (c) 2025  Logic Magicians Software.
# All Rights Reserved.
# Licensed under Gnu GPL V3.
#
#  This script generates all the source modules and build systems.
#
set -o pipefail;
set -o nounset;
set -o errexit;

SCRIPT="${BASH_SOURCE[0]}"
SRC_DIR=$(dirname "${SCRIPT}");

function main ()
{
    local n_modules="${BPC_MODULES:?Use setup.sh to configure environment.}";
    local module_size="${BPC_MODULE_SIZE:?Use setup.sh to configure environment.}";
    local SRC="${BPC_SOURCE:?Use setup.sh to configure environment.}";
    local BOD="${BPC_BOD:?:?Use setup.sh to configure environment.}";
    local PARALLEL="${BPC_PARALLEL:?:?Use setup.sh to configure environment.}";
    local FILES_PER_DIR="${BPC_FILES_PER_DIR:-100}"
    local VERBOSE="";

    if [ ! -z "${BPC_VERBOSE:-}" ]; then
        VERBOSE="--verbose";
    fi;

    echo "Removing source & build output (BOD).";
    rm -rf ${SRC} ${BOD};

    if [ -d ~/.cache/bazel ] ; then
        echo "Removing ~/.cache/bazel";
        local fmt_date=$(date +"%Y-%m-%d-%H-%M-%S")
        local cache_name=~/.cache/bazel.${fmt_date};
        mv ~/.cache/bazel ${cache_name};
        rm -rf ${cache_name} &
    fi;

    echo "Creating BOD.";
    mkdir --parents ${BOD};

    ${SRC_DIR}/../generator/generate.py         \
        --files-per-dir ${FILES_PER_DIR}        \
        --modules ${n_modules}                  \
        --module-size ${module_size}            \
        --root ${SRC}                           \
        ${VERBOSE};
}

main;

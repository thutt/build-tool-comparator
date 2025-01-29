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

SCRIPT="${BASH_SOURCE[0]}"
SRC_DIR=$(dirname "${SCRIPT}");


function build_all ()
{
    local nf="${1}";
    local SRC="${BPC_SOURCE:?Use setup.sh to configure environment.}";
    local BOD="${BPC_BOD:?:?Use setup.sh to configure environment.}";
    local RUN="${SRC_DIR}/run_build.py";
    local METRICS="$(readlink -f ${SRC_DIR}/../metrics/metrics.json)";

    export BPC_MODULES=${nf};

    echo -e "\n\n"
    echo "## ${BPC_MODULES} simulated modules.";
    echo -e "\n"
    echo "BOD          : ${BPC_BOD}";
    echo "Files Per Dir: ${BPC_FILES_PER_DIR}";
    echo "Modules      : ${BPC_MODULES}";
    echo "Parallel     : ${BPC_PARALLEL}";
    echo "Source       : ${BPC_SOURCE}";

    (
        echo -e "\nBash";
        ${RUN} --metrics "${METRICS}" --tool bash --name bash --kind full;
        ${SRC_DIR}/modify-most-used-interface.sh >/dev/null;
        ${RUN} --metrics "${METRICS}" --tool bash --name bash --kind incremental;
        ${RUN} --metrics "${METRICS}" --tool bash --name bash --kind NULL;
    );

    (
        echo -e "\nBazel";
        ${RUN} --metrics "${METRICS}" --tool bazel --name bazel --kind full;
        ${SRC_DIR}/modify-most-used-interface.sh >/dev/null;
        ${RUN} --metrics "${METRICS}" --tool bazel --name bazel --kind incremental;
        ${RUN} --metrics "${METRICS}" --tool bazel --name bazel --kind NULL;
    );

    (
        export BPC_BUILD_ADDITIONAL_ARGS="";

        echo -e "\nRecursive Make";
        ${RUN} --metrics "${METRICS}" --tool make --name recursive-make --kind full;
        ${SRC_DIR}/modify-most-used-interface.sh >/dev/null;
        ${RUN} --metrics "${METRICS}" --tool make --name recursive-make --kind incremental;
        ${RUN} --metrics "${METRICS}" --tool make --name recursive-make --kind NULL;
    );

    (
        export BPC_BUILD_ADDITIONAL_ARGS="--no-builtin-rules --no-builtin-variables"

        echo -e "\nRecursive Make + ${BPC_BUILD_ADDITIONAL_ARGS}";
        ${RUN} --metrics "${METRICS}" --tool make --name recursive-make --kind full;
        ${SRC_DIR}/modify-most-used-interface.sh >/dev/null;
        ${RUN} --metrics "${METRICS}" --tool make --name recursive-make --kind incremental;
        ${RUN} --metrics "${METRICS}" --tool make --name recursive-make --kind NULL;
    );

    (
        echo -e "\nScons: md5sum";
        ${RUN} --metrics "${METRICS}" --tool scons --name scons --kind full;
        ${SRC_DIR}/modify-most-used-interface.sh >/dev/null;
        ${RUN} --metrics "${METRICS}" --tool scons --name scons --kind incremental;
        ${RUN} --metrics "${METRICS}" --tool scons --name scons --kind NULL;
    );

    (
        echo -e "\nScons: make";
        export SCONS_MAKE=1;
        ${RUN} --metrics "${METRICS}" --tool scons --name scons --kind full;
        ${SRC_DIR}/modify-most-used-interface.sh >/dev/null;
        ${RUN} --metrics "${METRICS}" --tool scons --name scons --kind incremental;
        ${RUN} --metrics "${METRICS}" --tool scons --name scons --kind NULL;
    );

    (
        export BPC_BUILD_ADDITIONAL_ARGS="";
        echo -e "\nSingle Make";
        ${RUN} --metrics "${METRICS}" --tool make --name single-make --kind full;
        ${SRC_DIR}/modify-most-used-interface.sh >/dev/null;
        ${RUN} --metrics "${METRICS}" --tool make --name single-make --kind incremental;
        ${RUN} --metrics "${METRICS}" --tool make --name single-make --kind NULL;
    );

    (
        export BPC_BUILD_ADDITIONAL_ARGS="--no-builtin-rules --no-builtin-variables"

        echo -e "\nSingle Make + ${BPC_BUILD_ADDITIONAL_ARGS}";
        ${RUN} --metrics "${METRICS}" --tool make --name single-make --kind full;
        ${SRC_DIR}/modify-most-used-interface.sh >/dev/null;
        ${RUN} --metrics "${METRICS}" --tool make --name single-make --kind incremental;
        ${RUN} --metrics "${METRICS}" --tool make --name single-make --kind NULL;
    );
}


function check_bazel_cache ()
{
    local cache=~/.cache/bazel;

    if [ -d "${cache}" ] ; then
        cat <<EOF

To ensure a consistent runtime is measured without skewing results via
build tool caching, the tools used by this build comparison system
will delete:


  ${cache}


If you are a Bazel user and do not want this directory to be deleted,
you must rename or move it.  Otherwise, simply delete the entire
directory and re-run this script.

When this tool is finished, the directory will have been removed; you
can restore it from the one you saved.


EOF
        exit 1;
    fi;
}

function main ()
{
    local nf;                   # Number of files.

    check_bazel_cache;

    for nf in 50 100 1000 5000 10000 50000 100000; do
        build_all "${nf}";
    done;
}


main "${@}";

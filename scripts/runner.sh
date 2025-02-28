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

ALL_TOOLS="bash bazel make ninja scons"; # All tools to test.


function run_bash ()
{
    (
        echo -e "\nBash";
        ${RUN} --metrics "${METRICS}" --tool bash --name bash --kind full;
        ${SRC_DIR}/modify-most-used-interface.sh >/dev/null;
        ${RUN} --metrics "${METRICS}" --tool bash --name bash --kind incremental;
        ${RUN} --metrics "${METRICS}" --tool bash --name bash --kind NULL;
    );
}


function run_ninja ()
{
    (
        echo -e "\nNinja";
        ${RUN} --metrics "${METRICS}" --tool ninja --name ninja --kind full;
        ${SRC_DIR}/modify-most-used-interface.sh >/dev/null;
        ${RUN} --metrics "${METRICS}" --tool ninja --name ninja --kind incremental;
        ${RUN} --metrics "${METRICS}" --tool ninja --name ninja --kind NULL;
    );
}


function run_bazel ()
{
    (
        echo -e "\nBazel";
        ${RUN} --metrics "${METRICS}" --tool bazel --name bazel --kind full;
        ${SRC_DIR}/modify-most-used-interface.sh >/dev/null;
        ${RUN} --metrics "${METRICS}" --tool bazel --name bazel --kind incremental;
        ${RUN} --metrics "${METRICS}" --tool bazel --name bazel --kind NULL;
    );
}


function run_recursive_make ()
{
    (
        export BPC_BUILD_ADDITIONAL_ARGS="";

        echo -e "\nRecursive Make";
        ${RUN} --metrics "${METRICS}" --tool make --name recursive-make --tool-label recursive-make --kind full;
        ${SRC_DIR}/modify-most-used-interface.sh >/dev/null;
        ${RUN} --metrics "${METRICS}" --tool make --name recursive-make --tool-label recursive-make --kind incremental;
        ${RUN} --metrics "${METRICS}" --tool make --name recursive-make --tool-label recursive-make --kind NULL;
    );

    (
        export BPC_BUILD_ADDITIONAL_ARGS="--no-builtin-rules --no-builtin-variables"

        echo -e "\nRecursive Make + ${BPC_BUILD_ADDITIONAL_ARGS}";
        ${RUN} --metrics "${METRICS}" --tool make --name recursive-make --tool-label recursive-make --kind full;
        ${SRC_DIR}/modify-most-used-interface.sh >/dev/null;
        ${RUN} --metrics "${METRICS}" --tool make --name recursive-make --tool-label recursive-make --kind incremental;
        ${RUN} --metrics "${METRICS}" --tool make --name recursive-make --tool-label recursive-make --kind NULL;
    );
}


function run_single_make ()
{
    (
        export BPC_BUILD_ADDITIONAL_ARGS="";
        echo -e "\nSingle Make";
        ${RUN} --metrics "${METRICS}" --tool make --name single-make --tool-label single-make --kind full;
        ${SRC_DIR}/modify-most-used-interface.sh >/dev/null;
        ${RUN} --metrics "${METRICS}" --tool make --name single-make --tool-label single-make --kind incremental;
        ${RUN} --metrics "${METRICS}" --tool make --name single-make --tool-label single-make --kind NULL;
    );

    (
        export BPC_BUILD_ADDITIONAL_ARGS="--no-builtin-rules --no-builtin-variables"

        echo -e "\nSingle Make + ${BPC_BUILD_ADDITIONAL_ARGS}";
        ${RUN} --metrics "${METRICS}" --tool make --name single-make --tool-label single-make --kind full;
        ${SRC_DIR}/modify-most-used-interface.sh >/dev/null;
        ${RUN} --metrics "${METRICS}" --tool make --name single-make --tool-label single-make --kind incremental;
        ${RUN} --metrics "${METRICS}" --tool make --name single-make --tool-label single-make --kind NULL;
    );
}


function run_md5sum_scons ()
{
    (
        echo -e "\nScons: md5sum";
        ${RUN} --metrics "${METRICS}" --tool scons --name scons --tool-label scons-md5sum --kind full;
        ${SRC_DIR}/modify-most-used-interface.sh >/dev/null;
        ${RUN} --metrics "${METRICS}" --tool scons --name scons --tool-label scons-md5sum --kind incremental;
        ${RUN} --metrics "${METRICS}" --tool scons --name scons --tool-label scons-md5sum --kind NULL;
    );
}

function run_make_scons ()
{
    (
        echo -e "\nScons: make";
        export SCONS_MAKE=1;
        ${RUN} --metrics "${METRICS}" --tool scons --name scons --tool-label scons-make --kind full;
        ${SRC_DIR}/modify-most-used-interface.sh >/dev/null;
        ${RUN} --metrics "${METRICS}" --tool scons --name scons --tool-label scons-make --kind incremental;
        ${RUN} --metrics "${METRICS}" --tool scons --name scons --tool-label scons-make --kind NULL;
    );
}


function enabled ()
{
    local tool="${1}";

    if [[ ${TOOLS_TO_MEASURE} == *${tool}* ]] ; then
        # ${tool} enabled.
        if [ $(which "${tool}") ] ; then
            return 0;           # Tool found on path.
        fi;
        return 1;               # Tool not found in path.
    else
        # ${tool} not enabled.
        return 1;
    fi;
}


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

    if enabled "bash"; then
        run_bash;
    else
        echo -e "\nBash not enabled or not found; testing skipped.\n"
    fi;

    if enabled "ninja"; then
        run_ninja;
    else
        echo -e "\nNinja not enabled or not found; testing skipped.\n"
    fi;

    if enabled "bazel"; then
        run_bazel;
    else
        echo -e "\nBazel not enabled or not found; testing skipped.\n"
    fi;

    if enabled "make"; then
        run_recursive_make;
        run_single_make;
    else
        echo -e "\nMake not enabled or not found; testing skipped.\n"
    fi;

    if enabled "scons"; then
        run_md5sum_scons;
        run_make_scons;
    else
        echo -e "\nScons not enabled or not found; testing skipped.\n"
    fi;
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

function process_args ()
{
    TOOLS_TO_MEASURE="";

    while true ; do
        case "${1}" in
            -h)
                cat <<EOF
This program runs measurements for one or more build tools.

  --all   : Measure all tools.
  --bash  : Measure runs with Bash.
  --bazel : Measure runs using Bazel.
  --make  : Measure runs with Gnu Make.
  --ninja : Measure runs with Ninja.
  --scons : Measure runs with Scons.
  -h      : The help message.

  If no argument is supplied, '--all' is used.
EOF
                exit 0;
                ;;

            --all)
                export TOOLS_TO_MEASURE="${ALL_TOOLS}";
                shift 1;
                ;;

            --bash)
                export TOOLS_TO_MEASURE="bash ${TOOLS_TO_MEASURE}"
                shift 1;
                ;;

            --bazel)
                export TOOLS_TO_MEASURE="bazel ${TOOLS_TO_MEASURE}"
                shift 1;
                ;;

            --make)
                export TOOLS_TO_MEASURE="make ${TOOLS_TO_MEASURE}"
                shift 1;
                ;;

            --ninja)
                export TOOLS_TO_MEASURE="ninja ${TOOLS_TO_MEASURE}"
                shift 1;
                ;;

            --scons)
                export TOOLS_TO_MEASURE="scons ${TOOLS_TO_MEASURE}"
                shift 1;
                ;;

            --)                 # End of arguments
                shift;
                break;
                ;;

            *)
                echo "Unknown option '${1}'";
                return 1;
                ;;
        esac
    done

    if [ -z "${TOOLS_TO_MEASURE}" ] ; then
        TOOLS_TO_MEASURE="${ALL_TOOLS}";
    fi;

    return 0;
}


function main ()
{
    local nf;                   # Number of files.

    if process_args ${@} ; then
        check_bazel_cache;

        for nf in 50 100 1000 5000 10000 50000 100000; do
            build_all "${nf}";
        done;

        echo "Removing '${BPC_SOURCE}'"
        if ! rm -rf "${BPC_SOURCE}"; then
            echo "Failed to fully remove '${BPC_SOURCE}'";
        fi;

        echo "Removing '${BPC_BOD}'"
        if ! rm -rf "${BPC_BOD}"; then
            echo "Failed to fully remove '${BPC_BOD}'";
        fi;
    fi;
}

args=$(/usr/bin/getopt -o h --longoptions help,all,bash,bazel,make,ninja,scons -- "${@}")
set -- "${args}"            # Set postional args to ${args}.
unset args;

main ${@};

main "${@}";

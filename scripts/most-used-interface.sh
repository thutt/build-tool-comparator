#!/bin/bash
# Copyright (c) 2025  Logic Magicians Software.
# All Rights Reserved.
# Licensed under Gnu GPL V3.
set -o pipefail;
set -o nounset;
set -o errexit;

function main ()
{
    local SRC="${BPC_SOURCE:?Use setup.sh to configure environment.}";

    grep -h -r "import" ${SRC}/|sort|uniq -c|sort --numeric --reverse|head -10
}

main;

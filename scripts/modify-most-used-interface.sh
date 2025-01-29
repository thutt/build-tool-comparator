#!/bin/bash
# Copyright (c) 2025  Logic Magicians Software.
# All Rights Reserved.
# Licensed under Gnu GPL V3.
set -o nounset;
set -o errexit;

function main ()
{
    local SRC="${BPC_SOURCE:?Use setup.sh to configure environment.}";
    local mu;

    mu=$(grep -h -r "import" ${SRC}/|sort|uniq -c|sort --numeric --reverse|head -1|cut -d '"' -f 2);
    path=$(find ${SRC} -name "${mu}");
    echo "Modifying '${path}' using current timestamp.";
    date >"${path}";
}

main;

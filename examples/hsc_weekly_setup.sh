#!/usr/bin/env bash

EXAMPLES="$(dirname -- "$(readlink -f -- "$0";)";)"

source $EXAMPLES/examples/common_setup.sh

config="hsc_single_coll.yaml"
config_name="hsc_test_single_coll"
p_name="HSC"
lsst_version="w_2022_48"
c_name="${lsst_version}_test0"
fullname="${p_name}/${c_name}"

export CM_CONFIGS="src/lsst/cm/prod/configs/HSC/test"

#!/usr/bin/env bash

EXAMPLES="$(dirname -- "$(readlink -f -- "$0";)";)"

source $EXAMPLES/examples/common_setup.sh

config="hsc_weekly.yaml"
config_name="hsc_weekly"
p_name="HSC"
lsst_version="w_2023_08"
c_name="${lsst_version}_test0"
fullname="${p_name}/${c_name}"
db_path="output/cm_${p_name}.db"

export CM_CONFIGS="src/lsst/cm/prod/configs/HSC/test"
export CM_DB="sqlite:///${db_path}"

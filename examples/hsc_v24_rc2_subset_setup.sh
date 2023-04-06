#!/usr/bin/env bash

EXAMPLES="$(dirname -- "$(readlink -f -- "$0";)";)"

source $EXAMPLES/examples/common_setup.sh

config="hsc_rc2_subset.yaml"
config_name="hsc_rc2_subset"
p_name="HSC_rc2_subset"
lsst_version="v24.1.0.rc1"
c_name="${lsst_version}_rcTest1"
fullname="${p_name}/${c_name}"
db_path="output/cm_${p_name}.db"

export CM_CONFIGS="src/lsst/cm/prod/configs/HSC/test"
export CM_DB="sqlite:///${db_path}"

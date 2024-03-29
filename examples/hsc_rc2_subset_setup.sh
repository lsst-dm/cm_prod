#!/usr/bin/env bash

EXAMPLES=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

source $EXAMPLES/common_setup.sh

config="hsc_rc2_subset.yaml"
config_name="hsc_rc2_subset"
p_name="HSC_rc2_subset"
lsst_version="w_2023_08"
c_name="${lsst_version}_test0"
fullname="${p_name}/${c_name}"
db_path="output/cm_${p_name}.db"

export CM_CONFIGS="src/lsst/cm/prod/configs/HSC/test"
export CM_DB="sqlite:///${db_path}"

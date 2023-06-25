#!/usr/bin/env bash

EXAMPLES=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

source $EXAMPLES/common_setup.sh
ticket="DM-39132"
config="pdr2.yaml"
config_name="pdr2"
p_name="PDR2"
lsst_version="v24.1.0.rc3"
c_name="v24.1.0_${ticket}"
fullname="${p_name}/${c_name}"
db_path="output/cm_${p_name}.db"

export CM_CONFIGS="src/lsst/cm/prod/configs/PDR2"
export CM_DB="sqlite:///${db_path}"

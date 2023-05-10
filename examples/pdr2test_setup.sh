#!/usr/bin/env bash

EXAMPLES=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

source $EXAMPLES/common_setup.sh
ticket="DM-38928"
config="pdr2_test.yaml"
config_name="pdr2_test"
p_name="PDR2"
lsst_version="v24.1.0.rc2"
c_name="${lsst_version}_${ticket}_cl"
fullname="${p_name}/${c_name}"
db_path="output/cm_${p_name}.db"

export CM_CONFIGS="src/lsst/cm/prod/configs/PDR2/test"
export CM_DB="sqlite:///${db_path}"

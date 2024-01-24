#!/usr/bin/env bash

EXAMPLES=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

source $EXAMPLES/common_setup.sh
ticket_num="DM-42607"
config="pdr2.yaml"
config_name="pdr2"
lsst_version="w_2024_03"
p_name="${lsst_version}"
c_name="${ticket_num}"
fullname="${p_name}/${c_name}"
db_path="output/cm_${p_name}_${c_name}.db"

export CM_CONFIGS="src/lsst/cm/prod/configs/PDR2"
export CM_DB="sqlite:///${db_path}"

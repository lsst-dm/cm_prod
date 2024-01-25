#!/usr/bin/env bash

EXAMPLES=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

source $EXAMPLES/common_setup.sh

config="dc2_test-med-1.yaml"
config_name="dc2"
p_name="dc2-test-med-1"
lsst_version="w_2024_04"
ticket_num="DM-42670"
p_name="${lsst_version}"
c_name="${ticket_num}"
fullname="${p_name}/${c_name}"
db_path="output/cm_${p_name}_${c_name}.db"

export CM_CONFIGS="src/lsst/cm/prod/configs/DC2/test"
export CM_DB="sqlite:///${db_path}"

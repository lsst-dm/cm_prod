#!/usr/bin/env bash

EXAMPLES=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

source $EXAMPLES/common_setup.sh

config="dc2_test-med-1.yaml"
config_name="dc2"
lsst_version="d_2023_07_21"
ticket_num="DM-40157"
p_name="${ticket_num}"
c_name="${lsst_version}"
fullname="${p_name}/${c_name}"
db_path="output/${p_name}_${c_name}.db"

export CM_CONFIGS="src/lsst/cm/prod/configs/DC2/test"
export CM_DB="sqlite:///${db_path}"

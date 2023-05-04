#!/usr/bin/env bash

EXAMPLES=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

butler_repo="/sdf/group/rubin/repo/dc2"
source $EXAMPLES/common_setup.sh

config="dc2_test-med-1.yaml"
config_name="dc2"
p_name="dc2-test-med-1"
lsst_version="w_2023_13"
c_name="${lsst_version}_test1"
fullname="${p_name}/${c_name}"
db_path="output/cm_${p_name}_${c_name}.db"

export CM_CONFIGS="src/lsst/cm/prod/configs/DC2/test"
export CM_DB="sqlite:///${db_path}"

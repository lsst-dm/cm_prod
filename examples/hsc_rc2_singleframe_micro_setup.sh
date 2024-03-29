#!/usr/bin/env bash

EXAMPLES=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

source $EXAMPLES/common_setup.sh

config="rc2_singleframe_micro.yaml"
config_name="rc2_singleframe_micro"
p_name="RC2_singleframe_micro"
lsst_version="w_2023_15"
c_name="${lsst_version}_test0"
fullname="${p_name}/${c_name}"
db_path="output/cm_${p_name}.db"

export CM_CONFIGS="src/lsst/cm/prod/configs/HSC/test"
export CM_DB="sqlite:///${db_path}"

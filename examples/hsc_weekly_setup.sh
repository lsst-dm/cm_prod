#!/usr/bin/env bash

EXAMPLES=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

source $EXAMPLES/common_setup.sh

config="hsc_weekly.yaml"
config_name="hsc_weekly"
lsst_version="w_2024_06"
p_name="${lsst_version}"
ticket_num="DM-42797"
c_name="${ticket_num}"
fullname="${p_name}/${c_name}"
db_path="output/cm_${p_name}_${c_name}.db"

export CM_CONFIGS="src/lsst/cm/prod/configs/HSC/test"
export CM_DB="sqlite:///${db_path}"

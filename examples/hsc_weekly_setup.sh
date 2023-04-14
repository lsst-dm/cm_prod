#!/usr/bin/env bash

EXAMPLES="$(dirname -- "$(readlink -f -- "$0";)";)"

source $EXAMPLES/examples/common_setup.sh

config="hsc_weekly.yaml"
config_name="hsc_weekly"
lsst_version="w_2023_15"
ticket_num="DM-38691"
p_name="${lsst_version}"
c_name="${ticket_num}"
fullname="${p_name}/${c_name}"
db_path="output/cm_${p_name}.db"

export CM_CONFIGS="src/lsst/cm/prod/configs/HSC/test"
export CM_DB="sqlite:///${db_path}"

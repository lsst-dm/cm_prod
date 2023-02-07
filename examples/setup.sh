#!/usr/bin/env bash

EXAMPLES="$(dirname -- "$(readlink -f -- "$0";)";)"

db_path="output/cm.db"
config="hsc_single_coll.yaml"
p_name="HSC"
lsst_version="w_2022_48"
c_name="${lsst_version}_test0"
fullname="${p_name}/${c_name}"
butler_repo="/sdf/group/rubin/repo/main"
root_coll="u/${USER}/cm"

export CM_PROD_DIR="${EXAMPLES}"
export CM_DB="sqlite:///${db_path}"
export CM_PROD_URL="output/archive"
export CM_CONFIGS="src/lsst/cm/prod/configs/HSC/test"
export CM_SCRIPT_METHOD="slurm"
export CM_BUTLER="${butler_repo}"

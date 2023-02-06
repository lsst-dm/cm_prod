#!/usr/bin/env bash

EXAMPLES="$(dirname -- "$(readlink -f -- "$0";)";)"

db_path="output/cm_single_coll_02.db"
config="hsc_single_coll.yaml"
p_name="HSC"
c_name="test_single_coll_v02"
fullname="${p_name}/${c_name}"
butler_repo="/sdf/group/rubin/repo/main_20220411"

export CM_PROD_DIR="${EXAMPLES}"
export CM_DB="sqlite:///${db_path}"
export CM_PROD_URL="output/archive_02"
export CM_CONFIGS="src/lsst/cm/prod/configs/HSC/test"
export CM_SCRIPT_METHOD="slurm"
export CM_BUTLER="${butler_repo}"

\rm -rf $CM_PROD_URL/$fullname $db_path
mkdir -p output

cm create
cm parse --config-name hsc_test_single_coll --config-yaml ${config}
cm insert --production-name ${p_name}
cm insert --production-name ${p_name} --campaign-name ${c_name} --butler-repo ${butler_repo} --config-name hsc_test_single_coll --config-block campaign
cm daemon --fullname ${fullname} --max-running 0

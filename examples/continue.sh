#!/usr/bin/env bash

EXAMPLES="$(dirname -- "$(readlink -f -- "$0";)";)"

db_path="output/cm.db"
config="hsc_config.yaml"
p_name="HSC"
# Update this line to make a new campaign"
c_name="test4"
butler_repo="/sdf/group/rubin/repo/main_20220411"

export CM_PROD_DIR="${EXAMPLES}"
export CM_DB="sqlite:///${db_path}"
export CM_PROD_URL="output/archive"
export CM_CONFIGS="src/lsst/cm/prod/configs/HSC/test"
export CM_SCRIPT_METHOD="slurm"
export CM_BUTLER="${butler_repo}"


#cm parse --config-name hsc_test --config-yaml ${config}
#cm insert --production-name ${p_name}
cm insert --production-name ${p_name} --campaign-name ${c_name} --butler-repo ${butler_repo} --config-name hsc_test --config-block campaign
cm daemon --fullname ${p_name}/${c_name} --max-running 0

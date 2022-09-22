#!/usr/bin/env bash

EXAMPLES="$(dirname -- "$(readlink -f -- "$0";)";)"

db_path="output/cm.db"
config="hsc_config.yaml"
p_name="HSC"
c_name="test"
butler_repo="/sdf/group/rubin/repo/main"

export CM_DB="sqlite:///${db_path}"
export CM_PROD_URL="output/archive"
export CM_CONFIGS="$EXAMPLES/../src/lsst/cm/prod/configs/HSC/test"
export CM_SCRIPT_METHOD="slurm"

\rm -rf $CM_PROD_URL $db_path
mkdir -p output

cm create
cm parse --config-name hsc_test --config-yaml ${config}
cm insert --production-name ${p_name}
cm insert --production-name ${p_name} --campaign-name ${c_name} --butler-repo ${butler_repo} --config-name hsc_test --config-block campaign
cm daemon --fullname HSC/test --max-running 0

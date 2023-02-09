#!/usr/bin/env bash

EXAMPLES="$(dirname -- "$(readlink -f -- "$0";)";)"

db_path="output/cm_001.db"
config="hsc_single_coll.yaml"
p_name="HSC"
c_name="test"
butler_repo="/sdf/group/rubin/repo/main_20220411"

export CM_PROD_DIR="${EXAMPLES}"
export CM_DB="sqlite:///${db_path}"
export CM_PROD_URL="output/archive_001"
export CM_CONFIGS="src/lsst/cm/prod/configs/HSC/test"
export CM_SCRIPT_METHOD="fake_run"
export CM_BUTLER="${butler_repo}"

\rm -rf $CM_PROD_URL $db_path
mkdir -p output

cm create
cm parse --config-name hsc_test --config-yaml ${config}
cm insert --production-name ${p_name}
cm insert --production-name ${p_name} --campaign-name ${c_name} --butler-repo ${butler_repo} --config-name hsc_test --config-block campaign

#cm daemon --fullname HSC/test --max-running 0
cm queue --fullname ${p_name}/${c_name}
cm launch --fullname ${p_name}/${c_name}
cm fake-run --fullname ${p_name}/${c_name}
cm check --fullname ${p_name}/${c_name}
cm queue --fullname ${p_name}/${c_name}
#cm launch --fullname ${p_name}/${c_name}
cm print-table --table job

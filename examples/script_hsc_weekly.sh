#!/usr/bin/env bash

EXAMPLES="$(dirname -- "$(readlink -f -- "$0";)";)"

source $EXAMPLES/examples/hsc_weekly_setup.sh

\rm -rf $CM_PROD_URL/$fullname $db_path
mkdir -p output

cm create
cm parse --config-name ${config_name} --config-yaml ${config}
cm load-error-types --config-yaml examples/error_code_decisions.yaml
cm insert --production-name ${p_name}
cm insert --production-name ${p_name} --campaign-name ${c_name} --butler-repo ${butler_repo} --config-name ${config_name} --config-block campaign --lsst-version ${lsst_version} --root-coll ${root_coll}
cm daemon --fullname ${fullname} --max-running 0

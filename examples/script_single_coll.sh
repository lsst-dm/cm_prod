#!/usr/bin/env bash

EXAMPLES="$(dirname -- "$(readlink -f -- "$0";)";)"

source $EXAMPLES/examples/setup.sh

\rm -rf $CM_PROD_URL/$fullname $db_path
mkdir -p output

cm create
cm parse --config-name hsc_test_single_coll --config-yaml ${config}
cm insert --production-name ${p_name}
cm insert --production-name ${p_name} --campaign-name ${c_name} --butler-repo ${butler_repo} --config-name hsc_test_single_coll --config-block campaign --lsst-version ${lsst_version} --root-coll ${root_coll}
cm daemon --fullname ${fullname} --max-running 0

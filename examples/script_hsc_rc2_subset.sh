#!/usr/bin/env bash

EXAMPLES="$(dirname -- "$(readlink -f -- "$0";)";)"

source $EXAMPLES/examples/hsc_rc2_subset_setup.sh

read -p "This script will blow away the cm database and start a fresh one based on your setup file. Are you sure you want to do this? (y/N)" $ANSWER
if [[$ANSWER!='y']] && [[$ANSWER!='yes']] && [[$ANSWER!='Y']] && [[$ANSWER!='Yes']] && [[$ANSWER!='YES']]; then
    echo "The environment variables for your production were already sourced. You may proceed to your usual cm business without panic."
    exit 1
fi

\rm -rf $CM_PROD_URL/$fullname $db_path
mkdir -p output

cm create
cm parse --config-name ${config_name} --config-yaml ${config}
cm insert --production-name ${p_name}
cm insert --production-name ${p_name} --campaign-name ${c_name} --butler-repo ${butler_repo} --config-name ${config_name} --config-block campaign --lsst-version ${lsst_version} --root-coll ${root_coll}
cm daemon --fullname ${fullname} --max-running 0

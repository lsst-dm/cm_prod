#!/usr/bin/env bash

EXAMPLES=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Prompt for config/setup files
# Each new setup will need its own elif here

valid_config=false
daemon_options="--max-running 0"
read -p "Which config would you like to use? (HSC-RC2, rc2_subset, DC2_test-med-1, micro) " CONFIG
while [ $valid_config = false ]; do
    if [ $CONFIG = 'HSC-RC2' ]
    then
	    source $EXAMPLES/hsc_weekly_setup.sh
      butler_repo='/sdf/group/rubin/repo/main'
      valid_config=true
    elif [ $CONFIG = 'rc2_subset' ]
    then
        source $EXAMPLES/hsc_rc2_subset_setup.sh
        butler_repo='/sdf/group/rubin/repo/main'
        valid_config=true
    elif [ $CONFIG = 'DC2_test-med-1' ]
    then
        source $EXAMPLES/dc2_test-med-1_setup.sh
        butler_repo="/sdf/group/rubin/repo/dc2"
        valid_config=true
        daemon_options="--max-running 10 --sleep-time 300"
    elif [ $CONFIG = 'micro' ]
    then
        source $EXAMPLES/hsc_rc2_singleframe_micro_setup.sh
        valid_config=true
        daemon_options="--max-running 10 --sleep-time 30"
    else
        read -p "That config was not valid. Please enter a valid config " CONFIG
    fi
done

default=no
read -p "This script will blow away the cm database and start a fresh one based on your setup file. Are you sure you want to do this? (y/N)" ANSWER
ANSWER=${ANSWER:-$default}

yeses="y Y yes Yes YES yEs yES yeS YeS YEs"
blow_away=false
for yes in $yeses; do
    if [ $yes = $ANSWER ]
    then
	    blow_away=true
	    break
    else
	    continue
    fi
done

echo "Your environment variables have already been set up."
if $blow_away
then
    echo "Enjoy your fresh cm database!"
    \rm -rf $CM_PROD_URL/$fullname $db_path
    \rm -rf submit/${root_coll}/${fullname}
    butler remove-collections --confirm ${butler_repo} "${root_coll}/${fullname}*"

    mkdir -p output

    cm create
    cm parse --config-name ${config_name} --config-yaml ${config}
    cm load-error-types --config-yaml examples/error_code_decisions.yaml
    cm insert --production-name ${p_name}
    cm insert --production-name ${p_name} --campaign-name ${c_name} --butler-repo ${butler_repo} --config-name ${config_name} --config-block campaign --lsst-version ${lsst_version} --root-coll ${root_coll}
    cm daemon --fullname ${fullname} ${daemon_options}
else
    echo "We did not delete your cm database. You may proceed to your usual cm business without panic."
fi

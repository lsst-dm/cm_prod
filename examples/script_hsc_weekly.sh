#!/usr/bin/env bash

EXAMPLES="$(dirname -- "$(readlink -f -- "$0";)";)"

source $EXAMPLES/examples/hsc_weekly_setup.sh

default=no
read -p "This script will blow away the cm database and start a fresh one based on your setup file. Are you sure you want to do this? (y/N)" ANSWER
ANSWER=${ANSWER:-$default}

yeses="y Y yes Yes YES yEs yES yeS"
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
    mkdir -p output

    cm create
    cm parse --config-name ${config_name} --config-yaml ${config}
    cm insert --production-name ${p_name}
    cm insert --production-name ${p_name} --campaign-name ${c_name} --butler-repo ${butler_repo} --config-name ${config_name} --config-block campaign --lsst-version ${lsst_version} --root-coll ${root_coll}
    cm daemon --fullname ${fullname} --max-running 0
else
    echo "We did not delete your cm database. You may proceed to your usual cm business without panic."
fi

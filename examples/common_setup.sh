#!/usr/bin/env bash

EXAMPLES=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Use this for tests or things you're not quite sure of
#root_coll="u/${USER}/cm"
# Use this for runs you want in the butler in the traditional place
root_coll="HSC/runs/RC2"
#root_coll="2.2i/runs/test-med-1"

export CM_PROD_DIR=`echo ${EXAMPLES} | sed 's/\/examples//'`
export CM_PROD_URL="output/archive"
export CM_BUTLER="${butler_repo}"
export CM_SCRIPT_METHOD="slurm"


latest_panda=$(ls -td /cvmfs/sw.lsst.eu/linux-x86_64/panda_env/v* | head -1)
source $latest_panda/setup_panda_usdf.sh

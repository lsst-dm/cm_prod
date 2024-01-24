#!/usr/bin/env bash

EXAMPLES=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

root_coll="u/sierrav/panda_testing"

export CM_PROD_DIR="${EXAMPLES}/.."
export CM_PROD_URL="output/archive"
export CM_BUTLER="${butler_repo}"
export CM_SCRIPT_METHOD="slurm"

latest_panda=$(ls -td /cvmfs/sw.lsst.eu/linux-x86_64/panda_env/v* | head -1)
source $latest_panda/setup_panda_usdf.sh

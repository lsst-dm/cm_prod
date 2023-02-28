#!/usr/bin/env bash

EXAMPLES="$(dirname -- "$(readlink -f -- "$0";)";)"
butler_repo="/sdf/group/rubin/repo/main"
root_coll="u/${USER}/cm"

export CM_PROD_DIR="${EXAMPLES}"
export CM_PROD_URL="output/archive"
export CM_BUTLER="${butler_repo}"
export CM_SCRIPT_METHOD="slurm"
export PANDAMON_URL=https://panda-doma.cern.ch

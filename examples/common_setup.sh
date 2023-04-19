#!/usr/bin/env bash

EXAMPLES=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

butler_repo="/sdf/group/rubin/repo/main"
root_coll="u/${USER}/cm"

export CM_PROD_DIR="${EXAMPLES}"
export CM_PROD_URL="output/archive"
export CM_BUTLER="${butler_repo}"
export CM_SCRIPT_METHOD="slurm"

# Setting panda variables
export PANDA_CONFIG_ROOT=$HOME/.panda
export PANDA_URL_SSL=https://pandaserver-doma.cern.ch:25443/server/panda
export PANDA_URL=http://pandaserver-doma.cern.ch:25080/server/panda
export PANDACACHE_URL=$PANDA_URL_SSL
export PANDAMON_URL=https://panda-doma.cern.ch
export PANDA_AUTH=oidc
export PANDA_VERIFY_HOST=off
export PANDA_AUTH_VO=Rubin

# WMS plugin
export BPS_WMS_SERVICE_CLASS=lsst.ctrl.bps.panda.PanDAService

# Using pandaclient instead of sdfproxy
export no_proxy=.slac.stanford.edu,.cern.ch
export NO_PROXY=.slac.stanford.edu,.cern.ch

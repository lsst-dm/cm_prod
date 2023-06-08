#!/usr/bin/env bash

EXAMPLES=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )


# Let's see if we can move the butler to the campaign setup file instead so we don't have to do so much uncommenting
# HSC Butler:
#butler_repo="/sdf/group/rubin/repo/main"
# DC2 Butler:
#butler_repo="/sdf/group/rubin/repo/dc2"

# Use this for tests or things you're not quite sure of
#root_coll="u/${USER}/cm"
# Use this for runs you want in the butler in the traditional place
root_coll="HSC/runs/RC2"
#root_coll="2.2i/runs/test-med-1"

export CM_PROD_DIR=`echo ${EXAMPLES} | sed 's/\/examples//'`
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

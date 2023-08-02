#!/usr/bin/env -S -i CM_PROD_DIR="${CM_PROD_DIR}" HOME="${HOME}" bash

# The shebang lines above are needed b/c setup lsst_distrib in putting
# the lsst python _after_ the virtual env python in the PATH, which
# is causing errors

# setup LSST env from exact weekly stack.
#export WEEKLY='w_2023_29'#'{lsst_version}'
#source /cvmfs/sw.lsst.eu/linux-x86_64/lsst_distrib/${WEEKLY}/loadLSST.bash
#setup lsst_distrib

#setup LSST env from shared stack.
source /sdf/group/rubin/sw/tag/d_2023_07_21/loadLSST.bash
setup lsst_distrib

# setup PanDA env.
#latest_panda=$(ls -td /cvmfs/sw.lsst.eu/linux-x86_64/panda_env/v* | head -1)
#setupScript=${latest_panda}/setup_panda_s3df.sh
#source $setupScript ${WEEKLY}
# taken from panda setup script above since we are not using a weekly
# setup PanDA env. Will be a simple step when the deployment of PanDA is fully done.
export PANDA_CONFIG_ROOT=$HOME/.panda
export PANDA_URL_SSL=https://pandaserver-doma.cern.ch:25443/server/panda
export PANDA_URL=http://pandaserver-doma.cern.ch:25080/server/panda
export PANDACACHE_URL=$PANDA_URL_SSL
export PANDAMON_URL=https://panda-doma.cern.ch
export PANDA_AUTH=oidc
export PANDA_VERIFY_HOST=off
export PANDA_AUTH_VO=Rubin

# IDDS_CONFIG path depends on the weekly version
export PANDA_SYS=$CONDA_PREFIX
export IDDS_CONFIG=${PANDA_SYS}/etc/idds/idds.cfg.client.template

# WMS plugin
export BPS_WMS_SERVICE_CLASS=lsst.ctrl.bps.panda.PanDAService

env | grep PANDA

# let's drop a panda_auth status here for kicks
panda_auth status

#!/usr/bin/env -S -i CM_PROD_DIR="${CM_PROD_DIR}" HOME="${HOME}" bash

# The shebang lines above are needed b/c setup lsst_distrib in putting
# the lsst python _after_ the virtual env python in the PATH, which
# is causing errors

# setup LSST env (the LSST stack).
export WEEKLY='{lsst_version}'
source /cvmfs/sw.lsst.eu/linux-x86_64/lsst_distrib/${WEEKLY}/loadLSST.bash
setup lsst_distrib -t ${WEEKLY}

# setup PanDA env.
# If the stack is not set up elsewhere first, this setup will be insufficient.
latest_panda=$(ls -td /cvmfs/sw.lsst.eu/linux-x86_64/panda_env/v* | head -1)
source ${latest_panda}/setup_panda_usdf.sh

env | grep PANDA

# let's drop a panda_auth status here for kicks
panda_auth status

# Uncomment this for any custom bps setups
#setup -j -r path/to/local/ctrl_bps
#setup -j -r path/to/local/ctrl_bps_panda

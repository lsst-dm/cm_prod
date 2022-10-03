#!/bin/sh

# setup LSST env.
export WEEKLY='w_2022_40'
source /cvmfs/sw.lsst.eu/linux-x86_64/lsst_distrib/${WEEKLY}/loadLSST.bash
setup lsst_distrib

# setup PanDA env.
latest_panda=$(ls -td /cvmfs/sw.lsst.eu/linux-x86_64/panda_env/v* | head -1)
setupScript=${latest_panda}/setup_panda_s3df.sh
source $setupScript ${WEEKLY}

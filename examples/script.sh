\rm cm.db

p_name="HSC"
c_name="test"
handler="lsst.cm.prod.HSC.handler.HSCHandler"
config="${CM_PROD_DIR}/python/lsst/cm/prod/configs/HSC/test/hsc_config.yaml"
command="${CM_TOOLS_DIR}/bin.src/cm"
butler_repo=/sdf/group/rubin/repo/main

\rm -rf archive_hsc_test cm.db

${command} create 
${command} insert --level production --production_name ${p_name} --handler ${handler} --config_yaml ${config}
${command} insert --recurse --level campaign --production_name ${p_name} --campaign_name ${c_name} --handler ${handler} --config_yaml ${config} --butler_repo ${butler_repo}

${command} prepare --recurse --level step --production_name ${p_name} --campaign_name ${c_name} --step_name step1
${command} queue --level step --production_name ${p_name} --campaign_name ${c_name} --step_name step1
${command} launch --level step --production_name ${p_name} --campaign_name ${c_name} --step_name step1
${command} fake_run --level step --production_name ${p_name} --campaign_name ${c_name} --step_name step1
${command} accept --recurse --level step --production_name ${p_name} --campaign_name ${c_name} --step_name step1

${command} print_table --level production
${command} print_table --level campaign
${command} print_table --level step
${command} print_table --level group

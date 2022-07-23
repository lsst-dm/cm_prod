
p_name="HSC"
c_name="test"
handler="lsst.cm.prod.HSC.handler.HSCHandler"
config="python/lsst/cm/prod/configs/HSC/test/hsc_config.yaml"
command="cm"
butler_repo="/sdf/group/rubin/repo/main"

\rm -rf archive cm.db

${command} create 
${command} insert --level production --production_name ${p_name} --handler ${handler} --config_yaml ${config}
${command} insert --level campaign --production_name ${p_name} --campaign_name ${c_name} --handler ${handler} --config_yaml ${config} --butler_repo ${butler_repo}
${command} prepare --level campaign --production_name ${p_name} --campaign_name ${c_name}

${command} prepare --level step --production_name ${p_name} --campaign_name ${c_name} --step_name step1

${command} print_table --level production
${command} print_table --level campaign
${command} print_table --level step
${command} print_table --level group
${command} print_table --level workflow

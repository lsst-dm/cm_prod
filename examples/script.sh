
p_name="HSC"
c_name="test"
handler="lsst.cm.prod.HSC.handler.HSCHandler"
config="src/lsst/cm/prod/configs/HSC/test/hsc_config.yaml"
command="cm"
butler_repo="/sdf/group/rubin/repo/main"

\rm -rf archive cm.db

${command} create
${command} insert --level production --production-name ${p_name}
${command} insert --level campaign --production-name ${p_name} --campaign-name ${c_name} --handler ${handler} --config-yaml ${config} --butler-repo ${butler_repo}
${command} prepare --level campaign --production-name ${p_name} --campaign-name ${c_name}

${command} print-table --table production
${command} print-table --table campaign
${command} print-table --table step
${command} print-table --table group
${command} print-table --table workflow

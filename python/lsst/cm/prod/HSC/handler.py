# This file is part of cm_prod
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os

from typing import Any, Iterable, Optional
from collections import OrderedDict

from lsst.daf.butler import Butler

from lsst.cm.tools.core.utils import StatusEnum, LevelEnum
from lsst.cm.tools.core.grouper import Grouper
from lsst.cm.tools.core.db_interface import DbInterface, ScriptBase, DbId
from lsst.cm.tools.db.sqlalch_handler import SQLAlchemyHandler

from lsst.cm.tools.core.script_utils import (
    YamlChecker,
    make_butler_associate_command,
    make_butler_chain_command,
    make_bps_command,
    add_command_script,
    write_status_to_yaml,
)
from lsst.cm.prod.core.butler_utils import build_data_queries


class HSCStep1Grouper(Grouper):
    def _do_call(self):
        out_dict = dict(
            production_name=self.config["production_name"],
            campaign_name=self.config["campaign_name"],
            step_name=self.config["step_name"],
        )

        butler = Butler(
            self.dbi.get_repo(self.parent_db_id),
            collections=[self.config["coll_source"]],
        )

        data_queries = build_data_queries(butler, "raw", "exposure", 2, 500)

        for i, dq_ in enumerate(data_queries):
            out_dict.update(group_name=f"group_{i}", data_query=dq_)
            yield out_dict


class HSCStep2Grouper(Grouper):
    def _do_call(self):
        out_dict = dict(
            production_name=self.config["production_name"],
            campaign_name=self.config["campaign_name"],
            step_name=self.config["step_name"],
        )

        for i in range(20):
            out_dict.update(group_name=f"group_{i}", data_query=f"i == {i}")
            yield out_dict


class HSCStep3Grouper(Grouper):
    def _do_call(self):
        out_dict = dict(
            production_name=self.config["production_name"],
            campaign_name=self.config["campaign_name"],
            step_name=self.config["step_name"],
        )

        for i in range(20):
            out_dict.update(group_name=f"group_{i}", data_query=f"i == {i}")
            yield out_dict


class HSCStep4Grouper(Grouper):
    def _do_call(self):
        out_dict = dict(
            production_name=self.config["production_name"],
            campaign_name=self.config["campaign_name"],
            step_name=self.config["step_name"],
        )

        for i in range(20):
            out_dict.update(group_name=f"group_{i}", data_query=f"i == {i}")
            yield out_dict


class HSCStep5Grouper(Grouper):
    def _do_call(self):
        out_dict = dict(
            production_name=self.config["production_name"],
            campaign_name=self.config["campaign_name"],
            step_name=self.config["step_name"],
        )

        for i in range(20):
            out_dict.update(group_name=f"group_{i}", data_query=f"i == {i}")
            yield out_dict


class HSCStep6Grouper(Grouper):
    def _do_call(self):
        out_dict = dict(
            production_name=self.config["production_name"],
            campaign_name=self.config["campaign_name"],
            step_name=self.config["step_name"],
        )

        for i in range(20):
            out_dict.update(group_name=f"group_{i}", data_query=f"i == {i}")
            yield out_dict


class HSCStep7Grouper(Grouper):
    def _do_call(self):
        out_dict = dict(
            production_name=self.config["production_name"],
            campaign_name=self.config["campaign_name"],
            step_name=self.config["step_name"],
        )

        for i in range(20):
            out_dict.update(group_name=f"group_{i}", data_query=f"i == {i}")
            yield out_dict


class HSCHandler(SQLAlchemyHandler):

    step_dict = OrderedDict(
        [
            ("step1", HSCStep1Grouper),
            ("step2", HSCStep2Grouper),
            ("step3", HSCStep3Grouper),
            ("step4", HSCStep4Grouper),
            ("step5", HSCStep5Grouper),
            ("step6", HSCStep6Grouper),
            ("step7", HSCStep7Grouper),
        ]
    )

    default_config = SQLAlchemyHandler.default_config.copy()

    default_config.update(
        prepare_script_url_template="{prod_base_url}/{fullname}/01_prepare.sh",
        prepare_log_url_template="{prod_base_url}/{fullname}/01_prepare.log",
        run_script_url_template="{prod_base_url}/{fullname}/02_run.sh",
        run_log_url_template="{prod_base_url}/{fullname}/02_run.log",
        run_config_url_template="{prod_base_url}/{fullname}/02_run_bps.yaml",
        collect_script_url_template="{prod_base_url}/{fullname}/03_collect.sh",
        collect_log_url_template="{prod_base_url}/{fullname}/03_collect.log",
        coll_in_template="prod/{fullname}_input",
        coll_out_template="prod/{fullname}_output",
    )

    coll_template_names = dict(
        coll_in="coll_in_template",
        coll_out="coll_out_template",
    )

    prepare_script_url_template_names = dict(
        script_url="prepare_script_url_template",
        log_url="prepare_log_url_template",
    )

    collect_script_url_template_names = dict(
        script_url="collect_script_url_template",
        log_url="collect_log_url_template",
    )

    run_script_url_template_names = dict(
        script_url="run_script_url_template",
        log_url="run_log_url_template",
        config_url="run_config_url_template",
    )

    yaml_checker_class = YamlChecker().get_checker_class_name()

    def coll_name_hook(self, level: LevelEnum, insert_fields: dict, **kwargs) -> dict[str, str]:
        return self.resolve_templated_strings(self.coll_template_names, **insert_fields, **kwargs)

    def prepare_script_hook(
        self, level: LevelEnum, dbi: DbInterface, data
    ) -> Optional[ScriptBase]:
        assert level.value >= LevelEnum.campaign.value
        if level == LevelEnum.workflow:
            return None
        script_data = self.resolve_templated_strings(
            self.prepare_script_url_template_names,
            prod_base_url=data.prod_base_url,
            fullname=data.fullname,
        )
        command = make_butler_associate_command(data.butler_repo, data)
        script = add_command_script(
            dbi,
            command,
            script_data,
            "callback_stamp",
            checker=self.yaml_checker_class,
        )
        #stream = os.popen(f'source {os.path.abspath(script.script_url)}')
        #print(f'Running {command} gave {stream.read()}')
        return script

    def workflow_script_hook(self, dbi: DbInterface, data, **kwargs) -> Optional[ScriptBase]:
        """Internal function to write the bps.yaml file for a given workflow"""
        workflow_template_yaml = os.path.expandvars(self.config["workflow_template_yaml"])
        butler_repo = dbi.get_repo(data.db_id)
        script_data = self.resolve_templated_strings(
            self.run_script_url_template_names,
            prod_base_url=dbi.get_prod_base(data.db_id),
            fullname=data.fullname,
        )
        outpath = script_data["config_url"]
        script = dbi.add_script(checker=self.yaml_checker_class, **script_data)
        import yaml

        with open(workflow_template_yaml, "rt", encoding="utf-8") as fin:
            workflow_config = yaml.safe_load(fin)

        workflow_config["project"] = data.p_name
        workflow_config["campaign"] = f"{data.p_name}/{data.c_name}"

        workflow_config["pipelineYaml"] = self.config["pipeline_yaml"][data.s_name]
        payload = dict(
            payloadName=f"{data.p_name}/{data.c_name}",
            output=data.coll_out,
            butlerConfig=butler_repo,
            inCollection=f"{data.coll_in},/HSC/proc/ancil"
        )
        workflow_config["payload"] = payload
        with open(outpath, "wt", encoding="utf-8") as fout:
            yaml.dump(workflow_config, fout)

        command = make_bps_command(outpath)
        return add_command_script(dbi, command, script_data, "fake_stamp", checker=self.yaml_checker_class)

    def fake_run_hook(
        self,
        dbi: DbInterface,
        data,
        status: StatusEnum = StatusEnum.completed,
    ) -> None:
        script_id = data.run_script
        script = dbi.get_script(script_id)
        write_status_to_yaml(script.log_url, status)  # type: ignore

    def collect_script_hook(
        self, level: LevelEnum, dbi: DbInterface, itr: Iterable, data
    ) -> Optional[ScriptBase]:
        assert level.value >= LevelEnum.campaign.value
        if level == LevelEnum.campaign:
            return None
        script_data = self.resolve_templated_strings(
            self.collect_script_url_template_names,
            prod_base_url=data.prod_base_url,
            fullname=data.fullname,
        )
        command = make_butler_chain_command(data.butler_repo, data, itr)
        script = add_command_script(
            dbi,
            command,
            script_data,
            "callback_stamp",
            checker=self.yaml_checker_class,
        )
        #stream = os.popen(f'source {os.path.abspath(script.script_url)}')
        #print(f'Running {command} gave {stream.read()}')
        return script

    def accept_hook(self, level: LevelEnum, dbi: DbInterface, itr: Iterable, data) -> None:
        return

    def reject_hook(self, level: LevelEnum, dbi: DbInterface, data) -> None:
        return

import os
from collections import OrderedDict
from typing import Any, Iterable

import yaml
from lsst.cm.prod.core.butler_utils import build_data_queries
from lsst.cm.tools.core.db_interface import DbInterface, JobBase, ScriptBase
from lsst.cm.tools.core.handler import Handler
from lsst.cm.tools.core.script_utils import FakeRollback, YamlChecker, make_bps_command, write_command_script
from lsst.cm.tools.core.utils import StatusEnum
from lsst.cm.tools.db.campaign_handler import CampaignHandler
from lsst.cm.tools.db.group_handler import GroupHandler
from lsst.cm.tools.db.job_handler import JobHandler
from lsst.cm.tools.db.script_handler import AncillaryScriptHandler, CollectScriptHandler, PrepareScriptHandler
from lsst.cm.tools.db.step import Step
from lsst.cm.tools.db.step_handler import StepHandler
from lsst.cm.tools.db.workflow import Workflow
from lsst.cm.tools.db.workflow_handler import WorkflowHandler
from lsst.daf.butler import Butler


class HSCJobHandler(JobHandler):
    yaml_checker_class = YamlChecker().get_checker_class_name()
    fake_rollback_class = FakeRollback().get_rollback_class_name()

    def write_job_hook(self, dbi: DbInterface, parent: Workflow, job: JobBase, **kwargs: Any) -> None:
        """Internal function to write the bps.yaml file for a given workflow"""
        workflow_template_yaml = os.path.expandvars(self.config["bps_template_yaml"])
        butler_repo = parent.butler_repo

        outpath = job.config_url

        with open(workflow_template_yaml, "rt", encoding="utf-8") as fin:
            workflow_config = yaml.safe_load(fin)

        workflow_config["project"] = parent.p_.name
        workflow_config["campaign"] = f"{parent.p_.name}/{parent.c_.name}"

        workflow_config["pipelineYaml"] = self.config["pipeline_yaml"][parent.s_.name]
        payload = dict(
            payloadName=f"{parent.p_.name}/{parent.c_.name}",
            output=parent.coll_out,
            butlerConfig=butler_repo,
            inCollection=f"{parent.coll_in},/prod/HSC/test/calibs",
        )
        workflow_config["payload"] = payload
        with open(outpath, "wt", encoding="utf-8") as fout:
            yaml.dump(workflow_config, fout)

        prepend = """
export PANDA_AUTH=oidc
export PANDA_VERIFY_HOST=off
export PANDA_AUTH_VO=Rubin
export PANDA_URL_SSL=https://pandaserver-doma.cern.ch:25443/server/panda
export PANDA_URL=http://pandaserver-doma.cern.ch:25080/server/panda
"""

        command = make_bps_command(outpath)
        write_command_script(job, command, prepend=prepend)


class HSCWorkflowHander(WorkflowHandler):

    job_handler_class = HSCJobHandler().get_handler_class_name()

    def make_job_handler(self) -> JobHandler:
        return Handler.get_handler(self.job_handler_class, self.config_url)


class HSCEntryHandler:

    yaml_checker_class = YamlChecker().get_checker_class_name()
    fake_rollback_class = FakeRollback().get_rollback_class_name()

    prepare_handler_class = PrepareScriptHandler().get_handler_class_name()
    collect_handler_class = CollectScriptHandler().get_handler_class_name()

    def prepare_script_hook(self, dbi: DbInterface, entry: Any) -> list[ScriptBase]:
        handler = Handler.get_handler(self.prepare_handler_class, entry.config_yaml)
        script = handler.insert(
            dbi,
            entry,
            name="prepare",
            idx=0,
            prepend=f"# Written by {handler.get_handler_class_name()}\n",
            stamp=StatusEnum.completed,
        )
        status = handler.run(dbi, script)
        if status != StatusEnum.ready:
            script.update_values(dbi, script.id, status=status)
        return [script]

    def collect_script_hook(self, dbi: DbInterface, entry: Any) -> list[ScriptBase]:
        handler = Handler.get_handler(self.collect_handler_class, entry.config_yaml)
        script = handler.insert(
            dbi,
            entry,
            name="collect",
            idx=0,
            prepend=f"# Written by {handler.get_handler_class_name()}\n",
        )
        status = handler.run(dbi, script)
        if status != StatusEnum.ready:
            script.update_values(dbi, script.id, status=status)
        return [script]

    def validate_script_hook(self, dbi: DbInterface, entry: Any) -> list[ScriptBase]:
        assert dbi
        assert entry
        return []

    def accept_hook(self, dbi: DbInterface, itr: Iterable, entry: Any) -> None:
        pass

    def reject_hook(self, dbi: DbInterface, entry: Any) -> None:
        pass


class HSCGroupHandler(HSCEntryHandler, GroupHandler):

    workflow_handler_class = HSCWorkflowHander().get_handler_class_name()

    def make_workflow_handler(self) -> WorkflowHandler:
        return Handler.get_handler(self.workflow_handler_class, self.config_url)


class HSCStep1Handler(HSCEntryHandler, StepHandler):

    group_handler_class = HSCGroupHandler().get_handler_class_name()

    def group_iterator(self, dbi: DbInterface, entry: Step, **kwargs: Any) -> Iterable:
        out_dict = dict(
            production_name=entry.p_.name,
            campaign_name=entry.c_.name,
            step_name=entry.name,
        )

        butler = Butler(
            entry.butler_repo,
            collections=[entry.coll_source],
        )

        data_queries = build_data_queries(butler, "raw", "exposure", 20, 500)

        for i, dq_ in enumerate(data_queries):
            out_dict.update(group_name=f"group{i}", data_query=dq_)
            yield out_dict


class HSCStep2Handler(HSCEntryHandler, StepHandler):

    group_handler_class = HSCGroupHandler().get_handler_class_name()

    def group_iterator(self, dbi: DbInterface, entry: Step, **kwargs: Any) -> Iterable:
        out_dict = dict(
            production_name=entry.p_.name,
            campaign_name=entry.c_.name,
            step_name=entry.name,
        )
        for i in range(10):
            out_dict.update(group_name=f"group{i}", data_query=f"i == {i}")
            yield out_dict


class HSCStep3Handler(HSCEntryHandler, StepHandler):

    group_handler_class = HSCGroupHandler().get_handler_class_name()

    def group_iterator(self, dbi: DbInterface, entry: Step, **kwargs: Any) -> Iterable:
        out_dict = dict(
            production_name=entry.p_.name,
            campaign_name=entry.c_.name,
            step_name=entry.name,
        )
        for i in range(10):
            out_dict.update(group_name=f"group{i}", data_query=f"i == {i}")
            yield out_dict


class HSCStep4Handler(HSCEntryHandler, StepHandler):

    group_handler_class = HSCGroupHandler().get_handler_class_name()

    def group_iterator(self, dbi: DbInterface, entry: Step, **kwargs: Any) -> Iterable:
        out_dict = dict(
            production_name=entry.p_.name,
            campaign_name=entry.c_.name,
            step_name=entry.name,
        )
        for i in range(10):
            out_dict.update(group_name=f"group{i}", data_query=f"i == {i}")
            yield out_dict


class HSCStep5Handler(HSCEntryHandler, StepHandler):

    group_handler_class = HSCGroupHandler().get_handler_class_name()

    def group_iterator(self, dbi: DbInterface, entry: Step, **kwargs: Any) -> Iterable:
        out_dict = dict(
            production_name=entry.p_.name,
            campaign_name=entry.c_.name,
            step_name=entry.name,
        )
        for i in range(10):
            out_dict.update(group_name=f"group{i}", data_query=f"i == {i}")
            yield out_dict


class HSCStep6Handler(HSCEntryHandler, StepHandler):

    group_handler_class = HSCGroupHandler().get_handler_class_name()

    def group_iterator(self, dbi: DbInterface, entry: Step, **kwargs: Any) -> Iterable:
        out_dict = dict(
            production_name=entry.p_.name,
            campaign_name=entry.c_.name,
            step_name=entry.name,
        )
        for i in range(10):
            out_dict.update(group_name=f"group{i}", data_query=f"i == {i}")
            yield out_dict


class HSCStep7Handler(HSCEntryHandler, StepHandler):

    group_handler_class = HSCGroupHandler().get_handler_class_name()

    def group_iterator(self, dbi: DbInterface, entry: Step, **kwargs: Any) -> Iterable:
        out_dict = dict(
            production_name=entry.p_.name,
            campaign_name=entry.c_.name,
            step_name=entry.name,
        )
        for i in range(10):
            out_dict.update(group_name=f"group{i}", data_query=f"i == {i}")
            yield out_dict


class HSCHandler(HSCEntryHandler, CampaignHandler):

    ancil_chain_handler_class = AncillaryScriptHandler().get_handler_class_name()

    def prepare_script_hook(self, dbi: DbInterface, entry: Any) -> list[ScriptBase]:

        scripts = HSCEntryHandler.prepare_script_hook(self, dbi, entry)

        handler = Handler.get_handler(self.ancil_chain_handler_class, entry.config_yaml)
        script = handler.insert(
            dbi,
            entry,
            name="ancillary",
            prepend=f"# Written by {handler.get_handler_class_name()}",
            stamp=StatusEnum.completed,
        )
        status = handler.run(dbi, script)
        if status != StatusEnum.ready:
            script.update_values(dbi, script.id, status=status)
        scripts += [script]
        return scripts

    step_dict = OrderedDict(
        [
            ("step1", HSCStep1Handler),
            ("step2", HSCStep2Handler),
            ("step3", HSCStep3Handler),
            ("step4", HSCStep4Handler),
            ("step5", HSCStep5Handler),
            ("step6", HSCStep6Handler),
            ("step7", HSCStep7Handler),
        ]
    )

import os
from collections import OrderedDict
from typing import Any, Iterable

import yaml
from lsst.cm.tools.core.db_interface import DbInterface, JobBase
from lsst.cm.tools.core.handler import Handler
from lsst.cm.tools.core.script_utils import FakeRollback, YamlChecker, make_bps_command, write_command_script
from lsst.cm.tools.db.campaign_handler import CampaignHandler
from lsst.cm.tools.db.entry_handler import GenericEntryHandlerMixin
from lsst.cm.tools.db.group_handler import GroupHandler
from lsst.cm.tools.db.job_handler import JobHandler
from lsst.cm.tools.db.step import Step
from lsst.cm.tools.db.step_handler import StepHandler
from lsst.cm.tools.db.workflow import Workflow
from lsst.cm.tools.db.workflow_handler import WorkflowHandler
from lsst.daf.butler import Butler

from lsst.cm.prod.core.butler_utils import build_data_queries


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


class HSCGroupHandler(GenericEntryHandlerMixin, GroupHandler):

    workflow_handler_class = HSCWorkflowHander().get_handler_class_name()

    def make_workflow_handler(self) -> WorkflowHandler:
        return Handler.get_handler(self.workflow_handler_class, self.config_url)


class HSCStep1Handler(GenericEntryHandlerMixin, StepHandler):

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


class HSCStep2Handler(GenericEntryHandlerMixin, StepHandler):

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


class HSCStep3Handler(GenericEntryHandlerMixin, StepHandler):

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


class HSCStep4Handler(GenericEntryHandlerMixin, StepHandler):

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


class HSCStep5Handler(GenericEntryHandlerMixin, StepHandler):

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


class HSCStep6Handler(GenericEntryHandlerMixin, StepHandler):

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


class HSCStep7Handler(GenericEntryHandlerMixin, StepHandler):

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


class HSCHandler(GenericEntryHandlerMixin, CampaignHandler):

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

import os
from typing import Any, Iterable

import yaml
from lsst.cm.tools.core.db_interface import DbInterface, JobBase
from lsst.cm.tools.core.panda_utils import PandaChecker
from lsst.cm.tools.core.script_utils import make_bps_command, write_command_script
from lsst.cm.tools.db.job_handler import JobHandler
from lsst.cm.tools.db.step import Step
from lsst.cm.tools.db.step_handler import StepHandler
from lsst.cm.tools.db.workflow import Workflow
from lsst.daf.butler import Butler

from lsst.cm.prod.core.butler_utils import build_data_queries


class HSCJobHandler(JobHandler):

    checker_class_name = PandaChecker().get_checker_class_name()

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
            inCollection=f"{parent.coll_in},{parent.c_.coll_ancil}",
        )
        workflow_config["payload"] = payload
        with open(outpath, "wt", encoding="utf-8") as fout:
            yaml.dump(workflow_config, fout)

        bps_script_template = os.path.expandvars(self.config["bps_script_template"])

        with open(bps_script_template, "r") as fin:
            prepend = fin.read()

        command = make_bps_command(outpath, job.json_url, job.log_url)
        write_command_script(job, command, prepend=prepend)


class HSCStep1Handler(StepHandler):
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


class HSCStep2Handler(StepHandler):
    def group_iterator(self, dbi: DbInterface, entry: Step, **kwargs: Any) -> Iterable:
        out_dict = dict(
            production_name=entry.p_.name,
            campaign_name=entry.c_.name,
            step_name=entry.name,
        )
        for i in range(10):
            out_dict.update(group_name=f"group{i}", data_query=f"i == {i}")
            yield out_dict


class HSCStep3Handler(StepHandler):
    def group_iterator(self, dbi: DbInterface, entry: Step, **kwargs: Any) -> Iterable:
        out_dict = dict(
            production_name=entry.p_.name,
            campaign_name=entry.c_.name,
            step_name=entry.name,
        )
        for i in range(10):
            out_dict.update(group_name=f"group{i}", data_query=f"i == {i}")
            yield out_dict


class HSCStep4Handler(StepHandler):
    def group_iterator(self, dbi: DbInterface, entry: Step, **kwargs: Any) -> Iterable:
        out_dict = dict(
            production_name=entry.p_.name,
            campaign_name=entry.c_.name,
            step_name=entry.name,
        )
        for i in range(10):
            out_dict.update(group_name=f"group{i}", data_query=f"i == {i}")
            yield out_dict


class HSCStep5Handler(StepHandler):
    def group_iterator(self, dbi: DbInterface, entry: Step, **kwargs: Any) -> Iterable:
        out_dict = dict(
            production_name=entry.p_.name,
            campaign_name=entry.c_.name,
            step_name=entry.name,
        )
        for i in range(10):
            out_dict.update(group_name=f"group{i}", data_query=f"i == {i}")
            yield out_dict


class HSCStep6Handler(StepHandler):
    def group_iterator(self, dbi: DbInterface, entry: Step, **kwargs: Any) -> Iterable:
        out_dict = dict(
            production_name=entry.p_.name,
            campaign_name=entry.c_.name,
            step_name=entry.name,
        )
        for i in range(10):
            out_dict.update(group_name=f"group{i}", data_query=f"i == {i}")
            yield out_dict


class HSCStep7Handler(StepHandler):
    def group_iterator(self, dbi: DbInterface, entry: Step, **kwargs: Any) -> Iterable:
        out_dict = dict(
            production_name=entry.p_.name,
            campaign_name=entry.c_.name,
            step_name=entry.name,
        )
        for i in range(10):
            out_dict.update(group_name=f"group{i}", data_query=f"i == {i}")
            yield out_dict

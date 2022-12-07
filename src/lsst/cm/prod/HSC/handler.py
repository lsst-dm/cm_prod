import os
from typing import Any, Iterable

import yaml
from lsst.cm.tools.core.db_interface import DbInterface, JobBase
from lsst.cm.tools.core.panda_utils import PandaChecker
from lsst.cm.tools.core.script_utils import make_bps_command, write_command_script
from lsst.cm.tools.core.utils import StatusEnum
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
            outputRun=job.coll_out,
            butlerConfig=butler_repo,
            inCollection=f"{parent.coll_in},{parent.c_.coll_ancil}",
        )
        if parent.data_query:
            payload["dataQuery"] = parent.data_query

        workflow_config["payload"] = payload
        with open(outpath, "wt", encoding="utf-8") as fout:
            yaml.dump(workflow_config, fout)

        bps_script_template = os.path.expandvars(self.config["bps_script_template"])

        with open(bps_script_template, "r") as fin:
            prepend = fin.read()

        command = make_bps_command(outpath, job.json_url, job.log_url)
        write_command_script(job, command, prepend=prepend)

    def fake_run_hook(
        self, dbi: DbInterface, job: JobBase, status: StatusEnum = StatusEnum.completed
    ) -> None:
        job.update_values(dbi, job.id, status=status)


class HSCStepHandler(StepHandler):
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
        data_query_base = self.config["data_query_base"]
        split_args = self.config.get("split_args", {})
        split_vals = self.config.get("split_vals", {})

        if split_args:
            data_queries = build_data_queries(butler, **split_args)
        elif split_vals:
            split_field = split_vals["field"]
            data_queries = [f"{split_field} IN str({v})" for v in split_vals["values"]]
        else:
            data_queries = [None]
        for i, dq_ in enumerate(data_queries):
            data_query = data_query_base
            if dq_ is not None:
                data_query += f" AND {dq_}"
            out_dict.update(
                group_name=f"group{i}",
                data_query=data_query,
            )
            yield out_dict

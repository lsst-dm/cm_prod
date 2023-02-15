from lsst.cm.tools.core.panda_utils import PandaChecker
from lsst.cm.tools.core.utils import ScriptMethod
from lsst.cm.tools.db.job_handler import JobHandler


class HSCJobHandler(JobHandler):

    checker_class_name = PandaChecker().get_checker_class_name()

    JobHandler.checker_class_dict[ScriptMethod.slurm] = PandaChecker

# When cloning the project, to be run with 'pipenv run python examples/simple.py'
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
## ^^ Do not use statement up when installing library ^^

from pino import pino

logger = pino(bindings={"apptype": "prototype", "stats": {"job_name": "my_job"}}, millidiff=False)

logger.info("job started")
logger.debug("something happening")
logger.info({"err_code": 42, "stats": {"execution_time": 42}}, "job completed %s", "NOW")

logger.level = "warn"
logger.info("You wont see mee")
logger.warn("Unless I warn you")
logger.level = "info"
logger.info("Or I restore {level} level", level="info")

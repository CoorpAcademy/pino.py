
from pino import pino

logger = pino(
    bindings={"apptype": "prototype", "context": "main"}
)

logger.info("Hello, I just started")
logger.debug({"details": 42}, "Some details that won't be seen")

child_logger = logger.child(context="some_job")
child_logger.info("Job started")
child_logger.info({"duration": 4012}, "Job completed %s", "NOW")

logger.info("Program completed")
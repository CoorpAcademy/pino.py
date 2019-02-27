# When cloning the project, to be run with 'pipenv run python examples/simple.py'
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
## ^^ Do not use statement up when installing library ^^

from pino import pino

logger = pino(bindings={"apptype": "prototype"})

logger.info("toto")
logger.debug("tutu")
logger.warn({"err_code": 42}, "tata")
logger.error("tete")

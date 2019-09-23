# When cloning the project, to be run with 'pipenv run python examples/simple.py'
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
## ^^ Do not use statement up when installing library ^^
from time import sleep
from pino import pino

logger = pino(bindings={"apptype": "prototype"})

logger.info("toto")
sleep(0.1)
logger.debug("tutu")
sleep(0.012)
logger.warn({"err_code": 42}, "tata")
sleep(0.010)
logger.error("tete")

child_logger = logger.child({"apptype": "mega-prototype"})
child_logger.info("little logger")

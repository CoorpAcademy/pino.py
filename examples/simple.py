# When cloning the project, to be run with 'pipenv run python examples/simple.py'
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
## ^^ Do not use statement up when installing library ^^

from pino import pino

logger = pino('prefix')

logger.info("toto")
logger.debug("tutu")
logger.warn("tata")
logger.error("tete")

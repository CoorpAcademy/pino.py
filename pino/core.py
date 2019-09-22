import json
import sys
import os
from datetime import datetime
from collections import namedtuple
from .utils import merge_dicts

LoggingLevel = namedtuple('LoggingLevel', ['name', 'level'])
PinoConfig = namedtuple('PinoConfig', ['level', 'stream', 'binding', 'enabled', 'parent'])

LEVELS = [
   LoggingLevel("debug", 10),
   LoggingLevel("info", 20),
   LoggingLevel("warn", 30),
   LoggingLevel("error", 40),
   LoggingLevel("fatal", 50)
]
LEVEL_NAMES = [level.name for level in LEVELS]
LEVEL_BY_NAME = {level.name: level for level in LEVELS}


def get_logger(stream, level, metas={}):
    def log(*args):
        has_meta = isinstance(args[0], dict)
        message_metas = args[0] if has_meta else None
        complete_metas = (merge_dicts(metas, message_metas)
                          if message_metas else metas)
        message = args[1] if has_meta else args[0]  # !TODO: handle formating!
        json_log = {
            "level": level,
            "time": int(1000* datetime.now().timestamp()),
            # §todo: add host and other metas.
            "message": message,
            **complete_metas
        }
        stream.write(json.dumps(json_log))
        stream.write(os.linesep)
        stream.flush()
    log.__name__ = level
    return log

class DummyLogger:
    def fatal(self, *args):
        pass
    def error(self, *args):
        pass
    def warn(self, *args):
        pass
    def info(self, *args):
        pass
    def debug(self, *args):
        pass

class PinoLogger(DummyLogger):
    __slots__ = ["_config"]
    def __init__(self, bindings=None, level="info", stream=sys.stdout, enabled=True, parent=None):
        logging_level = LEVEL_BY_NAME.get(level)  # ! TODO: support LoggingLevel or Code?
        self._config = PinoConfig(logging_level, stream, bindings, enabled, parent)
        for level in LEVEL_NAMES:
            if enabled and LEVEL_BY_NAME.get(level).level >= logging_level.level:
                logging_method = get_logger(stream, level, bindings)
                setattr(self, level, logging_method)

    def child(self, metas):
        merged_bindings = merge_dicts(self._config.binding, metas)
        return PinoLogger(
            bindings=merged_bindings,
            level=self._config.level.name,
            enabled=self._config.enabled,
            stream=self._config.stream,
            parent=self
        )

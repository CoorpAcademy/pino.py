import json
import sys
import os
from datetime import datetime
from .utils import merge_dicts

LEVELS_NAME_TO_LEVEL = {
    "debug": 10,
    "info": 20,
    "warn": 30,
    "error": 40,
    "fatal": 50
}
LEVEL_NAMES = LEVELS_NAME_TO_LEVEL.keys()


def get_logger(stream, level, metas={}):
    def log(*args):
        has_meta = isinstance(args[0], dict)
        message_metas = args[0] if has_meta else None
        complete_metas = (merge_dicts(metas, message_metas)
                 if message_metas else metas)
        message = args[1] if has_meta else args[0]
        stream.write(json.dumps({
                "level": level,
                "time": int(1000* datetime.now().timestamp()),
                # §todo: add host and other metas.
                "message": message,
                **complete_metas}))
        stream.write(os.linesep)
        stream.flush()
    log.__name__ = level
    return log

def noop(*args):
    pass

class PinoLogger:
    def __init__(self, bindings=None, level="info", stream=sys.stdout, enabled=True):
        self._level = level
        self._logger_level = LEVELS_NAME_TO_LEVEL[level]
        self._logger_metas = bindings or {}
        self._is_logging = enabled
        self._stream = stream
        for level in LEVEL_NAMES:
            logging_method = (get_logger(self._stream, level, self._logger_metas)
              if enabled and LEVELS_NAME_TO_LEVEL[level] >= self._logger_level
              else noop)
            setattr(self, level, logging_method)

    def child(self, metas):
        # §TODO: handle level?
        merged_bindings = merge_dicts(self._logger_metas, metas)
        return PinoLogger(
            bindings=merged_bindings,
            level=self._level,
            enabled=self._is_logging,
            stream=self._stream
        )

import json
import sys
import os
from datetime import datetime
from collections import namedtuple
from .utils import merge_dicts

LoggingLevel = namedtuple('LoggingLevel', ['name', 'level'])
PinoConfig = namedtuple('PinoConfig', ['level', 'stream', 'bindings', 'enabled', 'millidiff', 'parent'])

DEBUG = LoggingLevel("debug", 10)
INFO = LoggingLevel("info", 20)
WARN = LoggingLevel("warn", 30)
ERROR = LoggingLevel("error", 40)
CRITICAL = LoggingLevel("critical", 50)

LEVELS = [DEBUG, INFO, WARN, ERROR, CRITICAL]
LEVEL_NAMES = [level.name for level in LEVELS]
LEVEL_BY_NAME = {level.name: level for level in LEVELS}
LEVEL_BY_CODE = {level.level: level for level in LEVELS}
def get_level(level_name_or_code):
    if isinstance(level_name_or_code, LoggingLevel):
        return level_name_or_code
    return (LEVEL_BY_CODE.get(level_name_or_code)
            if isinstance(level_name_or_code, int)
            else LEVEL_BY_NAME.get(level_name_or_code))


def get_logger(self):
    metas = self._config.bindings
    level = self._config.level.name
    stream = self._config.stream
    should_millidiff = self._config.millidiff

    def log(*args):
        has_meta = isinstance(args[0], dict)
        message_metas = args[0] if has_meta else None
        complete_metas = (merge_dicts(metas, message_metas)
                          if message_metas else metas)
        message = args[1] if has_meta else args[0]  # !TODO: handle formating!
        now = int(1000* datetime.now().timestamp())
        json_log = {
            "level": level,
            "time": now,
            # §todo: add host and other metas.
            "message": message,
            **complete_metas
        }
        if should_millidiff:
            delta = (now - self._last_timestamp) if self._last_timestamp else 0
            json_log["millidiff"] = delta
            self._last_timestamp = now
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
    __slots__ = ["_config", "_last_timestamp"]
    def __init__(self, bindings=None, level="info", stream=sys.stdout, enabled=True, parent=None, millidiff=True):
        logging_level = get_level(level)  # ! TODO: support LoggingLevel or Code?
        self._config = PinoConfig(logging_level, stream, bindings, enabled, millidiff, parent)
        self._last_timestamp = None
        for level in LEVELS:
            if enabled and level.level >= logging_level.level:
                logging_method = get_logger(self)
                setattr(self, level.name, logging_method)

    def child(self, metas):
        merged_bindings = merge_dicts(self._config.bindings, metas)
        child_logger = PinoLogger(
            bindings=merged_bindings,
            level=self._config.level.name,
            enabled=self._config.enabled,
            millidiff=self._config.millidiff,
            stream=self._config.stream,
            parent=self
        )
        child_logger._last_timestamp = self._last_timestamp
        return child_logger

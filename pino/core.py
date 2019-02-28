import json
import sys
import os
from datetime import datetime

LEVELS = {
    "fatal": 50,
    "error": 40,
    "warn": 30,
    "info": 20,
    "debug": 10
}

class PinoLogger:

    def __init__(self, bindings=None, level="info", stream=sys.stdout, disabled=False):
        self._level = level
        self._logger_level = LEVELS[level]
        self._logger_metas = bindings or {}
        self._is_logging = not disabled
        self._stream = stream

    def _log(self, metas, message, level = "info"):
        # for simple of api, expect a single message
        if self._is_logging and LEVELS[level] >= self._logger_level:
            real_message = message or metas
            message_metas = metas if message else {}
            self._stream.write(json.dumps({
                 "level": level,
                 "time": int(1000* datetime.now().timestamp()),
                 "message": real_message,
                 **self._logger_metas,
                 **message_metas}))
            self._stream.write(os.linesep)

    def fatal(self, metas, message=None):
        self._log(metas, message, level="fatal")
    def info(self, metas, message=None):
        self._log(metas, message, level="info")
    def error(self, metas, message=None):
        self._log(metas, message, level="error")
    def warn(self, metas, message=None):
        self._log(metas, message, level="warn")
    def debug(self, metas, message=None):
        self._log(metas, message, level="debug")

    def child(self, metas):
        # §TODO: handle level?
        merged_bindings = {**self._logger_metas, **metas}
        return PinoLogger(
            bindings=merged_bindings,
            level=self._level,
            disabled=not self._is_logging,
            stream=self._stream
        )

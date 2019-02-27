import json
import sys
import os

LEVELS = {
    "error": 40,
    "warn": 30,
    "info": 20,
    "debug": 10
}

class PinoLogger:

    def __init__(self, bindings=None, level="info", stream=sys.stdout):
        self._logger_level = LEVELS[level]
        self._logger_metas = bindings or {}
        self._is_logging = True
        self._stream = stream

    def _log(self, metas, message, level = "info"):
        # for simple of api, expect a single message
        if self._is_logging and LEVELS[level] >= self._logger_level:
            real_message = message or metas
            message_metas = metas if message else {}
            self._stream.write(json.dumps({"message": real_message, "level": level, **self._logger_metas, **message_metas}))
            self._stream.write(os.linesep)

    def info(self, metas, message=None):
        self._log(metas, message, level = "info")
    def error(self, metas, message=None):
        self._log(metas, message, level = "error")
    def warn(self, metas, message=None):
        self._log(metas, message, level = "warn")
    def debug(self, metas, message=None):
        self._log(metas, message, level = "debug")

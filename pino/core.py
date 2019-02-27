import json

LEVELS = {
    "error": 40,
    "warn": 30,
    "info": 20,
    "debug": 10
}

class PinoLogger:

    def __init__(self, options = None):
        self.options = options or {}
        self._logger_level = LEVELS[self.options.get("level", "info")]
        self._logger_metas = self.options.get("bindings", {})
        self._is_logging = True

    def _log(self, metas, message, level = "info"):
        real_message = message or metas
        message_metas = metas if message else {}

        # for simple of api, expect a single message
        if self._is_logging and LEVELS[level] >= self._logger_level:
            print(json.dumps({"message": real_message, "level": level, **self._logger_metas, **message_metas}))

    def info(self, metas, message=None):
        self._log(metas, message, level = "info")
    def error(self, metas, message=None):
        self._log(metas, message, level = "error")
    def warn(self, metas, message=None):
        self._log(metas, message, level = "warn")
    def debug(self, metas, message=None):
        self._log(metas, message, level = "debug")

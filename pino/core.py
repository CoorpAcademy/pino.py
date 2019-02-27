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
        self._metas = self.options.get("bindings", {})
        self._is_logging = True

    def _log(self, message, level = "info"):
        # for simple of api, expect a single message
        if self._is_logging and LEVELS[level] >= self._logger_level:
            print(json.dumps({"message": message, "level": level, **self._metas}))

    def info(self, message):
        self._log(message, level = "info")
    def error(self, message):
        self._log(message, level = "error")
    def warn(self, message):
        self._log(message, level = "warn")
    def debug(self, message):
        self._log(message, level = "debug")

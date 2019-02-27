
class PinoLogger:

    def __init__(self, prefix, options = None):
        self.prefix = prefix
        self.options = options

    def log(self, message, level = "info"):
        # for simple of api, expect a single message
        print(level, message)

    def info(self, message):
        self.log(message, level = "info")
    def error(self, message):
        self.log(message, level = "error")
    def warn(self, message):
        self.log(message, level = "warn")
    def debug(self, message):
        self.log(message, level = "debug")

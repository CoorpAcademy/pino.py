
class Pino:

    def __init__(self, prefix):
        self.prefix = prefix

    def __call__(self, message):
        print(self.prefix + " LOG " + message)

    def __enter__(self):
        return "logger"
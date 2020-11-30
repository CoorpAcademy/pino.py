pino.py
=======

> **Json natural logger for python** inspired by [pino.js](https://github.com/pinojs/pino) :evergreen_tree:

[![PyPI](https://img.shields.io/pypi/v/pino.svg)](https://pypi.org/project/pino/)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/pino.svg)](https://pypi.python.org/pypi/pino)
[![Build Status](https://travis-ci.com/CoorpAcademy/pino.py.svg?branch=master)](https://travis-ci.com/CoorpAcademy/pino.py)
[![codecov](https://codecov.io/gh/CoorpAcademy/pino.py/branch/master/graph/badge.svg)](https://codecov.io/gh/CoorpAcademy/pino.py)

> In building port of [pinojs](https://github.com/pinojs/pino) logging library to python :snake:

:warning: This is a in building prototype, it's API is subject to change.
A CHANGELOG will be introduced once it's stable enough and publicized.
Use it at you own risk, but feel free to reach with an issue.


## Basic Example

```python
from pino import pino

logger = pino(
    bindings={"apptype": "prototype", "context": "main"}
)

logger.info("Hello, I just started")
logger.debug({"details": 42}, "Some details that won't be seen")

child_logger = logger.child(context="some_job")
child_logger.info("Job started")
child_logger.info({"duration": 4012}, "Job completed %s", "NOW")

logger.info("Program completed")
```

Which would output:
```
{"level": "info", "time": 1587740056952, "message": "Hello, I just started", "host": "SomeHost", "apptype": "prototype", "context": "main", "millidiff": 0}
{"level": "info", "time": 1587740056952, "message": "Job started", "host": "SomeHost", "context": "some_job", "apptype": "prototype", "millidiff": 0}
{"level": "info", "time": 1587740056952, "message": "Job completed NOW", "host": "SomeHost", "duration": 4012, "context": "some_job", "apptype": "prototype", "millidiff": 0}
{"level": "info", "time": 1587740056952, "message": "Program completed", "host": "SomeHost", "apptype": "prototype", "context": "main", "millidiff": 0}
```

## API
### pino() constructor arguments

- `bindings`: meta attached to the messages by default
- `level`: minimal level to output logs, _default to `info`_
- `enabled`: is logger enabled, _default to true_
- `millidiff`: whether a millidiff is added to message, `ms` since last message, _enabled by default_.
- `stream` : stream to write logs to, default to `sys.stdout`
- `dump_function`: function to be used to serialise object to JSON, _default `json.dumps`_
- `messagekey`: key for message entry,  _default `message`_

### pino logger instance
- log methods: `critical`, `error`, `warn`, `info`, `debug`: (extra_bindings?), message, template value
- `.level`: access or update current log level

- `child(metas)`: create a child logger instance with new metas/bindings attached to it. (metas can be provided either as dict or kwargs)

### Complex examples

You can see more detailed examples in the [**examples** folder](./examples), notably [complex.py](./examples/complex.py)

## Development :hammer_and_wrench:

This library use [***Poetry***](https://python-poetry.org/) for management of the project, it's dependencies, build and else.

You can run test on all supported python version with `poetry run task test` (which will run `tox`),
or you can run on your current python version with `poetry run task pytest`.

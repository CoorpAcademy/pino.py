from io import StringIO
import json
from pino import pino

def test_create_simple_pino():
    stream = StringIO()
    logger = pino(stream=stream)
    logger.info("test")
    logger.warn("dangerous test")
    logger.debug("you wont see me")
    logged_output = stream.getvalue()
    logged_lines = logged_output.strip().split("\n")
    assert len(logged_lines) == 2
    for line in logged_lines:
        log = json.loads(line)
        assert sorted(log.keys()) == ["host", "level", "message", "millidiff", "time"]

def test_create_simple_pino_with_bindings_and_no_millidiff():
    stream = StringIO()
    logger = pino(stream=stream, bindings=dict(the="default binding"), millidiff=False, messagekey="msg")
    logger.info("test")
    logger.warn(dict(the="warn"), "dangerous test")
    logger.debug("you wont see me")
    logged_output = stream.getvalue()
    logged_lines = logged_output.strip().split("\n")
    assert len(logged_lines) == 2
    for line in logged_lines:
        log = json.loads(line)
        assert sorted(log.keys()) == ["host", "level", "msg", "the", "time"]
        if log["level"] == "warn":
            assert log["the"] == "warn"
        else:
            assert log["the"] =="default binding"

def test_create_pino_and_child():
    stream = StringIO()
    logger = pino(
        stream=stream,
        bindings=dict(the="default binding", and_some=dict(nested="value"))
    )
    logger.info("test")
    logger.warn(dict(the="warn"), "dangerous test")
    logger.debug("you wont see me")
    child_logger = logger.child(dict(the="child", and_some=dict(other=True)))
    child_logger.info("Still there")

    logged_output = stream.getvalue()
    logged_lines = logged_output.strip().split("\n")
    assert len(logged_lines) == 3

    for n, line in enumerate(logged_lines):
        log = json.loads(line)
        assert sorted(log.keys()) == ["and_some", "host", "level", "message", "millidiff", "the", "time"]

        if n == 0:
            assert log["the"] == "default binding"
            assert log["and_some"] == {"nested": "value"}
        elif n == 1:
            assert log["the"] == "warn"
            assert log["and_some"] == {"nested": "value"}
        else:
            assert log["the"] == "child"
            assert log["and_some"] == {"nested": "value", "other": True}

def test_update_level_on_the_fly():
    stream = StringIO()
    logger = pino(stream=stream, level="critical")

    logger.error("Wont see the error")
    logger.warn("Wont see the warn")
    logger.info("Wont see the info")
    logger.critical("Will see the critical (ooof)")

    assert logger.level == "critical"
    logger.level = "info"
    logger.info("News are back online")

    logged_output = stream.getvalue()
    logged_lines = logged_output.strip().split("\n")
    assert len(logged_lines) == 2  # 1 critical and 1 info (after level setting)

def test_log_formating_with_extra_args():
    stream = StringIO()
    logger = pino(stream=stream)
    logger.info("This is a %s %s", "wonderfull test", "you see")
    logger.warn("This is a {format} {test}", test="warning", format="wonderfull")

    logged_output = stream.getvalue()
    logged_lines = logged_output.strip().split("\n")
    assert len(logged_lines) == 2
    for n, line in enumerate(logged_lines):
        log = json.loads(line)
        if n == 0:
            assert log["message"] == "This is a wonderfull test you see"
        else:
            assert log["message"] == "This is a wonderfull warning"

def test_not_enabled():
    stream = StringIO()
    logger = pino(stream=stream, enabled=False)
    logger.info("Info")
    logger.info("Info")
    logger.warn("Attention")
    logger.critical("HEEEEEELP")

    assert stream.getvalue().strip() == ""

def test_level_by_value():
    stream = StringIO()
    logger = pino(stream=stream, level=30)
    logger.info("Info")
    logger.info("Info")
    logger.warn("Attention")
    logger.critical("HEEEEEELP")

    assert len(stream.getvalue().strip().split("\n")) == 2


def test_child_no_binding():
    stream = StringIO()
    logger = pino(stream=stream)
    child_logger = logger.child(dict(akey="avalue"))
    child_logger.info("Info")

    lines = stream.getvalue().strip().split("\n")
    assert len(lines) == 1
    log = json.loads(lines[0])
    assert sorted(log.keys()) == ["akey", "host", "level", "message", "millidiff", "time"]

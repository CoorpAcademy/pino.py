from io import StringIO
import json
from pino import pino


def test_bench_info(benchmark):
    stream = StringIO()
    logger = pino(stream=stream)
    benchmark(logger.info, "some info")


def test_bench_debug_non_activated(benchmark):
    stream = StringIO()
    logger = pino(stream=stream)
    benchmark(logger.debug, "some debug")


def test_bench_info_meta(benchmark):
    stream = StringIO()
    logger = pino(stream=stream)
    benchmark(logger.info, dict(hello="World"), "some info with meta")


def test_bench_info_meta_format(benchmark):
    stream = StringIO()
    logger = pino(stream=stream)
    benchmark(logger.info, dict(hello="World"), "some info with %s", "metas")


def test_bench_info_meta_merging(benchmark):
    stream = StringIO()
    logger = pino(stream=stream, bindings=dict(who="World"))
    benchmark(logger.info, dict(hello="Bonjour"), "some info with %s", "metas")

def test_create_pino_and_child(benchmark):
    stream = StringIO()
    logger = pino(
        stream=stream,
        bindings=dict(the="default binding", and_some=dict(nested="value"))
    )
    child = logger.child(dict(this="stuff",and_some=dict(other_nested="value")))
    benchmark(logger.info, dict(hello="Bonjour"), "Nest all the things")

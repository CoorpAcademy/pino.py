from pino.utils import merge_dicts

def test_merge_does_not_mutate():
    a = {"a": "a", "aa": "aa"}
    b = {"b": "b", "bb": "bb"}
    assert merge_dicts(a,b) == {"a": "a", "aa": "aa", "b": "b", "bb": "bb"}
    assert a == {"a": "a", "aa": "aa"}
    assert b == {"b": "b", "bb": "bb"}

def test_simple_merge():
    a = {"a": "a", "aa": "aa"}
    b = {"b": "b", "bb": "bb"}
    assert merge_dicts(a,b) == {"a": "a", "aa": "aa", "b": "b", "bb": "bb"}

def test_simple_merge_with_overwrite():
    a = {"key": "a"}
    b = {"key": "b"}
    assert merge_dicts(a, b) == {"key": "a"}

def test_complex_merge():
    a = {"a": "a", "common": {"a": "a"}}
    b = {"b": "b", "common": {"b": "b"}}
    assert merge_dicts(a,b) == {"a": "a", "b": "b", "common": {"a": "a", "b": "b"}}

def test_complex_merge_with_overwrite():
    a = {"a": "a", "common": {"a": "a", "key": "a"}}
    b = {"b": "b", "common": {"b": "b", "key": "b"}}
    assert merge_dicts(a,b) == {"a": "a", "b": "b", "common": {"a": "a", "b": "b", "key": "a"}}

def test_no_a_or_no_b():
    anyobj = {"b": "b", "common": {"b": "b", "key": "b"}}
    assert merge_dicts(None, anyobj) == anyobj
    assert merge_dicts({}, anyobj) == anyobj
    assert merge_dicts(anyobj, None) == anyobj
    assert merge_dicts(anyobj, {}) == anyobj

import pytest
from envkit import Registry


def test_resolve_rebuilds_on_different_kwargs():
    reg = Registry()
    reg.register("conn", lambda host="localhost": {"host": host})

    # 1. 首次解析：使用传入参数构建
    a = reg.resolve("conn", host="db1")
    assert a["host"] == "db1", "首次解析应正确应用 kwargs"

    # 2. 再次解析：传入不同参数，必须重建而非复用旧缓存
    b = reg.resolve("conn", host="db2")
    assert b["host"] == "db2", "不同参数应触发重建，返回新实例"
    assert b is not a, "参数不同时必须重建，不能静默复用旧实例"

    # 3. 再次解析：传入相同参数，必须复用缓存
    c = reg.resolve("conn", host="db2")
    assert c is b, "参数相同时应复用缓存，避免重复构建"


def test_resolve_cache_reuse_regression():
    """回归断言：确保修复未破坏相同参数下的缓存复用行为"""
    reg = Registry()
    reg.register("svc", lambda port=80: {"port": port})

    x = reg.resolve("svc", port=9090)
    y = reg.resolve("svc", port=9090)
    assert x is y, "相同参数必须命中缓存，不能重复构建"
    assert x["port"] == 9090

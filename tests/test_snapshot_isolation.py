import pytest
from envkit import Registry


def test_snapshot_shallow_modification_isolation():
    """复现步骤1：向快照添加新键，不应污染注册表"""
    reg = Registry()
    reg.register("service", lambda: {"name": "svc", "port": 8080})
    reg.resolve("service")

    snap = reg.snapshot()
    snap["evil"] = "injected"

    assert "evil" not in reg.snapshot(), "浅层添加新键污染了注册表"


def test_snapshot_deep_modification_isolation():
    """复现步骤2：修改快照嵌套字段，不应穿透污染注册表"""
    reg = Registry()
    reg.register("service", lambda: {"name": "svc", "port": 8080})
    reg.resolve("service")

    snap = reg.snapshot()
    snap["service"]["port"] = 1

    assert reg.snapshot()["service"]["port"] == 8080, "深层修改嵌套字段穿透污染了注册表"


def test_snapshot_exact_expected_output():
    """精确匹配正文期望输出"""
    reg = Registry()
    reg.register("service", lambda: {"name": "svc", "port": 8080})
    reg.resolve("service")

    snap = reg.snapshot()
    snap["evil"] = "injected"
    snap["service"]["port"] = 1

    expected = {'service': {'name': 'svc', 'port': 8080}}
    assert reg.snapshot() == expected, f"期望输出为 {expected}，实际为 {reg.snapshot()}"


def test_registry_caching_and_snapshot_regression():
    """回归断言：修复后注册表的缓存与快照基础行为必须保持不变"""
    reg = Registry()
    reg.register("db", lambda: {"host": "localhost", "port": 5432})

    # 缓存机制应正常工作
    obj1 = reg.resolve("db")
    obj2 = reg.resolve("db")
    assert obj1 is obj2, "resolve 缓存机制被破坏"

    # 初始快照应正确反映状态
    snap = reg.snapshot()
    assert snap == {"db": {"host": "localhost", "port": 5432}}

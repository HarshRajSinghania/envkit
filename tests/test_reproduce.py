import pytest
from envkit import TTLCache

class MockClock:
    def __init__(self):
        self.now = 0.0
    def __call__(self):
        return self.now
    def tick(self, s):
        self.now += s

def test_get_ignores_expiration_bug():
    """复现 Issue #2：get() 不检查过期时间，导致过期数据仍可读取"""
    clock = MockClock()
    cache = TTLCache(ttl=10, clock=clock)

    cache.set("token", "abc")
    clock.tick(11)  # 远超 ttl

    # 核心断言：修复前返回 "abc" (失败)，修复后返回 None (通过)
    assert cache.get("token") is None, "get() 必须对过期条目返回 None"

    # 一致性断言：与 contains 行为保持一致
    assert "token" not in cache, "contains 必须对过期条目返回 False"

def test_get_unexpired_and_boundary():
    """期望修复中的边界用例：未过期正常返回，刚好到期视为过期"""
    clock = MockClock()
    cache = TTLCache(ttl=10, clock=clock)

    cache.set("k", "v")
    clock.tick(9)     # 未过期
    assert cache.get("k") == "v", "未过期时应正常返回值"
    assert "k" in cache, "未过期时 contains 应为 True"

    clock.tick(1)     # 刚好到期 (now == expires_at)
    assert cache.get("k") is None, "刚好到期时应视为过期并返回 None"
    assert "k" not in cache, "刚好到期时 contains 应为 False"

def test_regression_contains_and_purge():
    """回归断言：确保 contains 与 purge 的既有正确行为不被破坏"""
    clock = MockClock()
    cache = TTLCache(ttl=5, clock=clock)

    cache.set("x", 100)
    cache.set("y", 200)

    # 未过期阶段
    clock.tick(2)
    assert cache.get("x") == 100
    assert cache.get("y") == 200
    assert "x" in cache
    assert "y" in cache

    # 过期阶段
    clock.tick(4)  # now = 6 > ttl=5
    assert cache.get("x") is None
    assert cache.get("y") is None
    assert "x" not in cache
    assert "y" not in cache

    # purge 清理过期项（验证 purge 逻辑未被意外改动）
    cache.purge()
    assert cache.get("x") is None
    assert cache.get("y") is None
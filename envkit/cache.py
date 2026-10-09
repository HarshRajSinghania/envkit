"""带过期时间的缓存。"""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import Any


class TTLCache:
    """一个简单的 TTL 缓存。

    :param ttl: 存活秒数，必须为正
    :param clock: 时间源，默认 ``time.monotonic``；
        测试时可以注入一个可控的假时钟，从而稳定地验证过期行为

    示例::

        >>> cache = TTLCache(ttl=60)
        >>> cache.set("a", 1)
        >>> cache.get("a")
        1
        >>> cache.get("missing") is None
        True
    """

    def __init__(self, ttl: float, *, clock: Callable[[], float] | None = None) -> None:
        if ttl <= 0:
            raise ValueError("ttl 必须为正数")
        self._ttl = ttl
        self._clock = clock or time.monotonic
        self._store: dict[str, tuple[Any, float]] = {}
        self._hits = 0
        self._misses = 0

    def set(self, key: str, value: Any) -> None:
        """写入一条记录，过期时间为当前时间 + ttl。"""
        expires_at = self._clock() + self._ttl
        self._store[key] = (value, expires_at)

    def get(self, key: str, default: Any = None) -> Any:
        """读取 ``key``；不存在或**已过期**时返回 ``default``。"""
        entry = self._store.get(key)
        if entry is None:
            self._misses += 1
            return default

        value, expires_at = entry
        if self._clock() >= expires_at:
            self._misses += 1
            return default

        self._hits += 1
        return value

    def purge(self) -> int:
        """删除所有已过期的记录，返回删除条数。"""
        now = self._clock()
        expired = [key for key, (_, expires_at) in self._store.items() if now >= expires_at]
        for key in expired:
            self._store.pop(key)
        return len(expired)

    def stats(self) -> dict[str, int]:
        """返回 ``{"hits":…, "misses":…, "size":…}``。"""
        return {"hits": self._hits, "misses": self._misses, "size": len(self._store)}

    def __contains__(self, key: str) -> bool:
        entry = self._store.get(key)
        if entry is None:
            return False
        return self._clock() < entry[1]

import pytest
from envkit import parse_offset


def test_parse_offset_positive():
    """既有行为：正号应正确解析为 480"""
    assert parse_offset("+08:00") == 480


def test_parse_offset_negative_05_30():
    """核心缺陷：负号被丢弃，期望 -330"""
    assert parse_offset("-05:30") == -330


def test_parse_offset_negative_00_45():
    """核心缺陷：负号被丢弃，期望 -45"""
    assert parse_offset("-00:45") == -45


def test_parse_offset_z():
    """既有行为：Z 应返回 0"""
    assert parse_offset("Z") == 0


def test_parse_offset_unsigned():
    """回归断言：无符号默认按正数处理，修复后不应改变"""
    assert parse_offset("03:00") == 180

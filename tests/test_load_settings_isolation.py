import pytest
from envkit import load_settings


def test_issue_4_nested_dict_mutation():
    """精确复现正文用例：修改返回值的嵌套字段，不应污染 defaults"""
    defaults = {"db": {"host": "localhost", "port": 5432}}
    settings = load_settings(defaults, env={})
    settings["db"]["host"] = "prod-db"
    assert defaults["db"]["host"] == "localhost", "defaults 被意外污染"


def test_issue_4_nested_dict_reference():
    """根因验证：嵌套 dict 不应共享引用"""
    defaults = {"db": {"host": "localhost"}}
    settings = load_settings(defaults, env={})
    assert defaults["db"] is not settings["db"], "嵌套字典应为深拷贝，不能共享引用"


def test_issue_4_list_in_dict_mutation():
    """期望修复要求：嵌套 list 等可变值也不能共享引用"""
    defaults = {"servers": ["node1", "node2"]}
    settings = load_settings(defaults, env={})
    settings["servers"].append("node3")
    assert defaults["servers"] == ["node1", "node2"], "defaults 中的 list 被意外污染"


def test_regression_flat_dict_isolation():
    """回归断言：扁平字典的隔离行为保持不变"""
    defaults = {"key": "value"}
    settings = load_settings(defaults, env={})
    settings["key"] = "new_value"
    assert defaults["key"] == "value"
    assert defaults is not settings


def test_regression_multiple_calls_no_pollution():
    """回归断言：多次调用 load_settings 不会因 defaults 污染而串味"""
    defaults = {"db": {"host": "localhost"}}
    s1 = load_settings(defaults, env={})
    s1["db"]["host"] = "polluted"
    s2 = load_settings(defaults, env={})
    assert s2["db"]["host"] == "localhost", "后续调用拿到了被污染的 defaults"
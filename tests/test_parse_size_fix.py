import pytest
from envkit import parse_size

@pytest.mark.parametrize("text, expected", [
    # 核心缺陷：无空格写法（修复前必抛 ValueError）
    ("512KB", 512_000),
    ("1.5GB", 1_500_000_000),
    # 回归断言：带空格写法（修复前后均应通过）
    ("1.5 MB", 1_500_000),
    ("512 KB", 512_000),
    ("2 TB", 2_000_000_000_000),
    # 回归断言：纯数字写法（修复前后均应通过）
    ("4096", 4096),
    # 回归断言：单字母别名（修复前后均应通过）
    ("2 G", 2_000_000_000),
])
def test_parse_size_all_variants(text, expected):
    assert parse_size(text) == expected

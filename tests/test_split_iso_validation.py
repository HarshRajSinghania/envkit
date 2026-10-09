import pytest
from envkit import split_iso

# 回归断言：合法常规输入应正常解析，保持向后兼容
def test_split_iso_valid_normal():
    res = split_iso("2024-03-05T08:30:00+08:00")
    assert res == {
        'year': 2024, 'month': 3, 'day': 5,
        'hour': 8, 'minute': 30, 'second': 0, 'offset': 480
    }

# 回归断言：边界值 23:59:59 必须合法，不可误伤
def test_split_iso_valid_boundary():
    res = split_iso("2024-03-05T23:59:59+08:00")
    assert res['hour'] == 23
    assert res['minute'] == 59
    assert res['second'] == 59

# 缺陷复现：hour 越界 (24) - 期望修复用例
def test_split_iso_invalid_hour_24():
    with pytest.raises(ValueError, match="非法时间"):
        split_iso("2024-03-05T24:00:00+08:00")

# 缺陷复现：hour 越界 (25) - 复现步骤用例
def test_split_iso_invalid_hour_25():
    with pytest.raises(ValueError, match="非法时间"):
        split_iso("2024-03-05T25:00:00+08:00")

# 缺陷复现：minute 越界 (75) - 复现步骤与期望修复用例
def test_split_iso_invalid_minute_75():
    with pytest.raises(ValueError, match="非法时间"):
        split_iso("2024-03-05T08:75:00+08:00")

# 缺陷复现：second 越界 (99) - 期望修复用例
def test_split_iso_invalid_second_99():
    with pytest.raises(ValueError, match="非法时间"):
        split_iso("2024-03-05T08:30:99+08:00")
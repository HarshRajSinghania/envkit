from envkit import get_bool

def test_get_bool_case_insensitivity_and_regression():
    # 1. 复现步骤：小写 true（基线，修复前后均应通过）
    assert get_bool("DEBUG", default=False, env={"DEBUG": "true"}) is True

    # 2. 复现步骤：大写 TRUE（缺陷，修复前返回 False，修复后返回 True）
    assert get_bool("DEBUG", default=False, env={"DEBUG": "TRUE"}) is True

    # 3. 复现步骤：首字母大写 True（缺陷，修复前返回 False，修复后返回 True）
    assert get_bool("DEBUG", default=False, env={"DEBUG": "True"}) is True

    # 4. 期望修复断言：TRUE -> True
    assert get_bool("F", env={"F": "TRUE"}) is True

    # 5. 期望修复断言：True -> True
    assert get_bool("F", env={"F": "True"}) is True

    # 6. 期望修复断言：OFF -> False（回归：大写 false 词应正确识别）
    assert get_bool("F", env={"F": "OFF"}) is False

    # 7. 期望修复断言：yes -> True（回归：小写 yes 应正确识别）
    assert get_bool("F", env={"F": "yes"}) is True

    # 8. 回归断言：未知值严格回退到 default
    assert get_bool("F", default=True, env={"F": "random_str"}) is True
    assert get_bool("F", default=False, env={"F": "random_str"}) is False

    # 9. 回归断言：原有小写 false 词识别不受影响
    assert get_bool("F", env={"F": "false"}) is False
    assert get_bool("F", env={"F": "0"}) is False
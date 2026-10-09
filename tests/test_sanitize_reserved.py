import pytest
from envkit import sanitize_filename


class TestSanitizeFilenameReserved:
    @pytest.mark.parametrize("inp, expected", [
        # 复现步骤明确给出的输入/期望对
        ("CON", "_CON"),
        ("nul.txt", "_nul.txt"),
        ("COM1", "_COM1"),
        # 期望修复中明确列出的断言
        ("con", "_con"),
        ("NUL", "_NUL"),
        # 兼容性/回归断言（正文强调“其余用例不受影响”）
        ("report.txt", "report.txt"),
        ("console.txt", "console.txt"),
        # 补充标准保留名以验证大小写不敏感与扩展名处理逻辑
        ("aux", "_aux"),
        ("PRN", "_PRN"),
        ("LPT1", "_LPT1"),
        ("com9.log", "_com9.log"),
    ])
    def test_reserved_and_normal_names(self, inp, expected):
        assert sanitize_filename(inp) == expected

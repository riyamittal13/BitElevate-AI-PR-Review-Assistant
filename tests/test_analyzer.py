
from analyzer import analyze_code


def test_valid_python_code():
    code = "x = 10\nprint(x)"

    result = analyze_code(code, "sample.py")

    assert result["error"] is None
    assert isinstance(result["ruff_findings"], list)
    assert isinstance(result["bandit_findings"], list)


def test_invalid_python_syntax():
    code = "def hello(:"

    result = analyze_code(code, "sample.py")

    assert result["error"] is not None
    assert "syntax error" in result["error"].lower()


def test_unsupported_file_type():
    code = "print('Hello')"

    result = analyze_code(code, "sample.js")

    assert result["error"] == "Only Python files are supported."

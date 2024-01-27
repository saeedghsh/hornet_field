# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
import subprocess

import pytest


def test_main_entry_point_script_smoke_test():
    cmd = ["python3", "-m", "main", "--max-iteration", str(100)]
    result = subprocess.run(cmd, capture_output=True, check=False)
    assert result.returncode == 0


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))

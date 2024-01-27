# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
import os
import subprocess

import pytest


def test_main_entry_point_script_smoke_test():
    cmd = ["python3", "-m", "main", "--max-iteration", str(10)]
    result = subprocess.run(cmd, capture_output=True, check=False)
    assert result.returncode == 0


def _contains_png(dir_path: str):
    for filename in os.listdir(dir_path):
        if filename.lower().endswith(".png"):
            return True
    return False


def test_main_entry_point_script_file_save(tmp_path: str):
    cmd = [
        "python3",
        "-m",
        "main",
        "--save-to-file",
        "--output-dir",
        tmp_path,
    ]
    result = subprocess.run(cmd, capture_output=True, check=False)
    assert result.returncode != 0

    cmd.extend(["--max-iteration", str(1)])
    result = subprocess.run(cmd, capture_output=True, check=False)
    assert result.returncode == 0
    assert _contains_png(tmp_path)


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))

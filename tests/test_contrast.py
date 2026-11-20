# 스킬의 대비 계산 스크립트 (PRD F3-1). 기대값은 WCAG 2.2 상대 휘도 정의로 손으로 구한 값이다.
import subprocess
import sys

import pytest
from test_generate import _REPO

_SCRIPT = _REPO / "designarche" / "scripts" / "contrast.py"


def contrast(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-I", str(_SCRIPT), *args], check=False, capture_output=True, text=True, encoding="utf-8"
    )


@pytest.mark.parametrize("fg, bg, ratio, text, large", [
    ("#000000", "#ffffff", "21.00", "pass", "pass"),
    ("#777777", "#ffffff", "4.48", "fail", "pass"),   # 4.5 바로 아래
    ("#767676", "#ffffff", "4.54", "pass", "pass"),   # 4.5 바로 위
    ("#ffffff", "#777777", "4.48", "fail", "pass"),   # 순서를 바꿔도 같다
    ("#999", "#fff", "2.85", "fail", "fail"),         # 세 자리 표기
])
def test_ratio_and_verdicts(fg, bg, ratio, text, large):
    result = contrast(fg, bg)
    assert result.returncode == 0, result.stderr
    assert result.stdout.split() == [f"{ratio}:1", f"text={text}", f"large={large}"]


@pytest.mark.parametrize("bad", [("#12345", "#ffffff"), ("red", "#ffffff"), ("#000000",)])
def test_bad_input_is_an_error(bad):
    result = contrast(*bad)
    assert result.returncode != 0
    assert result.stdout == ""

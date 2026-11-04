# 프로젝트에 만든 테마 파일이 원본 폴더 없이 혼자 동작하는지.
import json
import subprocess
import sys
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parent.parent
_GENERATE = _REPO / "skill" / "generate.py"
_CHECK = """
import json, sys
from importlib import import_module
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QApplication, QCheckBox
theme = import_module(sys.argv[1])
app = QApplication([])
theme.apply_theme(app, "light")
box = QCheckBox()
box.setChecked(True)
box.adjustSize()
image = box.grab().toImage()
mark = QColor(theme.color("on_accent")).rgb()
drawn = any(image.pixel(x, y) == mark for x in range(image.width()) for y in range(image.height()))
print(json.dumps({"tokens": theme.TOKENS, "drawn": drawn, "exists": theme.icon_path("radio").exists()}))
"""


def generate(project: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(_GENERATE), str(project), *args], check=False, capture_output=True, text=True, encoding="utf-8"
    )


@pytest.mark.parametrize("args, module, theme_file, icons", [
    ((), "ui.theme", "ui/theme.py", "assets/icons"),
    (("--theme", "theme.py", "--icons", "icons"), "theme", "theme.py", "icons"),
    (("--theme", "app/ui/theme.py", "--icons", "app/res"), "app.ui.theme", "app/ui/theme.py", "app/res"),
])
def test_generated_theme_works_alone(tmp_path, args, module, theme_file, icons):
    project = tmp_path / "앱 폴더"
    assert generate(project, *args).returncode == 0

    files = {p.relative_to(project).as_posix() for p in project.rglob("*") if p.is_file()}
    assert theme_file in files
    assert {p for p in files if p != theme_file} == {f"{icons}/{s.name}" for s in (_REPO / "graphite_paper/icons").iterdir()}

    code = (project / theme_file).read_text(encoding="utf-8")
    assert "graphite_paper" not in code
    assert "tokens.json" not in code

    # 원본 저장소를 볼 수 없는 위치에서 import 한다
    result = subprocess.run(
        [sys.executable, "-c", _CHECK, module], check=False, cwd=project, capture_output=True, text=True, encoding="utf-8"
    )
    assert result.returncode == 0, result.stderr
    out = json.loads(result.stdout.splitlines()[-1])
    assert out["tokens"] == json.loads((_REPO / "graphite_paper/tokens.json").read_text(encoding="utf-8"))
    assert out["drawn"] and out["exists"]


def test_existing_files_stop_without_force(tmp_path):
    theme_file = tmp_path / "ui" / "theme.py"
    theme_file.parent.mkdir()
    theme_file.write_text("# 앱의 파일\n", encoding="utf-8")

    result = generate(tmp_path)
    assert result.returncode != 0
    assert theme_file.read_text(encoding="utf-8") == "# 앱의 파일\n"
    assert not (tmp_path / "assets").exists()

    assert generate(tmp_path, "--force").returncode == 0
    assert "apply_theme" in theme_file.read_text(encoding="utf-8")


@pytest.mark.parametrize("bad", ["../theme.py", "C:/x/theme.py", "/x/theme.py"])
def test_paths_outside_project_are_refused(tmp_path, bad):
    assert generate(tmp_path, "--theme", bad).returncode != 0
    assert not list(tmp_path.iterdir())

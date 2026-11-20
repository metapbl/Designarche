# 스킬 폴더(designarche/) 하나만 다른 곳에 복사해도 동작하는지 (PRD F4-4, D043).
import re
import shutil
import subprocess
import sys

import pytest
from test_generate import _REPO, _files

_SKILL = _REPO / "designarche"


def test_copied_skill_folder_generates_same_theme(tmp_path):
    # 저장소·metarche 가 보이지 않는 곳에 스킬 폴더만 둔다 (예: ~/.agents/skills/designarche)
    skill = tmp_path / "skills" / "designarche"
    shutil.copytree(_SKILL, skill, ignore=shutil.ignore_patterns("__pycache__"))
    app = tmp_path / "app"

    result = subprocess.run(
        [sys.executable, "-I", str(skill / "scripts" / "generate.py"), str(app)],
        check=False, cwd=tmp_path, capture_output=True, text=True, encoding="utf-8",
    )

    assert result.returncode == 0, result.stderr
    assert _files(app) == _files(_REPO / "tests" / "golden")
    check = "from ui import theme; print(len(theme.TOKENS['dark']))"
    out = subprocess.run([sys.executable, "-c", check], check=True, cwd=app, capture_output=True, text=True)
    assert out.stdout.strip() == "22"


# Agent Skills 규격 (https://agentskills.io/specification) 과 D040~D043
_ALLOWED_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}


def _front_matter() -> dict[str, str]:
    lines = (_SKILL / "SKILL.md").read_text(encoding="utf-8").splitlines()
    assert lines[0] == "---"
    end = lines.index("---", 1)
    # 맨 앞 칸에서 시작하는 줄만 최상위 항목이다 (metadata 아래 줄은 들여쓴다)
    pairs = [line.split(":", 1) for line in lines[1:end] if line and not line[0].isspace()]
    return {key.strip(): value.strip() for key, value in pairs}


def test_skill_md_follows_agent_skills_spec():
    meta = _front_matter()
    assert set(meta) <= _ALLOWED_KEYS, set(meta) - _ALLOWED_KEYS
    assert re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", meta["name"]) and len(meta["name"]) <= 64
    assert meta["name"] == _SKILL.name
    assert 0 < len(meta["description"]) <= 1024
    assert len((_SKILL / "SKILL.md").read_text(encoding="utf-8").splitlines()) <= 500


def test_skill_links_point_to_files_inside_the_folder():
    for doc in _SKILL.rglob("*.md"):
        for target in re.findall(r"\]\(([^)#\s]+)", doc.read_text(encoding="utf-8")):
            if "://" in target:
                continue
            path = (doc.parent / target).resolve()
            assert path.is_relative_to(_SKILL.resolve()) and path.exists(), f"{doc.name}: {target}"


def test_skill_folder_has_no_shell_scripts_or_dev_records():
    files = [p for p in _SKILL.rglob("*") if p.is_file() and "__pycache__" not in p.parts]
    assert not [p.name for p in files if p.suffix in {".ps1", ".sh", ".bat", ".cmd"}]
    for p in files:
        if p.suffix in {".md", ".py", ".json"}:
            text = p.read_text(encoding="utf-8")
            assert "metarche" not in text.lower() and "docs/" not in text, p.name


# 원칙·플랫폼 규칙·징후·검사 (PRD F1~F3, D013, D026, D027)
_PLATFORMS = ["web", "desktop", "mobile", "terminal"]
_GRADED = re.compile(r"- `(must-fix|should-fix|consider)` \S")
# 계획 2 의 작업이 그 파일을 쓰면 여기서 지운다. strict 라서 다 쓰고 남겨 두면 실패한다
_TODO = {"SKILL.md", *_PLATFORMS}


def _todo(name: str):
    mark = pytest.mark.xfail(strict=True, reason="계획 2 작업 3~8 에서 씀")
    return pytest.param(name, marks=mark) if name in _TODO else name


def _section(text: str, title: str) -> list[str]:
    lines = text.splitlines()
    start = lines.index(f"## {title}") + 1
    end = next((i for i in range(start, len(lines)) if lines[i].startswith("## ")), len(lines))
    return lines[start:end]


@pytest.mark.parametrize("name", [_todo("SKILL.md")])
def test_skill_md_routes_to_every_platform_file(name):
    skill = (_SKILL / name).read_text(encoding="utf-8")
    for ref in [*_PLATFORMS, "slop-signs"]:
        assert f"(references/{ref}.md)" in skill, ref


@pytest.mark.parametrize("name", [_todo(n) for n in _PLATFORMS])
def test_platform_file_has_rules_signs_and_checks(name):
    text = (_SKILL / "references" / f"{name}.md").read_text(encoding="utf-8")
    for title in ("Rules", "Slop signs", "Check"):
        assert _section(text, title), title


@pytest.mark.parametrize("name", [_todo(n) for n in [*_PLATFORMS, "slop-signs"]])
def test_every_slop_sign_has_a_grade(name):
    text = (_SKILL / "references" / f"{name}.md").read_text(encoding="utf-8")
    items = [line for line in _section(text, "Slop signs") if line.startswith("- ")]
    assert items
    assert all(_GRADED.match(line) for line in items), [line for line in items if not _GRADED.match(line)]

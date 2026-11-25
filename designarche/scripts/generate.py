# 앱 프로젝트에 테마를 넣는다: 색표가 든 테마 파일 하나와 아이콘 폴더. 원본 폴더 이름은 남지 않는다.
# 실행: python generate.py <프로젝트> [--theme ui/theme.py] [--icons assets/icons] [--force]

import argparse
import json
import shutil
import sys
from pathlib import Path, PurePosixPath

SOURCE = Path(__file__).resolve().parent.parent / "assets" / "graphite_paper"


def relative(value: str) -> PurePosixPath:
    path = PurePosixPath(value.replace("\\", "/"))
    if path.is_absolute() or ":" in value or ".." in path.parts:
        sys.exit(f"Must be a relative path inside the project: {value}")
    return path


def render(theme: PurePosixPath, icons: PurePosixPath) -> str:
    """원본 theme.py 에서 색표 읽기와 아이콘 경로만 프로젝트에 맞게 바꾼다."""
    code = (SOURCE / "theme.py").read_text(encoding="utf-8")
    tokens = json.loads((SOURCE / "tokens.json").read_text(encoding="utf-8"))
    version = (SOURCE / "__init__.py").read_text(encoding="utf-8").split('"')[1]
    root = "Path(__file__).resolve()" + ".parent" * len(theme.parts)
    icon_dir = " / ".join([root, *(f'"{part}"' for part in icons.parts)])
    for old, new in (
        ("import json\n", ""),
        (
            "# 색 원본은 tokens.json. 창별 QSS 는",
            f"# Graphite/Paper 테마 {version}. Copyright (c) 2026 metapbl. MIT License.\n# 창별 QSS 는",
        ),
        ('_DIR = Path(__file__).resolve().parent\n', ""),
        (
            'TOKENS: dict = json.loads((_DIR / "tokens.json").read_text(encoding="utf-8"))\n',
            f"TOKENS: dict = {json.dumps(tokens, indent=4)}\n",
        ),
        ('_ICONS = _DIR / "icons"\n', f"_ICONS = {icon_dir}\n"),
    ):
        assert code.count(old) == 1, old
        code = code.replace(old, new)
    return code


def main() -> None:
    # 영어 콘솔(cp1252)에서도 비ASCII 경로를 출력하다 죽지 않게
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(errors="backslashreplace")  # type: ignore[union-attr]
    parser = argparse.ArgumentParser()
    parser.add_argument("project", type=Path)
    parser.add_argument("--theme", default="ui/theme.py", help="theme file to create, relative to the project")
    parser.add_argument("--icons", default="assets/icons", help="icon folder, relative to the project")
    parser.add_argument("--force", action="store_true", help="overwrite files that already exist")
    args = parser.parse_args()

    theme, icons = relative(args.theme), relative(args.icons)
    theme_file = args.project / theme
    icon_dir = args.project / icons
    svgs = sorted((SOURCE / "icons").glob("*.svg"))
    targets = [theme_file, *(icon_dir / svg.name for svg in svgs)]
    existing = [str(path) for path in targets if path.exists()]
    if existing and not args.force:
        sys.exit("Already exists, stopping (use --force to overwrite):\n" + "\n".join(existing))

    theme_file.parent.mkdir(parents=True, exist_ok=True)
    icon_dir.mkdir(parents=True, exist_ok=True)
    theme_file.write_text(render(theme, icons), encoding="utf-8", newline="\n")
    for svg in svgs:
        shutil.copyfile(svg, icon_dir / svg.name)
    print(f"{theme_file}\n{icon_dir} ({len(svgs)} icons)")


if __name__ == "__main__":
    main()

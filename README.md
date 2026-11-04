# Graphite / Paper 테마

PySide6 + PyInstaller 데스크톱 앱용 다크(Graphite)·라이트(Paper) 테마. 시스템 색 모드 따라가기와 실행 중 전환을 지원한다. 웹은 대상이 아니다.

- 확인한 환경: Windows 11, PySide6 6.12.0. **macOS 는 지원 대상이지만 실제 Mac 에서 돌려 본 적이 없다.**

- 필요: **Python 3.10 이상**, **PySide6 6.8 이상** (`QStyleHints.setColorScheme` 이 Qt 6.8 에 추가됨 — [Qt 문서](https://doc.qt.io/qt-6/qstylehints.html#setColorScheme)). 실제 실행 확인은 6.12.0 에서만 했다.
- 위젯 스타일은 Fusion 기준이다. `apply_theme` 이 처음 불릴 때 Fusion 으로 바꾼다.
- 폰트는 건드리지 않는다. 앱이 `app.setFont(...)` 로 정한다.

## 적용 (파일 복사)

`graphite_paper/` 폴더를 프로젝트 루트에 통째로 복사한다 (`__pycache__` 는 빼고). 복사본은 직접 고치지 않는다. 앱 고유 규칙은 앱의 창 QSS 에 둔다.

```python
from PySide6.QtWidgets import QApplication
from graphite_paper import theme

app = QApplication([])
theme.apply_theme(app, "system")  # system(시스템 따라가기) / dark / light
```

Claude Code 를 쓰면 `skill/` 의 `graphite-paper-theme` 스킬이 복사부터 캡처 확인까지 진행한다. 스킬 폴더에서 저장소로 링크를 건다.

```powershell
New-Item -ItemType SymbolicLink -Path "$HOME\.claude\skills\graphite-paper-theme" -Target "<저장소>\skill"
```

```bash
ln -s "<저장소>/skill" ~/.claude/skills/graphite-paper-theme
```

원격 저장소가 없으므로 Mac 에는 이 폴더(`venv` `shots` `build` `dist` 제외)를 직접 복사한 뒤 링크를 건다.

## 창 코드에서 색 쓰기

색을 직접 쓰지 않고 `@이름` 으로 쓴다. 없는 이름은 `KeyError` 가 난다. 창이 자기 QSS 를 가지면 전환 때 다시 칠해야 한다.

```python
class MyDialog(QDialog):
    def __init__(self):
        super().__init__()
        theme.notifier.changed.connect(self._apply_style)
        self._apply_style()

    def _apply_style(self):
        self.setStyleSheet(theme.qss("QLabel#hint { color: @muted; }"))
```

연결은 위처럼 창의 메서드로 한다. 창을 지우면 연결도 함께 끊긴다. 위젯을 잡은 람다로 연결하면 그 위젯을 지운 뒤 전환할 때 `RuntimeError` 가 난다.

`notifier.changed` 는 테마가 실제로 바뀔 때만 나간다. 첫 적용 때와 같은 테마를 다시 적용할 때는 나가지 않는다. 공통 위젯 스타일과 팔레트는 모듈이 다시 칠하므로 연결이 필요 없다.

색 값 하나가 필요하면 `theme.color("accent")`, 지금 테마 이름은 `theme.current()`.

## 버튼 역할

```python
btn.setProperty("role", "primary")  # primary / secondary / danger. 없으면 secondary
```

표시 뒤에 역할을 바꾸면 `btn.style().unpolish(btn); btn.style().polish(btn)` 을 함께 부른다.

## 색 이름 규칙

대비는 WCAG 기준이고 일반 글자는 4.5 이상이어야 한다. `tests/test_theme.py` 가 아래 "글자" 쌍을 검사한다.

| 이름 | 용도 | 지킬 것 |
|---|---|---|
| `base` `surface` `raised` | 입력·목록 바탕 / 창 바탕 / 머리글 | |
| `line` `line2` | 테두리 약하게 / 강하게 | |
| `btn` `btn2` | 기본 버튼 / hover | |
| `track` | 진행률·슬라이더 바탕 | |
| `sel` | 목록 선택 행 바탕 | 위 글자는 `text` |
| `text` `text2` | 본문 / 보조 글자 | 어느 바탕에서나 가능 |
| `muted` | 설명·상태 글자 | `base` `surface` `raised` 위에 쓴다. `btn` `btn2` 위에는 쓰지 않는다 |
| `faint` | 비활성 글자, 빈 화면 안내 | **일반 글자 금지** (대비 2.5~3.6) |
| `accent` `accent2` | 강조 / hover | `accent` 글자는 `base` `surface` 위만 |
| `on_accent` | `accent` `accent2` `danger` 위 글자 | |
| `danger` | 위험 버튼, 오류 글자 | 글자는 `base` `surface` 위만 |
| `on_strong` | 진한 색 위 **큰 글자·아이콘** | 일반 글자 금지. 다크의 `danger` `success` 위 대비 3.3~3.4 |
| `success` `success2` `warn` | 막대·아이콘·큰 글자 | **라이트에서 일반 글자 금지** (2.8~4.4) |
| `ext` | 링크·확장자 같은 부가 강조 글자 | `accent` 글자와 같은 조건 |

라이트 `muted`(`#656d77`)와 `accent2`(`#0c5697`)는 대비 기준을 맞추려고 AVD 의 값에서 바꿨다. 그래서 라이트 primary 버튼은 hover 때 어두워진다.

목록 행 높이는 공통 스타일로 키우지 않는다. `::item` 에 세로 `padding`·`height` 를 주면, 항목을 채운 뒤 레이아웃에 넣은 목록에서 행이 겹친다 (6.12.0 에서 재현). 높이가 필요하면 `item.setSizeHint(...)` 나 델리게이트를 쓴다.

진행률 막대는 글자를 숨긴다. 어떤 글자색도 `track` 과 `accent` 양쪽에서 읽히지 않으므로, 퍼센트는 옆 `QLabel` 에 쓴다.

색을 바꾸려면 `graphite_paper/tokens.json` 만 고친다. `check` `radio` `up` `down` SVG 는 색을 직접 가지므로 `accent` `on_accent` `text2` 를 바꾸면 SVG 도 고친다 (테스트가 불일치를 잡는다).

## PyInstaller

아이콘과 색표는 데이터 파일이라 spec 에 넣어야 한다. 빠지면 시작할 때 `tokens.json` 을 찾지 못해 실패한다. `LICENSE` 는 MIT 고지를 배포본에 포함하기 위한 것이다. onedir·onefile 모두 Windows 에서 확인했다.

macOS 도 datas 는 같고, `--windowed` 스펙이 `.app` 을 만든다. 확인할 때는 `dist/앱.app/Contents/MacOS/앱` 을 터미널에서 실행한다. Finder 로 띄우면 환경변수가 줄어든다.

폴더를 하위 패키지에 복사했으면 양쪽 경로를 패키지 위치에 맞춘다. 예: `app/ui/graphite_paper/tokens.json` → `app/ui/graphite_paper`.

```python
a = Analysis(
    ["main.py"],
    datas=[
        ("graphite_paper/tokens.json", "graphite_paper"),
        ("graphite_paper/icons", "graphite_paper/icons"),
        ("graphite_paper/LICENSE", "graphite_paper"),
    ],
)
```

SVG 를 읽는 Qt 플러그인은 PySide6 훅이 함께 묶는다 (onedir 빌드에서 확인). 스펙에서 `qsvg` 를 `excludes` 하지 않는다.

## 갱신

복사본의 버전은 `graphite_paper/__init__.py` 의 `__version__` 이다. 새 버전은 폴더를 통째로 덮어쓰고, 색이 바뀌었으면 앱 화면을 다시 확인한다.

## 앱 설정과 연결

저장 위치와 키는 앱이 정한다. 모듈은 `mode` 문자열만 받는다.

```python
settings = QSettings("MyCompany", "MyApp")
theme.apply_theme(app, settings.value("theme_mode", "system"))

def on_mode_selected(mode: str) -> None:  # 설정 창의 라디오 등에서
    settings.setValue("theme_mode", mode)
    theme.apply_theme(QApplication.instance(), mode)
```

알 수 없는 값은 `system` 처럼 동작한다.

## 개발

```bash
# macOS 는 venv\Scripts\ 대신 venv/bin/, py 대신 python3
py -m venv venv
venv\Scripts\python -m pip install -r requirements-dev.txt
venv\Scripts\python -m pytest
venv\Scripts\ruff check .
venv\Scripts\python gallery.py
venv\Scripts\python gallery.py dark --shot shots/dark.png
```

## 라이선스

MIT. `graphite_paper/LICENSE` 참고.

---
name: graphite-paper-theme
description: Applies or updates the Graphite (dark) / Paper (light) theme in a PySide6 desktop app or PyInstaller exe/app project on Windows or macOS. Use when starting a PySide6 app that needs a theme, adding dark/light mode or system color mode following to one, restyling one with this house theme, or updating a theme generated earlier.
---

# Graphite / Paper 테마 적용

프로젝트에는 테마 파일 하나(기본 `ui/theme.py`)와 아이콘 폴더(기본 `assets/icons/`)만 생긴다. 앱의 일부로 읽히도록 원본 폴더 이름을 앱에 남기지 않는다.

원본 저장소는 이 스킬 폴더의 실제 위치(심볼릭 링크를 따라간 경로)의 한 단계 위다. 거기에 `graphite_paper/` 가 없으면 멈추고 사용자에게 경로를 묻는다. 색 이름 규칙, 버튼 역할, 설정 연결 예는 원본의 `README.md` 에 있다. 시작할 때 읽는다.

대상은 Python 3.10 이상, PySide6 6.8 이상이다. 다른 GUI 기술이면 멈추고 사용자에게 알린다. 낮은 PySide6 핀을 올려야 하면 올리기 전에 묻는다.

아래 `python` 은 앱의 가상환경 파이썬이다 (Windows `venv\Scripts\python`, macOS `venv/bin/python`).

macOS 절차는 문서 근거로 썼고 실제 Mac 에서 돌려 본 적이 없다. 처음 쓸 때는 5단계 결과를 이 사실과 함께 보고한다.

첫 줄 근처에 `Graphite/Paper 테마` 가 적힌 테마 파일이 앱에 이미 있으면 맨 아래 **갱신** 으로 간다.

## 1. 만들기

앱 구조를 보고 테마 파일과 아이콘 폴더 위치를 정한다. `ui/` 나 `assets/` 처럼 앱에 이미 있는 폴더를 따른다.

```bash
python "<원본>/skill/generate.py" "<앱 루트>" --theme ui/theme.py --icons assets/icons
```

이미 있는 파일이 있으면 아무것도 쓰지 않고 멈춘다. 그 파일이 앱의 다른 코드면 다른 경로를 고르거나 사용자에게 묻는다.

완료: `python -c "from ui import theme; print(len(theme.TOKENS['dark']))"` 가 앱 루트에서 `22` 를 출력한다 (경로를 바꿨으면 import 도 맞춘다).

## 2. 연결

`QApplication` 을 만든 직후, 창을 만들기 전에 부른다.

```python
from ui import theme
theme.apply_theme(app, mode)  # system / dark / light
```

- `app.setStyle(...)` 과 직접 만든 `QPalette`, 앱 전체 `app.setStyleSheet` 는 모듈과 충돌하므로 지운다. 앱 고유 규칙이 있었으면 창의 QSS 로 옮긴다.
- 앱에 설정 저장소가 있으면 거기에 mode 를 저장하고, 없으면 `"system"` 으로 고정하고 사용자에게 알린다.

완료: 앱이 뜨고 콘솔에 `Could not parse stylesheet` 경고가 없다.

## 3. 직접 쓴 색 옮기기

Grep 도구로 찾는다. 대소문자 무시, `*.py` `*.qss` `*.ui` 대상, 테마 파일 제외. 셸에서 `rg` 로 돌릴 때는 경로 `.` 를 꼭 붙인다 (없으면 표준 입력을 기다린다).

```text
#[0-9a-fA-F]{3,8}\b|(rgba?|hsla?|hsva?)\(|QColor\(|QPalette\b|Qt\.(GlobalColor\.)?[a-zA-Z]*(white|black|red|green|blue|cyan|magenta|yellow|gray)\b|(color|background|border[a-z-]*)\s*:[^;"']*\b(white|black|red|green|blue|cyan|magenta|yellow|orange|purple|pink|brown|gray|grey|silver|navy|teal)\b
```

`#123` 같은 이슈 번호도 걸리므로 하나씩 읽고 가른다. 각 자리를 쓰임이 같은 색 이름으로 바꾼다.

- QSS 문자열은 `@이름` 으로 적고 `theme.qss(...)` 로 감싼다. `QColor` 와 `QPainter` 는 `QColor(theme.color("이름"))`.
- 자기 색을 칠하는 창·위젯은 칠하는 코드를 메서드로 모으고 그 메서드를 `theme.notifier.changed` 에 연결한다. 커스텀 `paintEvent` 는 `self.update` 를 연결한다. 위젯을 잡은 람다는 그 위젯이 지워진 뒤 전환할 때 `RuntimeError` 를 내므로 메서드로 바꾼다.
- 공통 스타일과 같은 규칙(버튼, 입력창, 스크롤바 등)은 옮기지 않고 지운다. 강조 버튼은 `setProperty("role", "primary")`, 위험 버튼은 `"danger"`.
- 목록 행 높이는 공통 스타일이 22px 로 정한다. 앱에 다른 높이가 필요할 때만 창 QSS 의 `::item { height: ...; }` 로 둔다.
- 글자에는 `text` `text2`, `base` `surface` `raised` 위의 `muted` 를 쓴다. `faint` 와 라이트의 `success` `success2` `warn` 은 일반 글자에서 뺀다.
- 데이터의 색(차트 계열, 사용자가 고른 색, 로고)은 그대로 두고 목록으로 사용자에게 알린다.

완료: 검색 결과가 모두 "그대로 둔 색" 목록이거나 색이 아닌 자리다. `theme.qss` `theme.color` 를 부르는 창마다 다시 칠하는 메서드가 `notifier.changed` 에 연결되어 있다.

## 4. 스펙에 넣기

PyInstaller 를 쓰면 `.spec` 의 `Analysis(datas=[...])` 에 아이콘 폴더를 더한다. Windows 와 macOS 가 같고, onedir 와 onefile 도 같다. 양쪽 값은 1단계의 `--icons` 경로다.

```python
("assets/icons", "assets/icons"),
```

스펙이 없고 사용자가 실행 파일을 원하면 `pyi-makespec --windowed main.py` 로 만든다. macOS 에서는 `--windowed` 가 `.app` 을 만드는 `BUNDLE` 블록을 넣는다. 빌드는 OS 마다 그 OS 에서 한다. `excludes` 에 `qsvg` 나 `PySide6.QtSvg` 가 있으면 뺀다.

완료: 스펙에 아이콘 폴더 줄이 있다.

## 5. 캡처로 확인

`app.exec()` 바로 앞에 임시로 넣는다. `window` 는 앱의 주 창 이름으로 바꾼다.

```python
import os
if os.environ.get("THEME_SHOT"):  # 임시: 확인 후 지운다
    from pathlib import Path
    from PySide6.QtCore import QTimer
    def _shots():
        for mode in ("dark", "light"):
            theme.apply_theme(app, mode)
            app.processEvents()
            window.grab().save(str(Path(os.environ["THEME_SHOT"]) / f"{mode}.png"))
        app.quit()
    QTimer.singleShot(500, _shots)
```

저장 폴더를 만들고 그 절대 경로를 `THEME_SHOT` 에 넣어 소스 실행과 빌드 결과를 각각 돌린다. 스펙이 있으면 `pyinstaller --noconfirm 앱이름.spec` 으로 빌드한다.

- Windows onedir: `dist\앱이름\앱이름.exe`
- macOS: 터미널에서 `dist/앱이름.app/Contents/MacOS/앱이름` 을 직접 실행한다. Finder 로 띄우면 환경변수가 줄어 캡처가 돌지 않는다.

Read 로 PNG 를 열어 두 테마를 눈으로 본다. 체크 표시, 글자와 바탕의 구분, 전환 뒤 옛 테마 색이 남은 곳을 본다. 빌드 결과에서 체크 표시가 비면 아이콘 폴더나 `qsvg` 플러그인이 빠진 것이므로, 빌드 폴더에서 `check_dark.svg` 와 `*qsvg*` 를 찾아 본다. macOS `.app` 안의 데이터 위치는 문서로 확인하지 못했으니 이 실행 결과로 판단한다.

캡처는 주 창 하나만 찍는다. 대화상자, 메뉴, 제목 표시줄은 찍히지 않는다.

끝나면 임시 코드를 지우고 **다시 빌드한다**. 그러지 않으면 배포본에 임시 코드가 남는다.

완료: 소스와 빌드 결과 양쪽의 두 PNG 를 확인해 사용자에게 보냈고, 앱 코드에 `THEME_SHOT` 이 없으며, 지운 뒤 다시 빌드했다. 찍히지 않은 화면과 돌리지 못한 OS 는 그대로 알린다.

## 6. 테스트

프로젝트 테스트와 린터를 돌린다. 색 문자열을 단언하던 테스트는 `theme.color(...)` 로 고친다.

완료: 결과를 출력 그대로 보고한다.

## 갱신

1. 테마 파일 머리의 버전과 원본 `graphite_paper/__init__.py` 의 `__version__` 을 비교한다. 같으면 끝낸다.
2. 빈 임시 폴더에 앱과 같은 `--theme` `--icons` 로 새 버전을 만들어 앱의 파일과 비교한다. 차이에는 원본의 변경도 섞여 있으니 원본의 `git log` 와 함께 읽는다. 앱에서 직접 고친 부분은 사용자에게 알리고, 앱 고유 규칙은 창 QSS 로 옮긴다.
3. 앱 루트에 `--force` 로 다시 만든다.
4. 5·6단계를 돌린다.

완료: 테마 파일 머리의 버전이 원본과 같고, 5·6단계의 완료 조건을 만족한다.

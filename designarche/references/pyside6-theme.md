# Graphite / Paper theme for PySide6

Applies or updates the Graphite (dark) / Paper (light) theme in a PySide6 desktop app or a PyInstaller exe/app project on Windows or macOS.

The app gets only one theme file (default `ui/theme.py`) and one icon folder (default `assets/icons/`). Nothing in the app names this skill or its source folder, so the files read as part of the app.

Paths below are relative to this skill folder: the generator is `scripts/generate.py`, the theme source is `assets/graphite_paper/`. Write `<skill>` for this skill folder's absolute path when you run a command from the app.

Targets: Python 3.10 or later, PySide6 6.8 or later. If the app uses another GUI toolkit, stop and tell the user. If a low PySide6 pin has to be raised, ask before raising it.

`python` below is the app's virtual-environment Python: `venv\Scripts\python` on Windows, `venv/bin/python` on macOS and Linux.

The macOS steps come from documentation and have not been run on a real Mac. The first time you use them, report the step 5 results together with that fact.

If the app already has a theme file with `Graphite/Paper` near its first line, go to **Update** at the end.

## 1. Generate

Look at the app's layout and choose where the theme file and the icon folder go. Follow folders the app already has, such as `ui/` or `assets/`.

```text
python "<skill>/scripts/generate.py" "<app root>" --theme ui/theme.py --icons assets/icons
```

If a target file already exists, it writes nothing and stops. If that file is other app code, pick another path or ask the user. `--force` overwrites.

Done when: run from the app root, `python -c "from ui import theme; print(len(theme.TOKENS['dark']))"` prints `22` (adjust the import if you changed the path).

## 2. Connect

Call it right after creating the `QApplication`, before creating any window.

```python
from ui import theme
theme.apply_theme(app, mode)  # "system" / "dark" / "light"
```

- Remove `app.setStyle(...)`, hand-made `QPalette`s and any app-wide `app.setStyleSheet`; they fight the module. Move app-specific rules into the window's own QSS.
- If the app has a settings store, save `mode` there (see **Settings**). If not, fix it to `"system"` and tell the user.

Done when: the app starts and the console shows no `Could not parse stylesheet` warning.

## 3. Move hard-coded colors

Search with a regular expression, case-insensitive, over `*.py`, `*.qss` and `*.ui`, excluding the theme file. When running `rg` in a shell, always pass the path `.` (without it, rg waits on standard input).

```text
#[0-9a-fA-F]{3,8}\b|(rgba?|hsla?|hsva?)\(|QColor\(|QPalette\b|Qt\.(GlobalColor\.)?[a-zA-Z]*(white|black|red|green|blue|cyan|magenta|yellow|gray)\b|(color|background|border[a-z-]*)\s*:[^;"']*\b(white|black|red|green|blue|cyan|magenta|yellow|orange|purple|pink|brown|gray|grey|silver|navy|teal)\b
```

Issue numbers such as `#123` match too, so read each hit. Replace each color with the color name of the same role (**Color names**).

- In QSS strings write `@name` and wrap the string in `theme.qss(...)`. For `QColor` and `QPainter`, use `QColor(theme.color("name"))`.
- A window or widget that paints its own colors collects that code in one method and connects the method to `theme.notifier.changed`. A custom `paintEvent` connects `self.update`. A lambda that captures a widget raises `RuntimeError` when the theme changes after the widget is deleted, so use a method.
- Rules the shared style already covers (buttons, inputs, scroll bars, and so on) are deleted, not moved. Emphasized buttons get `setProperty("role", "primary")`, destructive ones `"danger"` (**Button roles**).
- The shared style sets list rows to 22 px. Only if the app needs another height, set `::item { height: ...; }` in the window QSS.
- For text use `text` and `text2`, and `muted` only on `base`, `surface` or `raised`. Keep `faint`, and in light mode `success`, `success2` and `warn`, out of normal text.
- Leave data colors (chart series, user-picked colors, logos) as they are, and list them for the user.

Done when: every remaining search hit is in the "left as is" list or is not a color, and every window that calls `theme.qss` or `theme.color` has its repaint method connected to `notifier.changed`.

## 4. Add to the spec

If the app uses PyInstaller, add the icon folder to `Analysis(datas=[...])` in the `.spec`. It is the same on Windows and macOS, for onedir and onefile. Both values are the `--icons` path from step 1.

```python
("assets/icons", "assets/icons"),
```

If there is no spec and the user wants an executable, create one with `pyi-makespec --windowed main.py`. On macOS `--windowed` adds the `BUNDLE` block that builds the `.app`. Build on each OS for that OS. If `excludes` lists `qsvg` or `PySide6.QtSvg`, remove it; the SVG plugin draws the check marks.

Done when: the spec has the icon folder line.

## 5. Check with screenshots

Insert this temporarily right before `app.exec()`. Replace `window` with the app's main window.

```python
import os
if os.environ.get("THEME_SHOT"):  # temporary: remove after checking
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

Create an output folder, put its absolute path in the `THEME_SHOT` environment variable, and run both the source and the build. With a spec, build with `pyinstaller --noconfirm <app>.spec`.

- Windows onedir: `dist\<app>\<app>.exe`
- macOS: run `dist/<app>.app/Contents/MacOS/<app>` directly from a terminal. Launched from Finder, the environment is reduced and the screenshots do not run.

Open the PNGs and look at both themes: the check marks, text against its background, and any color left over from the previous theme after switching. If the check marks are empty in the build, the icon folder or the `qsvg` plugin is missing; look for `check_dark.svg` and `*qsvg*` in the build folder. Where data files land inside a macOS `.app` was not confirmed from documentation, so judge by this run.

The screenshot covers the main window only. Dialogs, menus and the title bar are not captured.

When done, remove the temporary code and **build again**, or the shipped build keeps it.

Done when: you have looked at both PNGs from both the source and the build and sent them to the user, the app code has no `THEME_SHOT`, and you rebuilt after removing it. Say which screens were not captured and which OS was not run.

## 6. Tests

Run the project's tests and linter. Tests that asserted color strings switch to `theme.color(...)`.

Done when: you report the results as printed.

## Update

1. Compare the version in the theme file's header with `__version__` in `assets/graphite_paper/__init__.py`. If they match, stop.
2. Generate the new version into an empty temporary folder with the app's `--theme` and `--icons`, and compare it with the app's files. The difference mixes changes in the theme with edits made in the app; if the skill came from a git repository, read its history alongside. Tell the user about direct edits in the app, and move app-specific rules into window QSS.
3. Generate again at the app root with `--force`.
4. Run steps 5 and 6.

Done when: the header version matches the source and steps 5 and 6 are done.

## Using colors in window code

Write colors as `@name`, never as values. An unknown name raises `KeyError`. A window that has its own QSS must repaint on a theme change.

```python
class MyDialog(QDialog):
    def __init__(self):
        super().__init__()
        theme.notifier.changed.connect(self._apply_style)
        self._apply_style()

    def _apply_style(self):
        self.setStyleSheet(theme.qss("QLabel#hint { color: @muted; }"))
```

Connect a method of the window as above; deleting the window also drops the connection. `notifier.changed` fires only when the theme actually changes, not on the first apply or when the same theme is applied again. The shared widget style and the palette are repainted by the module and need no connection.

One color value: `theme.color("accent")`. The current theme name: `theme.current()`.

## Button roles

```python
btn.setProperty("role", "primary")  # primary / secondary / danger; secondary when unset
```

If you change the role after the button is shown, also call `btn.style().unpolish(btn); btn.style().polish(btn)`.

- An enabled default button is outlined: `surface` background, a strong `muted` outline and `text` lettering. Only disabled buttons are filled gray (`raised` background, `faint` lettering, `line` outline), following the Windows 11 convention that a gray fill reads as "cannot press". Filled colors are only for `primary`, `danger` and checked toggle buttons (`setCheckable(True)`).
- Keyboard focus shows as a 2 px ring (`accent` on default buttons, check boxes and radio buttons; `on_accent` on filled buttons). Padding shrinks by the same amount, so the button keeps its size.
- Buttons, check boxes and radio buttons take focus from Tab only, as on Windows 11 (`apply_theme` changes Qt's default `StrongFocus` to `TabFocus`), so a clicked button keeps no ring. A button that must take focus on click sets a policy other than `StrongFocus` itself, such as `ClickFocus`.
- Outside dialogs, a focused `QPushButton` also presses on Enter (Qt's default is Space only). Inside dialogs Qt's default-button and `autoDefault` rules apply unchanged.
- A window's style sheet beats the application style sheet regardless of selector specificity. Restyling `QPushButton` in window QSS also overrides the role buttons, so leave button shapes to the shared style.

## Color names

Contrast follows WCAG; normal text needs at least 4.5:1.

| Name | Use | Keep to |
|---|---|---|
| `base` `surface` `raised` | input and list background / window background / headers | |
| `line` `line2` | weak / strong borders | outlines on a white `surface` (group boxes, cards, lists) use `line2` |
| `btn` `btn2` | palette Button / scroll bar handle | the shared button QSS no longer uses them |
| `track` | background of bars the app draws | shared progress and slider grooves use `line2` (light `track` disappears on white) |
| `sel` | selected list row background | text on it is `text` |
| `text` `text2` | body / secondary text | on any background |
| `muted` | descriptions, status text | on `base` `surface` `raised` only, never on `btn` `btn2` |
| `faint` | disabled text, empty-state hints | **never normal text** (contrast 2.5–3.6) |
| `accent` `accent2` | emphasis / hover | `accent` text only on `base` `surface` |
| `on_accent` | text on `accent` `accent2` `danger` | |
| `danger` | destructive buttons, error text | text only on `base` `surface` |
| `on_strong` | **large text and icons** on strong colors | never normal text; 3.3–3.4 on dark `danger` `success` |
| `success` `success2` `warn` | bars, icons, large text | **never normal text in light mode** (2.8–4.4) |
| `ext` | links, file extensions and similar secondary emphasis | same as `accent` text |

Progress bars hide their text, because no text color reads on both `line2` and `accent`; put the percentage in a `QLabel` next to it.

## Settings

The app chooses where and under which key to store the mode; the module only takes the `mode` string.

```python
settings = QSettings("MyCompany", "MyApp")
theme.apply_theme(app, settings.value("theme_mode", "system"))

def on_mode_selected(mode: str) -> None:  # e.g. from radio buttons in a settings window
    settings.setValue("theme_mode", mode)
    theme.apply_theme(QApplication.instance(), mode)
```

Unknown values behave like `"system"`.

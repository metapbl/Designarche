# 다크(Graphite)·라이트(Paper) 테마 — PySide6 6.8 이상 (QStyleHints.setColorScheme).
# 색 원본은 tokens.json. 창별 QSS 는 @이름 으로 적어 qss() 로 바꾼다.
# 설정 저장은 앱이 맡는다. 이 모듈은 mode 값만 받는다.

import json
import re
from pathlib import Path

from PySide6.QtCore import QObject, Qt, Signal
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QApplication

_DIR = Path(__file__).resolve().parent
TOKENS: dict = json.loads((_DIR / "tokens.json").read_text(encoding="utf-8"))

_current: dict = TOKENS["dark"]
_name: str | None = None  # 지금 칠해진 테마. 처음 적용 전에는 None
_mode = "system"
_listening = False


class _Notifier(QObject):
    changed = Signal()  # 테마가 실제로 바뀜 — 자기 QSS 를 가진 창이 다시 칠한다


notifier = _Notifier()


def qss(css: str) -> str:
    """QSS 의 @이름 을 현재 테마 색으로 바꾼다. 없는 이름은 KeyError."""
    return re.sub(r"@(\w+)", lambda m: _current[m.group(1)], css)


def color(name: str) -> str:
    """현재 테마의 색 하나."""
    return _current[name]


def current() -> str | None:
    """지금 칠해진 테마 이름(dark/light). 처음 적용 전에는 None."""
    return _name


def resolve(mode: str, scheme: Qt.ColorScheme) -> str:
    """설정값과 Windows 색 모드로 쓸 테마를 정한다. 알 수 없으면 다크."""
    if mode in TOKENS:
        return mode
    return "light" if scheme == Qt.ColorScheme.Light else "dark"


def icon_path(kind: str, name: str | None = None) -> Path:
    """테마별 아이콘(check, radio, up, down) 경로. SVG 는 색을 직접 가지므로 테마마다 파일이 다르다."""
    return _DIR / "icons" / f"{kind}_{name or _name or 'dark'}.svg"


# 역할 버튼: QPushButton 에 setProperty("role", "primary" | "danger"). 역할이 없거나 "secondary" 면 기본 모양.
_APP_QSS = """
QPushButton {
    background: @btn; color: @text2; border: 1px solid transparent; border-radius: 6px; padding: 6px 14px;
}
QPushButton:hover { background: @btn2; }
QPushButton:pressed { background: @line2; }
QPushButton:focus { border: 1px solid @accent; }
QPushButton[role="primary"] { background: @accent; color: @on_accent; font-weight: bold; }
QPushButton[role="primary"]:hover { background: @accent2; }
QPushButton[role="primary"]:pressed { background: @accent; }
QPushButton[role="primary"]:focus { border: 1px solid @text; }
/* 글자는 on_strong 이 아니라 on_accent: 다크에서 on_strong 은 danger 위 대비가 3.3 이다 */
QPushButton[role="danger"] { background: @danger; color: @on_accent; font-weight: bold; }
QPushButton[role="danger"]:hover, QPushButton[role="danger"]:focus { border: 1px solid @text; }
QPushButton:disabled, QPushButton[role="primary"]:disabled, QPushButton[role="danger"]:disabled {
    background: @raised; color: @faint; border: 1px solid transparent;
}

QLineEdit, QPlainTextEdit, QTextEdit, QAbstractSpinBox, QComboBox {
    background: @base; color: @text; border: 1px solid @line2; border-radius: 4px; padding: 4px 8px;
    selection-background-color: @accent; selection-color: @on_accent;
}
QLineEdit:focus, QPlainTextEdit:focus, QTextEdit:focus, QAbstractSpinBox:focus, QComboBox:focus {
    border: 1px solid @accent;
}
QLineEdit:disabled, QPlainTextEdit:disabled, QTextEdit:disabled, QAbstractSpinBox:disabled, QComboBox:disabled {
    background: @surface; color: @faint; border: 1px solid @line;
}

QComboBox::drop-down { border: none; width: 20px; }
QComboBox::down-arrow { image: url("%down%"); width: 10px; height: 10px; }
QAbstractSpinBox::up-button, QAbstractSpinBox::down-button { border: none; background: transparent; width: 18px; }
QAbstractSpinBox::up-button:hover, QAbstractSpinBox::down-button:hover { background: @raised; }
QAbstractSpinBox::up-arrow { image: url("%up%"); width: 10px; height: 10px; }
QAbstractSpinBox::down-arrow { image: url("%down%"); width: 10px; height: 10px; }

QAbstractItemView {
    background: @base; alternate-background-color: @surface; color: @text;
    border: 1px solid @line; border-radius: 6px; outline: 0; gridline-color: @line;
}
QAbstractItemView:focus { border: 1px solid @accent; }
/* 세로 padding·height 는 넣지 않는다: 항목을 채운 뒤 레이아웃에 넣은 목록은 행 간격이 그대로라 행이 겹친다 */
QAbstractItemView::item { padding: 0 6px; }
QAbstractItemView::item:hover { background: @raised; }
QAbstractItemView::item:selected { background: @sel; color: @text; }
QAbstractItemView:disabled { color: @faint; }
QHeaderView { background: @raised; }
QHeaderView::section {
    background: @raised; color: @text2; border: none; border-right: 1px solid @line; border-bottom: 1px solid @line;
    padding: 6px;
}
QTableCornerButton::section { background: @raised; border: none; }

/* 글자는 숨긴다: 어떤 글자색도 track 과 accent 양쪽에서 읽히지 않는다. 퍼센트는 옆 QLabel 로 */
QProgressBar { background: @track; color: transparent; border: none; border-radius: 3px; max-height: 6px; }
QProgressBar::chunk { background: @accent; border-radius: 3px; }

QGroupBox { color: @text2; border: 1px solid @line; border-radius: 6px; margin-top: 8px; padding: 12px 8px 8px 8px; }
QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 4px; }

QSlider::groove:horizontal { background: @track; height: 6px; border-radius: 3px; }
QSlider::groove:vertical { background: @track; width: 6px; border-radius: 3px; }
QSlider::sub-page:horizontal, QSlider::add-page:vertical { background: @accent; border-radius: 3px; }
QSlider::handle:horizontal, QSlider::handle:vertical {
    background: @accent; width: 12px; height: 12px; border: 2px solid @surface; border-radius: 8px;
}
QSlider::handle:horizontal { margin: -5px 0; }
QSlider::handle:vertical { margin: 0 -5px; }
QSlider::handle:horizontal:hover, QSlider::handle:vertical:hover { background: @accent2; }
QSlider::handle:horizontal:focus, QSlider::handle:vertical:focus { border: 2px solid @text; }
QSlider::sub-page:horizontal:disabled, QSlider::add-page:vertical:disabled,
QSlider::handle:horizontal:disabled, QSlider::handle:vertical:disabled { background: @faint; }

QCheckBox, QRadioButton { spacing: 8px; }
QCheckBox:disabled, QRadioButton:disabled { color: @faint; }
QCheckBox::indicator, QAbstractItemView::indicator {
    width: 16px; height: 16px; border-radius: 4px; border: 1px solid @muted; background: @base;
}
QAbstractItemView::indicator { width: 14px; height: 14px; }
QRadioButton::indicator { width: 16px; height: 16px; border-radius: 9px; border: 1px solid @muted; background: @base; }
QCheckBox::indicator:hover, QAbstractItemView::indicator:hover, QRadioButton::indicator:hover,
QCheckBox::indicator:focus, QRadioButton::indicator:focus { border: 1px solid @accent; }
QCheckBox::indicator:checked, QAbstractItemView::indicator:checked {
    background: @accent; border: 1px solid @accent; image: url("%check%");
}
QCheckBox::indicator:checked:hover, QAbstractItemView::indicator:checked:hover {
    background: @accent2; border: 1px solid @accent2;
}
QRadioButton::indicator:checked { background: @accent; border: 1px solid @accent; image: url("%radio%"); }
QCheckBox::indicator:checked:focus, QRadioButton::indicator:checked:focus { border: 1px solid @text; }
QCheckBox::indicator:disabled, QRadioButton::indicator:disabled { background: @surface; border: 1px solid @line2; }
QCheckBox::indicator:checked:disabled, QRadioButton::indicator:checked:disabled {
    background: @faint; border: 1px solid @faint; image: none;
}

QScrollBar:vertical { background: transparent; width: 10px; margin: 2px; }
QScrollBar:horizontal { background: transparent; height: 10px; margin: 2px; }
QScrollBar::handle { background: @btn2; border-radius: 3px; }
QScrollBar::handle:vertical { min-height: 28px; }
QScrollBar::handle:horizontal { min-width: 28px; }
QScrollBar::handle:hover { background: @muted; }
QScrollBar::add-line, QScrollBar::sub-line { width: 0; height: 0; }
QScrollBar::add-page, QScrollBar::sub-page { background: transparent; }
QAbstractScrollArea::corner { background: transparent; }

QToolTip { background: @raised; color: @text; border: 1px solid @line2; padding: 2px 4px; }
"""


def app_qss() -> str:
    """앱 전체에 거는 공통 위젯 스타일."""
    return qss(re.sub(r"%(\w+)%", lambda m: icon_path(m.group(1)).as_posix(), _APP_QSS))


def _paint(app: QApplication) -> None:
    palette = app.palette()
    role = QPalette.ColorRole
    for r, name in (
        (role.Window, "surface"),
        (role.Base, "base"),
        (role.AlternateBase, "surface"),
        (role.Text, "text"),
        (role.WindowText, "text"),
        (role.Button, "btn"),
        (role.ButtonText, "text"),
        (role.Highlight, "accent"),
        (role.HighlightedText, "on_accent"),
        (role.ToolTipBase, "raised"),
        (role.ToolTipText, "text"),
        (role.PlaceholderText, "muted"),
        (role.Link, "accent"),
    ):
        palette.setColor(r, QColor(_current[name]))
    for r in (role.Text, role.WindowText, role.ButtonText):
        palette.setColor(QPalette.ColorGroup.Disabled, r, QColor(_current["faint"]))
    app.setPalette(palette)
    app.setStyleSheet(app_qss())


def _sync() -> None:
    """설정과 Windows 색 모드에 맞춰 칠한다. 이미 그 테마면 아무것도 하지 않는다."""
    global _current, _name
    app = QApplication.instance()
    name = resolve(_mode, app.styleHints().colorScheme())
    if name == _name:
        return
    first = _name is None
    _name = name
    _current = TOKENS[name]
    _paint(app)
    if not first:
        notifier.changed.emit()


def apply_theme(app: QApplication, mode: str = "system") -> None:
    """테마를 적용한다. mode: system(Windows 따라가기) / dark / light."""
    global _mode, _listening
    _mode = mode
    hints = app.styleHints()
    if not _listening:
        app.setStyle("Fusion")  # QSS 와 팔레트는 Fusion 기준으로 맞췄다. windows11 스타일에서는 어긋난다
        hints.colorSchemeChanged.connect(lambda _scheme: _sync())
        _listening = True
    # 제목 표시줄도 같은 색 모드를 쓰게 한다. Unknown 은 Windows 설정을 따른다.
    hints.setColorScheme(
        {"dark": Qt.ColorScheme.Dark, "light": Qt.ColorScheme.Light}.get(mode, Qt.ColorScheme.Unknown)
    )
    _sync()

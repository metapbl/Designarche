# 색 원본, @이름, 대비, 전환, 아이콘.
import re

import pytest
from PySide6.QtCore import Qt, QtMsgType, qInstallMessageHandler
from PySide6.QtGui import QColor, QImage, QPalette
from PySide6.QtTest import QTest
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from gallery import _ink
from graphite_paper import theme

MODES = ["dark", "light"]
# 일반 글자로 쓰는 쌍. 기준 4.5 (WCAG AA 본문)
TEXT_PAIRS = [
    ("text", "base"), ("text", "surface"), ("text", "raised"), ("text", "sel"),
    ("text2", "base"), ("text2", "surface"), ("text2", "raised"), ("text2", "btn"), ("text2", "btn2"), ("text2", "sel"),
    ("muted", "base"), ("muted", "surface"), ("muted", "raised"),
    ("accent", "base"), ("accent", "surface"),
    ("on_accent", "accent"), ("on_accent", "accent2"), ("on_accent", "danger"),
    ("danger", "base"), ("danger", "surface"),
]


def luminance(hex_color: str) -> float:
    channels = [int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    r, g, b = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a: str, b: str) -> float:
    hi, lo = sorted((luminance(a), luminance(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


@pytest.fixture
def app():
    app = QApplication.instance() or QApplication([])
    theme.apply_theme(app, "dark")
    yield app
    theme.apply_theme(app, "dark")


def test_themes_have_same_22_names():
    assert theme.TOKENS["dark"].keys() == theme.TOKENS["light"].keys()
    assert len(theme.TOKENS["dark"]) == 22
    assert theme.TOKENS.keys() == set(MODES)


def test_app_qss_names_are_defined():
    used = set(re.findall(r"@(\w+)", theme._APP_QSS))
    assert used <= theme.TOKENS["dark"].keys()


def test_qss_replaces_and_rejects_unknown_names(app):
    assert theme.qss("color: @text;") == f"color: {theme.TOKENS['dark']['text']};"
    with pytest.raises(KeyError):
        theme.qss("color: @nope;")


def test_qss_leaves_at_sign_inside_paths(app):
    assert theme.qss('image: url("a@2x.png");') == 'image: url("a@2x.png");'


def test_app_qss_parses_without_warning(app):
    messages = []
    old = qInstallMessageHandler(lambda kind, _ctx, msg: kind != QtMsgType.QtDebugMsg and messages.append(msg))
    try:
        app.setStyleSheet("")
        app.setStyleSheet(theme.app_qss())
        for cls in (QPushButton, QCheckBox, QRadioButton, QProgressBar):
            cls().ensurePolished()
    finally:
        qInstallMessageHandler(old)
    assert not messages


@pytest.mark.parametrize("mode", MODES)
@pytest.mark.parametrize("fg, bg", TEXT_PAIRS)
def test_text_contrast(mode, fg, bg):
    tokens = theme.TOKENS[mode]
    assert contrast(tokens[fg], tokens[bg]) >= 4.5


@pytest.mark.parametrize("mode", MODES)
def test_faint_is_not_text_color(mode):
    # README 규칙의 근거: faint 는 어느 배경에서도 4.5 미만
    tokens = theme.TOKENS[mode]
    assert all(contrast(tokens["faint"], tokens[bg]) < 4.5 for bg in ("base", "surface", "raised"))


@pytest.mark.parametrize("mode, scheme, name", [
    ("system", Qt.ColorScheme.Dark, "dark"),
    ("system", Qt.ColorScheme.Light, "light"),
    ("system", Qt.ColorScheme.Unknown, "dark"),
    ("dark", Qt.ColorScheme.Light, "dark"),
    ("light", Qt.ColorScheme.Dark, "light"),
    ("이상한 값", Qt.ColorScheme.Light, "light"),
])
def test_resolve(mode, scheme, name):
    assert theme.resolve(mode, scheme) == name


def test_switch_repaints_and_notifies_once(app):
    got = []
    slot = lambda: got.append(theme.current())
    theme.notifier.changed.connect(slot)
    try:
        theme.apply_theme(app, "light")
        assert got == ["light"]
        assert theme.color("accent") == theme.TOKENS["light"]["accent"]
        window = app.palette().color(QPalette.ColorRole.Window).name()
        assert window == theme.TOKENS["light"]["surface"]
        assert "check_light.svg" in app.styleSheet()
        theme.apply_theme(app, "light")  # 같은 테마면 다시 칠하지 않는다
        assert got == ["light"]
    finally:
        theme.notifier.changed.disconnect(slot)


def test_system_mode_follows_color_scheme_signal(app):
    # setColorScheme 은 Windows 색 모드가 바뀔 때와 같은 colorSchemeChanged 를 낸다
    hints = app.styleHints()
    theme.apply_theme(app, "system")
    hints.setColorScheme(Qt.ColorScheme.Light)
    assert hints.colorScheme() == Qt.ColorScheme.Light
    assert theme.current() == "light"
    hints.setColorScheme(Qt.ColorScheme.Dark)
    assert theme.current() == "dark"


def test_fixed_mode_ignores_color_scheme_signal(app):
    theme.apply_theme(app, "light")
    app.styleHints().setColorScheme(Qt.ColorScheme.Dark)
    assert theme.current() == "light"


def test_title_bar_scheme_is_requested(app):
    theme.apply_theme(app, "light")
    assert app.styleHints().colorScheme() == Qt.ColorScheme.Light


@pytest.mark.parametrize("mode", MODES)
@pytest.mark.parametrize("kind", ["check", "radio", "up", "down"])
def test_icons_load(mode, kind):
    assert not QImage(str(theme.icon_path(kind, mode))).isNull()


@pytest.mark.parametrize("mode", MODES)
def test_icon_colors_are_tokens(mode):
    tokens = theme.TOKENS[mode]
    for kind, names in (("check", ["on_accent"]), ("radio", ["accent", "on_accent"]), ("up", ["text2"]), ("down", ["text2"])):
        found = set(re.findall(r"#[0-9a-fA-F]{6}", theme.icon_path(kind, mode).read_text(encoding="utf-8")))
        assert found == {tokens[n] for n in names}, kind


@pytest.mark.parametrize("mode", MODES)
def test_check_icon_is_drawn_in_stylesheet(app, mode):
    # 경로에 공백이 있어도 url("...") 이 읽히는지: 체크 표시 색이 실제로 칠해져야 한다
    theme.apply_theme(app, mode)
    box = QCheckBox()
    box.setChecked(True)
    box.adjustSize()
    image = box.grab().toImage()
    mark = QColor(theme.color("on_accent")).rgb()
    assert any(
        image.pixel(x, y) == mark
        for x in range(image.width()) for y in range(image.height())
    )


@pytest.mark.parametrize("mode", MODES)
def test_button_roles_differ(app, mode):
    # (윤곽, 바탕). 켜진 기본 버튼은 바탕색 + 진한 윤곽, 꺼진 버튼만 회색 채움
    theme.apply_theme(app, mode)
    colors = {}
    for role, enabled in (("primary", True), ("secondary", True), ("danger", True), ("primary", False)):
        btn = QPushButton("x")
        btn.setProperty("role", role)
        btn.setEnabled(enabled)
        btn.resize(60, 30)
        image = btn.grab().toImage()
        colors[role if enabled else "disabled"] = (image.pixelColor(30, 0).name(), image.pixelColor(30, 4).name())
    t = theme.TOKENS[mode]
    assert colors == {
        "primary": (t["accent"], t["accent"]),
        "secondary": (t["muted"], t["surface"]),
        "danger": (t["danger"], t["danger"]),
        "disabled": (t["line"], t["raised"]),
    }


@pytest.mark.parametrize("mode", MODES)
@pytest.mark.parametrize("role, ring", [("", "accent"), ("primary", "on_accent"), ("danger", "on_accent")])
def test_focus_ring_is_two_pixels_and_keeps_size(app, mode, role, ring):
    # 1px 색 바꿈은 muted→accent 대비가 1.0~1.4 라 보이지 않았다. 안쪽 1px 까지 고리색이어야 한다
    theme.apply_theme(app, mode)
    window = QWidget()
    layout = QVBoxLayout(window)
    focused, other = QPushButton("x"), QPushButton("x")
    for btn in (focused, other):
        btn.setProperty("role", role)
        layout.addWidget(btn)
    window.show()
    window.activateWindow()
    focused.setFocus()
    app.processEvents()
    image = focused.grab().toImage()
    ring_color = theme.TOKENS[mode][ring]
    assert focused.hasFocus()
    assert (image.pixelColor(30, 0).name(), image.pixelColor(30, 1).name()) == (ring_color, ring_color)
    assert focused.size() == other.size()
    window.close()


@pytest.mark.parametrize("make", [lambda: QPushButton("x"), lambda: QCheckBox("x"), lambda: QRadioButton("x")])
def test_buttons_take_focus_from_tab_not_click(app, make):
    # Windows 11 처럼 클릭으로는 포커스 고리가 남지 않고, Tab 이동 때만 보인다
    window = QWidget()
    layout = QVBoxLayout(window)
    first, target = QLineEdit(), make()
    layout.addWidget(first)
    layout.addWidget(target)
    window.show()
    window.activateWindow()
    first.setFocus()
    app.processEvents()
    QTest.mouseClick(target, Qt.MouseButton.LeftButton)
    assert not target.hasFocus()
    QTest.keyClick(first, Qt.Key.Key_Tab)
    assert target.hasFocus()
    window.close()


def test_buttons_keep_focus_policy_the_app_chose(app):
    btn = QPushButton("x")
    btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    btn.show()
    app.processEvents()
    assert btn.focusPolicy() == Qt.FocusPolicy.NoFocus
    btn.close()


@pytest.mark.parametrize("mode", MODES)
def test_checked_toggle_button_is_filled(app, mode):
    theme.apply_theme(app, mode)
    btn = QPushButton("x")
    btn.setCheckable(True)
    btn.resize(60, 30)
    off = btn.grab().toImage().pixelColor(30, 4).name()
    btn.setChecked(True)
    on = btn.grab().toImage().pixelColor(30, 4).name()
    assert (off, on) == (theme.TOKENS[mode]["surface"], theme.TOKENS[mode]["accent"])


@pytest.mark.parametrize("own_style, height", [("", 22), ("QListWidget::item { height: 36px; }", 36)])
def test_list_rows_filled_before_layout_do_not_overlap(app, own_style, height):
    # 항목을 채운 뒤 레이아웃에 넣는 순서. 창이 자기 높이를 정해도 같아야 한다
    root = QWidget()
    root.setStyleSheet(own_style)
    items = QListWidget()
    for i in range(3):
        item = QListWidgetItem(str(i))
        item.setCheckState(Qt.CheckState.Checked)
        items.addItem(item)
    QVBoxLayout(root).addWidget(items)
    root.show()
    app.processEvents()
    first, second = items.visualItemRect(items.item(0)), items.visualItemRect(items.item(1))
    root.close()
    assert first.height() == height
    assert second.y() - first.y() == height


def test_tree_rows_filled_before_layout_use_style_height(app):
    root = QWidget()
    tree = QTreeWidget()
    for i in range(3):
        QTreeWidgetItem(tree, [str(i)])
    QVBoxLayout(root).addWidget(tree)
    root.show()
    app.processEvents()
    first, second = tree.visualItemRect(tree.topLevelItem(0)), tree.visualItemRect(tree.topLevelItem(1))
    root.close()
    assert second.y() - first.y() == first.height() == 22


@pytest.mark.parametrize("mode", MODES)
def test_gallery_swatch_names_are_readable(mode):
    assert all(contrast(_ink(value), value) >= 4.5 for value in theme.TOKENS[mode].values())

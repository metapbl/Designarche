# 모든 공통 위젯을 두 테마로 보는 확인 앱.
# 실행: python gallery.py [system|dark|light]
# 캡처: python gallery.py dark --shot shots/dark.png

import argparse
import sys
from pathlib import Path

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QCheckBox,
    QComboBox,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QPlainTextEdit,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from graphite_paper import theme


def _button(text: str, role: str = "", enabled: bool = True) -> QPushButton:
    btn = QPushButton(text)
    if role:
        btn.setProperty("role", role)
    btn.setEnabled(enabled)
    return btn


def _group(title: str, *widgets: QWidget, layout=QVBoxLayout) -> QGroupBox:
    box = QGroupBox(title)
    lay = layout(box)
    for w in widgets:
        lay.addWidget(w)
    return box


class Gallery(QMainWindow):
    def __init__(self, mode: str):
        super().__init__()
        self.setWindowTitle("Graphite / Paper 갤러리")
        root = QWidget()
        self.setCentralWidget(root)
        grid = QGridLayout(root)

        grid.addWidget(self._mode_group(mode), 0, 0)
        grid.addWidget(self._buttons(), 1, 0)
        grid.addWidget(self._inputs(), 2, 0)
        grid.addWidget(self._indicators(), 3, 0)
        grid.addWidget(self._ranges(), 4, 0)
        grid.addWidget(self._views(), 0, 1, 4, 1)
        grid.addWidget(self._swatches(), 4, 1)

        theme.notifier.changed.connect(self._paint_swatches)
        self._paint_swatches()

    def _mode_group(self, mode: str) -> QGroupBox:
        row = []
        self._modes = QButtonGroup(self)
        for name in ("system", "dark", "light"):
            radio = QRadioButton(name)
            radio.setChecked(name == mode)
            radio.clicked.connect(lambda _checked, n=name: theme.apply_theme(QApplication.instance(), n))
            self._modes.addButton(radio)
            row.append(radio)
        return _group("테마 (실행 중 전환)", *row, layout=QHBoxLayout)

    def _buttons(self) -> QGroupBox:
        tip = _button("secondary (툴팁)")
        tip.setToolTip("QToolTip 스타일 확인")
        return _group(
            "버튼 역할",
            _button("primary", "primary"),
            tip,
            _button("danger", "danger"),
            _button("disabled", "primary", enabled=False),
            layout=QHBoxLayout,
        )

    def _inputs(self) -> QGroupBox:
        placeholder = QLineEdit()
        placeholder.setPlaceholderText("placeholder (@muted)")
        disabled = QLineEdit("disabled")
        disabled.setEnabled(False)
        combo = QComboBox()
        combo.addItems(["콤보박스 항목 1", "콤보박스 항목 2"])
        spin = QSpinBox()
        spin.setValue(42)
        text = QPlainTextEdit("여러 줄 입력\nQPlainTextEdit")
        text.setFixedHeight(56)
        return _group("입력창", QLineEdit("한글 입력 값"), placeholder, disabled, combo, spin, text)

    def _indicators(self) -> QGroupBox:
        checked = QCheckBox("체크됨")
        checked.setChecked(True)
        off = QCheckBox("체크 안 됨")
        off_disabled = QCheckBox("disabled")
        off_disabled.setEnabled(False)
        on_disabled = QCheckBox("disabled 체크됨")
        on_disabled.setChecked(True)
        on_disabled.setEnabled(False)
        radio_on = QRadioButton("라디오 선택됨")
        radio_on.setChecked(True)
        radio_disabled = QRadioButton("disabled")
        radio_disabled.setEnabled(False)
        box = QGroupBox("체크박스·라디오")
        grid = QGridLayout(box)
        for i, w in enumerate((checked, off, off_disabled, on_disabled)):
            grid.addWidget(w, 0, i)
        for i, w in enumerate((radio_on, QRadioButton("라디오"), radio_disabled)):
            grid.addWidget(w, 1, i)
        return box

    def _ranges(self) -> QGroupBox:
        bar = QProgressBar()
        bar.setValue(60)
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setValue(35)
        slider_off = QSlider(Qt.Orientation.Horizontal)
        slider_off.setValue(70)
        slider_off.setEnabled(False)
        return _group("진행률·슬라이더", bar, slider, slider_off)

    def _views(self) -> QGroupBox:
        items = QListWidget()
        for i in range(30):
            item = QListWidgetItem(f"목록 항목 {i + 1}")
            item.setCheckState(Qt.CheckState.Checked if i % 2 else Qt.CheckState.Unchecked)
            items.addItem(item)
        items.setCurrentRow(1)
        table = QTableWidget(30, 8)
        table.setAlternatingRowColors(True)
        table.setHorizontalHeaderLabels([f"열 {c + 1}" for c in range(8)])
        for r in range(30):
            for c in range(8):
                table.setItem(r, c, QTableWidgetItem(f"{r + 1}-{c + 1}"))
        table.selectRow(2)
        return _group("목록·표·스크롤바", items, table)

    def _swatches(self) -> QGroupBox:
        box = QGroupBox("색 이름 22개")
        grid = QGridLayout(box)
        grid.setSpacing(2)
        self._swatch_labels = {}
        for i, name in enumerate(theme.TOKENS["dark"]):
            label = QLabel(name)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setMinimumHeight(24)
            grid.addWidget(label, i // 6, i % 6)
            self._swatch_labels[name] = label
        return box

    def _paint_swatches(self) -> None:
        # 창이 스스로 칠하는 위젯은 notifier.changed 에 연결해 다시 칠한다
        for name, label in self._swatch_labels.items():
            label.setStyleSheet(theme.qss(f"background: @{name}; color: @text; border: 1px solid @line;"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", nargs="?", default="system", choices=["system", "dark", "light"])
    parser.add_argument("--shot", type=Path, help="창을 PNG 로 저장하고 끝낸다")
    args = parser.parse_args()

    app = QApplication(sys.argv[:1])
    theme.apply_theme(app, args.mode)
    window = Gallery(args.mode)
    window.show()
    if args.shot:
        args.shot.parent.mkdir(parents=True, exist_ok=True)
        QTimer.singleShot(300, lambda: (window.grab().save(str(args.shot)), app.quit()))
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())

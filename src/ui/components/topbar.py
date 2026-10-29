from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt, pyqtSignal

from src.ui.components.common import make_label, repolish
from src.ui.copy import NAV_ITEMS, PRODUCT_NAME


class TopBar(QWidget):
    """Горизонтальная навигация: бренд, разделы, состояние соединения."""

    page_changed = pyqtSignal(int)

    ITEMS = list(NAV_ITEMS)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("topbar")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setFixedHeight(66)
        self.buttons = []

        layout = QHBoxLayout(self)
        layout.setContentsMargins(32, 0, 32, 0)
        layout.setSpacing(6)

        mark = make_label("C")
        mark.setObjectName("brandMark")
        mark.setFixedSize(30, 30)
        mark.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(mark)

        brand = make_label(PRODUCT_NAME)
        brand.setObjectName("brand")
        layout.addWidget(brand)
        layout.addSpacing(30)

        for index, name in enumerate(self.ITEMS):
            btn = QPushButton(name)
            btn.setObjectName("nav")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setProperty("active", index == 0)
            btn.clicked.connect(lambda _=False, i=index: self.select(i))
            self.buttons.append(btn)
            layout.addWidget(btn)

        layout.addStretch()

        self.chip = QLabel("Соединение · напрямую или VPN")
        self.chip.setObjectName("chip")
        layout.addWidget(self.chip)

    def select(self, index: int, emit: bool = True):
        for i, btn in enumerate(self.buttons):
            btn.setProperty("active", i == index)
            repolish(btn)
        if emit:
            self.page_changed.emit(index)

    def set_connection(self, proxy: str):
        self.chip.setText(f"Прокси · {proxy}" if proxy else "Соединение · напрямую или VPN")

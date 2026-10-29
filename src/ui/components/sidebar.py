from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFrame
from PyQt6.QtCore import Qt, pyqtSignal

from src.ui.components.common import make_label, make_section, repolish
from src.ui.copy import NAV_ITEMS, PRODUCT_NAME, PRODUCT_TAGLINE, PRODUCT_VERSION


class Sidebar(QWidget):
    page_changed = pyqtSignal(int)

    ITEMS = list(NAV_ITEMS)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setFixedWidth(224)
        self.buttons = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 22, 14, 18)
        layout.setSpacing(0)

        brand_row = QHBoxLayout()
        brand_row.setSpacing(10)
        mark = make_label("C")
        mark.setObjectName("brandMark")
        mark.setFixedSize(34, 34)
        mark.setAlignment(Qt.AlignmentFlag.AlignCenter)
        brand_row.addWidget(mark)

        brand_column = QVBoxLayout()
        brand_column.setSpacing(0)
        brand = make_label(PRODUCT_NAME)
        brand.setObjectName("brand")
        version = make_label(f"версия {PRODUCT_VERSION}", "caption")
        brand_column.addWidget(brand)
        brand_column.addWidget(version)
        brand_row.addLayout(brand_column, 1)
        layout.addLayout(brand_row)

        tagline = make_label(PRODUCT_TAGLINE, "caption")
        tagline.setWordWrap(True)
        layout.addSpacing(14)
        layout.addWidget(tagline)
        layout.addSpacing(24)

        layout.addWidget(make_section("НАВИГАЦИЯ"))
        layout.addSpacing(8)

        for index, name in enumerate(self.ITEMS):
            btn = QPushButton(name)
            btn.setObjectName("nav")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setProperty("active", index == 0)
            btn.clicked.connect(lambda _=False, i=index: self.select(i))
            self.buttons.append(btn)
            layout.addWidget(btn)
            layout.addSpacing(2)

        layout.addStretch()

        card = QFrame()
        card.setObjectName("connectionCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(12, 10, 12, 10)
        card_layout.setSpacing(4)
        card_layout.addWidget(make_section("СОЕДИНЕНИЕ"))

        status_row = QHBoxLayout()
        status_row.setSpacing(7)
        self.dot = make_label("●", "caption")
        status_row.addWidget(self.dot, 0, Qt.AlignmentFlag.AlignTop)
        self.connection = make_label("", "caption")
        self.connection.setWordWrap(True)
        status_row.addWidget(self.connection, 1)
        card_layout.addLayout(status_row)
        layout.addWidget(card)

    def select(self, index: int, emit: bool = True):
        for i, btn in enumerate(self.buttons):
            btn.setProperty("active", i == index)
            repolish(btn)
        if emit:
            self.page_changed.emit(index)

    def set_connection(self, proxy: str):
        self.connection.setText(proxy if proxy else "напрямую или VPN")
        self.dot.setProperty("role", "ok" if proxy else "caption")
        repolish(self.dot)

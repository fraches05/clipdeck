"""ClipForge visual system: palette, typography and widget styling."""

from pathlib import Path

BG = "#0a0b0f"
SURFACE = "#12141a"
SURFACE_2 = "#171a22"
SURFACE_3 = "#1e222c"
BORDER = "#232833"
BORDER_STRONG = "#343b49"
TEXT = "#eef0f5"
MUTED = "#8b92a2"
FAINT = "#596070"
ACCENT = "#8b5cf6"
ACCENT_STRONG = "#a78bfa"
ACCENT_SOFT = "#241d3a"
ACCENT_BORDER = "#3b2f63"
SUCCESS = "#3ecf8e"
WARNING = "#f2b544"
DANGER = "#ef5f6b"

CHEVRON = (Path(__file__).parent / "assets" / "chevron.svg").as_posix()
CHEVRON_UP = (Path(__file__).parent / "assets" / "chevron-up.svg").as_posix()
CHECK = (Path(__file__).parent / "assets" / "check.svg").as_posix()
FONT_FAMILY = '"Segoe UI Variable Text", "Segoe UI", "Inter", sans-serif'
DISPLAY_FAMILY = '"Segoe UI Variable Display", "Segoe UI Semibold", "Segoe UI", sans-serif'

APP_STYLE = f"""
* {{
    font-family: {FONT_FAMILY};
    font-size: 13px;
    color: {TEXT};
    outline: 0;
}}

QMainWindow, QDialog, QMessageBox, QInputDialog, QWidget#content {{
    background: {BG};
}}

QLabel {{ background: transparent; }}
QLabel#pageTitle {{
    font-family: {DISPLAY_FAMILY};
    font-size: 26px;
    font-weight: 600;
}}
QLabel#brand {{ font-family: {DISPLAY_FAMILY}; font-size: 16px; font-weight: 600; }}
QLabel#brandMark {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {ACCENT}, stop:1 #e879f9);
    border-radius: 10px;
    color: #ffffff;
    font-family: {DISPLAY_FAMILY};
    font-size: 15px;
    font-weight: 700;
}}
QLabel#statValue {{
    font-family: {DISPLAY_FAMILY};
    font-size: 30px;
    font-weight: 600;
}}
QLabel#statCaption {{ color: {MUTED}; font-size: 12px; }}
QLabel#emptyTitle {{ font-family: {DISPLAY_FAMILY}; font-size: 16px; font-weight: 600; }}
QLabel[role="muted"] {{ color: {MUTED}; }}
QLabel[role="caption"] {{ color: {MUTED}; font-size: 12px; }}
QLabel[role="section"] {{ color: {FAINT}; font-size: 11px; font-weight: 600; }}
QLabel[role="eyebrow"] {{ color: {ACCENT_STRONG}; font-size: 11px; font-weight: 600; }}
QLabel[role="ok"] {{ color: {SUCCESS}; }}
QLabel[role="warn"] {{ color: {WARNING}; }}
QLabel[role="err"] {{ color: {DANGER}; }}

QFrame#divider {{ background: {BORDER}; border: none; max-height: 1px; min-height: 1px; }}

QWidget#sidebar {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #101218, stop:1 {BG});
    border-right: 1px solid {BORDER};
}}

QWidget#statCard {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #171a23, stop:1 #12141a);
    border: 1px solid #2b3242;
    border-radius: 14px;
}}
QWidget#statCard:hover {{ border-color: {ACCENT_BORDER}; }}
QFrame#panel {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #151821, stop:1 {SURFACE});
    border: 1px solid #262d3b;
    border-radius: 14px;
}}
QFrame#connectionCard {{
    background: {SURFACE_2};
    border: 1px solid {BORDER};
    border-radius: 10px;
}}

QPushButton {{
    background: transparent;
    border: 1px solid {BORDER_STRONG};
    border-radius: 8px;
    padding: 0 18px;
    min-height: 36px;
    color: {TEXT};
}}
QPushButton:hover {{ background: {SURFACE_3}; border-color: #414a5c; }}
QPushButton:pressed {{ background: {SURFACE_2}; }}
QPushButton:disabled {{ color: {FAINT}; border-color: {BORDER}; background: transparent; }}

QPushButton[variant="primary"] {{
    background: {ACCENT};
    border: 1px solid {ACCENT};
    color: #ffffff;
    font-weight: 600;
}}
QPushButton[variant="primary"]:hover {{ background: {ACCENT_STRONG}; border-color: {ACCENT_STRONG}; }}
QPushButton[variant="primary"]:pressed {{ background: #7c4ce0; border-color: #7c4ce0; }}
QPushButton[variant="primary"]:disabled {{ background: {BORDER}; color: {FAINT}; border-color: {BORDER}; }}

QPushButton[variant="danger"] {{ color: {DANGER}; }}
QPushButton[variant="danger"]:hover {{ border-color: {DANGER}; background: rgba(239, 95, 107, 24); }}
QPushButton[variant="danger"]:disabled {{ color: {FAINT}; }}

QPushButton[variant="ghost"] {{ border-color: transparent; color: {MUTED}; }}
QPushButton[variant="ghost"]:hover {{ color: {TEXT}; background: {SURFACE_2}; }}

QPushButton#nav {{
    text-align: left;
    border: 1px solid transparent;
    border-radius: 9px;
    padding: 0 14px;
    min-height: 38px;
    color: {MUTED};
}}
QPushButton#nav:hover {{ color: {TEXT}; background: {SURFACE_2}; }}
QPushButton#nav[active="true"] {{
    color: {TEXT};
    background: {ACCENT_SOFT};
    border: 1px solid {ACCENT_BORDER};
    font-weight: 600;
}}

QCheckBox {{ spacing: 9px; }}
QCheckBox::indicator {{
    width: 16px;
    height: 16px;
    border: 1px solid {BORDER_STRONG};
    border-radius: 5px;
    background: {SURFACE};
}}
QCheckBox::indicator:hover {{ border-color: {ACCENT}; }}
QCheckBox::indicator:checked {{
    background: {ACCENT};
    border-color: {ACCENT};
    image: url({CHECK});
}}
QCheckBox:disabled {{ color: {FAINT}; }}

QLineEdit, QTextEdit, QPlainTextEdit, QComboBox, QSpinBox {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 9px;
    padding: 9px 12px;
    color: {TEXT};
    selection-background-color: {ACCENT};
    selection-color: #ffffff;
}}
QLineEdit:hover, QTextEdit:hover, QPlainTextEdit:hover, QComboBox:hover, QSpinBox:hover {{ border-color: {BORDER_STRONG}; }}
QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QComboBox:focus, QSpinBox:focus {{
    border-color: {ACCENT};
    background: {SURFACE_2};
}}
QLineEdit:disabled, QSpinBox:disabled {{ color: {FAINT}; }}
QSpinBox {{ padding-right: 26px; min-height: 18px; }}
QSpinBox::up-button, QSpinBox::down-button {{
    background: transparent;
    border: none;
    width: 22px;
}}
QSpinBox::up-button:hover, QSpinBox::down-button:hover {{ background: {SURFACE_3}; }}
QSpinBox::up-arrow {{
    image: url({CHEVRON_UP});
    width: 10px;
    height: 10px;
}}
QSpinBox::down-arrow {{
    image: url({CHEVRON});
    width: 10px;
    height: 10px;
}}
QPlainTextEdit#log {{
    font-family: Consolas, "Cascadia Mono", monospace;
    font-size: 12px;
    color: {MUTED};
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 12px 14px;
}}

QComboBox {{ padding: 0 12px; min-height: 36px; }}
QComboBox::drop-down {{ border: none; width: 28px; }}
QComboBox::down-arrow {{
    image: url({CHEVRON});
    width: 12px;
    height: 12px;
    margin-right: 10px;
}}
QComboBox QAbstractItemView {{
    background: {SURFACE_2};
    border: 1px solid {BORDER_STRONG};
    border-radius: 8px;
    padding: 4px;
    selection-background-color: {ACCENT_SOFT};
    selection-color: {TEXT};
}}

QTableWidget {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 12px;
    gridline-color: transparent;
    selection-background-color: {ACCENT_SOFT};
    selection-color: {TEXT};
    alternate-background-color: {SURFACE};
}}
QTableWidget::item {{
    padding: 0 16px;
    border-bottom: 1px solid {BORDER};
}}
QTableWidget::item:hover {{ background: {SURFACE_2}; }}
QTableWidget::item:selected {{ background: {ACCENT_SOFT}; color: {TEXT}; }}
QHeaderView {{ background: transparent; }}
QHeaderView::section {{
    background: {SURFACE};
    color: {MUTED};
    padding: 12px 16px;
    border: none;
    border-bottom: 1px solid {BORDER};
    font-size: 11px;
    font-weight: 600;
}}
QTableCornerButton::section {{ background: transparent; border: none; }}

QScrollBar:vertical {{ background: transparent; width: 10px; margin: 2px; }}
QScrollBar::handle:vertical {{ background: {BORDER_STRONG}; border-radius: 3px; min-height: 32px; }}
QScrollBar::handle:vertical:hover {{ background: {FAINT}; }}
QScrollBar:horizontal {{ background: transparent; height: 10px; margin: 2px; }}
QScrollBar::handle:horizontal {{ background: {BORDER_STRONG}; border-radius: 3px; min-width: 32px; }}
QScrollBar::add-line, QScrollBar::sub-line {{ width: 0; height: 0; }}
QScrollBar::add-page, QScrollBar::sub-page {{ background: none; }}

QMenu {{
    background: {SURFACE_2};
    border: 1px solid {BORDER_STRONG};
    border-radius: 9px;
    padding: 5px;
}}
QMenu::item {{ padding: 8px 24px 8px 16px; border-radius: 6px; }}
QMenu::item:selected {{ background: {ACCENT_SOFT}; }}
QMenu::separator {{ height: 1px; background: {BORDER}; margin: 4px 8px; }}

QToolTip {{
    background: {SURFACE_2};
    color: {TEXT};
    border: 1px solid {BORDER_STRONG};
    border-radius: 6px;
    padding: 5px 9px;
}}

QProgressBar {{ background: {BORDER}; border: none; border-radius: 2px; max-height: 3px; min-height: 3px; }}
QProgressBar::chunk {{ background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {ACCENT}, stop:1 #e879f9); border-radius: 2px; }}

QMessageBox QLabel {{ min-width: 280px; }}
QMessageBox QPushButton, QInputDialog QPushButton {{ min-width: 84px; }}
"""

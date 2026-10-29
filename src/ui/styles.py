"""ClipForge visual system: warm paper palette, editorial typography, light surfaces."""

from pathlib import Path

BG = "#f4f3ef"
SURFACE = "#ffffff"
SURFACE_2 = "#faf9f6"
SURFACE_3 = "#f0eee8"
BORDER = "#e3e1da"
BORDER_STRONG = "#cdcac1"
TEXT = "#17181c"
MUTED = "#6d7080"
FAINT = "#9a9ca6"
ACCENT = "#d9542b"
ACCENT_STRONG = "#bf4620"
ACCENT_SOFT = "#fbeae4"
ACCENT_BORDER = "#f0c9bb"
SUCCESS = "#157f4a"
WARNING = "#a9761a"
DANGER = "#c0392b"

CHEVRON = (Path(__file__).parent / "assets" / "chevron.svg").as_posix()
CHEVRON_UP = (Path(__file__).parent / "assets" / "chevron-up.svg").as_posix()
CHECK = (Path(__file__).parent / "assets" / "check.svg").as_posix()
FONT_FAMILY = '"Segoe UI", "Inter", sans-serif'
DISPLAY_FAMILY = 'Georgia, "Times New Roman", serif'

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
    font-size: 34px;
    font-weight: 600;
    color: {TEXT};
}}
QLabel#brand {{
    font-family: {DISPLAY_FAMILY};
    font-size: 20px;
    font-weight: 600;
    color: {TEXT};
}}
QLabel#brandMark {{
    background: {ACCENT};
    border-radius: 8px;
    color: #ffffff;
    font-family: {FONT_FAMILY};
    font-size: 15px;
    font-weight: 700;
}}
QLabel#statValue {{
    font-family: {DISPLAY_FAMILY};
    font-size: 38px;
    font-weight: 600;
    color: {TEXT};
}}
QLabel#statCaption {{ color: {FAINT}; font-size: 11px; font-weight: 600; }}
QLabel#emptyTitle {{ font-family: {DISPLAY_FAMILY}; font-size: 20px; font-weight: 600; }}
QLabel#chip {{
    background: {SURFACE_2};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 6px 12px;
    color: {MUTED};
    font-size: 12px;
}}
QLabel[role="muted"] {{ color: {MUTED}; }}
QLabel[role="caption"] {{ color: {MUTED}; font-size: 12px; }}
QLabel[role="section"] {{ color: {FAINT}; font-size: 11px; font-weight: 600; }}
QLabel[role="eyebrow"] {{ color: {ACCENT}; font-size: 11px; font-weight: 700; }}
QLabel[role="ok"] {{ color: {SUCCESS}; }}
QLabel[role="warn"] {{ color: {WARNING}; }}
QLabel[role="err"] {{ color: {DANGER}; }}

QFrame#divider {{ background: {BORDER}; border: none; max-height: 1px; min-height: 1px; }}
QFrame#vdivider {{ background: {BORDER}; border: none; max-width: 1px; min-width: 1px; }}

QWidget#topbar {{
    background: {SURFACE};
    border-bottom: 1px solid {BORDER};
}}

QWidget#statCard {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 16px;
}}
QWidget#statCard:hover {{ border-color: {BORDER_STRONG}; }}
QFrame#panel {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 16px;
}}
QFrame#connectionCard {{
    background: {SURFACE_2};
    border: 1px solid {BORDER};
    border-radius: 12px;
}}

QPushButton {{
    background: {SURFACE};
    border: 1px solid {BORDER_STRONG};
    border-radius: 9px;
    padding: 0 18px;
    min-height: 38px;
    color: {TEXT};
}}
QPushButton:hover {{ background: {SURFACE_3}; border-color: {BORDER_STRONG}; }}
QPushButton:pressed {{ background: {BORDER}; }}
QPushButton:disabled {{ color: {FAINT}; border-color: {BORDER}; background: {SURFACE_2}; }}

QPushButton[variant="primary"] {{
    background: {ACCENT};
    border: 1px solid {ACCENT};
    color: #ffffff;
    font-weight: 600;
}}
QPushButton[variant="primary"]:hover {{ background: {ACCENT_STRONG}; border-color: {ACCENT_STRONG}; }}
QPushButton[variant="primary"]:pressed {{ background: #a63c1b; border-color: #a63c1b; }}
QPushButton[variant="primary"]:disabled {{ background: {BORDER}; border-color: {BORDER}; color: {FAINT}; }}

QPushButton[variant="danger"] {{ color: {DANGER}; }}
QPushButton[variant="danger"]:hover {{ border-color: {DANGER}; background: #fbeeec; }}
QPushButton[variant="danger"]:disabled {{ color: {FAINT}; }}

QPushButton[variant="ghost"] {{ border-color: transparent; background: transparent; color: {MUTED}; }}
QPushButton[variant="ghost"]:hover {{ color: {TEXT}; background: {SURFACE_3}; }}

QPushButton#nav {{
    text-align: center;
    border: none;
    border-bottom: 2px solid transparent;
    border-radius: 0;
    padding: 0 14px;
    min-height: 66px;
    background: transparent;
    color: {MUTED};
}}
QPushButton#nav:hover {{ color: {TEXT}; background: transparent; }}
QPushButton#nav[active="true"] {{
    color: {TEXT};
    border-bottom: 2px solid {ACCENT};
    font-weight: 600;
}}

QCheckBox {{ spacing: 9px; }}
QCheckBox::indicator {{
    width: 17px;
    height: 17px;
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
    border: 1px solid {BORDER_STRONG};
    border-radius: 10px;
    padding: 10px 13px;
    color: {TEXT};
    selection-background-color: {ACCENT_SOFT};
    selection-color: {TEXT};
}}
QLineEdit:hover, QTextEdit:hover, QPlainTextEdit:hover, QComboBox:hover, QSpinBox:hover {{ border-color: {FAINT}; }}
QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QComboBox:focus, QSpinBox:focus {{
    border-color: {ACCENT};
    background: {SURFACE};
}}
QLineEdit:disabled, QSpinBox:disabled {{ color: {FAINT}; background: {SURFACE_2}; }}
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
    background: {SURFACE_2};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 12px 14px;
}}

QComboBox {{ padding: 0 12px; min-height: 38px; }}
QComboBox::drop-down {{ border: none; width: 28px; }}
QComboBox::down-arrow {{
    image: url({CHEVRON});
    width: 12px;
    height: 12px;
    margin-right: 10px;
}}
QComboBox QAbstractItemView {{
    background: {SURFACE};
    border: 1px solid {BORDER_STRONG};
    border-radius: 10px;
    padding: 4px;
    selection-background-color: {ACCENT_SOFT};
    selection-color: {TEXT};
}}

QTableWidget {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 14px;
    gridline-color: transparent;
    selection-background-color: {ACCENT_SOFT};
    selection-color: {TEXT};
    alternate-background-color: {SURFACE_2};
}}
QTableWidget::item {{
    padding: 0 16px;
    border-bottom: 1px solid {SURFACE_3};
}}
QTableWidget::item:hover {{ background: {SURFACE_2}; }}
QTableWidget::item:selected {{ background: {ACCENT_SOFT}; color: {TEXT}; }}
QHeaderView {{ background: transparent; }}
QHeaderView::section {{
    background: {SURFACE_2};
    color: {MUTED};
    padding: 12px 16px;
    border: none;
    border-bottom: 1px solid {BORDER};
    font-size: 11px;
    font-weight: 600;
}}
QTableCornerButton::section {{ background: {SURFACE_2}; border: none; }}

QScrollBar:vertical {{ background: transparent; width: 10px; margin: 2px; }}
QScrollBar::handle:vertical {{ background: {BORDER_STRONG}; border-radius: 3px; min-height: 32px; }}
QScrollBar::handle:vertical:hover {{ background: {FAINT}; }}
QScrollBar:horizontal {{ background: transparent; height: 10px; margin: 2px; }}
QScrollBar::handle:horizontal {{ background: {BORDER_STRONG}; border-radius: 3px; min-width: 32px; }}
QScrollBar::add-line, QScrollBar::sub-line {{ width: 0; height: 0; }}
QScrollBar::add-page, QScrollBar::sub-page {{ background: none; }}

QMenu {{
    background: {SURFACE};
    border: 1px solid {BORDER_STRONG};
    border-radius: 10px;
    padding: 5px;
}}
QMenu::item {{ padding: 8px 24px 8px 16px; border-radius: 6px; }}
QMenu::item:selected {{ background: {ACCENT_SOFT}; }}
QMenu::separator {{ height: 1px; background: {BORDER}; margin: 4px 8px; }}

QToolTip {{
    background: {TEXT};
    color: #ffffff;
    border: 1px solid {TEXT};
    border-radius: 6px;
    padding: 5px 9px;
}}

QProgressBar {{ background: {SURFACE_3}; border: none; border-radius: 2px; max-height: 3px; min-height: 3px; }}
QProgressBar::chunk {{ background: {ACCENT}; border-radius: 2px; }}

QMessageBox QLabel {{ min-width: 280px; }}
QMessageBox QPushButton, QInputDialog QPushButton {{ min-width: 84px; }}
"""

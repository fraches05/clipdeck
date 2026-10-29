from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame
from PyQt6.QtCore import Qt, pyqtSignal

from src.app.services import ClipForgeService
from src.ui.components.common import (
    PageHeader,
    make_button,
    make_card,
    make_divider,
    make_label,
    make_section,
    set_role,
)


class OverviewPage(QWidget):
    go_upload = pyqtSignal()

    def __init__(self, service: ClipForgeService, parent=None):
        super().__init__(parent)
        self.service = service
        root = QVBoxLayout(self)
        root.setContentsMargins(48, 40, 48, 36)
        root.setSpacing(0)

        hero = QHBoxLayout()
        hero.setSpacing(16)
        self.header = PageHeader("Обзор", "Состояние публикаций и аккаунтов ClipForge", eyebrow="ПАНЕЛЬ УПРАВЛЕНИЯ")
        hero.addWidget(self.header, 1)
        self.btn_new = make_button("Новая публикация", "primary")
        self.btn_new.clicked.connect(self.go_upload.emit)
        hero.addWidget(self.btn_new, 0, Qt.AlignmentFlag.AlignBottom)
        root.addLayout(hero)
        root.addSpacing(32)

        strip = make_card("panel")
        strip_layout = QHBoxLayout(strip)
        strip_layout.setContentsMargins(0, 4, 0, 4)
        strip_layout.setSpacing(0)
        self.account_value, self.account_hint = self._metric(strip_layout, "АККАУНТЫ")
        strip_layout.addWidget(self._rule())
        self.group_value, self.group_hint = self._metric(strip_layout, "ГРУППЫ")
        strip_layout.addWidget(self._rule())
        self.history_value, self.history_hint = self._metric(strip_layout, "ПУБЛИКАЦИИ")
        strip_layout.addWidget(self._rule())
        self.error_value, self.error_hint = self._metric(strip_layout, "ОШИБКИ")
        root.addWidget(strip)
        root.addSpacing(20)

        panels = QHBoxLayout()
        panels.setSpacing(20)

        recent = make_card("panel")
        recent_layout = QVBoxLayout(recent)
        recent_layout.setContentsMargins(24, 20, 24, 22)
        recent_layout.setSpacing(0)
        recent_layout.addWidget(make_section("ПОСЛЕДНИЕ ПУБЛИКАЦИИ"))
        recent_layout.addSpacing(12)
        self.recent_layout = QVBoxLayout()
        self.recent_layout.setSpacing(0)
        recent_layout.addLayout(self.recent_layout)
        recent_layout.addStretch()
        panels.addWidget(recent, 3)

        start = make_card("panel")
        start_layout = QVBoxLayout(start)
        start_layout.setContentsMargins(24, 20, 24, 22)
        start_layout.setSpacing(0)
        start_layout.addWidget(make_section("БЫСТРЫЙ СТАРТ"))
        start_layout.addSpacing(14)
        for number, title, note in (
            ("01", "Добавьте аккаунт", "Вход через браузер или импорт списка"),
            ("02", "Соберите группу", "Тег объединяет аккаунты для публикации"),
            ("03", "Отправьте видео", "Уникализация включается на странице публикаций"),
        ):
            row = QHBoxLayout()
            row.setSpacing(14)
            badge = make_label(number, "eyebrow")
            badge.setFixedWidth(22)
            badge.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
            row.addWidget(badge)
            column = QVBoxLayout()
            column.setSpacing(2)
            column.addWidget(make_label(title))
            note_label = make_label(note, "caption")
            note_label.setWordWrap(True)
            column.addWidget(note_label)
            row.addLayout(column, 1)
            start_layout.addLayout(row)
            start_layout.addSpacing(16)
        start_layout.addStretch()
        panels.addWidget(start, 2)

        root.addLayout(panels, 1)
        self.refresh()

    def _metric(self, layout, title):
        column = QVBoxLayout()
        column.setContentsMargins(26, 18, 26, 18)
        column.setSpacing(2)
        value = make_label("0")
        value.setObjectName("statValue")
        column.addWidget(value)
        hint = make_label(title, "statCaption")
        column.addWidget(hint)
        layout.addLayout(column, 1)
        return value, hint

    @staticmethod
    def _rule():
        line = QFrame()
        line.setObjectName("vdivider")
        line.setFrameShape(QFrame.Shape.VLine)
        return line

    def _clear_recent(self):
        while self.recent_layout.count():
            item = self.recent_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                # deleteLater() отложен, поэтому снимаем с отрисовки сразу.
                widget.setParent(None)
                widget.deleteLater()

    def _recent_row(self, outcome):
        row = QWidget()
        layout = QHBoxLayout(row)
        layout.setContentsMargins(0, 11, 0, 11)
        layout.setSpacing(12)

        name = make_label(f"@{outcome.username}" if outcome.username else "аккаунт")
        layout.addWidget(name)
        layout.addStretch()

        moment = (outcome.created_at or "")[:16].replace("T", " ")
        layout.addWidget(make_label(moment, "caption"))
        status = make_label("опубликовано", "ok") if outcome.status == "ok" else make_label("ошибка", "err")
        layout.addWidget(status)
        return row

    def refresh(self):
        groups = self.service.list_account_groups()
        history = self.service.recent_uploads(200)
        account_count = sum(count for _, count in groups)
        errors = sum(item.status != "ok" for item in history)

        self.account_value.setText(str(account_count))
        self.group_value.setText(str(len(groups)))
        self.history_value.setText(str(len(history)))
        self.error_value.setText(str(errors))
        set_role(self.error_value, "err" if errors else "")

        self.account_hint.setText("АККАУНТЫ" if account_count else "АККАУНТОВ ПОКА НЕТ")
        self.group_hint.setText("ГРУППЫ")
        self.history_hint.setText("ПУБЛИКАЦИИ")
        self.error_hint.setText("ОШИБКИ" if errors else "ОШИБОК НЕТ")

        self._clear_recent()
        for index, outcome in enumerate(self.service.recent_uploads(5)):
            if index:
                self.recent_layout.addWidget(make_divider())
            self.recent_layout.addWidget(self._recent_row(outcome))
        if not self.recent_layout.count():
            empty = make_label("Пока нет публикаций — начните с кнопки справа сверху.", "muted")
            empty.setWordWrap(True)
            self.recent_layout.addWidget(empty)

        self.header.set_subtitle(
            "ClipForge готов к работе. Отправьте видео и следите за результатом."
            if account_count else "Добавьте аккаунты, выберите группу и начните первую публикацию."
        )
        self.btn_new.setEnabled(bool(account_count))

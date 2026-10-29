from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
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
        root.setContentsMargins(40, 36, 40, 32)
        root.setSpacing(0)

        hero = QHBoxLayout()
        hero.setSpacing(16)
        self.header = PageHeader("Обзор", "Состояние публикаций и аккаунтов ClipForge", eyebrow="ЦЕНТР УПРАВЛЕНИЯ")
        hero.addWidget(self.header, 1)
        self.btn_new = make_button("Новая публикация", "primary")
        self.btn_new.clicked.connect(self.go_upload.emit)
        hero.addWidget(self.btn_new, 0, Qt.AlignmentFlag.AlignTop)
        root.addLayout(hero)
        root.addSpacing(26)

        self.cards = QHBoxLayout()
        self.cards.setSpacing(14)
        self.account_card, self.account_value, self.account_hint = self._card("Аккаунты", "в активных группах")
        self.group_card, self.group_value, self.group_hint = self._card("Группы", "по тегам")
        self.history_card, self.history_value, self.history_hint = self._card("Публикации", "в журнале")
        self.error_card, self.error_value, self.error_hint = self._card("Ошибки", "за последние записи")
        for card in (self.account_card, self.group_card, self.history_card, self.error_card):
            self.cards.addWidget(card, 1)
        root.addLayout(self.cards)
        root.addSpacing(18)

        panels = QHBoxLayout()
        panels.setSpacing(14)

        recent = make_card("panel")
        recent_layout = QVBoxLayout(recent)
        recent_layout.setContentsMargins(20, 16, 20, 18)
        recent_layout.setSpacing(0)
        recent_layout.addWidget(make_section("ПОСЛЕДНИЕ ПУБЛИКАЦИИ"))
        recent_layout.addSpacing(10)
        self.recent_layout = QVBoxLayout()
        self.recent_layout.setSpacing(0)
        recent_layout.addLayout(self.recent_layout)
        panels.addWidget(recent, 3)

        start = make_card("panel")
        start_layout = QVBoxLayout(start)
        start_layout.setContentsMargins(20, 16, 20, 18)
        start_layout.setSpacing(0)
        start_layout.addWidget(make_section("БЫСТРЫЙ СТАРТ"))
        start_layout.addSpacing(12)
        for number, title, note in (
            ("1", "Добавьте аккаунт", "Вход через браузер или импорт списка"),
            ("2", "Соберите группу", "Тег объединяет аккаунты для публикации"),
            ("3", "Отправьте видео", "Уникализация включается на странице публикаций"),
        ):
            row = QHBoxLayout()
            row.setSpacing(10)
            badge = make_label(number)
            badge.setObjectName("statValue")
            badge.setFixedWidth(18)
            badge.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
            row.addWidget(badge)
            column = QVBoxLayout()
            column.setSpacing(1)
            column.addWidget(make_label(title))
            note_label = make_label(note, "caption")
            note_label.setWordWrap(True)
            column.addWidget(note_label)
            row.addLayout(column, 1)
            start_layout.addLayout(row)
            start_layout.addSpacing(14)
        start_layout.addStretch()
        panels.addWidget(start, 2)

        root.addLayout(panels, 1)
        self.refresh()

    def _card(self, title, hint):
        card = make_card("statCard")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(6)
        layout.addWidget(make_label(title, "statCaption"))
        value = make_label("0")
        value.setObjectName("statValue")
        layout.addWidget(value)
        hint_label = make_label(hint, "caption")
        layout.addWidget(hint_label)
        return card, value, hint_label

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
        layout.setContentsMargins(0, 9, 0, 9)
        layout.setSpacing(10)

        name = make_label(f"@{outcome.username}" if outcome.username else "аккаунт")
        layout.addWidget(name)
        layout.addStretch()

        moment = (outcome.created_at or "")[:16].replace("T", " ")
        when = make_label(moment, "caption")
        layout.addWidget(when)

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

        self.account_hint.setText("в активных группах" if account_count else "пока ни одного")
        self.group_hint.setText("по тегам" if groups else "появятся вместе с аккаунтами")
        self.history_hint.setText("в журнале" if history else "журнал пуст")
        self.error_hint.setText("за последние записи" if errors else "ошибок нет")

        self._clear_recent()
        recent = self.service.recent_uploads(5)
        for index, outcome in enumerate(recent):
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

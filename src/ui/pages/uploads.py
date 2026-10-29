import contextlib
import os
import sys
import time

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFileDialog, QPlainTextEdit,
                             QComboBox, QProgressBar)
from PyQt6.QtCore import Qt, QThread, pyqtSignal

from src.core.database import Database
from src.core.paths import app_dir
from src.ui.components.common import PageHeader, make_button, make_label, make_divider, set_role, plural
from src.ui.dialogs.styled_dialogs import show_warning

CAPTION_LIMIT = 2200
PROJECT_DIR = app_dir()


class _LineEmitter:
    def __init__(self, emit):
        self.emit = emit
        self.buffer = ""

    def write(self, text):
        self.buffer += text
        while "\n" in self.buffer:
            line, self.buffer = self.buffer.split("\n", 1)
            if line.strip():
                self.emit(line.rstrip())
        return len(text)

    def flush(self):
        if self.buffer.strip():
            self.emit(self.buffer.strip())
        self.buffer = ""


class UploadThread(QThread):
    line = pyqtSignal(str)
    account_result = pyqtSignal(str, bool, str)
    finished_all = pyqtSignal(int, int)

    def __init__(self, video_path, caption, usernames, delay=0):
        super().__init__()
        self.video_path = video_path
        self.caption = caption
        self.usernames = usernames
        self.delay = max(0, int(delay or 0))
        self.stop_requested = False

    def _sleep(self, seconds):
        """Пауза, которую можно прервать кнопкой «Остановить»."""
        deadline = time.monotonic() + seconds
        while time.monotonic() < deadline:
            if self.stop_requested:
                return
            time.sleep(min(0.5, max(0.0, deadline - time.monotonic())))

    def run(self):
        if str(PROJECT_DIR) not in sys.path:
            sys.path.insert(0, str(PROJECT_DIR))
        done = 0
        try:
            from tiktok_uploader import tiktok
        except Exception as e:
            self.line.emit(f"Не удалось загрузить модуль загрузки: {e}")
            self.finished_all.emit(0, len(self.usernames))
            return

        total = len(self.usernames)
        for index, username in enumerate(self.usernames, 1):
            if self.stop_requested:
                self.line.emit("Остановлено пользователем")
                break
            self.line.emit(f"[{index}/{total}] @{username}")
            emitter = _LineEmitter(lambda text: self.line.emit("    " + text))
            ok = False
            error = ""
            try:
                with contextlib.redirect_stdout(emitter):
                    result = tiktok.upload_video(
                        session_user=username,
                        video=self.video_path,
                        title=self.caption,
                        proxy=os.environ.get("TIKTOK_PROXY") or None,
                    )
                ok = result is not False
                if not ok:
                    error = "TikTok не принял публикацию"
            except (Exception, SystemExit) as e:
                error = str(e) or type(e).__name__
            finally:
                emitter.flush()

            if ok:
                done += 1
                self.line.emit("    Опубликовано")
            else:
                self.line.emit(f"    Ошибка: {error}")
            self.account_result.emit(username, ok, error)

            if index < total and self.delay and not self.stop_requested:
                self.line.emit(f"    Пауза {self.delay} с перед следующим аккаунтом")
                self._sleep(self.delay)

        self.finished_all.emit(done, total)


class UploadsPage(QWidget):
    accounts_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = Database()
        self.video_path = None
        self.thread = None
        self.failed = []
        self.last_job = None
        self._last_status = None
        self._build()
        self.refresh()

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(40, 36, 40, 32)
        root.setSpacing(0)

        self.header = PageHeader("Загрузка", "Одно видео на все аккаунты выбранной группы")
        root.addWidget(self.header)
        root.addSpacing(28)

        form = QVBoxLayout()
        form.setContentsMargins(0, 0, 0, 0)
        form.setSpacing(6)

        form.addWidget(make_label("Видео", "caption"))
        video_row = QHBoxLayout()
        video_row.setSpacing(12)
        self.video_label = make_label("Файл не выбран", "muted")
        self.btn_video = make_button("Выбрать файл")
        self.btn_video.clicked.connect(self._select_video)
        video_row.addWidget(self.video_label, 1)
        video_row.addWidget(self.btn_video)
        form.addLayout(video_row)
        form.addSpacing(16)

        caption_head = QHBoxLayout()
        caption_head.addWidget(make_label("Подпись и хэштеги", "caption"))
        caption_head.addStretch()
        self.counter = make_label(f"0 / {CAPTION_LIMIT}", "caption")
        caption_head.addWidget(self.counter)
        form.addLayout(caption_head)
        self.caption = QPlainTextEdit()
        self.caption.setFixedHeight(120)
        self.caption.setPlaceholderText("Текст под видео. Хэштеги пишите прямо здесь.")
        self.caption.textChanged.connect(self._on_caption)
        form.addWidget(self.caption)
        form.addSpacing(16)

        form.addWidget(make_label("Аккаунты", "caption"))
        self.group = QComboBox()
        self.group.currentIndexChanged.connect(self._update_state)
        form.addWidget(self.group)

        form_wrap = QWidget()
        form_wrap.setLayout(form)
        form_wrap.setMaximumWidth(720)
        root.addWidget(form_wrap)
        root.addSpacing(24)

        actions = QHBoxLayout()
        actions.setContentsMargins(0, 0, 0, 0)
        actions.setSpacing(8)
        self.btn_start = make_button("Опубликовать", "primary")
        self.btn_start.clicked.connect(lambda: self._start())
        self.btn_stop = make_button("Остановить")
        self.btn_stop.clicked.connect(self._stop)
        self.btn_stop.setVisible(False)
        self.btn_retry = make_button("Повторить ошибки")
        self.btn_retry.clicked.connect(self._retry_failed)
        self.btn_retry.setVisible(False)
        self.status = make_label("", "muted")
        actions.addWidget(self.btn_start)
        actions.addWidget(self.btn_stop)
        actions.addWidget(self.btn_retry)
        actions.addSpacing(8)
        actions.addWidget(self.status, 1)
        actions_wrap = QWidget()
        actions_wrap.setLayout(actions)
        actions_wrap.setMaximumWidth(720)
        root.addWidget(actions_wrap)
        root.addSpacing(16)

        self.progress = QProgressBar()
        self.progress.setRange(0, 0)
        self.progress.setTextVisible(False)
        self.progress.setVisible(False)
        root.addWidget(self.progress)

        root.addSpacing(8)
        root.addWidget(make_divider())
        root.addSpacing(16)
        log_head = QHBoxLayout()
        log_head.addWidget(make_label("Журнал", "caption"))
        log_head.addStretch()
        self.btn_copy_log = make_button("Скопировать журнал")
        self.btn_copy_log.clicked.connect(self._copy_log)
        log_head.addWidget(self.btn_copy_log)
        root.addLayout(log_head)
        root.addSpacing(6)
        self.log = QPlainTextEdit()
        self.log.setObjectName("log")
        self.log.setReadOnly(True)
        self.log.setPlaceholderText("Здесь появится ход загрузки и причины ошибок.")
        root.addWidget(self.log, 1)

    def refresh(self):
        current = self.group.currentData()
        self.group.blockSignals(True)
        self.group.clear()
        rows = self.db.fetchall(
            "SELECT tag, COUNT(*) AS c FROM accounts WHERE status = 'active' AND tag IS NOT NULL "
            "GROUP BY tag ORDER BY tag")
        for row in rows:
            self.group.addItem(f"{row[0]}   ·   {plural(row[1], 'аккаунт', 'аккаунта', 'аккаунтов')}", row[0])
        if current is not None:
            index = self.group.findData(current)
            if index >= 0:
                self.group.setCurrentIndex(index)
        self.group.blockSignals(False)
        self._update_state()

    def _select_video(self):
        path, _ = QFileDialog.getOpenFileName(self, "Выбрать видео", "",
                                              "Видео (*.mp4 *.mov *.avi *.mkv);;Все файлы (*)")
        if path:
            self._last_status = None
            self.video_path = path
            size_mb = os.path.getsize(path) / 1024 / 1024
            self.video_label.setText(f"{os.path.basename(path)}   ·   {size_mb:.1f} МБ")
            set_role(self.video_label, "")
            self.failed = []
            self.btn_retry.setVisible(False)
            self._update_state()

    def _on_caption(self):
        self._last_status = None
        length = len(self.caption.toPlainText())
        self.counter.setText(f"{length} / {CAPTION_LIMIT}")
        set_role(self.counter, "err" if length > CAPTION_LIMIT else "caption")
        self._update_state()

    def _busy(self):
        return self.thread is not None

    def _update_state(self):
        busy = self._busy()
        caption = self.caption.toPlainText().strip()
        ready = bool(self.video_path and caption and len(caption) <= CAPTION_LIMIT and self.group.count())
        self.btn_start.setEnabled(ready and not busy)
        self.btn_video.setEnabled(not busy)
        self.group.setEnabled(not busy)
        self.caption.setReadOnly(busy)
        self.btn_retry.setVisible(bool(self.failed) and not busy)
        if busy:
            return
        if self._last_status:
            text, role = self._last_status
            self.status.setText(text)
            set_role(self.status, role)
            return
        if not self.group.count():
            self.status.setText("Сначала добавьте аккаунт")
        elif not ready:
            self.status.setText("Нужны видео, подпись и группа")
        else:
            self.status.setText("")

    def _log(self, text):
        self.log.appendPlainText(text)

    def _copy_log(self):
        from PyQt6.QtWidgets import QApplication
        QApplication.clipboard().setText(self.log.toPlainText())

    def _usernames(self, tag):
        return self.db.get_accounts_by_tag(tag)

    def _start(self, usernames=None):
        if self._busy():
            return
        caption = self.caption.toPlainText().strip()
        tag = self.group.currentData()
        targets = usernames or self._usernames(tag)
        if not targets:
            show_warning(self, "Нет аккаунтов", f"В группе «{tag}» нет активных аккаунтов.")
            return
        if not self.video_path:
            show_warning(self, "Нет видео", "Выберите файл видео.")
            return

        self.failed = []
        self.last_job = (self.video_path, caption)
        self._last_status = None
        self.db.save_video(self.video_path, caption[:100], caption)

        self.log.clear()
        self._log(f"Видео: {os.path.basename(self.video_path)}")
        proxy = os.environ.get("TIKTOK_PROXY")
        self._log(f"Соединение: {proxy if proxy else 'напрямую или VPN'}")
        delay = int(self.db.get("upload_delay", 0) or 0)
        if delay:
            self._log(f"Пауза между аккаунтами: {delay} с")
        self._log(f"Аккаунтов в очереди: {len(targets)}")
        self._log("")

        self.thread = UploadThread(self.video_path, caption, targets, delay)
        self.thread.line.connect(self._log)
        self.thread.account_result.connect(self._account_done)
        self.thread.finished_all.connect(self._finished)
        self.thread.finished.connect(self._thread_closed)
        self.progress.setRange(0, len(targets))
        self.progress.setValue(0)
        self.progress.setVisible(True)
        self.btn_stop.setVisible(True)
        self.btn_stop.setEnabled(True)
        self.status.setText(f"Загрузка идёт: 0 из {len(targets)}")
        set_role(self.status, "muted")
        self.thread.start()
        self._update_state()

    def _retry_failed(self):
        if self.failed and self.last_job:
            path, caption = self.last_job
            self.video_path = path
            if not self.caption.toPlainText().strip():
                self.caption.setPlainText(caption)
            self._start(usernames=list(self.failed))

    def _stop(self):
        if self.thread:
            self.thread.stop_requested = True
            self.btn_stop.setEnabled(False)
            self.status.setText("Остановится после текущего аккаунта")
            set_role(self.status, "muted")

    def _account_done(self, username, ok, error):
        if ok:
            self.db.increment_account_uploads([username])
        self.db.log_upload(username, "ok" if ok else "error",
                           video_path=self.video_path, caption=self.caption.toPlainText().strip(),
                           error=error or None)
        if not ok:
            self.failed.append(username)
        self.progress.setValue(self.progress.value() + 1)
        self.status.setText(f"Загрузка идёт: {self.progress.value()} из {self.progress.maximum()}")
        self.accounts_changed.emit()

    def _finished(self, done, total):
        self.btn_stop.setVisible(False)
        self.progress.setVisible(False)
        self._log("")
        self._log(f"Готово: опубликовано {done} из {total}")
        if self.failed:
            self._log(f"Не удалось: {', '.join('@' + name for name in self.failed)}")
        self._last_status = (f"Опубликовано {done} из {total}",
                             "ok" if done == total and total else "muted" if done else "err")
        self._update_state()

    def _thread_closed(self):
        # QThread нельзя удалять, пока он работает: чистим ссылку только здесь.
        thread = self.thread
        self.thread = None
        if thread is not None:
            thread.deleteLater()
        if not self.failed:
            self.video_path = None
            self.video_label.setText("Файл не выбран")
            set_role(self.video_label, "muted")
            self.caption.clear()
            self.last_job = None
        self._update_state()

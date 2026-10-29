"""Render ClipForge windows for the README (native platform, real text)."""
import os
import sys
import tempfile
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication

from src.app.services import ClipForgeService
from src.core.database import Database
from src.core.stats_store import StatsStore
from src.core.video_randomizer import resolve_ffmpeg
from src.ui.styles import APP_STYLE
from src.ui.windows.main import MainWindow

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "screenshots")
WIDTH, HEIGHT = 1180, 760
PAGES = (("overview", 0), ("uploads", 1), ("accounts", 2), ("stats", 3), ("settings", 4))


def _seed(db):
    for name, tag in (("studio.nord", "launch"), ("studio.sud", "launch"),
                      ("reels.daily", "daily"), ("reels.night", "daily"),
                      ("clips.archive", "archive")):
        db.save_account(name, f"tiktok_session-{name}.cookie", tag=tag)
    db.log_upload("studio.nord", "ok", video_path="launch-reel.mp4", caption="Запуск")
    db.log_upload("studio.sud", "ok", video_path="launch-reel.mp4", caption="Запуск")
    db.log_upload("reels.daily", "error", video_path="launch-reel.mp4", error="сессия недействительна")
    db.log_upload("reels.night", "ok", video_path="launch-reel.mp4", caption="Запуск")
    db.set("upload_delay", 30)
    db.set("randomize_variants", True)
    db.set("randomize_intensity", "medium")

    store = StatsStore(db)
    now = int(time.time())
    demo = {
        "studio.nord": ("nord.studio", 18420, 312),
        "reels.daily": ("reels.daily", 9310, 148),
        "clips.archive": ("clips.archive", 4120, 61),
    }
    for username, (handle, followers, plays) in demo.items():
        data = {"handle": handle, "nickname": handle, "user": {"followers": followers, "following": 120,
                                                               "likes": 4500, "videos": 24},
                "items": [{"id": "730000000000000001", "desc": "Новый ролик · запуск продукта",
                           "createTime": now - 7200, "plays": plays, "likes": plays // 12,
                           "comments": plays // 90, "shares": plays // 60, "saves": plays // 40, "duration": 18}]}
        store.save_snapshot(username, data)
    for username, (handle, followers, plays) in demo.items():
        data = {"handle": handle, "nickname": handle, "user": {"followers": followers + 120, "following": 120,
                                                               "likes": 4500, "videos": 24},
                "items": [{"id": "730000000000000001", "desc": "Новый ролик · запуск продукта",
                           "createTime": now - 7200, "plays": plays + 860, "likes": plays // 12,
                           "comments": plays // 90, "shares": plays // 60, "saves": plays // 40, "duration": 18}]}
        store.save_snapshot(username, data)


def main():
    app = QApplication.instance() or QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setFont(QFont("Segoe UI", 10))
    app.setStyleSheet(APP_STYLE)
    os.makedirs(OUT, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        db = Database(os.path.join(tmp, "shots.db"))
        _seed(db)
        service = ClipForgeService(db)

        video = os.path.join(tmp, "launch-reel.mp4")
        with open(video, "wb") as handle:
            handle.truncate(12_000_000)

        window = MainWindow(service)
        window.uploads_page.caption.setPlainText("Запуск нового ролика · #clipforge #studio")
        window.uploads_page._use_video(video)
        window.uploads_page.log.setPlainText(
            "[1/3] @studio.nord\n"
            "    Готовлю уникальную версию\n"
            "    Вариант: launch-reel-01-studio.nord.mp4 · контраст 1.032 · яркость 0.021 · шум 15 · CRF 25\n"
            "    Опубликовано\n"
            "[2/3] @reels.daily\n"
            "    Готовлю уникальную версию\n"
            "    Вариант: launch-reel-02-reels.daily.mp4 · контраст 0.978 · яркость -0.018 · шум 20 · CRF 27\n"
            "    Опубликовано"
        )
        window.resize(WIDTH, HEIGHT)
        window.show()

        for name, index in PAGES:
            window.show_page(index)
            app.processEvents()
            window.grab().save(os.path.join(OUT, f"{name}.png"))

    print("README SHOTS OK", resolve_ffmpeg() is not None)


if __name__ == "__main__":
    main()

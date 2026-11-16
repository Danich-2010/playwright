# ФИО: Данич И. А.
# Дата: 15.11.2026
# Время: 20:45
# Тема: Videos в Playwright, раздел "Videos"
# Описание: Код скопирован из документации без искажений
# (подраздел "Record video"). Создаёт контекст с записью видео
# в папку videos/. Видео сохраняется ТОЛЬКО при закрытии
# контекста — поэтому обязательно context.close().
# ============================================================

import os
from playwright.sync_api import sync_playwright

os.makedirs("videos", exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(record_video_dir="videos/")
    page = context.new_page()
    page.goto("data:text/html,<html><body><h1>Hello</h1></body></html>")

    # Make sure to close, so that videos are saved.
    context.close()
    browser.close()

print("Видео сохранено в videos/")
# ФИО: Данич И. А.
# Дата: 15.11.2026
# Время: 22:05
# Тема: Selenium Grid (experimental) в Playwright, раздел "Selenium Grid (experimental)"
# Описание: Код скопирован из документации без искажений
# (подраздел "Connecting Playwright to Selenium Grid").
# Подключается к Selenium Grid 4 через переменную окружения
# SELENIUM_REMOTE_URL и запускает Chromium на удалённом узле.
# Код теста менять не нужно — используется browser_type.launch()
# как обычно.
# ============================================================

import os
from playwright.sync_api import sync_playwright

# Эквивалент: SELENIUM_REMOTE_URL=http://<selenium-hub-ip>:4444 pytest --browser chromium
os.environ["SELENIUM_REMOTE_URL"] = os.environ.get(
    "SELENIUM_REMOTE_URL", "http://localhost:4444"
)

with sync_playwright() as p:
    # Playwright сам подключится к Grid по SELENIUM_REMOTE_URL
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://playwright.dev/")
    print("Заголовок:", page.title())
    browser.close()
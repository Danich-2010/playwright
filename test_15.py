# ФИО: Данич И. А.
# Дата: 15.11.2026
# Время: 20:50
# Тема: Браузеры в Playwright, раздел "Браузеры"
# Описание: Код скопирован из документации без искажений.
# Запускает Chromium с указанием канала браузера "msedge"
# (Microsoft Edge), открывает playwright.dev и выводит заголовок.
# Демонстрирует запуск в фирменном браузере через параметр channel.
# ============================================================

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # Channel can be "chrome", "msedge", "chrome-beta", "msedge-beta" or "msedge-dev".
    browser = p.chromium.launch(channel="msedge")
    page = browser.new_page()
    page.goto("https://playwright.dev")
    print(page.title())
    browser.close()
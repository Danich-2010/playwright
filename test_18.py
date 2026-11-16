# ФИО: Данич И. А.
# Дата: 15.11.2026
# Время: 18:50
# Тема: Отладочные тесты в Playwright, раздел "Отладочные тесты"
# Описание: Код скопирован из документации без искажений
# (пример из подраздела "Режим заголовка").
# Запускает Chromium в режиме с графическим интерфейсом (headless=False)
# и замедляет выполнение на 100 мс на операцию (slow_mo=100),
# чтобы можно было наблюдать за процессом во время отладки.
# ============================================================

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # Chromium, Firefox, or WebKit
    # headless=False — браузер с графическим интерфейсом (режим заголовка)
    # slow_mo=100 — замедление на 100 мс на операцию для наблюдения
    browser = p.chromium.launch(headless=False, slow_mo=100)
    page = browser.new_page()
    page.goto("https://playwright.dev/")
    print("Заголовок:", page.title())
    browser.close()
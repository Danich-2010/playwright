# ФИО: Данич И. А.
# Дата: 15.11.2026
# Время: 20:10
# Тема: Выполнение JavaScript в Playwright, раздел "Выполнение JavaScript"
# Описание: Код скопирован из документации без искажений
# (подраздел "Введение"). Запускает функцию JavaScript в контексте
# веб-страницы через page.evaluate() и возвращает результат
# (href текущей страницы) обратно в среду Playwright.
# ============================================================

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://playwright.dev/")

    # Выполняем функцию в контексте страницы, получаем href.
    href = page.evaluate('() => document.location.href')
    print("href:", href)

    browser.close()
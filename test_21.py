# ФИО: Данич И. А.
# Дата: 15.11.2026
# Время: 20:45
# Тема: Эмуляция в Playwright, раздел "Эмуляция"
# Описание: Код скопирован из документации без искажений
# (подраздел "Устройства"). Получает параметры устройства
# iPhone 13 из playwright.devices и создаёт контекст браузера
# WebKit с этими параметрами (user agent, screen size,
# viewport, touch и т.д.).
# ============================================================

from playwright.sync_api import sync_playwright, Playwright

def run(playwright: Playwright):
    iphone_13 = playwright.devices['iPhone 13']
    browser = playwright.webkit.launch(headless=False)
    context = browser.new_context(
        **iphone_13,
    )
    page = context.new_page()
    page.goto("https://playwright.dev/")
    print("Заголовок:", page.title())
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
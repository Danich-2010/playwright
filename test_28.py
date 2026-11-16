# ФИО: Данич И. А.
# Дата: 15.11.2026
# Время: 21:50
# Тема: Isolation в Playwright, раздел "Isolation"
# Описание: Код скопирован из документации без искажений
# (подраздел "Multiple Contexts in a Single Test").
# Создаёт экземпляр Chromium, затем два изолированных
# browser context — user_context и admin_context. Каждый
# контекст эквивалентен профилю инкогнито: свои cookies,
# localStorage, sessionStorage. Страницы в контекстах можно
# использовать независимо (например, для тестирования
# многопользовательского сценария — чата).
# ============================================================

from playwright.sync_api import sync_playwright, Playwright

def run(playwright: Playwright):
    # create a chromium browser instance
    chromium = playwright.chromium
    browser = chromium.launch()

    # create two isolated browser contexts
    user_context = browser.new_context()
    admin_context = browser.new_context()

    # create pages and interact with contexts independently
    user_page = user_context.new_page()
    admin_page = admin_context.new_page()

    user_page.goto("https://playwright.dev/")
    admin_page.goto("https://playwright.dev/")

    print("user title:", user_page.title())
    print("admin title:", admin_page.title())

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
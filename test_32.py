# ФИО: Данич И. А.
# Дата: 15.11.2026
# Время: 20:15
# Тема: Network в Playwright, раздел "Network"
# Описание: Код скопирован из документации без искажений
# (подраздел "Network events"). Подписывается на события
# "request" и "response", открывает страницу и выводит в консоль
# все запросы (метод, URL) и ответы (статус, URL).
# ============================================================

from playwright.sync_api import sync_playwright, Playwright

def run(playwright: Playwright):
    chromium = playwright.chromium
    browser = chromium.launch()
    page = browser.new_page()

    # Subscribe to "request" and "response" events.
    page.on("request", lambda request: print(">>", request.method, request.url))
    page.on("response", lambda response: print("<<", response.status, response.url))

    page.goto("https://example.com")
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
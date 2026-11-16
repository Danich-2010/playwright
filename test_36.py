# ФИО: Данич И. А.
# Дата: 15.11.2026
# Время: 21:50
# Тема: Screenshots в Playwright, раздел "Screenshots"
# Описание: Код скопирован из документации без искажений
# (подраздел "Introduction"). Делает скриншот страницы и
# сохраняет его в файл screenshot.png.
# ============================================================

from playwright.sync_api import sync_playwright

HTML = "<html><body><h1>Hello</h1></body></html>"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(f"data:text/html,{HTML}")

    page.screenshot(path="screenshot.png")
    print("Скриншот сохранён: screenshot.png")

    browser.close()
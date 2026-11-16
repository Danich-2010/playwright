# ФИО: Данич И. А.
# Дата: 15.11.2026
# Время: 20:50
# Тема: События в Playwright, раздел "События"
# Описание: Код скопирован из документации без искажений
# (подраздел "Ожидание события"). Ожидает сетевой запрос
# с URL, содержащим "logo" и заканчивающимся на .png,
# при переходе на wikipedia.org, затем выводит URL запроса.
# ============================================================

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    # Начинаем ждать запрос до перехода на страницу.
    with page.expect_request("**/*logo*.png") as first:
        page.goto("https://wikipedia.org")

    print(first.value.url)
    browser.close()
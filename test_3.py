# ФИО: Данич И. А.
# Дата: 14.11.2026
# Время: 18:10
# Описание кода своими словами:
# Этот скрипт написан с использованием синхронного API Playwright (`sync_playwright`) без тест-раннера Pytest
# (такую структуру обычно создает генератор кода `playwright codegen`).
#
# Что делает каждая значимая часть:
# 1. `with sync_playwright() as playwright:` — запускает движок Playwright и передает его в функцию `run()`.
# 2. `playwright.chromium.launch(headless=False)` — запускает браузер Chromium в графическом режиме
#    (`headless=False` означает, что окно браузера реально откроется на экране монитора).
# 3. `browser.new_context(viewport={"width":800,"height":600})` — создает изолированный контекст (сессию)
#    и принудительно задает размер рабочей области окна браузера 800 на 600 пикселей.
# 4. `context.new_page()` и `page.goto(...)` — открывает новую вкладку и переходит на сайт playwright.dev.
# 5. `page.get_by_role("link", name="Get started").click()` — находит ссылку "Get started" и кликает по ней.
# 6. Блок проверок `expect` с использованием CSS-локаторов (`page.locator`):
#    - `page.locator("h1")` — ищет заголовок первого уровня по HTML-тегу `<h1>` и проверяет, что в нем есть текст "Installation".
#    - `page.locator("#introduction")` — ищет элемент по уникальному ID (`id="introduction"`) и проверяет текст "Introduction".
#    - `page.locator(".tabs").first` — ищет элементы по CSS-классу `class="tabs"`, берет самый первый из них (`.first`)
#      и проверяет, что он виден на экране (`to_be_visible()`).
# 7. `context.close()` и `browser.close()` — корректно закрывают сессию и сам браузер для освобождения памяти.

import re
from playwright.sync_api import Playwright, expect, sync_playwright


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(viewport={"width": 800, "height": 600})
    page = context.new_page()
    page.goto("https://playwright.dev/")
    page.get_by_role("link", name="Get started").click()
    expect(page.locator("h1")).to_contain_text("Installation")
    expect(page.locator("#introduction")).to_contain_text("Introduction")
    expect(page.locator(".tabs").first).to_be_visible()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
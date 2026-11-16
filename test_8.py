# ФИО: Данич И. А.
# Дата: 14.11.2026
# Время: 23:30
# Описание раздела "Getting started - Library" и кода своими словами:
# В этом разделе показано, как использовать Playwright напрямую как Python-библиотеку (без Pytest).
# Установка базовой библиотеки выполняется командами: `pip install playwright` и `playwright install`.
#
# Playwright поддерживает два варианта API: синхронный (`sync_playwright`) и асинхронный (`async_playwright`).
#
# Что делает каждая значимая часть кода ниже:
# 1. Блок синхронного запуска (Usage & First script):
#    - Конструкция `with sync_playwright() as p:` автоматически запускает фоновый драйвер Playwright
#      и гарантированно останавливает его при выходе из блока `with`.
#    - `p.chromium.launch()` и `p.webkit.launch()` — запускают браузеры Chromium и WebKit (по умолчанию
#      в фоновом режиме `headless=True`).
#    - `browser.new_page()` — создает новую вкладку в браузере.
#    - `page.goto("https://playwright.dev/")` — переходит по указанному адресу.
#    - `print(page.title())` — выводит в консоль текстовый заголовок открытой веб-страницы.
#    - `page.screenshot(path="example.png")` — делает снимок экрана страницы и сохраняет его в файл `example.png`.
#    - `browser.close()` — закрывает браузер.
#
# 2. Блок асинхронного запуска (Async API):
#    - Используется в современных проектах, построенных на библиотеке `asyncio`.
#    - Внутри асинхронной функции `async def main():` используется менеджер `async with async_playwright() as p:`.
#    - Перед каждым вызовом метода Playwright (запуск браузера, создание вкладки, переход по URL,
#      получение заголовка и закрытие) обязательно ставится ключевое слово `await`, чтобы не блокировать
#      цикл событий (Event Loop). Запускается функция через `asyncio.run(main())`.
#
# 3. Также в разделе описаны:
#    - Интерактивный режим (REPL): запуск без блока `with` вручную через `playwright = sync_playwright().start()`
#      и завершение через `playwright.stop()`.
#    - Сборка в исполняемый файл (.exe) через `pyinstaller -F main.py` (переменная `PLAYWRIGHT_BROWSERS_PATH=0`
#      позволяет упаковать браузер внутрь самого файла).
#    - Известные проблемы (Known issues): запрет на использование `time.sleep()` (вместо него нужно
#      использовать `page.wait_for_timeout()`), отсутствие потокобезопасности (в каждом потоке Threading
#      нужен свой экземпляр Playwright) и защита асинхронных задач через `asyncio.shield()`.

import asyncio
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright

# --- 1. Синхронный API (Usage & First script) ---
with sync_playwright() as p:
    # Запуск Chromium и вывод заголовка страницы
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://playwright.dev")
    print(page.title())
    browser.close()

    # Запуск WebKit и сохранение скриншота страницы
    browser_webkit = p.webkit.launch()
    page_webkit = browser_webkit.new_page()
    page_webkit.goto("https://playwright.dev/")
    page_webkit.screenshot(path="example.png")
    browser_webkit.close()


# --- 2. Асинхронный API (Async API) ---
async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://playwright.dev")
        print(await page.title())
        await browser.close()


asyncio.run(main())
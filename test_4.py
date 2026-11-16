# ФИО: Данич И. А.
# Дата: 14.11.2026
# Время: 19:30
# Описание раздела документации "Запуск и отладка тестов" своими словами:
# В этом разделе описаны флаги командной строки для управления запуском тестов через Pytest и их отладки.
#
# 1. Базовый запуск:
#    Команда `pytest` — запускает все тесты в проекте. По умолчанию используется браузер Chromium
#    в фоновом ("безголовом" / headless) режиме без открытия графического окна.
#
# 2. Видимый режим браузера:
#    Команда `pytest --headed` — запускает тесты с открытием реального графического окна браузера на экране.
#
# 3. Выбор браузеров:
#    Команда `pytest --browser webkit` — запускает тесты в движке WebKit (движок браузера Apple Safari).
#    Команда `pytest --browser webkit --browser firefox` — запускает каждый тест последовательно
#    сразу в нескольких указанных браузерах (WebKit и Mozilla Firefox).
#
# 4. Выборочный запуск тестов:
#    Команда `pytest test_login.py` — запускает тесты только из одного конкретного файла.
#    Команда `pytest tests/test_todo_page.py tests/test_landing_page.py` — запускает несколько указанных файлов.
#    Команда `pytest -k test_get_started_link` — флаг `-k` позволяет запустить только одну конкретную
#    тестовую функцию по её имени (или по части имени).
#
# 5. Параллельный запуск:
#    Команда `pytest --numprocesses 2` — запускает тесты параллельно в 2 потока (процесса) для ускорения
#    прогона (требует установленного плагина `pytest-xdist`). Рекомендуется ставить половину от ядер процессора.
#
# 6. Отладка через Playwright Inspector:
#    Команда `PWDEBUG=1 pytest -s` (для Bash) или `$env:PWDEBUG=1; pytest -s` (для PowerShell в Windows) —
#    включает режим отладки. При этом открывается видимый браузер и окно утилиты Playwright Inspector,
#    где можно выполнять тест пошагово (Step over), исследовать и копировать локаторы элементов в реальном времени.
#    Также можно отлаживать отдельный файл (`PWDEBUG=1 pytest -s test_example.py`)
#    или конкретный тест (`PWDEBUG=1 pytest -s -k test_get_started_link`).

import re
from playwright.sync_api import Page, expect


# Тестовый код из документации для проверки работы всех команд запуска и отладки:
def test_has_title(page: Page):
    page.goto("https://playwright.dev/")
    expect(page).to_have_title(re.compile("Playwright"))


def test_get_started_link(page: Page):
    page.goto("https://playwright.dev/")
    page.get_by_role("link", name="Get started").click()
    expect(page.get_by_role("heading", name="Installation")).to_be_visible()


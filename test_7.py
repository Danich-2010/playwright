# ФИО: Данич И. А.
# Дата: 14.11.2026
# Время: 22:30
# Описание раздела "Pytest Plugin Reference" и кода своими словами:
# Плагин `pytest-playwright` предоставляет специальные аргументы командной строки, фикстуры и маркеры:
#
# 1. Конфигурация `pytest.ini`: чтобы не вводить флаги (--headed, --browser, --slowmo, --video, --screenshot)
#    вручную при каждом запуске, их можно прописать в файле `pytest.ini` в параметре `addopts`.
#    Важно: флаги CLI применяются только к встроенным фикстурам (`page`, `context`, `new_context`).
#
# 2. Области видимости фикстур (Scopes):
#    - Function scope (создаются заново для каждого теста): `page`, `context`, `new_context`.
#    - Session scope (создаются один раз на весь прогон всех тестов): `playwright`, `browser`,
#      `browser_type`, `browser_name`, булевы флаги `is_chromium`, `is_firefox`, `is_webkit`.
#
# 3. Что делает скопированный ниже код из раздела Examples:
#    - Фикстура `browser_context_args` (scope="session"): переопределяет стандартные настройки контекста
#      для всех тестов — включает игнорирование ошибок HTTPS-сертификатов (`ignore_https_errors: True`)
#      и задает FullHD разрешение экрана (`1920x1080`).
#    - Тест `test_foo`: использует фикстуру `new_context` (CreateContextCallback) для создания второго
#      независимого контекста браузера внутри одного теста. Это нужно для тестирования многопользовательских
#      сценариев (например, когда нужно проверить чат между двумя разными пользователями `page` и `page2`).
#    - Тест `test_visit_example_skip`: использует маркер `@pytest.mark.skip_browser("firefox")`, который
#      автоматически пропускает этот тест, если прогон запущен в браузере Firefox.
#    - Тест `test_visit_example_only`: использует маркер `@pytest.mark.only_browser("chromium")`, который
#      разрешает запуск теста только в браузере Chromium.

from playwright.sync_api import BrowserContext, Page
import pytest
from pytest_playwright.pytest_playwright import CreateContextCallback


# Переопределение параметров контекста (Ignore HTTPS errors + Custom viewport size)
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "ignore_https_errors": True,
        "viewport": {
            "width": 1920,
            "height": 1080,
        },
    }


# Пример "Using multiple contexts" (Симуляция нескольких пользователей в одном тесте)
def test_foo(page: Page, new_context: CreateContextCallback) -> None:
    page.goto("https://example.com")
    context = new_context()
    page2 = context.new_page()
    page2.goto("https://example.com")
    # page и page2 находятся в разных изолированных контекстах (не делят cookies)


# Пример "Skip test by browser" (Пропуск теста для конкретного браузера)
@pytest.mark.skip_browser("firefox")
def test_visit_example_skip(page: Page):
    page.goto("https://example.com")


# Пример "Run on a specific browser" (Запуск только в указанном браузере)
@pytest.mark.only_browser("chromium")
def test_visit_example_only(page: Page):
    page.goto("https://example.com")

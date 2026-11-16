# ФИО: Данич И. А.
# Дата: 14.11.2026
# Время: 16:00
# Описание кода своими словами (Раздел: Изоляция тестов и Использование фикстур):
# 1. Декоратор `@pytest.fixture(scope="function", autouse=True)` создает тестовый хук (приспособление),
#    который автоматически (`autouse=True`) запускается перед КАЖДОЙ тестовой функцией (`scope="function"`).
# 2. До ключевого слова `yield` выполняется предусловие (аналог beforeEach): в консоль выводится текст
#    "before the test runs" и браузер автоматически переходит на сайт https://playwright.dev/.
# 3. Команда `yield` передает управление самому тесту (`test_main_navigation`).
# 4. В самом тесте нам уже не нужно писать `page.goto()`, так как фикстура сделала это за нас.
#    Тест сразу проверяет через утверждение `expect(page).to_have_url()`, что открыт правильный адрес.
# 5. После завершения теста управление возвращается в фикстуру после слова `yield` (аналог afterEach),
#    и в консоль выводится сообщение "after the test runs". При этом каждый тест работает в своем
#    изолированном контексте браузера (BrowserContext), как в новом профиле.

import pytest
from playwright.sync_api import Page, expect


@pytest.fixture(scope="function", autouse=True)
def before_each_after_each(page: Page):
    print("before the test runs")

    # Переходим на стартовый URL перед каждым тестом
    page.goto("https://playwright.dev/")
    yield

    print("after the test runs")


def test_main_navigation(page: Page):
    # Утверждение проверяет, что текущая страница имеет ожидаемый URL
    expect(page).to_have_url("https://playwright.dev/")
    
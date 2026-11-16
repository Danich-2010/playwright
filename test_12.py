
# ФИО: Данич И. А.
# Дата: 14.11.2026
# Время: 21:15
# Описание раздела документации "Тестирование API (API Testing)" и кода своими словами:
# Playwright позволяет тестировать REST API сервера напрямую через `APIRequestContext`, не загружая
# веб-страницу в браузере. Это используется в 4 случаях:
# 1. Прямое тестирование бэкенда (REST API).
# 2. Быстрая подготовка данных на сервере (Setup) перед открытием страницы в браузере.
# 3. Проверка постусловий (post-conditions) на сервере после действий пользователя в браузере.
# 4. Быстрая авторизация через API и передача полученных cookies в браузер через `storage_state()`.
#
# Что делает каждая значимая часть полного примера кода ниже:
# 1. Чтение переменных окружения: с помощью `os.getenv()` скрипт получает персональный токен
#    `GITHUB_API_TOKEN` и логин `GITHUB_USER` для работы с API GitHub.
# 2. Сессионная фикстура `api_request_context`:
#    - Создается один раз на всю тестовую сессию (`scope="session"`).
#    - Формирует заголовки `headers`: стандартный заголовок версии API GitHub (`Accept`) и токен авторизации (`Authorization`).
#    - Вызывает `playwright.request.new_context(base_url="https://api.github.com", extra_http_headers=headers)`,
#      чтобы все последующие запросы автоматически шли на сервер GitHub с нужными заголовками.
#    - После завершения всех тестов (`yield`) очищает память вызовом `request_context.dispose()`.
# 3. Сессионная фикстура `create_test_repository` (`autouse=True`):
#    - Выполняет предусловие (Setup / "Before all"): до запуска тестов отправляет POST-запрос на `/user/repos`,
#      создавая временный репозиторий с именем "test".
#    - Выполняет постусловие (Teardown / "After all"): после прогона всех тестов (после `yield`) отправляет
#      DELETE-запрос и удаляет тестовый репозиторий.
# 4. Тесты `test_should_create_bug_report` и `test_should_create_feature_request`:
#    - Отправляют POST-запрос с JSON-данными (`title` и `body`) для создания новой задачи (Issue) в репозитории.
#    - Проверяют успешность создания через `assert new_issue.ok` (статус-код 200–299).
#    - Отправляют GET-запрос для получения списка всех задач репозитория, преобразуют ответ из JSON
#      в список словарей Python (`issues.json()`), находят созданную задачу через `filter()` и проверяют её текст.

from enum import auto
import os
from typing import Generator

from playwright.sync_api import APIRequestContext, Page, Playwright, expect
import pytest

GITHUB_API_TOKEN = os.getenv("GITHUB_API_TOKEN")
assert GITHUB_API_TOKEN, "GITHUB_API_TOKEN is not set"

GITHUB_USER = os.getenv("GITHUB_USER")
assert GITHUB_USER, "GITHUB_USER is not set"

GITHUB_REPO = "test"


@pytest.fixture(scope="session")
def api_request_context(
    playwright: Playwright,
) -> Generator[APIRequestContext, None, None]:
    headers = {
        # Устанавливаем заголовок в соответствии с рекомендациями документации GitHub
        "Accept": "application/vnd.github.v3+json",
        # Добавляем токен авторизации ко всем запросам
        "Authorization": f"token {GITHUB_API_TOKEN}",
    }
    request_context = playwright.request.new_context(
        base_url="https://api.github.com", extra_http_headers=headers
    )
    yield request_context
    request_context.dispose()


@pytest.fixture(scope="session", autouse=True)
def create_test_repository(
    api_request_context: APIRequestContext,
) -> Generator[None, None, None]:
    # Before all (Предусловие: создаем тестовый репозиторий перед всеми тестами)
    new_repo = api_request_context.post(
        "/user/repos", data={"name": GITHUB_REPO}
    )
    assert new_repo.ok
    yield
    # After all (Постусловие: удаляем тестовый репозиторий после всех тестов)
    deleted_repo = api_request_context.delete(
        f"/repos/{GITHUB_USER}/{GITHUB_REPO}"
    )
    assert deleted_repo.ok


def test_should_create_bug_report(
    api_request_context: APIRequestContext,
) -> None:
    data = {
        "title": "[Bug] report 1",
        "body": "Bug description",
    }
    new_issue = api_request_context.post(
        f"/repos/{GITHUB_USER}/{GITHUB_REPO}/issues", data=data
    )
    assert new_issue.ok

    issues = api_request_context.get(
        f"/repos/{GITHUB_USER}/{GITHUB_REPO}/issues"
    )
    assert issues.ok
    issues_response = issues.json()
    issue = list(
        filter(
            lambda issue: issue["title"] == "[Bug] report 1", issues_response
        )
    )[0]
    assert issue
    assert issue["body"] == "Bug description"


def test_should_create_feature_request(
    api_request_context: APIRequestContext,
) -> None:
    data = {
        "title": "[Feature] request 1",
        "body": "Feature description",
    }
    new_issue = api_request_context.post(
        f"/repos/{GITHUB_USER}/{GITHUB_REPO}/issues", data=data
    )
    assert new_issue.ok

    issues = api_request_context.get(
        f"/repos/{GITHUB_USER}/{GITHUB_REPO}/issues"
    )
    assert issues.ok
    issues_response = issues.json()
    issue = list(
        filter(
            lambda issue: issue["title"] == "[Feature] request 1",
            issues_response,
        )
    )[0]
    assert issue
    assert issue["body"] == "Feature description"

# ФИО: Данич И. А.
# Дата: 15.11.2026
# Время: 15:10
# Описание изменений: Я модифицировал исходный код из документации примерно на 30%.
# 1. Вынес адрес сайта в отдельную константу `BASE_URL`.
#    Зачем: чтобы избежать дублирования кода (принцип DRY). Если URL изменится, его нужно поменять только в одном месте.
# 2. В первом тесте добавил поиск и проверку видимости главного заголовка на странице (`main_heading`).
#    Зачем: проверка только тега <title> не гарантирует, что сама веб-страница корректно отрисовалась на экране.
# 3. Во втором тесте после клика добавил проверку URL через `expect(page).to_have_url()`.
#    Зачем: при тестировании навигации важно убедиться, что не только появился заголовок "Installation",
#    но и адресная строка браузера изменилась на корректный маршрут документации (/docs/intro).

import re
from playwright.sync_api import Page, expect

BASE_URL = "https://playwright.dev/"  # Добавлено: константа базового адреса


def test_has_title(page: Page):
    page.goto(BASE_URL)

    expect(page).to_have_title(re.compile("Playwright"))

    # Добавлено: проверка отображения главного баннера/заголовка на самой странице
    main_heading = page.get_by_role(
        "heading", name=re.compile("Playwright enables")
    )
    expect(main_heading).to_be_visible()


def test_get_started_link(page: Page):
    page.goto(BASE_URL)

    page.get_by_role("link", name="Get started").click()

    # Добавлено: проверка того, что URL изменился на страницу введения в документацию
    expect(page).to_have_url(re.compile(".*/docs/intro"))

    expect(page.get_by_role("heading", name="Installation")).to_be_visible()


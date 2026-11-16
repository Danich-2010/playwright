# ФИО: Данич И. А.
# Дата: 14.11.2026
# Время: 18:00
# Описание раздела "Release notes" и кода своими словами:
# Раздел Release Notes описывает ключевые нововведения и изменения API Playwright от версии 1.7 до 1.65:
# - Появление пользовательских локаторов `get_by_role`, `get_by_label`, `get_by_placeholder` (v1.27) и Strict Mode (v1.14).
# - Устаревание метода `.type()` и замена его на быстрый `.fill()` и посимвольный `.press_sequentially()` (v1.38).
# - Появление генератора утверждений в Codegen (v1.40), обработчиков баннеров `add_locator_handler` (v1.42),
#   управления временем `page.clock` (v1.45), снимков дерева доступности `to_match_aria_snapshot` и групп
#   трассировки `tracing.group` (v1.49), кастомных описаний `locator.describe` (v1.53), поддержки WebP (v1.62)
#   и вложенных локаторов `locator.within` (v1.64).
#
# Что делает каждая значимая часть скопированного ниже кода (из примеров v1.40 и v1.49):
# 1. `page.goto("https://playwright.dev/")` — открывает главную страницу документации Playwright.
# 2. `page.get_by_role("link", name="Get started").click()` — переходит в раздел начала работы.
# 3. `expect(page.get_by_label("Breadcrumbs").get_by_role("list")).to_contain_text("Installation")` —
#    находит навигационную цепочку ("хлебные крошки" по aria-label="Breadcrumbs"), внутри неё ищет список
#    и проверяет, что мы находимся на странице "Installation".
# 4. `expect(page.get_by_label("Search")).to_be_visible()` — проверяет видимость кнопки поиска по сайту
#    и кликает по ней (`.click()`), открывая модальное окно поиска.
# 5. `page.get_by_placeholder("Search docs").fill("locator")` — находит поле ввода по тексту-подсказке
#    (placeholder="Search docs") и мгновенно заполняет его словом "locator".
# 6. `expect(...).to_have_value("locator")` — проверяет, что в поле ввода действительно установлено значение "locator".

from playwright.sync_api import Page, expect


def test_example(page: Page) -> None:
    page.goto("https://playwright.dev/")
    page.get_by_role("link", name="Get started").click()
    expect(
        page.get_by_label("Breadcrumbs").get_by_role("list")
    ).to_contain_text("Installation")
    expect(page.get_by_label("Search")).to_be_visible()
    page.get_by_label("Search").click()
    page.get_by_placeholder("Search docs").fill("locator")
    expect(page.get_by_placeholder("Search docs")).to_have_value("locator")
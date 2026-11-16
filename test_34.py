# ФИО: Данич И. А.
# Дата: 15.11.2026
# Время: 21:10
# Тема: Pages в Playwright, раздел "Pages"
# Описание: Код скопирован из документации без искажений
# (подраздел "Pages"). Создаёт страницу в контексте, явно
# переходит по URL через goto(), заполняет поле #search,
# кликает #submit (неявная навигация) и выводит новый URL.
# ============================================================

from playwright.sync_api import sync_playwright

# Локальная страница вместо example.com: форма с #search и #submit.
HTML = """
<html><body>
  <input id="search" type="text">
  <a id="submit" href="data:text/html,<html><body>result page</body></html>">Submit</a>
</body></html>
"""

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context()
    page = context.new_page()

    # Navigate explicitly, similar to entering a URL in the browser.
    page.goto(f"data:text/html,{HTML}")

    # Fill an input.
    page.locator('#search').fill('query')

    # Navigate implicitly by clicking a link.
    page.locator('#submit').click()

    # Expect a new url.
    print(page.url)

    browser.close()
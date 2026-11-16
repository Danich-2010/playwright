# ФИО: Данич И. А.
# Дата: 15.11.2026
# Время: 21:05
# Тема: Extensibility → Custom selector engines, раздел документации Playwright
# Описание: Код скопирован из документации без искажений.
# Регистрирует пользовательский движок селекторов "tag", который
# ищет элементы по имени тега (query/queryAll). После регистрации
# движка можно использовать селекторы "tag=button", "tag=div" и т.д.,
# комбинировать с встроенными локаторами и вызывать count().
# ============================================================

from playwright.sync_api import sync_playwright

# HTML-страница с кнопкой и div, чтобы пример запускался.
HTML = """
<html><body>
  <button>Submit</button>
  <div>click me</div>
</body></html>
"""

tag_selector = """
    // Must evaluate to a selector engine instance.
    {
      // Returns the first element matching given selector in the root's subtree.
      query(root, selector) {
        return root.querySelector(selector);
      },

      // Returns all elements matching given selector in the root's subtree.
      queryAll(root, selector) {
        return Array.from(root.querySelectorAll(selector));
      }
    }"""

with sync_playwright() as p:
    # register the engine. selectors will be prefixed with "tag=".
    p.selectors.register("tag", tag_selector)

    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(f"data:text/html,{HTML}")

    # now we can use "tag=" selectors.
    button = page.locator("tag=button")
    button.click()

    # we can combine it with built-in locators.
    page.locator("tag=div").get_by_text("click me").click()

    # we can use it in any methods supporting selectors.
    button_count = page.locator("tag=button").count()

    print("Количество кнопок:", button_count)
    browser.close()
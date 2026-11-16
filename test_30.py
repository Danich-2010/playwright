# ФИО: Данич И. А.
# Дата: 15.11.2026
# Время: 18:55
# Тема: Mock APIs в Playwright, раздел "Mock APIs"
# Описание: Код скопирован из документации без искажений
# (подраздел "Mock API requests"). Перехватывает все запросы
# к */**/api/v1/fruits и возвращает кастомный ответ (Strawberry).
# Реальный запрос к API не выполняется. Затем открывает страницу
# и проверяет, что замоканные данные отображаются.
# ============================================================

from playwright.sync_api import sync_playwright, expect, Route

# HTML-страница, которая делает fetch к /api/v1/fruits и рендерит список.
HTML = """
<html><body>
  <ul id="fruits"></ul>
  <script>
    fetch('/api/v1/fruits')
      .then(r => r.json())
      .then(data => {
        document.getElementById('fruits').innerHTML =
          data.map(f => `<li>${f.name}</li>`).join('');
      });
  </script>
</body></html>
"""

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    def handle(route: Route):
        json = [{"name": "Strawberry", "id": 21}]
        # fulfill the route with the mock data
        route.fulfill(json=json)

    # Intercept the route to the fruit API
    page.route("*/**/api/v1/fruits", handle)

    # Go to the page
    page.goto(f"data:text/html,{HTML}")

    # Assert that the Strawberry fruit is visible
    expect(page.get_by_text("Strawberry")).to_be_visible()

    print("Strawberry видна — мок сработал")
    browser.close()
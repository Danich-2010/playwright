# ФИО: Данич И. А.
# Дата: 15.11.2026
# Время: 19:35
# Тема: Navigations в Playwright, раздел "Navigations"
# Описание: Код скопирован из документации без искажений
# (подраздел "Basic navigation"). Открывает страницу через
# page.goto() и ждёт события load — загрузки всей страницы,
# включая стили, скрипты, iframe и изображения. Затем кликает
# по тексту "example domain" — Playwright автоматически ждёт,
# пока элемент станет actionable (видимым, стабильным и т.д.).
# ============================================================

from playwright.sync_api import sync_playwright

# Локальная страница вместо example.com (работает без сети).
HTML = """
<html><body>
  <a href="data:text/html,<html><body>target page</body></html>">example domain</a>
</body></html>
"""

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    # Navigate the page
    page.goto(f"data:text/html,{HTML}")

    # Navigate and click element
    # Click will auto-wait for the element
    page.get_by_text("example domain").click()

    print("Переход выполнен, URL:", page.url[:50] + "...")
    browser.close()
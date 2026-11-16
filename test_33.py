# ФИО: Данич И. А.
# Дата: 15.11.2026
# Время: 20:55
# Тема: Other locators в Playwright, раздел "Other locators"
# Описание: Код скопирован из документации без искажений
# (подраздел "CSS: matching only visible elements").
# Демонстрирует разницу между css=button (все кнопки, включая
# скрытую — strictness violation) и css=button:visible (только
# видимая кнопка). Для запуска используется локальная страница
# с двумя кнопками: скрытой и видимой.
# ============================================================

from playwright.sync_api import sync_playwright

# HTML-страница с двумя кнопками: скрытой и видимой.
HTML = """
<html><body>
  <button style='display: none'>Invisible</button>
  <button>Visible</button>
</body></html>
"""

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(f"data:text/html,{HTML}")

    # Это найдёт обе кнопки и выбросит strictness violation:
    try:
        page.locator("button").click()
        print("Ошибки не было (неожиданно)")
    except Exception as e:
        print(f"strictness violation: {type(e).__name__}")

    # Это найдёт только видимую кнопку и кликнет её:
    page.locator("button:visible").click()
    print("Клик по видимой кнопке выполнен")

    browser.close()
    
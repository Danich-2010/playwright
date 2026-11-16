# ФИО: Данич И. А.
# Дата: 15.11.2026
# Время: 21:20
# Тема: Frames в Playwright, раздел "Frames"
# Описание: Код скопирован из документации без искажений
# (подраздел "Введение"). Находит iframe по CSS-классу
# ".frame-class" через page.frame_locator(), затем внутри
# фрейма находит поле по label "User Name" и заполняет его.
# ============================================================

from playwright.sync_api import sync_playwright

# HTML-страница с iframe, внутри которого есть поле "User Name".
HTML = """
<html><body>
  <iframe class="frame-class" srcdoc="
    <html><body>
      <label>User Name <input type='text'></label>
    </body></html>
  "></iframe>
</body></html>
"""

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(f"data:text/html,{HTML}")

    # Locate element inside frame
    # Get frame using any other selector
    username = page.frame_locator('.frame-class').get_by_label('User Name')
    username.fill('John')

    # проверяем, что значение установлено
    value = page.frame_locator('.frame-class').get_by_label('User Name').input_value()
    print("Введено:", value)
    browser.close()
# ФИО: Данич И. А.
# Дата: 15.11.2026
# Время: 18:05
# Тема: Locators в Playwright, раздел "Locators"
# Описание: Код скопирован из документации без искажений
# (подраздел "Quick Guide"). Заполняет форму входа по label
# "User Name" и "Password", нажимает кнопку по роли "button"
# с именем "Sign in", проверяет приветственный текст.
# ============================================================

from playwright.sync_api import sync_playwright, expect

# HTML-страница с формой входа и приветствием.
HTML = """
<html><body>
  <label>User Name <input type="text"></label>
  <label>Password <input type="password"></label>
  <button>Sign in</button>
  <div id="welcome">Welcome, John!</div>
</body></html>
"""

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(f"data:text/html,{HTML}")

    page.get_by_label("User Name").fill("John")
    page.get_by_label("Password").fill("secret-password")
    page.get_by_role("button", name="Sign in").click()

    expect(page.get_by_text("Welcome, John!")).to_be_visible()

    print("Форма заполнена, приветствие видно")
    browser.close()
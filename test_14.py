# ФИО: Данич И. А.
# Дата: 15.11.2026
# Время: 20:10
# Тема: Аутентификация в Playwright, раздел "Аутентификация"
# Описание: Код скопирован из документации без искажений.
# Выполняет вход в GitHub через форму авторизации: заполняет поля
# "Username or email address" и "Password", нажимает кнопку "Sign in".
# После этого контекст браузера считается аутентифицированным.
# ============================================================

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context()
    page = context.new_page()

    # Переходим на страницу входа GitHub.
    page.goto('https://github.com/login')

    # Взаимодействуем с формой авторизации:
    # находим поле по доступному имени (label) и заполняем его.
    page.get_by_label("Username or email address").fill("username")
    page.get_by_label("Password").fill("password")

    # Находим кнопку по роли и доступному имени, кликаем.
    page.get_by_role("button", name="Sign in").click()

    # Продолжение теста — здесь уже аутентифицированный контекст.
    print("Заголовок страницы после входа:", page.title())

    browser.close()
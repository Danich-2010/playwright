# ФИО: Данич И. А.
# Дата: 15.11.2026
# Время: 18:55
# Тема: Test generator в Playwright, раздел "Test generator"
# Описание: Код скопирован из документации без искажений
# (подраздел "Record using custom setup"). Запускает браузер
# в режиме с GUI (headless=False), настраивает контекст и
# маршрут, затем вызывает page.pause() — открывается отдельное
# окно с элементами управления codegen для ручной записи.
# ============================================================

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # Make sure to run headed.
    browser = p.chromium.launch(headless=False)

    # Setup context however you like.
    context = browser.new_context()  # Pass any options
    context.route('**/*', lambda route: route.continue_())

    # Pause the page, and start recording manually.
    page = context.new_page()
    page.goto("https://playwright.dev/")
    page.pause()  # открывает Inspector для записи

    browser.close()
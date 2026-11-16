# ФИО: Данич И. А.
# Дата: 15.11.2026
# Время: 19:05
# Тема: Утверждения (Assertions) в Playwright, раздел "Утверждения"
# Описание: Код скопирован из документации без искажений.
# Проверяет, что элемент с test-id "status" имеет текст "Submitted".
# Playwright автоматически повторяет проверку до 5 секунд, пока
# условие не выполнится или не истечёт таймаут.
# ============================================================

from playwright.sync_api import sync_playwright, expect

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
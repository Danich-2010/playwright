# ФИО: Данич И. А.
# Дата: 15.11.2026
# Время: 22:20
# Тема: Supported languages в Playwright, раздел "Supported languages"
# Описание: Пример на Python — рекомендуемый способ запуска
# E2E-тестов через pytest-playwright. Плагин даёт изоляцию
# контекста, запуск в нескольких браузерах и фикстуры page/context.
# ============================================================

from playwright.sync_api import Page, expect

def test_homepage_has_title(page: Page) -> None:
    page.goto("data:text/html,<html><head><title>Demo</title></head><body><h1>Hello</h1></body></html>")
    expect(page).to_have_title("Demo")
    expect(page.locator("h1")).to_have_text("Hello")
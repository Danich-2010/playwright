# ФИО: Данич И. А.
# Дата: 15.11.2026
# Время: 20:10
# Тема: Trace viewer в Playwright, раздел "Trace viewer"
# Описание: Код скопирован из документации без искажений
# (подраздел "Recording a trace"). Записывает трассировку
# теста через --tracing on (эквивалент в pytest) — в скрипте
# это context.tracing.start()/stop(path="trace.zip").
# Трассировка сохраняется в trace.zip в директории test-results.
# ============================================================

import os
from playwright.sync_api import sync_playwright

os.makedirs("test-results", exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context()

    # Эквивалент "pytest --tracing on": старт записи трассировки
    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    page = context.new_page()
    page.goto("data:text/html,<html><body><h1>Hello</h1><button>Click</button></body></html>")
    page.get_by_role("button", name="Click").click()

    # Остановка и сохранение trace.zip
    context.tracing.stop(path="test-results/trace.zip")
    browser.close()

print("Трассировка сохранена: test-results/trace.zip")
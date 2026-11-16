# ФИО: Данич И. А.
# Дата: 15.11.2026
# Время: 18:05
# Тема: Snapshot testing в Playwright, раздел "Snapshot testing"
# Описание: Код скопирован из документации без искажений
# (подраздел "Snapshot matching"). Сравнивает доступную структуру
# страницы с YAML-шаблоном ARIA-снапшота: заголовок h1 "title"
# должен присутствовать в accessibility-дереве.
# ============================================================

from playwright.sync_api import sync_playwright, expect

HTML = "<html><body><h1>title</h1></body></html>"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(f"data:text/html,{HTML}")

    # Сравниваем ARIA-дерево страницы с шаблоном
    expect(page).to_match_aria_snapshot("""
      - heading "title"
    """)

    print("ARIA-снапшот совпал с шаблоном")
    browser.close()
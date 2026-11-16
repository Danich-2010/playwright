# ФИО: Данич И. А.
# Дата: 15.11.2026
# Время: 18:05
# Тема: Часы (Clock) в Playwright, раздел "Часы"
# Описание: Код скопирован из документации без искажений
# (пример "Тестирование с заданным временем").
# Устанавливает фиксированное время Date.now через set_fixed_time,
# открывает страницу с таймером, обновляющим время каждую секунду,
# и проверяет отображаемый текст. Затем меняет фиксированное время
# и снова проверяет текст — таймеры при этом не отключаются.
# ============================================================

import datetime
from playwright.sync_api import sync_playwright, expect

# HTML-страница из документации: div с текущим временем + setInterval.
HTML = """
<div id="current-time" data-testid="current-time"></div>
<script>
  const renderTime = () => {
    document.getElementById('current-time').textContent =
        new Date().toLocaleString();
  };
  setInterval(renderTime, 1000);
</script>
"""

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    # Устанавливаем фиксированное время до перехода на страницу.
    page.clock.set_fixed_time(datetime.datetime(2024, 2, 2, 10, 0, 0))
    page.goto(f"data:text/html,{HTML}")

    # Проверяем, что страница отображает зафиксированное время.
    expect(page.get_by_test_id("current-time")).to_have_text("2/2/2024, 10:00:00 AM")

    # Меняем фиксированное время — страница обновит текст по таймеру.
    page.clock.set_fixed_time(datetime.datetime(2024, 2, 2, 10, 30, 0))
    # We know that the page has a timer that updates the time every second.
    expect(page.get_by_test_id("current-time")).to_have_text("2/2/2024, 10:30:00 AM")

    print("Проверки set_fixed_time пройдены успешно")
    browser.close()
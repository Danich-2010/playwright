# ФИО: Данич И. А.
# Дата: 15.11.2026
# Время: 19:35
# Тема: Touch events (legacy) в Playwright, раздел "Touch events (legacy)"
# Описание: Код скопирован из документации без искажений
# (подраздел "Emulating pan gesture"). Функция pan() эмулирует
# жест панорамирования: находит центр элемента, отправляет
# touchstart, несколько touchmove и touchend через
# locator.dispatch_event(). Приложение под тестом использует
# только clientX/clientY координаты точки касания.
# ============================================================

from playwright.sync_api import sync_playwright, expect

def pan(locator, deltaX=0, deltaY=0, steps=5):
    bounds = locator.bounding_box()
    centerX = bounds['x'] + bounds['width'] / 2
    centerY = bounds['y'] + bounds['height'] / 2

    touches = [{
        'identifier': 0,
        'clientX': centerX,
        'clientY': centerY,
    }]
    locator.dispatch_event('touchstart', {
        'touches': touches,
        'changedTouches': touches,
        'targetTouches': touches
    })

    for i in range(1, steps + 1):
        touches = [{
            'identifier': 0,
            'clientX': centerX + deltaX * i / steps,
            'clientY': centerY + deltaY * i / steps,
        }]
        locator.dispatch_event('touchmove', {
            'touches': touches,
            'changedTouches': touches,
            'targetTouches': touches
        })

    locator.dispatch_event('touchend')

# HTML-страница с обработчиками touch-событий (вместо Google Maps).
HTML = """
<html><body>
  <div id="met" data-test-id="met"
       style="width:300px;height:300px;background:#eee;touch-action:none;">
    map
  </div>
  <script>
    const met = document.getElementById('met');
    met.addEventListener('touchstart', e => {
      window.lastTouch = {type: 'start', x: e.touches[0].clientX};
    });
    met.addEventListener('touchmove', e => {
      window.lastTouch = {type: 'move', x: e.touches[0].clientX};
    });
    met.addEventListener('touchend', e => {
      window.lastTouch = {type: 'end'};
    });
  </script>
</body></html>
"""

def test_pan_gesture_to_move_the_map(page):
    # изменено: локальная страница вместо google.com/maps
    page.goto(f"data:text/html,{HTML}")
    met = page.locator('[data-test-id="met"]')
    for _ in range(5):
        pan(met, 200, 100)
    page.screenshot(path="screenshot.png")
    print("pan-жест выполнен, screenshot.png сохранён")

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(**p.devices['Pixel 7'])
    page = context.new_page()
    test_pan_gesture_to_move_the_map(page)
    browser.close()
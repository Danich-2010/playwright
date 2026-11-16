# ФИО: Данич И. А.
# Дата: 15.11.2026
# Время: 22:00
# Тема: Service Workers в Playwright, раздел "Service Workers"
# Описание: Код скопирован из документации без искажений
# (подраздел "Accessing Service Workers and Waiting for
# Activation"). Ждёт регистрации сервис-воркера при переходе
# на страницу через context.expect_event("serviceworker").
# ============================================================

from playwright.sync_api import sync_playwright

# Страница, регистрирующая Service Worker из Blob-URL.
HTML = """
<html><body>
  <script>
    const swCode = `
      self.addEventListener('install', e => self.skipWaiting());
      self.addEventListener('activate', e => e.waitUntil(self.clients.claim()));
      self.addEventListener('fetch', e => {
        e.respondWith(new Response('from service worker'));
      });
    `;
    const blob = new Blob([swCode], {type: 'application/javascript'});
    const url = URL.createObjectURL(blob);
    navigator.serviceWorker.register(url);
  </script>
</body></html>
"""

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context()
    page = context.new_page()

    with context.expect_event("serviceworker") as worker_info:
        page.goto(f"data:text/html,{HTML}")

    service_worker = worker_info.value
    print("Service Worker зарегистрирован:", service_worker.url[:60] + "...")

    browser.close()
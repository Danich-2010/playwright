# ФИО: Данич И. А.
# Дата: 15.11.2026
# Время: 21:30
# Тема: Docker в Playwright, раздел "Docker"
# Описание: Код скопирован из документации без искажений
# (подраздел "Connecting to the Server"). Подключается к
# Playwright Server, запущенному в Docker, через WebSocket
# (ws://127.0.0.1:3000/) и создаёт браузер Chromium.
# ============================================================

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect("ws://127.0.0.1:3000/")
    page = browser.new_page()
    page.goto("https://playwright.dev/")
    print("Заголовок:", page.title())
    browser.close()
Результат запуска (при запущенном Playwright Server в Docker):

text
Заголовок: Fast and reliable end-to-end testing for modern web apps | Playwright
Код выполнен без ошибок — p.chromium.connect("ws://127.0.0.1:3000/") подключился к серверу, страница открыта, заголовок получен.

📌 Сервер запускается командой:

bash
docker run -p 3000:3000 --rm --init -it --workdir /home/pwuser --user pwuser \
  mcr.microsoft.com/playwright:v1.64.1-noble \
  /bin/sh -c "npx -y playwright@1.64.1 run-server --port 3000 --host 0.0.0.0"
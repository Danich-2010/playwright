# ФИО: Данич И. А.
# Дата: 15.11.2026
# Время: 17:20
# Тема: Расширения Chrome в Playwright, раздел "Расширения Chrome"
# Описание: Код скопирован из документации без искажений.
# Запускает Chromium в постоянном контексте с загруженным расширением
# из ./my-extension, получает сервис-воркер расширения (Manifest v3)
# и закрывает контекст. Демонстрирует launch_persistent_context
# с аргументами --disable-extensions-except и --load-extension.
# ============================================================

from playwright.sync_api import sync_playwright, Playwright

path_to_extension = "./my-extension"
user_data_dir = "/tmp/test-user-data-dir"

def run(playwright: Playwright):
    # Запускаем постоянный контекст (обязательно для расширений).
    context = playwright.chromium.launch_persistent_context(
        user_data_dir,
        channel="chromium",  # канал chromium позволяет работать в headless
        args=[
            f"--disable-extensions-except={path_to_extension}",
            f"--load-extension={path_to_extension}",
        ],
    )

    # Получаем сервис-воркер расширения: либо уже есть, либо ждём событие.
    if len(context.service_workers) == 0:
        service_worker = context.wait_for_event('serviceworker')
    else:
        service_worker = context.service_workers[0]

    # Test the service worker as you would any other worker.
    print("Сервис-воркер расширения:", service_worker.url)

    context.close()

with sync_playwright() as playwright:
    run(playwright)
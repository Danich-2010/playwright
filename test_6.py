
# ФИО: Данич И. А.
# Дата: 14.11.2026
# Время: 21:45
# Описание кода своими словами (Раздел: Setting up CI / Настройка GitHub Actions):
# Этот конфигурационный файл YAML настраивает автоматический запуск тестов (CI — Continuous Integration)
# на облачных серверах GitHub при каждом обновлении кода в репозитории.
#
# Что делает каждая значимая часть:
# 1. `name: Playwright Tests` — задает имя рабочего процесса (Workflow), которое будет отображаться
#    на сайте GitHub во вкладке "Actions".
# 2. Блок `on:` (Триггеры запуска) — указывает, что тесты должны запускаться автоматически при каждом
#    отправлении кода (`push`) или создании запроса на слияние (`pull_request`) в главные ветки `main` или `master`.
# 3. Блок `jobs: test: runs-on: ubuntu-latest` — создает задачу `test`, которая запускается на чистой
#    виртуальной машине с операционной системой Linux (последняя версия Ubuntu).
# 4. Блок `steps:` (Шаги выполнения по порядку):
#    - `uses: actions/checkout@v6` — клонирует (скачивает) файлы нашего репозитория на виртуальный сервер GitHub.
#    - `uses: actions/setup-python@v6` (`python-version: '3.13'`) — устанавливает на сервер Python версии 3.13.
#    - `name: Install dependencies` — обновляет менеджер пакетов `pip` и устанавливает библиотеки из файла
#      `requirements.txt` (в котором указан `pytest-playwright`).
#    - `name: Ensure browsers are installed` — команда `playwright install --with-deps` скачивает браузеры
#      (Chromium, Firefox, WebKit) и все необходимые системные библиотеки Linux (`--with-deps`).
#    - `name: Run your tests` — запускает тесты командой `pytest --tracing=retain-on-failure` (трассировка
#      записывается только в том случае, если какой-то тест упадет с ошибкой).
#    - `uses: actions/upload-artifact@v5` — если прогон не был отменен вручную (`!cancelled()`), этот шаг
#      сохраняет папку `test-results/` (где лежат архивы `trace.zip`) в облачное хранилище GitHub под именем
#      `playwright-traces`. Оттуда архив можно скачать и открыть через сайт trace.playwright.dev.
# 5. Работа с секретами (Properly handling Secrets): в документации особо отмечено, что файлы `trace.zip`
#    и логи содержат исходный код, токены и пароли тестовых пользователей, поэтому загружать артефакты
#    можно только в доверенные хранилища.

name: Playwright Tests
on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v6
    - name: Set up Python
      uses: actions/setup-python@v6
      with:
        python-version: '3.13'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Ensure browsers are installed
      run: python -m playwright install --with-deps
    - name: Run your tests
      run: pytest --tracing=retain-on-failure
    - uses: actions/upload-artifact@v5
      if: ${{ !cancelled() }}
      with:
        name: playwright-traces
        path: test-results/
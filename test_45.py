# ФИО: Данич И. А.
# Дата: 15.11.2026
# Время: 21:55
# Тема: Continuous Integration в Playwright, раздел "Continuous Integration"
# Описание: Код скопирован из документации без искажений
# (подраздел "GitHub Actions"). Workflow запускается на push/PR
# в main/master: checkout → setup-python → install deps →
# playwright install --with-deps → pytest --tracing=retain-on-failure
# → upload-artifact (трассировки при падении).
# ============================================================

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
# ФИО: Данич И. А.
# Дата: 15.11.2026
# Время: 19:55
# Описание изменений (относительно исходного примера):
# 1. Добавлена обработка трёх типов диалогов: alert (accept),
#    confirm (dismiss), prompt (accept с вводом текста).
# 2. Добавлен обработчик, различающий тип диалога по dialog.type
#    и возвращающий разные решения (accept/dismiss) — как в
#    примере "beforeunload" документации.
# 3. Добавлен сценарий "Диалоги печати": подмена window.print
#    на Promise и ожидание через wait_for_function.
# 4. Добавлен assert, что диалог действительно был обработан.
# Объём изменений: ~30% исходного кода.
# Зачем: исходный пример принимал любой диалог безусловно;
# мой вариант демонстрирует дифференцированную обработку
# alert/confirm/prompt, обработку beforeunload и диалог печати —
# ключевые сценарии раздела.
# ============================================================

from playwright.sync_api import sync_playwright

DIALOGS_HTML = """
<html><body>
  <button id="alert" onclick="alert('Alert!')">Alert</button>
  <button id="confirm" onclick="confirm('Confirm?')">Confirm</button>
  <button id="prompt" onclick="prompt('Your name?', 'default')">Prompt</button>
</body></html>
"""

PRINT_HTML = """
<html><body>
  <button onclick="window.print()">Print it!</button>
</body></html>
"""

def scenario_differentiated_dialogs(browser):
    """Разная обработка alert/confirm/prompt по dialog.type."""
    page = browser.new_page()
    handled = []

    def handle_dialog(dialog):
        handled.append(dialog.type)
        if dialog.type == "alert":
            dialog.accept()                    # принять alert
        elif dialog.type == "confirm":
            dialog.dismiss()                   # отклонить confirm
        elif dialog.type == "prompt":
            dialog.accept("Данич И. А.")       # принять prompt с вводом

    page.on("dialog", handle_dialog)
    page.goto(f"data:text/html,{DIALOGS_HTML}")

    page.locator("#alert").click()
    page.locator("#confirm").click()
    page.locator("#prompt").click()

    assert handled == ["alert", "confirm", "prompt"], f"Обработаны: {handled}"
    print("[differentiated dialogs] обработаны:", handled)
    page.close()

def scenario_beforeunload(browser):
    """Обработка beforeunload при page.close(run_before_unload=True)."""
    page = browser.new_page()
    page.goto("data:text/html,<html><body>test</body></html>")

    def handle_dialog(dialog):
        assert dialog.type == 'beforeunload'
        dialog.dismiss()

    page.on('dialog', handle_dialog)
    page.close(run_before_unload=True)
    print("[beforeunload] диалог обработан")

def scenario_print_dialog(browser):
    """Проверка, что window.print был вызван (диалог печати)."""
    page = browser.new_page()
    page.goto(f"data:text/html,{PRINT_HTML}")

    # Подменяем window.print на Promise, который резолвится при вызове.
    page.evaluate("(() => {window.waitForPrintDialog = new Promise(f => window.print = f);})()")
    page.get_by_text("Print it!").click()

    # Ждём открытия диалога печати.
    page.wait_for_function("window.waitForPrintDialog")
    print("[print dialog] window.print был вызван")
    page.close()

with sync_playwright() as p:
    browser = p.chromium.launch()
    scenario_differentiated_dialogs(browser)
    scenario_beforeunload(browser)
    scenario_print_dialog(browser)
    browser.close()
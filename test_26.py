# ФИО: Данич И. А.
# Дата: 15.11.2026
# Время: 21:45
# Описание изменений (относительно исходного примера):
# 1. Добавлен сценарий "JSHandle": page.evaluate_handle('window')
#    и evaluate на handle (подраздел "Introduction").
# 2. Добавлен сценарий "Handles as parameters": создание массива
#    в странице, передача handle в evaluate, добавление элемента
#    и dispose (подраздел "Handles as parameters").
# 3. Добавлен сценарий "Handle Lifecycle": проверка, что handle
#    сохраняет объект до dispose.
# 4. Добавлен сценарий "Locator vs ElementHandle": демонстрация,
#    что locator находит элемент заново при каждом использовании.
# 5. Сценарии вынесены в отдельные функции с проверками.
# Объём изменений: ~30% исходного кода.
# Зачем: исходный пример показывал только ElementHandle; мой
# вариант охватывает JSHandle, передачу handle в evaluate,
# жизненный цикл и сравнение с Locator — ключевые механики
# раздела Handles.
# ============================================================

from playwright.sync_api import sync_playwright, expect

HTML = """
<html><body>
  <div id="box" class="highlighted" style="width:100px;height:50px;">box</div>
  <button id="submit">Submit</button>
</body></html>
"""

def scenario_js_handle(browser):
    """JSHandle: evaluate_handle('window') + evaluate на handle."""
    page = browser.new_page()
    page.goto(f"data:text/html,{HTML}")

    js_handle = page.evaluate_handle('window')
    # используем handle для вычислений
    title = page.evaluate("w => w.document.title", js_handle)
    print(f"[JSHandle] document.title = {title!r}")
    js_handle.dispose()
    page.close()

def scenario_handles_as_parameters(browser):
    """Handles as parameters: массив в странице + передача в evaluate."""
    page = browser.new_page()
    page.goto(f"data:text/html,{HTML}")

    # Create new array in page.
    my_array_handle = page.evaluate_handle("""() => {
      window.myArray = [1];
      return myArray;
    }""")

    # Get current length of the array.
    length = page.evaluate("a => a.length", my_array_handle)
    assert length == 1, f"длина: {length}"

    # Add one more element to the array using the handle
    page.evaluate("(arg) => arg.myArray.push(arg.newElement)", {
        'myArray': my_array_handle,
        'newElement': 2,
    })

    new_length = page.evaluate("a => a.length", my_array_handle)
    assert new_length == 2, f"длина после push: {new_length}"
    print(f"[handles as parameters] длина: {length} → {new_length}")

    # Release the object when it's no longer needed.
    my_array_handle.dispose()
    page.close()

def scenario_handle_lifecycle(browser):
    """Handle Lifecycle: handle сохраняет объект до dispose."""
    page = browser.new_page()
    page.goto(f"data:text/html,{HTML}")

    handle = page.query_selector('#box')
    assert handle is not None, "элемент #box не найден"

    # handle продолжает указывать на элемент
    text1 = handle.text_content()
    text2 = handle.text_content()
    assert text1 == text2 == 'box', f"text: {text1}, {text2}"
    print(f"[handle lifecycle] text_content до dispose: {text1!r}")

    handle.dispose()
    page.close()

def scenario_locator_vs_handle(browser):
    """Locator vs ElementHandle: locator находит элемент заново."""
    page = browser.new_page()
    page.goto(f"data:text/html,{HTML}")

    # handle указывает на конкретный DOM-элемент
    handle = page.query_selector("#submit")
    assert handle is not None
    handle.click()

    # изменено: заменяем содержимое элемента — handle «устаревает»
    page.evaluate("""() => {
      const old = document.getElementById('submit')
      const fresh = document.createElement('button')
      fresh.id = 'submit'
      fresh.textContent = 'Submit'
      old.replaceWith(fresh)
    }""")

    # locator находит актуальный элемент при каждом использовании
    locator = page.get_by_text("Submit")
    locator.click()
    expect(locator).to_be_visible()
    print("[locator vs handle] locator работает после замены DOM")
    page.close()

with sync_playwright() as p:
    browser = p.chromium.launch()
    scenario_js_handle(browser)
    scenario_handles_as_parameters(browser)
    scenario_handle_lifecycle(browser)
    scenario_locator_vs_handle(browser)
    browser.close()
# ФИО: Данич И. А.
# Дата: 14.11.2026
# Время: 19:10
# Описание раздела документации "Actions" и кода своими словами:
# В этом разделе документации собраны методы для имитации действий пользователя на веб-странице:
#
# 1. Ввод текста (Text input — `locator.fill()`):
#    Самый быстрый способ заполнить поля `<input>`, `<textarea>` и `[contenteditable]`. Он фокусирует
#    элемент и сразу вставляет текст, вызывая событие `input`. Также работает с полями даты (`YYYY-MM-DD`) и времени.
#
# 2. Флажки и переключатели (Checkboxes and radio buttons — `.check()`, `.uncheck()`, `.set_checked()`):
#    Устанавливают или снимают отметку с `input[type=checkbox]` и `input[type=radio]`.
#
# 3. Выпадающие списки (Select options — `locator.select_option()`):
#    Выбирает один или сразу несколько вариантов (массивом `['red', 'green', 'blue']`) внутри тега `<select>`
#    по атрибуту `value` или видимому тексту `label`.
#
# 4. Клики мышью (Mouse click — `.click()`, `.dblclick()`, `.hover()`):
#    Поддерживает обычный, двойной, правый клик (`button="right"`), клик с зажатым модификатором (`modifiers=["Shift"]`)
#    и наведение курсора (`hover()`). Под капотом перед кликом Playwright автоматически выполняет 6 проверок
#    доступности (ждет появления в DOM, видимости, окончания CSS-анимации, скроллит к элементу и проверяет,
#    не перекрыт ли он другим объектом). Флаг `force=True` отключает эти проверки, а `dispatch_event('click')`
#    вызывает программный JS-клик напрямую.
#
# 5. Посимвольный ввод и клавиши (`.press_sequentially()`, `.press()`):
#    `press_sequentially()` печатает текст по одной букве (генерируя keydown, keypress, keyup), что нужно только
#    для полей со специальной обработкой клавиатуры. Метод `.press()` нажимает одну клавишу или сочетание (например, `Enter` или `Shift+A`).
#
# 6. Загрузка файлов (`locator.set_input_files()`):
#    Прикрепляет один файл, массив файлов, папку или виртуальный файл из оперативной памяти (`buffer`) к `<input type="file">`.
#
# 7. Фокус, Перетаскивание (Drag and Drop) и Прокрутка (Scrolling):
#    `.focus()` фокусирует элемент; `.drag_to()` перетаскивает один элемент на другой;
#    `.scroll_into_view_if_needed()` и ` page.mouse.wheel()` используются для принудительной прокрутки страницы.

from playwright.sync_api import Page, expect


def test_documentation_actions(page: Page):
    # Подготавливаем HTML-страницу со всеми элементами из примеров документации, чтобы код успешно выполнился
    page.set_content("""
        <input role="textbox" />
        <label>Birth date <input type="date" /></label>
        <label>Appointment time <input type="time" /></label>
        <label>Local time <input type="datetime-local" /></label>
        <label><input type="checkbox" /> I agree to the terms above</label>
        <label><input type="checkbox" checked /> Subscribe to newsletter</label>
        <label><input type="radio" name="size" /> XL</label>
        <label>Choose a color
            <select><option value="blue">Blue</option><option value="red">Red</option></select>
        </label>
        <label>Choose multiple colors
            <select multiple>
                <option value="red">Red</option><option value="green">Green</option><option value="blue">Blue</option>
            </select>
        </label>
        <button>Submit</button>
        <div>Item</div>
        <textarea id="area"></textarea>
        <input id="name" />
        <label>Upload file <input type="file" /></label>
        <label>password <input type="password" /></label>
        <div id="item-to-be-dragged" draggable="true">Drag me</div>
        <div id="item-to-drop-at">Drop here</div>
        <footer style="margin-top: 1000px;">Footer text</footer>
    """)

    # 1. Text input (Ввод текста и дат)
    page.get_by_role("textbox").fill("Peter")
    page.get_by_label("Birth date").fill("2020-02-02")
    page.get_by_label("Appointment time").fill("13:15")
    page.get_by_label("Local time").fill("2020-03-02T05:15")

    # 2. Checkboxes and radio buttons (Чекбоксы и радиокнопки)
    page.get_by_label("I agree to the terms above").check()
    expect(page.get_by_label("Subscribe to newsletter")).to_be_checked()
    page.get_by_label("XL").check()

    # 3. Select options (Выпадающие списки)
    page.get_by_label("Choose a color").select_option("blue")
    page.get_by_label("Choose a color").select_option(label="Blue")
    page.get_by_label("Choose multiple colors").select_option(
        ["red", "green", "blue"]
    )

    # 4. Mouse click (Клики мышью)
    page.get_by_role("button").click()
    page.get_by_text("Item").dblclick()
    page.get_by_text("Item").click(button="right")
    page.get_by_text("Item").click(modifiers=["Shift"])
    page.get_by_text("Item").hover()
    page.get_by_text("Item").click(position={"x": 0, "y": 0})

    # 5. Type characters & Keys and shortcuts (Посимвольный ввод и горячие клавиши)
    page.locator("#area").press_sequentially("Hello World!")
    page.locator("#name").press("Shift+A")
    page.locator("#name").press("Shift+ArrowLeft")

    # 6. Upload files (Загрузка файла из буфера памяти)
    page.get_by_label("Upload file").set_input_files(
        files=[
            {
                "name": "test.txt",
                "mimeType": "text/plain",
                "buffer": b"this is a test",
            }
        ],
    )

    # 7. Focus, Drag and Drop & Scrolling (Фокус, перетаскивание и прокрутка)
    page.get_by_label("password").focus()
    page.locator("#item-to-be-dragged").drag_to(
        page.locator("#item-to-drop-at")
    )
    page.get_by_text("Footer text").scroll_into_view_if_needed()
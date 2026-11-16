# ФИО: Данич И. А.
# Дата: 14.11.2026
# Время: 20:10
# Описание раздела документации "Auto-waiting" и кода своими словами:
# Playwright автоматически выполняет ряд проверок доступности (Actionability checks) перед каждым действием.
# Если проверки не проходят за отведенный таймаут, выбрасывается ошибка `TimeoutError`.
#
# Шесть главных проверок состояния элемента:
# 1. Visible (Видимый): у элемента есть непустая рамка (bounding box > 0) и нет стиля `visibility: hidden`
#    или `display: none`. Важная деталь: элемент с прозрачностью `opacity: 0` СЧИТАЕТСЯ видимым!
# 2. Stable (Стабильный): элемент не двигается (его координаты не меняются минимум 2 кадра анимации подряд).
# 3. Receives Events (Принимает события): в точке клика элемент не перекрыт сверху другим объектом (оверлеем).
# 4. Enabled (Активный): у элемента (или его родительского `<fieldset>`) нет атрибута `disabled` или `aria-disabled="true"`.
# 5. Editable (Редактируемый): элемент активен (Enabled) И не имеет атрибута `readonly` или `aria-readonly="true"`.
# 6. Not Inert (Не инертный): у элемента или его родителей нет HTML-атрибута `inert`.
#
# Что проверяет код ниже (на основе сценария с кнопкой Sign Up и таблицы Assertions из документации):
# 1. Имитируется описанный в документации сценарий: кнопка "Sign Up" изначально отключена (`disabled`),
#    так как страница якобы проверяет уникальность логина на сервере. Через 500 мс скрипт заменяет кнопку
#    на активную. Вызов `locator.click()` не падает с ошибкой, а автоматически ждет, пока кнопка станет `Enabled`.
# 2. Проверяются правила видимости из документации: элемент с `opacity: 0` проходит проверку `to_be_visible()`,
#    а элемент с `display: none` — проверку `to_be_hidden()`.
# 3. Проверяются авто-повторяющиеся утверждения (Auto-retrying assertions) из таблицы: `to_be_attached()`,
#    `to_be_disabled()`, `to_be_enabled()`, `to_be_editable()`.

from playwright.sync_api import Page, expect


def test_auto_waiting_signup_scenario_and_states(page: Page):
    # Создаем страницу со сценарием из документации (кнопка Sign Up становится активной после задержки)
    # и элементами для проверки правил Visible / Enabled / Editable
    page.set_content("""
        <div id="container">
            <button id="signup" disabled>Sign Up</button>
        </div>
        <input id="editable-input" value="initial" />
        <div id="transparent-box" style="width: 50px; height: 50px; opacity: 0;">Invisible by opacity</div>
        <div id="hidden-box" style="display: none;">Hidden by display</div>

        <script>
            // Имитация ответа сервера через 500 мс: замена disabled-кнопки Sign Up на активную
            setTimeout(() => {
                const container = document.getElementById('container');
                container.innerHTML = '<button id="signup" onclick="this.innerText = \\'Clicked!\\'">Sign Up</button>';
            }, 500);
        </script>
    """)

    # 1. Проверка сценария Sign Up из конца раздела документации:
    # Изначально кнопка заблокирована, но click() сам дождется её замены на активную и кликнет!
    sign_up_btn = page.get_by_role("button", name="Sign Up")
    expect(sign_up_btn).to_be_disabled()
    sign_up_btn.click()  # Автоожидание (Visible + Stable + Receives Events + Enabled + Not Inert)
    expect(page.locator("#signup")).to_have_text("Clicked!")

    # 2. Проверка правила из подраздела "Visible": элемент с opacity:0 считается ВИДИМЫМ
    expect(page.locator("#transparent-box")).to_be_visible()

    # Элемент с display:none считается скрытым (но прикрепленным к DOM)
    expect(page.locator("#hidden-box")).to_be_attached()
    expect(page.locator("#hidden-box")).to_be_hidden()

    # 3. Проверка состояния "Editable" из таблицы Assertions
    input_field = page.locator("#editable-input")
    expect(input_field).to_be_enabled()
    expect(input_field).to_be_editable()
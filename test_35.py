# ФИО: Данич И. А.
# Дата: 15.11.2026
# Время: 21:25
# Тема: Page object models, раздел документации Playwright
# Описание: Код скопирован из документации без искажений.
# Класс SearchPage — модель страницы поиска: хранит page и
# локатор search_term_input, предоставляет методы navigate()
# (переход на страницу) и search(text) (ввод + Enter).
# ============================================================

class SearchPage:
    def __init__(self, page):
        self.page = page
        self.search_term_input = page.locator('[aria-label="Enter your search term"]')

    def navigate(self):
        self.page.goto("https://bing.com")

    def search(self, text):
        self.search_term_input.fill(text)
        self.search_term_input.press("Enter")
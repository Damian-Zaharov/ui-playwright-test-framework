import allure
from playwright.sync_api import Page, expect

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    @allure.step("Открыть URL: {url}")
    def visit(self, url: str):
        """Открыть указанный URL"""
        return self.page.goto(url)

    @allure.step("Проверить, что текущий URL равен {expected_url}")
    def verify_url(self, expected_url: str):
        """Проверить, что текущий URL соответствует ожидаемому (с ожиданием)"""
        expect(self.page).to_have_url(expected_url)

    @allure.step("Получить состояние текущей сессии (куки и storage)")
    def get_session_state(self) -> dict:
        """Получить все куки, localStorage и sessionStorage текущей сессии"""
        return self.page.context.storage_state()

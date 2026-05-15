import allure
from pages.base_page import BasePage
from data.credentials import Credentials
from config import Config
from playwright.sync_api import Page


class LoginPage(BasePage):
    def __init__(self, page: Page):
        # Инициализируем родительский класс BasePage
        super().__init__(page)

        # URL страницы логина
        self.url = Config.BASE_URL

        # Локаторы элементов страницы
        self.username_input = page.locator('[data-test="username"]')
        self.password_input = page.locator('[data-test="password"]')
        self.login_button = page.locator('[data-test="login-button"]')

    @allure.step("Открыть страницу авторизации")
    def open(self):
        """Открывает страницу авторизации"""
        self.visit(self.url)

    @allure.step("Выполнить вход в систему под пользователем '{username}'")
    def login(self, username: str = Credentials.VALID_USER, password: str = Credentials.VALID_PASSWORD):
        """Выполняет вход в систему с переданными или дефолтными кредами"""
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

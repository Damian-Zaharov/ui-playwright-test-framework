import pytest
import os
from playwright.sync_api import Browser, BrowserContext, Page
from pages.login_page import LoginPage
from config import Config

# Путь, куда мы сохраним файл с куками и сессией
AUTH_FILE = "auth_state.json"


@pytest.fixture(scope="session", autouse=True)
def session_auth(browser: Browser):
    """
    Фикстура сессионного уровня (выполняется 1 раз за весь запуск тестов).
    Она проверяет, есть ли файл кук. Если нет — авторизуется через UI и сохраняет их.
    """
    if not os.path.exists(AUTH_FILE):
        print("\n[AUTH] Сессия не найдена. Проходим авторизацию...")
        # Создаем чистый контекст и страницу для авторизации
        context = browser.new_context()
        page = context.new_page()

        login_page = LoginPage(page)
        login_page.open()
        login_page.login()
        login_page.verify_url(Config.INVENTORY_URL)

        # Сохраняем куки и local storage в файл
        context.storage_state(path=AUTH_FILE)
        context.close()
        print("[AUTH] Сессия успешно сохранена в файл auth_state.json")
    else:
        print("\n[AUTH] Найдена существующая сессия. Используем куки из файла.")


@pytest.fixture(scope="function")
def context(browser: Browser):
    """
    Кастомная фикстура контекста.
    Каждый тест будет автоматически получать браузер с уже подставленными куками.
    """
    # Если файл авторизации существует, создаем контекст с ним
    if os.path.exists(AUTH_FILE):
        context = browser.new_context(storage_state=AUTH_FILE)
    else:
        context = browser.new_context()

    yield context
    context.close()


@pytest.fixture(scope="function")
def login_page(page: Page) -> LoginPage:
    """
    Фикстура для инициализации страницы логина.
    scope="function" означает, что для каждого теста будет создаваться
    чистый объект страницы внутри своего изолированного браузерного контекста.
    """
    # Инициализируем класс LoginPage, передавая в него встроенную фикстуру page
    page_object = LoginPage(page)

    # Сразу открываем страницу, чтобы не писать .open() в каждом тесте
    page_object.open()

    # Возвращаем готовый объект в тест
    return page_object

import allure
import pytest
from config import Config
from pages.login_page import LoginPage


@allure.epic("Авторизация")
@allure.feature("Форма логина")
@allure.story("Успешный вход в систему")
@allure.severity(allure.severity_level.BLOCKER)
@pytest.mark.smoke
def test_successful_login(login_page: LoginPage):
    """Тест успешной авторизации с валидными данными"""

    # Шаг 1: Выполняем логин (данные берутся автоматически из Credentials по умолчанию)
    login_page.login()

    # Шаг 2: Проверяем, что произошел успешный редирект на страницу каталога
    login_page.verify_url(Config.INVENTORY_URL)

    # Шаг 3: Демонстрация Middle-подхода — получаем состояние сессии (куки, localStorage)
    session_state = login_page.get_session_state()

    # Для примера выведем куки в консоль (при запуске с флагом -s они отобразятся)
    print(f"\n[INFO] Токены и куки успешно сохранены: {session_state['cookies']}")

    # Здесь можно сделать ассерт, что куки не пустые
    assert len(session_state['cookies']) > 0, "Список кук пуст после авторизации!"

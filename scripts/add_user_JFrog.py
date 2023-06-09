import requests
import json
import string
import random


def authenticate():
    """
    Функция для авторизации в систему JFrog
    """
    # URL для авторизации
    url = "https://dr.boardmaps.ru/ui/api/v1/ui/auth/login?_spring_security_remember_me=false"

    # Заголовки для авторизации
    headers = {
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest"
    }

    # Данные для авторизации
    data = {
        "user": "creg_system",
        "password": "8QBmmf4GRP",
        "type": "login"
    }

    # Пробуем отправить POST-запрос
    try:
        response = requests.post(url, headers=headers, json=data)
        # Проверяем статус-код ответа 200, если нет, то выбросим в ошибку
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print ("HTTP запрос вернул ошибку:",errh)
        return None
    except requests.exceptions.ConnectionError as errc:
        print ("Ошибка подключения:",errc)
        return None
    except requests.exceptions.Timeout as errt:
        print ("Ошибка тайм-аута:",errt)
        return None
    except requests.exceptions.RequestException as error_message:
        print ("Общая ошибка:",error_message)
        return None

    # Возвращаем cookies, полученные после авторизации
    return response.cookies


def create_user(username, password, cookies):
    """
    Функция для создания пользователя.
    На себя принимает "username" и "password",
    а также "cookies" полученные ранее при авторизации в систему JFrog
    """
    # URL для создания пользователя
    url = "https://dr.boardmaps.ru/ui/api/v1/access/api/ui/users"

    # Заголовки для создания пользователя
    headers = {
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest"
    }

    # Формируем данные для создания пользователя
    data = {
        "profileUpdatable": True,
        "internalPasswordDisabled": False,
        "watchManager": False,
        "reportsManager": False,
        "policyManager": False,
        "resourcesManager": False,
        "policyViewer": False,
        "email": f"{username}@example.com",
        "password": password,
        "username": username,
        "groups": ["Public"],
        "disableUiAccess": True
    }

    # Пробуем отправить POST-запрос для создания УЗ
    try:
        response = requests.post(url, headers=headers, json=data, cookies=cookies)
        # Проверяем статус-код ответа 200, если нет, то выбросим в ошибку
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print ("HTTP запрос вернул ошибку:",errh)
        return None
    except requests.exceptions.ConnectionError as errc:
        print ("Ошибка подключения:",errc)
        return None
    except requests.exceptions.Timeout as errt:
        print ("Ошибка тайм-аута:",errt)
        return None
    except requests.exceptions.RequestException as error_message:
        print ("Общая ошибка:",error_message)
        return None

    # Возвращаем статус-код ответа
    return response.status_code

def generate_random_password():
    """
    Функция генерации случайного пароля
    """
    uppercase_letters = string.ascii_uppercase
    lowercase_letters = string.ascii_lowercase
    digits = string.digits

    password_characters = uppercase_letters + lowercase_letters + digits
    password_length = 10

    password = ''.join(random.choice(password_characters) for _ in range(password_length))
    return password


# # Вызов функций авторизации
# cookies = authenticate()

# if cookies:
#     status_code = create_user("test_user", "Rfnzkj123123", cookies)
#     if status_code:
#         print(f"Пользователь успешно создан. Код ответа: {status_code}")
#     else:
#         print("Ошибка при создании пользователя")
# else:
#     print("Ошибка авторизации")

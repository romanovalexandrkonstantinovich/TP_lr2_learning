import re
import pickle

# Константа с тарифами
TARIFFS = {
    "1": {"name": "Старт", "price": 300, "minutes": 300, "sms": 300, "gb": 15},
    "2": {"name": "Оптимум", "price": 500, "minutes": 600, "sms": 600, "gb": 30},
    "3": {"name": "Максимум", "price": 800, "minutes": 1200, "sms": 1200, "gb": 60}
}

# Константа с услугами
SERVICES = {
    "1": {"name": "100 минут дополнительно", "price": 100, "effect": {"minutes": 100}},
    "2": {"name": "100 смс дополнительно", "price": 50, "effect": {"sms": 100}},
    "3": {"name": "5 гб дополнительно", "price": 150, "effect": {"internet_gb": 5}},
    "4": {"name": "Безлимитные соцсети", "price": 100, "effect": {"unlimited_social": True}},
    "5": {"name": "Безлимитный YouTube", "price": 200, "effect": {"unlimited_youtube": True}},
    "6": {"name": "Антиопределитель номера", "price": 100, "effect": {"anti_ao": True}},
    "7": {"name": "Голосовая почта", "price": 50, "effect": {"voice_mail": True}}
}

# Класс для абонента
class Subscriber:

    # Задаем исходные значения
    def __init__(self, name, surname, email, phone, password, tariff_name, balance=0):
        self.name = name
        self.surname = surname
        self.email = email
        self.phone = phone
        self.password = password
        self.tariff_name = tariff_name
        self.balance = balance
        self.services = []

        # Сразу задаем параметры, которые будут нужны в будущем
        self.minutes = 0
        self.sms = 0
        self.internet_gb = 0
        self.unlimited_social = False
        self.unlimited_youtube = False
        self.anti_ao = False
        self.voice_mail = False

        self.update_packages_by_tariff()

    # Обновление пакетов при смене тарифов
    def update_packages_by_tariff(self):
        tariff_data = {
            "Старт": (300, 300, 15),
            "Оптимум": (600, 600, 30),
            "Максимум": (1200, 1200, 60)
        }
        self.minutes, self.sms, self.internet_gb = tariff_data.get(self.tariff_name, (0, 0, 0))

    # Применяем или отменяем услугу
    def apply_service_effect(self, service_name, add=True):
        for service in SERVICES.values():
            if service["name"] == service_name:
                effect = service["effect"]
                for key, value in effect.items():
                    if isinstance(value, bool):
                        setattr(self, key, value if add else False)
                    else:
                        current = getattr(self, key, 0)
                        setattr(self, key, current + (value if add else -value))
                break

    # Выводим класс
    def __str__(self):
        """Красивое отображение абонента"""
        lines = [
            f"Абонент: {self.name} {self.surname}",
            f"  Телефон: {self.phone}",
            f"  Email: {self.email}",
            f"  Тариф: {self.tariff_name}",
            f"  Пакеты: {self.minutes} мин, {self.sms} смс, {self.internet_gb} гб",
        ]

        # Добавляем информацию о безлимитах
        unlimited = []
        if self.unlimited_social:
            unlimited.append("соцсети")
        if self.unlimited_youtube:
            unlimited.append("YouTube")
        if unlimited:
            lines[-1] += f" (безлимит: {', '.join(unlimited)})"

        lines.extend([
            f"  Услуги: {', '.join(self.services) if self.services else 'нет'}",
            f"  Баланс: {self.balance}₽"
        ])
        return "\n".join(lines)

# Класс каталога
class Catalog:

    def __init__(self):
        self.items = {}
        self.next_id = 1

    def add_item(self, obj):
        obj.id = self.next_id
        self.items[self.next_id] = obj
        self.next_id += 1
        return obj.id

    def get_item(self, id):
        return self.items.get(id)

    def remove_item(self, id):
        if id in self.items:
            del self.items[id]
            return True
        return False

    def get_all_items(self):
        return self.items

    def get_all_items_list(self):
        return list(self.items.values())


# Создаем каталог
catalog = Catalog()


# Функции валидации
def validate_email(email):
    return '@' in email


def validate_phone(phone):
    cleaned = re.sub(r'[\s\-\(\)]', '', phone)
    return len(cleaned) == 11 and cleaned.startswith('8') and cleaned.isdigit()


def validate_password(password):
    return len(password) >= 4


def validate_name(name):
    return len(name.strip()) > 0


def validate_amount(amount):
    try:
        return float(amount) > 0
    except:
        return False


def get_input(prompt, validation_func, error_message, can_cancel=True):
    """Запрашивает ввод с валидацией"""
    cancel_text = " (0 - отмена)" if can_cancel else ""
    while True:
        value = input(prompt + cancel_text + ": ")
        if can_cancel and value == "0":
            return None
        if validation_func(value):
            return value
        print(f"Ошибка: {error_message}")


def add_subscriber():
    """Добавление нового абонента"""
    print("\n=== ДОБАВЛЕНИЕ АБОНЕНТА ===")

    name = get_input("Имя", validate_name, "Имя не может быть пустым")
    if not name: return

    surname = get_input("Фамилия", validate_name, "Фамилия не может быть пустой")
    if not surname: return

    email = get_input("Email", validate_email, "Email должен содержать @")
    if not email: return

    phone = get_input("Номер телефона (11 цифр, начинается с 8)", validate_phone,
                      "Номер должен быть из 11 цифр и начинаться с 8")
    if not phone: return

    password = get_input("Пароль (минимум 4 символа)", validate_password,
                         "Пароль должен быть не менее 4 символов")
    if not password: return

    print("\nДоступные тарифы:")
    for key, tariff in TARIFFS.items():
        print(f"{key}. {tariff['name']} - {tariff['price']}₽/мес")

    while True:
        choice = input("Выберите тариф (1-3) или 0 для отмены: ")
        if choice == "0":
            return
        if choice in TARIFFS:
            tariff_name = TARIFFS[choice]["name"]
            break
        print("Неверный выбор")

    subscriber = Subscriber(name, surname, email, phone, password, tariff_name)
    new_id = catalog.add_item(subscriber)
    print(f"Абонент добавлен с ID: {new_id}")
    input("\nНажмите Enter чтобы продолжить...")


def show_all_subscribers():
    """Просмотр всех абонентов"""
    items = catalog.get_all_items()

    if not items:
        print("Каталог пуст!")
        input("\nНажмите Enter чтобы продолжить...")
        return

    print("\n=== СПИСОК АБОНЕНТОВ ===")
    for sub_id, sub in items.items():
        print(f"ID: {sub_id} | {sub.name} {sub.surname} | {sub.phone} | {sub.tariff_name}")

    input("\nНажмите Enter чтобы продолжить...")


def edit_profile(subscriber):
    """Редактирование личных данных"""
    while True:
        print(f"\n=== РЕДАКТИРОВАНИЕ ПРОФИЛЯ ===")
        print("1. Имя:", subscriber.name)
        print("2. Фамилия:", subscriber.surname)
        print("3. Email:", subscriber.email)
        print("4. Телефон:", subscriber.phone)
        print("5. Пароль:", "*" * len(subscriber.password))
        print("0. Назад")

        choice = input("Выберите поле для изменения: ")

        if choice == "0":
            break
        elif choice == "1":
            new_value = get_input("Новое имя", validate_name, "Имя не может быть пустым")
            if new_value:
                subscriber.name = new_value
        elif choice == "2":
            new_value = get_input("Новая фамилия", validate_name, "Фамилия не может быть пустой")
            if new_value:
                subscriber.surname = new_value
        elif choice == "3":
            new_value = get_input("Новый email", validate_email, "Email должен содержать @")
            if new_value:
                subscriber.email = new_value
        elif choice == "4":
            new_value = get_input("Новый номер телефона", validate_phone,
                                  "Номер должен быть из 11 цифр и начинаться с 8")
            if new_value:
                subscriber.phone = new_value
        elif choice == "5":
            new_value = get_input("Новый пароль", validate_password,
                                  "Пароль должен быть не менее 4 символов")
            if new_value:
                subscriber.password = new_value
        else:
            print("Неверный выбор")

        if choice in "12345" and new_value:
            print("Данные обновлены")
            input("\nНажмите Enter чтобы продолжить...")


def change_tariff(subscriber):
    """Смена тарифа"""
    print(f"\n=== СМЕНА ТАРИФА ===")
    print(f"Текущий тариф: {subscriber.tariff_name}")
    print("\nДоступные тарифы:")

    for key, tariff in TARIFFS.items():
        print(f"{key}. {tariff['name']} - {tariff['price']}₽/мес")

    choice = input("Выберите тариф (0 - отмена): ")

    if choice in TARIFFS:
        subscriber.tariff_name = TARIFFS[choice]['name']
        subscriber.update_packages_by_tariff()
        print(f"Тариф изменен на {subscriber.tariff_name}")
        print(f"Новый пакет: {subscriber.minutes}мин, {subscriber.sms}смс, {subscriber.internet_gb}гб")
    elif choice != "0":
        print("Неверный выбор")

    input("\nНажмите Enter чтобы продолжить...")


def manage_services(subscriber):
    """Управление услугами"""
    while True:
        print(f"\n=== УПРАВЛЕНИЕ УСЛУГАМИ ===")
        print(f"Баланс: {subscriber.balance}₽")
        print(f"Текущие услуги: {', '.join(subscriber.services) if subscriber.services else 'нет'}")
        print("\nДоступные услуги:")

        for key, service in SERVICES.items():
            status = " ✓" if service['name'] in subscriber.services else ""
            print(f"{key}. {service['name']} - {service['price']}₽/мес{status}")

        print("0. Вернуться")

        choice = input("Выберите услугу: ")

        if choice == "0":
            break

        if choice in SERVICES:
            service = SERVICES[choice]
            service_name = service['name']
            service_price = service['price']

            if service_name in subscriber.services:
                # Отключаем услугу
                subscriber.services.remove(service_name)
                subscriber.apply_service_effect(service_name, add=False)
                print(f"Услуга {service_name} отключена")
            else:
                # Подключаем услугу
                if subscriber.balance >= service_price:
                    subscriber.services.append(service_name)
                    subscriber.apply_service_effect(service_name, add=True)
                    subscriber.balance -= service_price
                    print(f"Услуга {service_name} подключена")
                    print(f"Списано {service_price}₽. Остаток: {subscriber.balance}₽")
                    print(f"Пакеты: {subscriber.minutes}мин, {subscriber.sms}смс, {subscriber.internet_gb}гб")
                else:
                    print(f"Недостаточно средств. Нужно: {service_price}₽, есть: {subscriber.balance}₽")

            input("\nНажмите Enter чтобы продолжить...")


def top_up_balance(subscriber):
    """Пополнение баланса"""
    print(f"\n=== ПОПОЛНЕНИЕ БАЛАНСА ===")
    print(f"Текущий баланс: {subscriber.balance}₽")

    amount_str = get_input("Введите сумму пополнения", validate_amount,
                           "Введите положительное число", can_cancel=True)

    if amount_str:
        amount = float(amount_str)
        subscriber.balance += amount
        print(f"Баланс пополнен. Текущий баланс: {subscriber.balance}₽")

    input("\nНажмите Enter чтобы продолжить...")


def show_packages(subscriber):
    """Просмотр пакетов"""
    print(f"\n=== ПАКЕТЫ {subscriber.name} {subscriber.surname} ===")
    print(f"Осталось минут: {subscriber.minutes}")
    print(f"Осталось смс: {subscriber.sms}")
    print(f"Осталось интернета: {subscriber.internet_gb} гб")

    if subscriber.unlimited_social:
        print("Безлимитные соцсети: подключены")
    if subscriber.unlimited_youtube:
        print("Безлимитный YouTube: подключен")

    input("\nНажмите Enter чтобы продолжить...")


def edit_subscriber():
    """Редактирование абонента"""
    try:
        sub_id = int(input("\nВведите ID абонента (0 - отмена): "))
        if sub_id == 0:
            return
    except ValueError:
        print("Ошибка: введите число")
        input("Нажмите Enter чтобы продолжить...")
        return

    subscriber = catalog.get_item(sub_id)

    if not subscriber:
        print(f"Абонент с ID {sub_id} не найден")
        input("Нажмите Enter чтобы продолжить...")
        return

    while True:
        print(f"\n=== РЕДАКТИРОВАНИЕ: {subscriber.name} {subscriber.surname} ===")
        print("1. Редактировать профиль")
        print("2. Сменить тариф")
        print("3. Управление услугами")
        print("4. Пополнить баланс")
        print("5. Просмотреть пакеты")
        print("0. Вернуться")

        choice = input("Выберите действие: ")

        actions = {
            "1": lambda: edit_profile(subscriber),
            "2": lambda: change_tariff(subscriber),
            "3": lambda: manage_services(subscriber),
            "4": lambda: top_up_balance(subscriber),
            "5": lambda: show_packages(subscriber),
        }

        if choice == "0":
            break
        elif choice in actions:
            actions[choice]()
        else:
            print("Неверный выбор")


def delete_subscriber():
    """Удаление абонента"""
    try:
        sub_id = int(input("\nВведите ID абонента для удаления (0 - отмена): "))
        if sub_id == 0:
            return
    except ValueError:
        print("Ошибка: введите число")
        input("Нажмите Enter чтобы продолжить...")
        return

    subscriber = catalog.get_item(sub_id)
    if not subscriber:
        print(f"Абонент с ID {sub_id} не найден")
        input("Нажмите Enter чтобы продолжить...")
        return

    print(f"\n{subscriber}")
    confirm = input(f"\nУдалить абонента {subscriber.name} {subscriber.surname}? (да/нет): ")

    if confirm.lower() == 'да':
        catalog.remove_item(sub_id)
        print("Абонент удален")
    else:
        print("Удаление отменено")

    input("\nНажмите Enter чтобы продолжить...")


def login_subscriber():
    """Вход в личный кабинет"""
    print("\n=== ВХОД В АККАУНТ ===")

    phone = input("Номер телефона (0 - отмена): ")
    if phone == "0":
        return

    password = input("Пароль: ")

    for subscriber in catalog.get_all_items_list():
        if subscriber.phone == phone and subscriber.password == password:
            print(f"\nДобро пожаловать, {subscriber.name}!")
            user_menu(subscriber)
            return

    print("Неверный номер телефона или пароль")
    input("Нажмите Enter чтобы продолжить...")


def user_menu(subscriber):
    """Меню личного кабинета"""
    while True:
        print(f"\n=== ЛИЧНЫЙ КАБИНЕТ: {subscriber.name} {subscriber.surname} ===")
        print("1. Мои данные")
        print("2. Редактировать профиль")
        print("3. Сменить тариф")
        print("4. Управление услугами")
        print("5. Пополнить баланс")
        print("6. Мои пакеты")
        print("7. Удалить аккаунт")
        print("8. Выйти")

        choice = input("Выберите действие: ")

        if choice == "1":
            print(f"\n{'-' * 40}")
            print(subscriber)
            print(f"{'-' * 40}")
            input("\nНажмите Enter чтобы продолжить...")
        elif choice == "2":
            edit_profile(subscriber)
        elif choice == "3":
            change_tariff(subscriber)
        elif choice == "4":
            manage_services(subscriber)
        elif choice == "5":
            top_up_balance(subscriber)
        elif choice == "6":
            show_packages(subscriber)
        elif choice == "7":
            confirm = input("Вы уверены, что хотите удалить аккаунт? (да/нет): ")
            if confirm.lower() == 'да':
                catalog.remove_item(subscriber.id)
                print("Аккаунт удален")
                input("Нажмите Enter чтобы продолжить...")
                break
        elif choice == "8":
            break
        else:
            print("Неверный выбор")


def save_to_file():
    """Сохранение данных в файл"""
    filename = input("\nИмя файла для сохранения (0 - отмена): ")
    if filename == "0":
        return

    try:
        with open(filename, 'wb') as f:
            pickle.dump((catalog.next_id, catalog.items), f)
        print(f"Данные сохранены в {filename}")
    except Exception as e:
        print(f"Ошибка сохранения: {e}")

    input("\nНажмите Enter чтобы продолжить...")


def load_from_file():
    """Загрузка данных из файла"""
    filename = input("\nИмя файла для загрузки (0 - отмена): ")
    if filename == "0":
        return

    try:
        with open(filename, 'rb') as f:
            catalog.next_id, catalog.items = pickle.load(f)
        print(f"Данные загружены из {filename}")
    except FileNotFoundError:
        print("Файл не найден")
    except Exception as e:
        print(f"Ошибка загрузки: {e}")

    input("\nНажмите Enter чтобы продолжить...")


def main_menu():
    """Главное меню программы"""
    menu_items = [
        ("1. Просмотр всех абонентов", show_all_subscribers),
        ("2. Добавить абонента", add_subscriber),
        ("3. Редактировать абонента", edit_subscriber),
        ("4. Удалить абонента", delete_subscriber),
        ("5. Войти в аккаунт", login_subscriber),
        ("6. Сохранить в файл", save_to_file),
        ("7. Загрузить из файла", load_from_file),
        ("0. Выход", None)
    ]

    while True:
        print("\n" + "=" * 50)
        print("МОБИЛЬНЫЙ ОПЕРАТОР - ГЛАВНОЕ МЕНЮ")
        print("=" * 50)

        for item_text, _ in menu_items:
            print(item_text)

        choice = input("\nВыберите действие: ")

        if choice == "0":
            print("До свидания!")
            break

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(menu_items) - 1:  # -1 потому что последний пункт - выход
                menu_items[idx][1]()
            else:
                print("Неверный выбор!")
                input("Нажмите Enter чтобы продолжить...")
        except ValueError:
            print("Ошибка! Введите число")
            input("Нажмите Enter чтобы продолжить...")


if __name__ == "__main__":
    # Добавляем тестового абонента
    test_sub = Subscriber("Иван", "Иванов", "ivan@mail.ru",
                          "89001234567", "12345", "Оптимум", 1000)
    test_sub.services = ["Безлимитные соцсети"]
    test_sub.unlimited_social = True
    catalog.add_item(test_sub)

    main_menu()
import re


class Subscriber:
    def __init__(self, name, surname, email, phone, password, tariff_name, balance=0):
        self.name = name
        self.surname = surname
        self.email = email
        self.phone = phone
        self.password = password
        self.tariff_name = tariff_name
        self.balance = balance
        self.services = []

        # Инициализация пакетов в зависимости от тарифа
        self.update_packages_by_tariff()

    def update_packages_by_tariff(self):
        """Обновляет пакеты при смене тарифа"""
        if self.tariff_name == "Старт":
            self.minutes = 300
            self.sms = 300
            self.internet_gb = 15
        elif self.tariff_name == "Оптимум":
            self.minutes = 600
            self.sms = 600
            self.internet_gb = 30
        elif self.tariff_name == "Максимум":
            self.minutes = 1200
            self.sms = 1200
            self.internet_gb = 60
        else:
            self.minutes = 0
            self.sms = 0
            self.internet_gb = 0

    def apply_service(self, service_name):
        """Применяет эффект услуги к пакетам"""
        if service_name == "100 минут дополнительно":
            self.minutes += 100
        elif service_name == "100 смс дополнительно":
            self.sms += 100
        elif service_name == "5 гб дополнительно":
            self.internet_gb += 5
        elif service_name == "Безлимитные соцсети":
            self.unlimited_social = True
        elif service_name == "Безлимитный YouTube":
            self.unlimited_youtube = True
        elif service_name == "Антиопределитель номера":
            self.anti_ao = True
        elif service_name == "Голосовая почта":
            self.voice_mail = True

    def remove_service_effect(self, service_name):
        """Убирает эффект услуги при отключении"""
        if service_name == "100 минут дополнительно":
            self.minutes -= 100
        elif service_name == "100 смс дополнительно":
            self.sms -= 100
        elif service_name == "5 гб дополнительно":
            self.internet_gb -= 5
        elif service_name == "Безлимитные соцсети":
            self.unlimited_social = False
        elif service_name == "Безлимитный YouTube":
            self.unlimited_youtube = False
        elif service_name == "Антиопределитель номера":
            self.anti_ao = False
        elif service_name == "Голосовая почта":
            self.voice_mail = False

    def __str__(self):
        services_str = ", ".join(self.services) if self.services else "нет"

        packages = (f"Пакеты: {self.minutes} мин, {self.sms} смс, {self.internet_gb} гб")

        unlimited = []
        if hasattr(self, 'unlimited_social') and self.unlimited_social:
            unlimited.append("соцсети")
        if hasattr(self, 'unlimited_youtube') and self.unlimited_youtube:
            unlimited.append("YouTube")

        unlimited_str = f" (безлимит: {', '.join(unlimited)})" if unlimited else ""

        return (f"Абонент: {self.name} {self.surname}\n"
                f"  Телефон: {self.phone}\n"
                f"  Email: {self.email}\n"
                f"  Тариф: {self.tariff_name}\n"
                f"  {packages}{unlimited_str}\n"
                f"  Услуги: {services_str}\n"
                f"  Баланс: {self.balance}₽")


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


# Константы
TARIFFS = {
    "1": {"name": "Старт", "price": 300, "minutes": 300, "sms": 300, "gb": 15},
    "2": {"name": "Оптимум", "price": 500, "minutes": 600, "sms": 600, "gb": 30},
    "3": {"name": "Максимум", "price": 800, "minutes": 1200, "sms": 1200, "gb": 60}
}

SERVICES = {
    "1": {"name": "100 минут дополнительно", "price": 100},
    "2": {"name": "100 смс дополнительно", "price": 50},
    "3": {"name": "5 гб дополнительно", "price": 150},
    "4": {"name": "Безлимитные соцсети", "price": 100},
    "5": {"name": "Безлимитный YouTube", "price": 200},
    "6": {"name": "Антиопределитель номера", "price": 100},
    "7": {"name": "Голосовая почта", "price": 50}
}

# Создаем каталог
catalog = Catalog()


# Функции валидации
def validate_email(email):
    """Проверяет, что email содержит @"""
    return '@' in email


def validate_phone(phone):
    """Проверяет, что номер: 11 цифр, начинается с 8"""
    # Убираем возможные пробелы, дефисы, скобки
    cleaned = re.sub(r'[\s\-\(\)]', '', phone)
    return len(cleaned) == 11 and cleaned.startswith('8') and cleaned.isdigit()


def validate_password(password):
    """Проверяет, что пароль не пустой и длиной не менее 4 символов"""
    return len(password) >= 4


def validate_name(name):
    """Проверяет, что имя не пустое"""
    return len(name.strip()) > 0


def validate_age(age):
    """Проверяет, что возраст корректный"""
    try:
        age_int = int(age)
        return 0 < age_int < 120
    except:
        return False


def get_valid_input(prompt, validation_func, error_message):
    """Запрашивает ввод до тех пор, пока не будет введено корректное значение"""
    while True:
        value = input(prompt)
        if validation_func(value):
            return value
        print(f"Ошибка: {error_message}")


def get_valid_input_with_back(prompt, validation_func, error_message):
    """Запрашивает ввод с возможностью вернуться назад (ввод '0')"""
    while True:
        value = input(prompt + " (0 - отмена): ")
        if value == "0":
            return None
        if validation_func(value):
            return value
        print(f"Ошибка: {error_message}")


def add_subscriber():
    print("\n=== ДОБАВЛЕНИЕ АБОНЕНТА ===")
    print("(введите 0 в любом поле для отмены)")

    name = get_valid_input_with_back("Имя", validate_name, "Имя не может быть пустым")
    if name is None: return

    surname = get_valid_input_with_back("Фамилия", validate_name, "Фамилия не может быть пустой")
    if surname is None: return

    email = get_valid_input_with_back("Email", validate_email, "Email должен содержать @")
    if email is None: return

    phone = get_valid_input_with_back("Номер телефона (11 цифр, начинается с 8)", validate_phone,
                                      "Номер должен быть из 11 цифр и начинаться с 8")
    if phone is None: return

    password = get_valid_input_with_back("Пароль (минимум 4 символа)", validate_password,
                                         "Пароль должен быть не менее 4 символов")
    if password is None: return

    print("\nДоступные тарифы:")
    for key, tariff in TARIFFS.items():
        print(f"{key}. {tariff['name']} - {tariff['price']}₽/мес")

    while True:
        tariff_choice = input("Выберите тариф (1-3) или 0 для отмены: ")
        if tariff_choice == "0":
            return
        if tariff_choice in TARIFFS:
            tariff_name = TARIFFS[tariff_choice]["name"]
            break
        print("Неверный выбор")

    subscriber = Subscriber(name, surname, email, phone, password, tariff_name)
    new_id = catalog.add_item(subscriber)
    print(f"Абонент добавлен с ID: {new_id}")


def show_all_subscribers():
    all_items = catalog.get_all_items()

    if not all_items:
        print("Каталог пуст!")
        input("\nНажмите Enter чтобы продолжить...")
        return

    print("\n=== СПИСОК АБОНЕНТОВ ===")
    for sub_id, subscriber in all_items.items():
        print(f"ID: {sub_id} | {subscriber.name} {subscriber.surname} | {subscriber.phone} | {subscriber.tariff_name}")

    input("\nНажмите Enter чтобы продолжить...")


def edit_profile(subscriber):
    """Редактирование личных данных"""
    while True:
        print(f"\n=== РЕДАКТИРОВАНИЕ ПРОФИЛЯ ===")
        print("1. Изменить имя")
        print("2. Изменить фамилию")
        print("3. Изменить email")
        print("4. Изменить номер телефона")
        print("5. Изменить пароль")
        print("0. Назад")

        choice = input("Выберите действие: ")

        if choice == "0":
            break
        elif choice == "1":
            new_name = get_valid_input_with_back("Новое имя", validate_name, "Имя не может быть пустым")
            if new_name:
                subscriber.name = new_name
                print("Имя обновлено")
        elif choice == "2":
            new_surname = get_valid_input_with_back("Новая фамилия", validate_name, "Фамилия не может быть пустой")
            if new_surname:
                subscriber.surname = new_surname
                print("Фамилия обновлена")
        elif choice == "3":
            new_email = get_valid_input_with_back("Новый email", validate_email, "Email должен содержать @")
            if new_email:
                subscriber.email = new_email
                print("Email обновлен")
        elif choice == "4":
            new_phone = get_valid_input_with_back("Новый номер телефона", validate_phone,
                                                  "Номер должен быть из 11 цифр и начинаться с 8")
            if new_phone:
                subscriber.phone = new_phone
                print("Номер телефона обновлен")
        elif choice == "5":
            new_password = get_valid_input_with_back("Новый пароль", validate_password,
                                                     "Пароль должен быть не менее 4 символов")
            if new_password:
                subscriber.password = new_password
                print("Пароль обновлен")
        else:
            print("Неверный выбор")


def change_tariff(subscriber):
    """Смена тарифа"""
    while True:
        print("\n=== СМЕНА ТАРИФА ===")
        print(f"Текущий тариф: {subscriber.tariff_name}")
        print("\nДоступные тарифы:")
        for key, tariff in TARIFFS.items():
            print(f"{key}. {tariff['name']} - {tariff['price']}₽/мес")

        print("0. Назад")
        tariff_choice = input("Выберите тариф: ")

        if tariff_choice == "0":
            break

        if tariff_choice in TARIFFS:
            subscriber.tariff_name = TARIFFS[tariff_choice]['name']
            subscriber.update_packages_by_tariff()
            print(f"Тариф изменен на {subscriber.tariff_name}")
            print(f"Новый пакет: {subscriber.minutes}мин, {subscriber.sms}смс, {subscriber.internet_gb}гб")
            input("\nНажмите Enter чтобы продолжить...")
            break
        else:
            print("Неверный выбор")


def manage_services(subscriber):
    """Управление услугами"""
    while True:
        print(f"\n=== УПРАВЛЕНИЕ УСЛУГАМИ ===")
        print(f"Баланс: {subscriber.balance}₽")
        print(f"Текущие услуги: {', '.join(subscriber.services) if subscriber.services else 'нет'}")
        print("\nДоступные услуги:")
        for key, service in SERVICES.items():
            status = " (подключено)" if service['name'] in subscriber.services else ""
            print(f"{key}. {service['name']} - {service['price']}₽/мес{status}")

        print("0. Вернуться")

        choice = input("Выберите услугу: ")

        if choice == "0":
            break

        if choice in SERVICES:
            service_name = SERVICES[choice]['name']
            service_price = SERVICES[choice]['price']

            if service_name in subscriber.services:
                # Отключаем услугу
                subscriber.services.remove(service_name)
                subscriber.remove_service_effect(service_name)
                print(f"Услуга {service_name} отключена")
            else:
                # Подключаем услугу (проверяем баланс)
                if subscriber.balance >= service_price:
                    subscriber.services.append(service_name)
                    subscriber.apply_service(service_name)
                    subscriber.balance -= service_price
                    print(f"Услуга {service_name} подключена")
                    print(f"Списано {service_price}₽. Остаток на балансе: {subscriber.balance}₽")

                    # Показываем обновленные пакеты
                    print(f"Текущие пакеты: {subscriber.minutes}мин, {subscriber.sms}смс, {subscriber.internet_gb}гб")
                else:
                    print(f"Недостаточно средств. Нужно: {service_price}₽, есть: {subscriber.balance}₽")

            input("\nНажмите Enter чтобы продолжить...")
        else:
            print("Неверный выбор")


def top_up_balance(subscriber):
    """Пополнение баланса"""
    while True:
        print(f"\n=== ПОПОЛНЕНИЕ БАЛАНСА ===")
        print(f"Текущий баланс: {subscriber.balance}₽")
        print("0. Назад")

        try:
            amount_input = input("Введите сумму пополнения: ")
            if amount_input == "0":
                break

            amount = float(amount_input)
            if amount > 0:
                subscriber.balance += amount
                print(f"Баланс пополнен. Текущий баланс: {subscriber.balance}₽")
                input("\nНажмите Enter чтобы продолжить...")
                break
            else:
                print("Сумма должна быть положительной")
        except ValueError:
            print("Введите число")


def show_packages(subscriber):
    """Просмотр пакетов"""
    print(f"\n=== ПАКЕТЫ {subscriber.name} {subscriber.surname} ===")
    print(f"Осталось минут: {subscriber.minutes}")
    print(f"Осталось смс: {subscriber.sms}")
    print(f"Осталось интернета: {subscriber.internet_gb} гб")

    if hasattr(subscriber, 'unlimited_social') and subscriber.unlimited_social:
        print("Безлимитные соцсети: подключены")
    if hasattr(subscriber, 'unlimited_youtube') and subscriber.unlimited_youtube:
        print("Безлимитный YouTube: подключен")

    input("\nНажмите Enter чтобы продолжить...")


def edit_subscriber(subscriber=None):
    """Полное редактирование абонента"""
    if subscriber is None:
        try:
            sub_id = int(input("Введите ID абонента для редактирования (0 - отмена): "))
            if sub_id == 0:
                return
        except ValueError:
            print("Ошибка: введите число")
            return

        subscriber = catalog.get_item(sub_id)

        if not subscriber:
            print(f"Абонент с ID {sub_id} не найден")
            input("Нажмите Enter чтобы продолжить...")
            return

    while True:
        print(f"\n=== РЕДАКТИРОВАНИЕ: {subscriber.name} {subscriber.surname} ===")
        print("1. Редактировать профиль (имя, email, пароль...)")
        print("2. Сменить тариф")
        print("3. Управление услугами")
        print("4. Пополнить баланс")
        print("5. Просмотреть пакеты")
        print("0. Вернуться")

        choice = input("Выберите действие: ")

        if choice == "0":
            break
        elif choice == "1":
            edit_profile(subscriber)
        elif choice == "2":
            change_tariff(subscriber)
        elif choice == "3":
            manage_services(subscriber)
        elif choice == "4":
            top_up_balance(subscriber)
        elif choice == "5":
            show_packages(subscriber)
        else:
            print("Неверный выбор")


def delete_subscriber():
    print("\n=== УДАЛЕНИЕ АБОНЕНТА ===")
    try:
        sub_id = int(input("Введите ID абонента для удаления (0 - отмена): "))
        if sub_id == 0:
            return
    except ValueError:
        print("Ошибка: введите число")
        return

    # Подтверждение удаления
    confirm = input(f"Вы уверены, что хотите удалить абонента с ID {sub_id}? (да/нет): ")
    if confirm.lower() == 'да':
        if catalog.remove_item(sub_id):
            print(f"Абонент с ID {sub_id} удален")
        else:
            print(f"Абонент с ID {sub_id} не найден")
    else:
        print("Удаление отменено")

    input("\nНажмите Enter чтобы продолжить...")


def login_subscriber():
    print("\n=== ВХОД В АККАУНТ ===")
    print("0. Назад")

    phone = input("Введите номер телефона: ")
    if phone == "0":
        return

    password = input("Введите пароль: ")
    if password == "0":
        return

    found_subscriber = None
    for subscriber in catalog.get_all_items_list():
        if subscriber.phone == phone and subscriber.password == password:
            found_subscriber = subscriber
            break

    if found_subscriber:
        print(f"Добро пожаловать, {found_subscriber.name}!")
        user_menu(found_subscriber)
    else:
        print("Неверный номер телефона или пароль")
        input("Нажмите Enter чтобы продолжить...")


def user_menu(subscriber):
    while True:
        print(f"\n=== ЛИЧНЫЙ КАБИНЕТ: {subscriber.name} {subscriber.surname} ===")
        print("1. Просмотреть свои данные")
        print("2. Редактировать профиль")
        print("3. Сменить тариф")
        print("4. Управление услугами")
        print("5. Пополнить баланс")
        print("6. Просмотреть пакеты")
        print("7. Удалить свой аккаунт")
        print("8. Выйти из аккаунта")

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
            print("Выход из аккаунта")
            break
        else:
            print("Неверный выбор")


def save_to_file():
    import pickle
    print("\n=== СОХРАНЕНИЕ В ФАЙЛ ===")
    print("0. Назад")

    filename = input("Введите имя файла для сохранения: ")
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
    import pickle
    print("\n=== ЗАГРУЗКА ИЗ ФАЙЛА ===")
    print("0. Назад")

    filename = input("Введите имя файла для загрузки: ")
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


def show_menu():
    menu = [
        ("1. Просмотр всех абонентов", show_all_subscribers),
        ("2. Добавить абонента", add_subscriber),
        ("3. Редактировать абонента", edit_subscriber),
        ("4. Удалить абонента", delete_subscriber),
        ("5. Войти в аккаунт", login_subscriber),
        ("6. Сохранить в файл", save_to_file),
        ("7. Загрузить из файла", load_from_file),
        ("0. Выход", exit)
    ]

    while True:
        print("\n" + "=" * 50)
        print("МОБИЛЬНЫЙ ОПЕРАТОР - ГЛАВНОЕ МЕНЮ")
        print("=" * 50)
        for item_text, _ in menu:
            print(item_text)

        try:
            choice = input("Выберите действие: ")
            if choice == "0":
                print("До свидания!")
                break

            choice = int(choice)
            if 1 <= choice <= len(menu):
                menu[choice - 1][1]()
            else:
                print(f"Неверный выбор! Введите число от 0 до {len(menu)}")
                input("Нажмите Enter чтобы продолжить...")
        except ValueError:
            print("Ошибка! Введите число")
            input("Нажмите Enter чтобы продолжить...")
        except Exception as e:
            print(f"Ошибка: {e}")
            input("Нажмите Enter чтобы продолжить...")


if __name__ == "__main__":
    # Добавим тестового абонента
    test_sub = Subscriber("Иван", "Иванов", "ivan@mail.ru", "89001234567", "12345", "Оптимум", 1000)
    test_sub.services = ["Безлимитные соцсети"]
    test_sub.unlimited_social = True
    catalog.add_item(test_sub)

    show_menu()
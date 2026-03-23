class UniversityMember:
    def __init__(self, name, age, ident):
        self.name = name
        self.age = age
        self.ident = ident

    def __str__(self):
        return (f"Член университета: {self.name}. "
                f"Возраст: {self.age}. "
                f"Уникальный идентификатор {self.ident}")


class Student(UniversityMember):
    def __init__(self, name, age, ident, group, course):
        super().__init__(name, age, ident)
        self.group = group
        self.course = course

    def __str__(self):
        return (f"Студент {self.name} группы {self.group}")


class Teacher(UniversityMember):
    def __init__(self, name, age, ident, department, subjects):
        super().__init__(name, age, ident)
        self.department = department
        self.subjects = subjects

    def __str__(self):
        return (f"Преподаватель {self.name} кафедры {self.department}")


class Catalog:
    def __init__(self):
        self.items = {}
        self.next_ident = 1

    def add_item(self, obj):
        obj.ident = self.next_ident
        self.items[self.next_ident] = obj
        self.next_ident += 1
        return obj.ident

    def get_item(self, ident):
        return self.items.get(ident)

    def remove_item(self, ident):
        if ident in self.items:
            del self.items[ident]
            return True
        return False

    def remove_all_items(self):
        self.items.clear()
        return True

    def get_all_items(self):
        return self.items

    def get_all_items_list(self):
        return list(self.items.values())

    def get_all_items_with_keys(self):
        return list(self.items.items())

    def __str__(self):
        result = "Картотека:\n"
        for obj in self.items.values():
            result += f"  {obj}\n"
        return result


member = UniversityMember("Петр Петров", 45, "U001")
student = Student("Анна Иванова", 19, "S123", "ИВТ-31", 3)
teacher = Teacher("Мария Сидорова", 38, "T456", "Информатики", ["Python", "Базы данных", "Алгоритмы"])

catalog = Catalog()
catalog.add_item(student)
catalog.add_item(teacher)


def add_student():
    print("Добавление студента...")
    name = input("Введите имя студента: ")
    age = int(input("Введите возраст: "))
    group = input("Введите группу: ")
    course = int(input("Введите курс: "))

    student = Student(name, age, ident, group, course)
    new_id = catalog.add_item(student)
    print(f"Студент добавлен с ID: {new_id}")


def delete_person():
    print("Удаление...")
    ident = int(input("Введите ID для удаления: "))
    if catalog.remove_item(ident):
        print(f"Элемент с ID {ident} удален")
    else:
        print(f"Элемент с ID {ident} не найден")


def show_all_university_members():
    all_items = catalog.get_all_items()

    if not all_items:
        print("Каталог пуст!")
        return

    print("\n=== СПИСОК ВСЕХ ЧЛЕНОВ УНИВЕРСИТЕТА ===")
    for member_id, member in all_items.items():
        print(f"ID: {member_id}")
        print(f"Имя: {member.name}")
        print(f"Возраст: {member.age}")

        if isinstance(member, Student):
            print(f"Группа: {member.group}")
            print(f"Курс: {member.course}")
        elif isinstance(member, Teacher):
            print(f"Кафедра: {member.department}")
            print(f"Предметы: {', '.join(member.subjects)}")

        print(f"Тип: {type(member).__name__}")
        print("-" * 30)


def show_menu():
    menu = [
        ("1. Добавить студента", add_student),
        ("2. Удалить", delete_person),
        ("3. Показать всех", show_all_university_members),
        ("4. Выход", exit)
    ]

    while True:
        print("\n" + "=" * 40)
        print("МЕНЮ:")
        for i, (item_text, _) in enumerate(menu, 1):
            print(f"{i}. {item_text}")

        try:
            choice = int(input("Выберите действие: "))
            if 1 <= choice <= len(menu):
                menu[choice - 1][1]()
            else:
                print(f"Неверный выбор! Введите число от 1 до {len(menu)}")
        except ValueError:
            print("Ошибка! Введите число")
        except Exception as e:
            print(f"Ошибка: {e}")


if __name__ == "__main__":
    show_menu()
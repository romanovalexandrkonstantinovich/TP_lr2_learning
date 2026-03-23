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
    def __init__(self, name, age, ident, departament, subjects):
        super().__init__(name, age, ident)
        self.departament = departament
        self.subjects = subjects
    def __str__(self):
        return (f"Преподаватель {self.name} кафедры {self.departament}")

member = UniversityMember("Петр Петров", 45, "U001")
student = Student("Анна Иванова", 19, "S123", "ИВТ-31", 3)
teacher = Teacher("Мария Сидорова", 38, "T456", "Информатики", ["Python", "Базы данных", "Алгоритмы"])

print(member)
print(student)
print(teacher)

# Чем отличается класс от объекта?
# Класс это шаблон для создания объекта
#
# Зачем нужен __init__?
# Метод необходимый, для того чтобы задать начальные значения
#
# Что такое self?
# Обращение к классу в окружении которого мы на данный момент находимся
# p.s. Ссылка на объект
#
# Как вызвать метод родительского класса?
# через super()
#
# Что произойдет, если не определить __str__?
# Мы просто не получим значение на возврат
# p.s. Если нет __str__, Python использует стандартное представление от object,
# которое выглядит как <__main__.Student object at 0x00000123456789>

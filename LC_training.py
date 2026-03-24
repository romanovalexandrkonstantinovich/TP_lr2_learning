class Book:
    def __init__(self, title, author, pages, year):
        self.title = title
        self.author = author
        self.pages = pages
        self.year = year

    def get_info(self):
        return f'📖 "{self.title}"\n   Автор: {self.author}\n   Страниц: {self.pages}\n   Год: {self.year}'


class FictionBook(Book):
    def __init__(self, title, author, pages, year, genre, has_illustrations):
        super().__init__(title, author, pages, year)
        self.genre = genre
        self.has_illustrations = has_illustrations

    def calculate_popularity(self):
        if self.genre == 'fantastic':
            popularity = 95
        elif self.genre == 'detective':
            popularity = 85
        elif self.genre == 'roman':
            popularity = 75
        else:
            popularity = 50

        if self.has_illustrations:
            popularity += 10

        return popularity

    def display_info(self):
        """Вывод полной информации о художественной книге"""
        print("=" * 40)
        print("📖 ХУДОЖЕСТВЕННАЯ КНИГА")
        print("=" * 40)
        print(f"   {self.get_info()}")
        print(f"   Жанр: {self.genre}")
        print(f"   Иллюстрации: {'✅ Да' if self.has_illustrations else '❌ Нет'}")
        print(f"   🔥 Популярность: {self.calculate_popularity()}")
        print("=" * 40)


class TextBook(Book):
    def __init__(self, title, author, pages, year, subject, grade_level):
        super().__init__(title, author, pages, year)
        self.subject = subject
        self.grade_level = grade_level

    def calculate_usefulness(self):
        if self.subject in ['Mathematics', 'Physics']:
            usefulness = 100
        elif self.subject == 'History':
            usefulness = 80
        else:
            usefulness = 60

        if self.grade_level >= 9:
            usefulness += 10

        return usefulness

    def display_info(self):
        """Вывод полной информации об учебнике"""
        print("=" * 40)
        print("📚 УЧЕБНИК")
        print("=" * 40)
        print(f"   {self.get_info()}")
        print(f"   Предмет: {self.subject}")
        print(f"   Класс: {self.grade_level}")
        print(f"   ⭐ Полезность: {self.calculate_usefulness()}")
        print("=" * 40)


# Тестирование
if __name__ == '__main__':
    print("\n" + "🎓 БИБЛИОТЕЧНАЯ СИСТЕМА".center(40))
    print("\n")

    fantasy_book = FictionBook("Властелин колец", "Дж.Р.Р. Толкин", 1200, 1954, "fantastic", True)
    detective_book = FictionBook("Убийство в Восточном экспрессе", "Агата Кристи", 256, 1934, "detective", False)
    romance_book = FictionBook("Гордость и предубеждение", "Джейн Остин", 432, 1813, "roman", False)

    math_book = TextBook("Алгебра 7 класс", "А.Г. Мордкович", 288, 2020, "Mathematics", 7)
    physics_book = TextBook("Физика 9 класс", "А.В. Перышкин", 256, 2021, "Physics", 9)
    history_book = TextBook("История России 10 класс", "А.Н. Улунян", 320, 2019, "History", 10)

    fantasy_book.display_info()
    print("\n")
    detective_book.display_info()
    print("\n")
    romance_book.display_info()
    print("\n")
    math_book.display_info()
    print("\n")
    physics_book.display_info()
    print("\n")
    history_book.display_info()
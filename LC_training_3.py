class Device:
    def __init__(self, name, power, battery_life):
        self.name = name
        self.power = power
        self.battery_life = battery_life

    def get_info(self):
        return f'Название: {self.name} Мощность: {self.power} Заряд батареи (часов): {self.battery_life}'

class Smartphone(Device):
    def __init__(self, name, power, battery_life, camera_mp, has_5g):
        super().__init__(name, power, battery_life)
        self.camera_mp = camera_mp
        self.has_5g = has_5g

    def calculate_rating(self):
        rating = self.camera_mp / 10
        if self.has_5g:
            rating += 20
        if self.battery_life > 10:
            rating += 15
        if rating > 100:
            rating = 100
        return rating

    def display_info(self):
        print(f'📱 СМАРТФОН')
        print(f'    {self.get_info()}')
        print(f'    Камера: {self.camera_mp}')
        print(f'    5G: {'Да' if self.has_5g else 'Нет'}')
        print(f'    Рейтинг: {self.calculate_rating()}')

if __name__ == '__main__':
    iphone = Smartphone("iphone", 100, 10, 100, True)

    iphone.display_info()
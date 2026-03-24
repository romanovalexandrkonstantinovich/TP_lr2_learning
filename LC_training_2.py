class Vehicle:
    def __init__(self, brand, weight, max_speed):
        self.brand = brand
        self.weight = weight
        self.max_speed = max_speed

    def get_info(self):
        return f'Бренд: {self.brand} Масса: {self.weight} Максимальная скорость: {self.max_speed}'

class Car(Vehicle):
    def __init__(self, brand, weight, max_speed, doors, fuel_type):
        super().__init__(brand, weight, max_speed)
        self.doors = doors
        self.fuel_type = fuel_type

    def calculate_efficiency(self):
        if self.fuel_type == 'электричество':
            efficiency = 95
        elif self.fuel_type == 'дизель':
            efficiency = 80
        elif self.fuel_type == 'бензин':
            efficiency = 70
        else:
            efficiency = 50
        if self.doors >= 4:
            efficiency += 10
        return efficiency

    def display_info(self):
        print('🚗 АВТОМОБИЛЬ')
        print(f'    {self.get_info()}')
        print(f'    Двери: {self.doors}')
        print(f'    Топливо: {self.fuel_type}')
        print(f'    Эффективность: {self.calculate_efficiency()}')

if __name__ == '__main__':
    car_mers = Car("mers", "5000", "50", 3, "дизель")
    car_mers.display_info()

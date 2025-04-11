import sys
from enum import Enum


class CarType(Enum):
    TRUCK = "Грузовик"
    PASSENGER = "Легковой"


class Car:
    def __init__(self, car_id: str, model: str, car_type: CarType):
        self.car_id = car_id
        self.model = model
        self.type = car_type
        self.needs_repair = False

    def __str__(self):
        status = " (требуется ремонт)" if self.needs_repair else ""
        return f"{self.type.value} {self.model} (ID: {self.car_id}){status}"


class Truck(Car):
    def __init__(self, car_id: str, model: str, max_load: float):
        super().__init__(car_id, model, CarType.TRUCK)
        self.max_load = max_load


class PassengerCar(Car):
    def __init__(self, car_id: str, model: str, seats: int):
        super().__init__(car_id, model, CarType.PASSENGER)
        self.seats = seats


class Driver:
    def __init__(self, driver_id: str, name: str):
        self.driver_id = driver_id
        self.name = name
        self.is_active = True
        self.current_car = None
        self.current_trip = None

    def request_repair(self):
        if not self.current_car:
            return "Ошибка: у водителя нет автомобиля!"
        self.current_car.needs_repair = True
        return f"Заявка на ремонт {self.current_car} отправлена."

    def complete_trip(self, car_status_ok: bool):
        if not self.current_trip:
            return "Ошибка: нет активного рейса!"

        self.current_trip.is_completed = True
        if not car_status_ok:
            self.current_car.needs_repair = True
        self.current_trip = None
        return f"Рейс завершен. Статус авто: {'OK' if car_status_ok else 'Требуется ремонт'}"

    def __str__(self):
        status = " (отстранен)" if not self.is_active else ""
        car_info = f", Авто: {self.current_car}" if self.current_car else ""
        trip_info = f", Рейс: {self.current_trip}" if self.current_trip else ""
        return f"{self.name} (ID: {self.driver_id}){status}{car_info}{trip_info}"


class Trip:
    def __init__(self, trip_id: str, destination: str):
        self.trip_id = trip_id
        self.destination = destination
        self.is_completed = False

    def __str__(self):
        return f"Рейс {self.trip_id} -> {self.destination} ({'завершен' if self.is_completed else 'активен'})"


class Dispatcher:
    def __init__(self, name: str):
        self.name = name

    def assign_trip(self, driver: Driver, car: Car, trip: Trip):
        if not driver.is_active:
            return f"Ошибка: {driver.name} отстранен от работы!"
        if car.needs_repart:
            return f"Ошибка: {car} требует ремонта!"

        driver.current_car = car
        driver.current_trip = trip
        return f"Назначено: {driver.name} на {trip} с {car}"

    def suspend_driver(self, driver: Driver):
        driver.is_active = False
        driver.current_trip = None
        return f"{driver.name} отстранен от работы."


def create_car():
    print("\nСоздание автомобиля:")
    car_id = input("Введите ID автомобиля: ")
    model = input("Вете модель: ")
    car_type = input("Тип (1 - Грузовик, 2 - Легковой): ")
    if car_type == "1":
        max_load = float(input("Грузоподъемность (тонн): "))
        return Truck(car_id, model, max_load)

    seats = int(input("Количество мест: "))
    return PassengerCar(car_id, model, seats)


def create_driver():
    print"\nСоздание водителя:")
    driver_id = input("Введите ID водителя: ")
    name = input("Введите ФИО водителя: ")
    return Driver(driver_id, name)


def create_trip():
    print("\nСоздание рейса:")
    trip_id = input("Введите ID рейса: ")
    destination = input("Введите пункт назначения: ")
    return Trip(trip_id, destination)


def show_drivers(drivers):
    print("\nСписок водителей:")
    for driver in drivers:
        print(driver)


def show_cars(cars):
    print("\nСписок автомобилей:")
    for car in cars:
        print(car)


def handle_assignment(dispatcher, drivers, cars, trips):
    if not drivers or not cars or not trips:
        print("Ошибка: сначала создайте водителей, автомобили и рейсы!")
        return

    print("Выберите водителя:")
    for i, driver in enumerate(drivers):
        print(f"{i + 1}. {driver}")
    driver_idx = int(input("Номер водитора: ")) - 1

    print("Выберите автомобиль:")
    for i, car in enumerate(cars):
        print(f"{i + 1}. {car}")
    car_idx = int(input("Номер автомобиля: ")) - 1

    print("Выберите рейс:")
    for i, trip in enumerate(trips):
        print(f"{i + 1}. {trip}")
    trip_idx = int(input("Номер рейса: ")) - 1

    print(dispatcher.assign_trip(drivers[driver_idx], cars[car_idx], trips[trip_idx]))


def handle_complete_trip(drivers):
    print("Выберите водителя для завершения рейса:")
    for i, driver in enumerate(drivers):
        print(f"{i + 1}. {driver}")
    driver_idx = int(input("Номер водителя: ")) - 1
    status = input("Авто в порядке? (1 - Да, 2 - Нет): ") == "1"
    print(drivers[driver_idx].complete_trip(status))


def handle_request_repair(drivers):
    print("Выберите водителя:")
    for i, driver in enumerate(drivers):
        print(f"{i + 1}. {driver}")
    driver_idx = int(input("Номер водителя: ")) - 1
    print(drivers[driver_idx].request_repair())


def handle_suspend_driver(dispatcher, drivers):
    print("Выберите водителя для отстранения:")
    for i, driver in enumerate(drivers):
        print(f"{i + 1}. {driver}")
    driver_idx = int(input("Номер водителя: ")) - 1
    print(dispatcher.suspend_driver(drivers[driver_idx]))


def main():
    dispatcher = Dispatcher(input("Вете ФИО диспетчера: "))
    cars = []
    drivers = []
    trips = []

    menu_actions = {
        "1": lambda: cars.append(create_car()),
        "2": lambda: drivers.append(create_driver()),
        "3": lambda: trips.append(create_trip()),
        "4": lambda: handle_assignment(dispatcher, drivers, cars, trips),
        "5": lambda: handle_complete_trip(drivers),
        "6": lambda: handle_request_repair(drivers),
        "7": lambda: handle_suspend_driver(dispatcher, drivers),
        "8": show_drivers,  # Убрана лишняя лямбда
        "9": show_cars,      # Убрана лишняя лямбда
        "10": sys.exit,      # Использован sys.exit вместо exit()
    }

    while True:
        print("\n1. Добавить автомобиль")
        print("2. Добавить водителя")
        print("3. Создать рейс")
        print("4. Назначить рейс")
        print("5. Завершить рейс")
        print("6. Подать заявку на ремонт")
        print("7. Отстранить водителя")
        print("8. Показать всех водителей")
        print("9. Показать все автомобили")
        print("10. Выход")

        choice = input("Выберите действие: ")
        action = menu_actions.get(choice, lambda: print("Неверный ввод!"))
        if action == sys.exit:
            action()  # Вызов sys.exit()
        else:
            action(drivers) if choice == "8" else (action(cars) if choice == "9" else action())


if __name__ == "__main__":
    main()

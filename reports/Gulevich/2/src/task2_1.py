class LimitedCharSet:
    def __init__(self, max_size, initial_chars=None):
        self.max_size = max_size
        self.elements = []

        if initial_chars:
            for char in initial_chars:
                self.add(char)

    def add(self, char):
        if len(self.elements) >= self.max_size:
            print("Ошибка: достигнута максимальная мощность множества!")
            return False
        if char not in self.elements:
            self.elements.append(char)
            print(f"Символ '{char}' успешно добавлен.")
            return True
        print(f"Символ '{char}' уже есть в множестве.")
        return False

    def remove(self, char):
        if char in self.elements:
            self.elements.remove(char)
            print(f"Символ '{char}' успешно удален.")
            return True
        print(f"Символ '{char}' не найден в множестве.")
        return False

    def contains(self, char):
        if char in self.elements:
            print(f"Символ '{char}' принадлежит множеству.")
        else:
            print(f"Символ '{char}' отсутствует в множестве.")
        return char in self.elements

    def union(self, other_set):
        new_max_size = self.max_size + other_set.max_size
        new_set = LimitedCharSet(new_max_size)

        for char in self.elements:
            new_set.add(char)

        for char in other_set.elements:
            new_set.add(char)

        return new_set

    def __str__(self):
        return f"Текущее множество (мощность {self.max_size}): {', '.join(self.elements) if self.elements else 'пусто'}"

    def __eq__(self, other):
        if not isinstance(other, LimitedCharSet):
            return False
        return sorted(self.elements) == sorted(other.elements) and self.max_size == other.max_size


def create_set(set_number):
    print(f"Создание множества {set_number}:")
    max_size = int(input("Введите максимальную мощность множества: "))
    initial_chars = input("Введите начальные символы (через пробел, или оставьте пустым): ").split()
    return LimitedCharSet(max_size, initial_chars if initial_chars else None)


def manage_set(current_set):
    while True:
        print(f"\nТекущее множество: {current_set}")
        print("1. Добавить символ")
        print("2. Удалить символ")
        print("3. Проверить наличие символа")
        print("4. Назад")
        sub_choice = input("Выберите действие (1-4): ")

        if sub_choice == "1":
            char = input("Введите символ для добавления: ").strip()
            current_set.add(char)
        elif sub_choice == "2":
            char = input("Введите символ для удаления: ").strip()
            current_set.remove(char)
        elif sub_choice == "3":
            char = input("Введите символ для проверки: ").strip()
            current_set.contains(char)
        elif sub_choice == "4":
            break
        else:
            print("Неверный ввод!")


def main():
    set1 = create_set(1)
    set2 = create_set(2)

    while True:
        print("\n1. Работа с множеством 1")
        print("2. Работа с множеством 2")
        print("3. Объединить множества")
        print("4. Сравнить множества")
        print("5. Выход")
        choice = input("Выберите действие (1-5): ")

        if choice == "1":
            manage_set(set1)
        elif choice == "2":
            manage_set(set2)
        elif choice == "3":
            new_set = set1.union(set2)
            print("\nРезультат объединения:")
            print(new_set)
        elif choice == "4":
            print("\nРезультат сравнения:")
            print("Множества идентичны." if set1 == set2 else "Множества различны.")
        elif choice == "5":
            break
        else:
            print("Неверный ввод!")


if __name__ == "__main__":
    main()

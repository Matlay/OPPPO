from abc import ABC, abstractmethod
from enum import Enum


class FloweringMonth(Enum):
    JANUARY = "JANUARY"
    FEBRUARY = "FEBRUARY"
    MARCH = "MARCH"
    APRIL = "APRIL"
    MAY = "MAY"
    JUNE = "JUNE"
    JULY = "JULY"
    AUGUST = "AUGUST"
    SEPTEMBER = "SEPTEMBER"
    OCTOBER = "OCTOBER"
    NOVEMBER = "NOVEMBER"
    DECEMBER = "DECEMBER"


class Plant(ABC):
    """Абстрактный базовый класс растения"""

    def __init__(self, name: str) -> None:
        self.name = name

    def get_base_info(self) -> str:
        """Возвращает общую часть описания растения"""
        return f"Тип: {self.get_type()}, Название: {self.name}"

    @abstractmethod
    def get_type(self) -> str:
        """Возвращает тип растения"""

    @abstractmethod
    def get_info(self) -> str:
        """Возвращает строковое описание растения"""

    def __str__(self) -> str:
        return self.get_info()


class Tree(Plant):
    """Дерево. Уникальный параметр — возраст"""

    def __init__(self, name: str, age: int) -> None:
        if age < 0:
            raise ValueError("Возраст не может быть отрицательным")
        super().__init__(name)
        self.age = age

    def get_type(self) -> str:
        return "Дерево"

    def get_info(self) -> str:
        return f"{self.get_base_info()}, Возраст: {self.age}"


class Shrub(Plant):
    """Кустарник. Уникальный параметр — месяц цветения"""

    def __init__(self, name: str, flowering_month: FloweringMonth) -> None:
        super().__init__(name)
        self.flowering_month = flowering_month

    def get_type(self) -> str:
        return "Кустарник"

    def get_info(self) -> str:
        return (
            f"{self.get_base_info()}, "
            f"Месяц цветения: {self.flowering_month.value}"
        )


class Cactus(Plant):
    """Кактус. Уникальный параметр — длина колючек"""

    def __init__(self, name: str, spine_length: float) -> None:
        if spine_length < 0:
            raise ValueError("Длина колючек не может быть отрицательной")
        super().__init__(name)
        self.spine_length = spine_length

    def get_type(self) -> str:
        return "Кактус"

    def get_info(self) -> str:
        return (
            f"{self.get_base_info()}, "
            f"Длина колючек: {self.spine_length}"
        )


class PlantContainer:
    """Контейнер для хранения растений"""

    def __init__(self) -> None:
        self.plants: list[Plant] = []

    def add(self, plant: Plant) -> None:
        self.plants.append(plant)

    def remove_by_name(self, name: str) -> int:
        """Удаляет все растения с указанным названием"""
        old_size = len(self.plants)

        self.plants = [
            plant
            for plant in self.plants
            if plant.name != name
        ]

        return old_size - len(self.plants)

    def print_all(self) -> None:
        """Выводит все растения"""
        if not self.plants:
            print("Контейнер пуст")
            return

        for number, plant in enumerate(self.plants, start=1):
            print(f"{number}. {plant}")


def parse_month(value: str) -> FloweringMonth:
    """Преобразует строку в месяц цветения"""
    value = value.upper()

    try:
        return FloweringMonth(value)
    except ValueError as exc:
        raise ValueError(
            f"Неизвестный месяц цветения: {value}"
        ) from exc


def ensure_arg_count(parts: list[str], expected_len: int, usage: str) -> None:
    """Проверяет точное количество аргументов команды"""
    if len(parts) != expected_len:
        raise ValueError(f"Формат: {usage}")


def create_tree(parts: list[str], name: str) -> Tree:
    """Создаёт объект дерева из аргументов команды"""
    ensure_arg_count(parts, 4, "ADD TREE <название> <возраст>")
    age = int(parts[3])
    return Tree(name, age)


def create_shrub(parts: list[str], name: str) -> Shrub:
    """Создаёт объект кустарника из аргументов команды"""
    ensure_arg_count(parts, 4, "ADD SHRUB <название> <месяц>")
    month = parse_month(parts[3])
    return Shrub(name, month)


def create_cactus(parts: list[str], name: str) -> Cactus:
    """Создаёт объект кактуса из аргументов команды"""
    ensure_arg_count(parts, 4, "ADD CACTUS <название> <длина_колючек>")
    spine_length = float(parts[3])
    return Cactus(name, spine_length)


def process_add(parts: list[str], container: PlantContainer) -> None:
    """Обработка команды ADD"""

    if len(parts) < 3:
        raise ValueError("Неверный формат команды ADD")

    plant_type = parts[1].upper()
    name = parts[2]
    plant: Plant

    if plant_type == "TREE":
        plant = create_tree(parts, name)
    elif plant_type == "SHRUB":
        plant = create_shrub(parts, name)
    elif plant_type == "CACTUS":
        plant = create_cactus(parts, name)
    else:
        raise ValueError(
            f"Неизвестный тип растения: {plant_type}"
        )

    container.add(plant)
    print(f"Добавлено: {plant}")


def process_rem(parts: list[str], container: PlantContainer) -> None:
    """Обработка команды REM"""

    if len(parts) != 3:
        raise ValueError(
            "Формат: REM NAME <название>"
        )

    condition_type = parts[1].upper()
    value = parts[2]

    if condition_type == "NAME":
        removed = container.remove_by_name(value)

        print(f"Удалено объектов: {removed}")

    else:
        raise ValueError(
            f"Неизвестное условие удаления: {condition_type}"
        )


def process_command(line: str, container: PlantContainer) -> None:
    """Распознаёт и выполняет одну команду"""

    line = line.strip()

    if not line:
        return

    parts = line.split()
    command = parts[0].upper()

    if command == "ADD":
        process_add(parts, container)

    elif command == "REM":
        process_rem(parts, container)

    elif command == "PRINT":
        container.print_all()

    else:
        raise ValueError(
            f"Неизвестная команда: {command}"
        )


def process_file(filename: str) -> PlantContainer:
    """Читает файл построчно и выполняет команды"""

    container = PlantContainer()

    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                try:
                    process_command(line, container)

                except (ValueError, IndexError) as error:
                    print(
                        f"Ошибка в строке {line_number}: {error}"
                    )

    except FileNotFoundError:
        print(f"Файл не найден: {filename}")

    return container


def main() -> None:
    filename = "input.txt"

    process_file(filename)


if __name__ == "__main__":
    main()

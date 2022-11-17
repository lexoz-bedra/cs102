import math
import typing as tp


def change_base(num: int, base: int) -> str:
    """Меняем систему счисления"""
    if num < 0:
        return "Переводимое число должно быть неотрицательным!!"
    if num == 0:
        return "0"
    if not 2 <= base <= 9:
        return "Система счисления должна быть от 2 до 9!!"
    final_number = ""
    while num > 0:
        final_number += str(int(num % base))
        num //= base
    return final_number[::-1]


def match_case_calc_unary(num_1: float, command: str) -> tp.Union[float, str]:  # type: ignore
    """Унарные операции"""
    match command:
        case "sqr":
            return num_1**2
        case "sin":
            return math.sin(num_1)
        case "cos":
            return math.cos(num_1)
        case "tan":
            if math.cos(num_1) == 0:
                return "Тангенс не определён!!"
            return math.tan(num_1)
        case "ln":
            if num_1 <= 0:
                return "Натуральный логарифм не определён!!"
            return math.log(num_1)
        case "lg":
            if num_1 <= 0:
                return "Десятичный логарифм не определён!!"
            return math.log10(num_1)


def match_case_calc_binary(num_1: float, num_2: float, command: str) -> tp.Union[float, str]:  # type: ignore
    """Бинарные операции"""
    match command:
        case "+":
            return num_1 + num_2
        case "*":
            return num_1 * num_2
        case "^":
            return num_1**num_2
        case "/":
            if num_2 == 0:
                return "Делить на ноль нельзя!!"
            return num_1 / num_2
        case "-":
            return num_1 - num_2
        case _:
            return f"Неизвестный оператор: {command!r}!!"


def is_number(input_string: str) -> tp.Union[float, None]:
    """Проверяем, является ли строка числом"""
    if (
        input_string.isdigit()
        or (input_string[0] == "-" and input_string[1:].isdigit())
        or (input_string.count(".") == 1 and input_string.replace(".", "").isdigit())
        or (input_string[0] == "-" and input_string[1:].replace(".", "").isdigit() and input_string.count(".") == 1)
    ):
        return float(input_string)
    return  # type: ignore


if __name__ == "__main__":
    print(
        "Привет!!"
        "\nЧтобы выключить меня, нажмите 0.\nЧтобы начать, напишите 'начать' или 'start'.\n\n"
        "Вот что вы можете сделать:\n> Сложение (+)\n> Вычитание (-)\n> Умножение (*)"
        "\n> Деление (/)\n> Возведение в квадрат (sqr)"
        "\n> Ввозведение в степень (^)\n> Синус (sin)\n> Косинус (cos)"
        "\n> Тангенс (tan)\n> Натуральный логарифм (ln)\n> Десятичный логарифм (lg)"
        "\n> Поменять систему счисления (#)"
        "\n\nПриятного использования!!:')\n"
    )
    cmd = input("Напишите что-нибудь > ")
    if cmd == "start" or cmd == "начать":
        while True:
            COMMAND = input("Введите операцию > ")
            if COMMAND.isdigit() and int(COMMAND) == 0:
                print("Спокойной ночи!!")
                break
            if COMMAND in ["sqr", "sin", "cos", "tan", "ln", "lg"]:
                n1 = input("Число > ")
                NUM_1 = is_number(n1)
                print(match_case_calc_unary(NUM_1, COMMAND)) if NUM_1 is not None else print(
                    "Нужно было ввести число!!"
                )
            elif COMMAND in ["+", "-", "*", "/", "^"]:
                n1 = input("Первое число > ")
                NUM_1 = is_number(n1)
                if NUM_1 is None:
                    print("Нужно было ввести число!!")
                    continue
                n2 = input("Второе число > ")
                NUM_2 = is_number(n2)
                if NUM_2 is None:
                    print("Нужно было ввести число!!")
                    continue
                print(match_case_calc_binary(NUM_1, NUM_2, COMMAND))
            elif COMMAND == "#":
                NUM_1 = is_number(input("Число > "))
                if NUM_1 is None:
                    print("Нужно было ввести число!!")
                    continue
                NUM_2 = is_number(input("Основание > "))
                if NUM_2 is None:
                    print("Нужно было ввести число!!")
                    continue
                print(change_base(int(NUM_1), int(NUM_2)))
            else:
                print("Нужно было ввести операцию!!")

import math
import typing as tp


def change_base(num: int, base: int) -> str:
    """Меняем систему счисления"""
    if num < 0:
        return "Основание системы счисления должно быть неотрицательным!!"
    if base > 9 or base < 2:
        return "Система счисления должна быть от 2 до 9!!"
    string = ""
    while num >= 0:
        string += str(num % base)
        num //= base
    return string[::-1]


def match_case_calc_unary(num_1: float, command: str) -> tp.Union[float, str]:  # type: ignore
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
                n1 = input("Первое число > ")
                if (
                    n1.isdigit()
                    or (n1[0] == "-" and n1[1:].isdigit())
                    or (n1.count(".") == 1 and n1.replace(".", "").isdigit())
                    or (n1[0] == "-" and n1[1:].replace(".", "").isdigit() and n1.count(".") == 1)
                ):
                    NUM_1 = float(n1)
                else:
                    print("Нужно было ввести число!!")
                    continue
                print(match_case_calc_unary(NUM_1, COMMAND))
            elif COMMAND in ["+", "-", "*", "/", "^"]:
                n1 = input("Первое число > ")
                if (
                    n1.isdigit()
                    or (n1[0] == "-" and n1[1:].isdigit())
                    or (n1.count(".") == 1 and n1.replace(".", "").isdigit())
                    or (n1[0] == "-" and n1[1:].replace(".", "").isdigit() and n1.count(".") == 1)
                ):
                    NUM_1 = float(n1)
                else:
                    print("Нужно было ввести число!!")
                    continue
                n2 = input("Второе число > ")
                if (
                    n2.isdigit()
                    or (n2[0] == "-" and n2[1:].isdigit())
                    or (n2.count(".") == 1 and n2.replace(".", "").isdigit())
                    or (n2[0] == "-" and n2[1:].replace(".", "").isdigit() and n2.count(".") == 1)
                ):
                    NUM_2 = float(n2)
                else:
                    print("Нужно было ввести число!!")
                    continue
                print(match_case_calc_binary(NUM_1, NUM_2, COMMAND))
            elif COMMAND == "change base":
                NUM_1 = int(input("Число > "))
                NUM_2 = int(input("Основание > "))
                print(change_base(NUM_1, NUM_2))
            else:
                print("Нужно было ввести операцию!!")

import math
import typing as tp

"""
- Возможность ввода всей цепочки операций целиком и ее решение, 
если она введена корректно. Цепочка может содержать скобки (ДЛЯ ТЕХ, У КОГО ПОЛУЧИЛИСЬ 
ВСЕ ОСТАЛЬНЫЕ ЧАСТИ ЗАДАНИЯ)

Продемонстрируйте работу программы. Для этого реализуйте соответствующее меню.
"""


def calc(num_1: float, num_2: float, command: str) -> tp.Union[float, str]:
    if command == "+":
        return num_1 + num_2
    if command == "-":
        return num_1 - num_2
    else:
        return f"Неизвестный оператор: {command!r}"


def change_base(num: int, base: int) -> str:
    if num < 0 or base > 9 or base < 2:
        return "Некорректный формат ввода"
    s = ""
    while num > 0:
        s += str(num % base)
        num //= base
    return s[::-1]


def match_case_calc_unary(num_1: float, command: str) -> tp.Union[float, str]:  # type: ignore
    match command:
        case "sqr":
            return num_1**2
        case "sin":
            return math.sin(num_1)
        case "cos":
            return math.cos(num_1)
        case "tan":
            return math.tan(num_1)
        case "ln":
            return math.log(num_1)
        case "lg":
            return math.log10(num_1)


def match_case_calc_binary(num_1: float, num_2: float, command: str) -> tp.Union[float, str]:  # type: ignore
    match command:
        case "+":
            return num_1 + num_2
        case "*":
            return num_1 * num_2
        case "^":
            return num_1**num_2
        case "/" if num_2 != 0:
            return num_1 / num_2
        case "-":
            return num_1 - num_2
        case _:
            return f"Неизвестный оператор: {command!r}."


if __name__ == "__main__":
    while True:
        COMMAND = input("Введите оперцию > ")
        if COMMAND.isdigit() and int(COMMAND) == 0:
            break
        if COMMAND in ["sqr", "sin", "cos", "tan", "ln", "lg"]:
            NUM_1 = float(input("Число > "))
            print(match_case_calc_unary(NUM_1, COMMAND))
        elif COMMAND in ["+", "-", "*", "/", "^"]:
            NUM_1 = float(input("Первое число > "))
            NUM_2 = float(input("Второе число > "))
            print(match_case_calc_binary(NUM_1, NUM_2, COMMAND))
        elif COMMAND == "change base":
            NUM_1 = int(input("Число > "))
            NUM_2 = int(input("Основание > "))
            print(change_base(NUM_1, NUM_2))

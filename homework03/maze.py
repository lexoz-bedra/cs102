from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd  # type: ignore


def create_grid(rows: int, cols: int) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param coord:
    :return:
    """
    row = len(grid[0]) - 2
    y, x = coord
    options = (0, 1)  # 0 - вверх, 1 - вправо
    direction = choice(list(options))
    if y > 1 and x == row:
        grid[y - 1][x] = " "
    elif y == 1 and x < row:
        grid[y][x + 1] = " "
    elif y > 1 and x < row:
        match direction:
            case 0:
                grid[y - 1][x] = " "
            case 1:
                grid[y][x + 1] = " "

    return grid


def bin_tree_maze(rows: int, cols: int, random_exit: bool = True) -> List[List[Union[str, int]]]:
    """

    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """

    # решётка (работает нормально)
    grid = create_grid(rows, cols)
    empty_cells = []
    for y, row in enumerate(grid):
        for x, _ in enumerate(row):
            if y % 2 == 1 and x % 2 == 1:
                grid[y][x] = " "
                empty_cells.append((y, x))

    # стенки (работает нормально)
    for cell in empty_cells:
        grid = remove_wall(grid, cell)

    for i, _ in enumerate(grid):
        if grid[i][cols - 1] != "■":
            grid[i][cols - 1] = "■"

    # 1. выбрать любую клетку
    # 2. выбрать направление: наверх или направо.
    # Если в выбранном направлении следующая клетка лежит за границами поля,
    # выбрать второе возможное направление
    # 3. перейти в следующую клетку, сносим между клетками стену
    # 4. повторять 2-3 до тех пор, пока не будут пройдены все клетки

    # генерация входа и выхода (работает нормально)
    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """

    :param grid:
    :return:
    """
    exits = []
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == "X":
                exits.append((y, x))
    return exits


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param k:
    :return:
    """

    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == k:
                print(y, x)
                m = k + 1
                if x != 0 and (grid[y][x - 1] == 0 or grid[y][x - 1] == " "):
                    grid[y][x - 1] = m
                if x != len(row) - 1 and (grid[y][x + 1] == 0 or grid[y][x + 1] == " "):
                    grid[y][x + 1] = m
                if y != 0 and (grid[y - 1][x] == 0 or grid[y - 1][x] == " "):
                    grid[y - 1][x] = m
                if y != len(grid) - 1 and (grid[y + 1][x] == 0 or grid[y + 1][x] == " "):
                    grid[y + 1][x] = m
    return grid


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """

    :param grid:
    :param exit_coord:
    :return:
    """
    exit_num = grid[exit_coord[0]][exit_coord[1]]
    k = int(grid[exit_coord[0]][exit_coord[1]]) - 1

    y, x = exit_coord
    cur_y = exit_coord[0]
    cur_x = exit_coord[1]
    way = [(cur_y, cur_x)]

    while k != 0:
        if y + 1 < len(grid):
            if grid[y + 1][x] == k:
                cur_y = y + 1
                y += 1
        if y - 1 >= 0:
            if grid[y - 1][x] == k:
                cur_y = y - 1
                y -= 1
        if x + 1 < len(grid):
            if grid[y][x + 1] == k:
                cur_x = x + 1
                x += 1
        if x - 1 >= 0:
            if grid[y][x - 1] == k:
                cur_x = x - 1
                x -= 1
        way.append((cur_y, cur_x))
        k -= 1

    if len(way) != exit_num:
        y = way[-1][0]
        x = way[-1][1]
        grid[y][x] = " "
        x_2, y_2 = way[-2][0], way[-2][1]
        way = shortest_path(grid, (x_2, y_2))  # type: ignore

    return way


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """

    :param grid:
    :param coord:
    :return:
    """

    y, x = coord
    # углы
    if (
        x == y == 0
        or x == 0
        and y == len(grid) - 1
        or y == 0
        and x == len(grid[0]) - 1
        or x == len(grid[0]) - 1
        and y == len(grid) - 1
    ):
        return True

    # не углы (а стены)
    if (
        y == 0
        and grid[y + 1][x] == "■"
        or x == 0
        and grid[y][x + 1] == "■"
        or x == len(grid[0]) - 1
        and grid[y][x - 1] == "■"
        or y == len(grid) - 1
        and grid[y - 1][x] == "■"
    ):
        return True
    return False


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    """

    :param grid:
    :return:
    """
    k = 0
    exits = get_exits(grid)

    # один выход
    if len(exits) == 1:
        return grid, exits[0]

    y_1, x_1 = exits[0]
    y_2, x_2 = exits[1]

    # тупик :(((
    if encircled_exit(grid, (y_1, x_1)) or encircled_exit(grid, (y_2, x_2)):
        return grid, None

    grid[y_1][x_1], grid[y_2][x_2] = 1, 0

    grid = deepcopy(grid)
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == " ":
                grid[i][j] = 0

    while grid[y_2][x_2] == 0:
        k += 1
        grid = make_step(grid, k)

    return grid, shortest_path(grid, (y_2, x_2))


def add_path_to_grid(
    grid: List[List[Union[str, int]]], path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param path:
    :return:
    """

    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    # print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))

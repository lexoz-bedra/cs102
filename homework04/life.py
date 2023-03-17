import pathlib
import random
import typing as tp

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.
        """
        if randomize:
            return [[random.randint(0, 1) for _ in range(self.cols)] for _ in range(self.rows)]
        return [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки.
        """
        neighbours = []
        y, x = cell
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if (j, i) != cell and 0 <= i < self.cols and 0 <= j < self.rows:
                    neighbours.append(self.curr_generation[j][i])
        return neighbours

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.
        """
        new_grid = self.create_grid(randomize=False)
        for y in range(self.rows):
            for x in range(self.cols):
                neighbours = self.get_neighbours((y, x))
                if self.curr_generation[y][x] == 1:
                    if sum(neighbours) in [2, 3]:
                        new_grid[y][x] = 1
                else:
                    if sum(neighbours) == 3:
                        new_grid[y][x] = 1
        return new_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.max_generations is None:
            return False
        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.prev_generation != self.curr_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename, "r") as f:
            grid = [[int(i) for i in j] for j in f.read().splitlines()]
        return GameOfLife((len(grid[0]), len(grid)), randomize=False)

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        grid_to_save = self.curr_generation
        grid_str = "\n".join(["".join([str(i) for i in j]) for j in grid_to_save])

        with open(filename, "w") as g:
            g.write(grid_str)

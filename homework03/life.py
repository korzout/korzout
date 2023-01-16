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
        max_generations: float = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations if max_generations > 0 else float("inf")
        # Теeкущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        if randomize:
            return [[random.randint(0, 1) for _ in range(self.cols)] for _ in range(self.rows)]
        return [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def get_cell(self, cell: Cell) -> int:
        return self.curr_generation[cell[0]][cell[1]]

    def get_neighbours(self, cell: Cell) -> Cells:
        result = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if 0 <= cell[0] + i < self.rows and 0 <= cell[1] + j < self.cols:
                    result.append(self.curr_generation[cell[0] + i][cell[1] + j])
        return result

    def get_next_generation(self) -> Grid:
        newgrid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.cols):
                neighrours = self.get_neighbours((i, j))
                if (self.curr_generation[i][j] == 1 and 2 <= sum(neighrours) <= 3) or (
                    self.curr_generation[i][j] == 0 and sum(neighrours) == 3
                ):
                    newgrid[i][j] = 1
                else:
                    newgrid[i][j] = 0
        self.generations += 1
        return newgrid

    def invert_value(self, cell: Cell) -> None:
        self.curr_generation[cell[0]][cell[1]] = 1 - self.curr_generation[cell[0]][cell[1]]

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation, self.curr_generation = (
            self.curr_generation[:],
            self.get_next_generation(),
        )

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
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
        file = open(filename, "r")
        lst = list(file.read().split("\n"))
        n = len(lst)
        m = len(lst[0])
        grid = [[0 for _ in range(m)] for _ in range(n)]
        for i in range(n):
            for j in range(m):
                grid[i][j] = int(lst[i][j])
        game = GameOfLife((n, m))
        game.curr_generation = grid
        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        file = open(filename, "w")
        file.write(
            "\n".join([" ".join(map(str, self.curr_generation[i])) for i in range(self.rows)])
        )
        file.close()

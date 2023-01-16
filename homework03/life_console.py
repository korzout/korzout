import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """Отобразить рамку."""
        screen.border("|", "|", "-", "-", ".", ".", ".", ".")

    def draw_grid(self, screen) -> None:
        """Отобразить состояние клеток."""
        for row in range(self.life.rows):
            for col in range(self.life.cols):
                if self.life.curr_generation[row][col] == 1:
                    screen.addch(row + 1, col + 1, "■")
                else:
                    screen.addch(row + 1, col + 1, " ")

    def run(self) -> None:
        screen = curses.initscr()

        while True:
            self.draw_borders(screen)
            self.draw_grid(screen)
            screen.refresh()
            curses.flash()
            self.life.step()
            if screen.getch() == ord("q"):
                curses.endwin()
                break


if __name__ == "__main__":
    game = GameOfLife(size=(25, 50))
    consuse = Console(life=game)
    consuse.run()

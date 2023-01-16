import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)

        self.speed = speed
        self.cell_size = cell_size
        self.width, self.height = self.life.rows * self.cell_size, self.life.cols * self.cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))

    def draw_lines(self) -> None:
        # Copy from previous assignment
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        for row in range(self.life.rows):
            for col in range(self.life.cols):
                if self.life.curr_generation[row][col]:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("skyblue"),
                        (
                            col * self.cell_size,
                            row * self.cell_size,
                            self.cell_size,
                            self.cell_size,
                        ),
                    )
                else:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("deeppink"),
                        (
                            col * self.cell_size,
                            row * self.cell_size,
                            self.cell_size,
                            self.cell_size,
                        ),
                    )
        return None

    def run(self) -> None:
        # Copy from previous assignment

        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))
        started = False
        while not started:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    coordinates = pygame.mouse.get_pos()
                    x, y = coordinates[1] // self.cell_size, coordinates[0] // self.cell_size
                    self.life.curr_generation[x][y] = 1 - self.life.curr_generation[x][y]
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        started = True
            self.draw_grid()
            self.draw_lines()
            pygame.display.flip()
        running = True
        paused = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = not paused
                    elif event.key == pygame.K_EQUALS:
                        self.speed = self.speed + 5
                    elif event.key == pygame.K_MINUS:
                        self.speed = max(self.speed - 5, 1)
                if event.type == pygame.MOUSEBUTTONUP:
                    coordinates = pygame.mouse.get_pos()
                    x, y = coordinates[1] // self.cell_size, coordinates[0] // self.cell_size
                    self.life.curr_generation[x][y] = 1 - self.life.curr_generation[x][y]
                if event.type == pygame.QUIT:
                    running = False
            self.draw_grid()
            self.draw_lines()
            if not paused:
                self.life.step()
            if self.life.is_max_generations_exceeded or not self.life.is_changing:
                fl_running = False
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()


game = GameOfLife((20, 20), max_generations=2500)
gui = GUI(game)
gui.run()

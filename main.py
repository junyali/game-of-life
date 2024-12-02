# Conway's Game of Life
# A (slow) Python 3.12 implementation of John Horton Conway's concept of cellular automata

## // Imports \\ ##
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import sys
sys.path.insert(1, "./patterns/")
import importlib
import pygame
import numpy as np
import time
import timeit
import argparse

## // CONSTANTS \\ ##
cell_alive = 1
cell_dead = 0

colour_grid = (255, 255, 255)
colour_gridline = (192, 192, 192)
colour_cell_alive = (0, 0, 0)
colour_cell_about_to_die = (0, 0, 0)

class Simulation:
    def update(self):
        next_grid = np.zeros((self.grid.shape[0], self.grid.shape[1]))

        for row, column in np.ndindex(self.grid.shape):
            num_alive = np.sum(self.grid[row - 1:row + 2, column - 1:column + 2]) - self.grid[row, column]

            if self.grid[row, column] == 1 and num_alive < 2 or num_alive > 3:
                colour = colour_cell_about_to_die
                next_grid[row, column] = 0
            elif (self.grid[row, column] == 1 and 2 <= num_alive <= 3) or (self.grid[row, column] == 0 and num_alive == 3):
                next_grid[row, column] = 1
                colour = colour_cell_alive

            colour = colour if self.grid[row, column] == 1 else colour_grid

            pygame.draw.rect(self.surface, colour_gridline, (column * self.cellsize, row * self.cellsize, self.cellsize, self.cellsize), 1)

            pygame.draw.rect(self.surface, colour, (column * self.cellsize, row * self.cellsize, self.cellsize - 1, self.cellsize - 1))

        return next_grid



    def run(self):
        pygame.init()
        self.surface = pygame.display.set_mode((self.gridsize * self.cellsize, self.gridsize * self.cellsize))
        pygame.display.set_caption("Conway's Game of Life")

        self.start_time = timeit.default_timer()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Ending simulation...")
                    pygame.quit()
                    print("Simulation ended [Time: {time} | Generation: {iteration} | Population: {alive}]".format(time=round(timeit.default_timer() - self.start_time, 1), iteration=self.iteration, alive=self.alive))
                    sys.exit(0)
            self.iteration += 1

            unique, counts = np.unique(self.grid, return_counts=True)
            count_list = np.asarray((unique, counts))

            try:
                if len(count_list[0]) == 1:
                    self.alive = 0
                elif len(count_list) == 2:
                    self.alive = int(count_list[1][1])
                else:
                    print("Could not count number of alive cells?")
                    self.alive = -1
            except ValueError:
                print("Could not count number of alive cells?")
                self.alive = -1

            self.surface.fill(colour_grid)
            self.grid = self.update()
            pygame.display.update()

            pygame.display.set_caption("Game of Life [Time: {time} | Generation: {iteration} | Population: {alive}]".format(time=round(timeit.default_timer() - self.start_time, 1), iteration=self.iteration, alive=self.alive))

            time.sleep(self.delay / 1000)


    def set_pattern(self):
        self.grid = np.zeros(self.gridsize * self.gridsize).reshape(self.gridsize, self.gridsize)

        if self.pattern == "random":
            self.grid = np.random.choice([cell_alive, cell_dead], size=self.gridsize * self.gridsize, p=[0.2, 0.8]).reshape(self.gridsize, self.gridsize)
        else:
            try:
                module = importlib.import_module(self.pattern)
            except ModuleNotFoundError:
                print("Error! No pattern named {name}.".format(name=self.pattern))
                sys.exit(1)
            else:
                print("""
                Loading pattern {name}
                {description}
                """.format(name=module.name, description=module.description))

                try:
                    add_pattern = np.array(module.pattern)
                    self.grid[self.xoffset:self.xoffset + module.offset_x, self.yoffset:self.yoffset + module.offset_y] = add_pattern
                except ValueError:
                    print("Error! Unable to append pattern to grid - is the pattern offset appropriate?")
                    sys.exit(1)
                else:
                    print("Pattern successfully appended.")

    def __init__(self, cellsize, gridize, delay, pattern, xoffset, yoffset):
        # Initialise object attributes
        self.alive = 0
        self.surface = None
        self.cellsize = cellsize
        self.gridsize = gridize
        self.delay = delay
        self.pattern = pattern.replace(".py", "")
        self.xoffset = xoffset
        self.yoffset = yoffset
        self.grid = np.array([])
        self.start_time = 0
        self.iteration = 0

        self.grid = None




def parsing():
    parser = argparse.ArgumentParser(description="Conway's Game of Life")
    parser.add_argument("-c", "--cellsize", type=int, help="Size of each cell (pixels)", default=8)
    parser.add_argument("-g", "--gridsize", type=int, help="Size of the simulation (cells)", default=100)
    parser.add_argument("-d", "--delay", type=int, help="Animation delay between each generation (milliseconds)", default=0)
    parser.add_argument("-p", "--pattern", type=str, help="Pattern to use", default="random")
    parser.add_argument("-x", "--xoffset", type=int, help="Pattern offset on x-axis", default=8)
    parser.add_argument("-y", "--yoffset", type=int, help="Pattern offset on y-axis", default=8)

    args = parser.parse_args()

    return args

if __name__ == '__main__':
    params = parsing()
    Game = Simulation(params.cellsize, params.gridsize, params.delay, params.pattern, params.xoffset, params.yoffset)
    Game.set_pattern()
    Game.run()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/

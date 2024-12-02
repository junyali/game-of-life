# Conway's Game of Life
# A (slow) Python 3.12 implementation of John Horton Conway's concept of cellular automata

## // Imports \\ ##
import os
from multiprocessing.managers import Value

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import sys
sys.path.insert(1, "./patterns/")
import importlib
import pygame
import numpy as np
import timeit
import math
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

    def run(self):
        pygame.init()
        self.surface = pygame.display.setmode((self.gridsize * self.cellsize, self.gridsize * self.cellsize))
        pygame.display.set_caption("Conway's Game of Life")

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
                dead = len(count_list[0])
                if dead == 1:
                    self.alive = 0
                alive = len(count_list)
                if alive == 2:
                    self.alive = int(count_list[1][1])
                else:
                    print("Could not count number of alive cells?")
                    self.alive = -1
            except ValueError:
                print("Could not count number of alive cells?")
                self.alive = -1

            self.surface.fill(colour_grid)


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
        self.pattern = pattern.strip(".py")
        self.xoffset = xoffset
        self.yoffset = yoffset
        self.grid = np.array([])
        self.start_time = 0
        self.iteration = 0




def parsing():
    parser = argparse.ArgumentParser(description="Conway's Game of Life")
    parser.add_argument("-c", "--cellsize", type=int, help="Size of each cell (pixels)", default=8)
    parser.add_argument("-g", "--gridsize", type=int, help="Size of the simulation (cells)", default=100)
    parser.add_argument("-d", "--delay", type=int, help="Animation delay between each generation", default=0)
    parser.add_argument("-p", "--pattern", type=str, help="Pattern to use", default="glider.py")
    parser.add_argument("-x", "--xoffset", type=int, help="Pattern offset on x-axis", default=0)
    parser.add_argument("-y", "--yoffset", type=int, help="Pattern offset on y-axis", default=0)

    args = parser.parse_args()

    module = importlib.import_module(args.pattern.strip(".py"))
    print(module.description)

if __name__ == '__main__':
    parsing()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

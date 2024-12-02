# Conway's Game of Life
# A (slow) Python 3.12 implementation of John Horton Conway's concept of cellular automata

## // Imports \\ ##
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import numpy as np
import timeit
import math
import argparse

class Simulation:
    def __init__(self):
        print("Hello World!")

def parsing():
    parser = argparse.ArgumentParser(description="Conway's Game of Life")
    parser.add_argument("-c", "--cellsize", type=int, help="Size of each cell (pixels)", default=8)
    parser.add_argument("-g", "--gridsize", type=int, help="Size of the simulation (cells)", default=100)
    parser.add_argument("-d", "--delay", type=int, help="Animation delay between each generation", default=0)
    parser.add_argument("-p", "--pattern", type=str, help="Pattern to use", default="random.py")
    parser.add_argument("-x", "--xoffset", type=int, help="Pattern offset on x-axis", default=0)
    parser.add_argument("-y", "--yoffset", type=int, help="Pattern offset on y-axis", default=0)

    args = parser.parse_args()

if __name__ == '__main__':
    parsing()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

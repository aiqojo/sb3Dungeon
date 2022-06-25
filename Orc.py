import pygame
import Constants


class Orc:
    def __init__(self, x=0, y=0, size=Constants.CELL_SIZE, color=Constants.ORC_COLOR):
        self.x = x
        self.y = y

        self.previous_x = x
        self.previous_y = y
        self.previous_cells = {}

        self.size = size
        self.color = color

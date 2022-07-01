import pygame
import Constants


class Cell:
    def __init__(
        self,
        x,
        y,
        size=Constants.CELL_SIZE,
        terrain="empty",
        color=Constants.EMPTY,
        screen=None,
    ):
        self.screen = screen
        self.x = x
        self.y = y
        self.size = size

        self.terrain = terrain
        self.brownian_path = False
        self.color = color

        self.creature = None

    def draw(self):
        if self.creature == None:
            pygame.draw.rect(
                self.screen,
                self.color,
                (self.x * self.size, self.y * self.size, self.size, self.size),
            )
        else:
            self.creature.draw(self.screen)

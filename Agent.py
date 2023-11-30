import pygame
import Constants
import random


class Agent:
    def __init__(self, x=0, y=0, size=Constants.CELL_SIZE, color=Constants.AGENT):
        self.x = x
        self.y = y
        self.previous_x = x
        self.previous_y = y
        self.dist = 9999999
        self.previous_cells = {}

        self.size = size
        self.color = color

        self.alive = True
        self.health = 100

        self.score = 0

    def draw(self, screen):
        if self.alive:
            if self.previous_x == self.x and self.previous_y == self.y:
                return
            else:
                pygame.draw.rect(
                    screen,
                    self.color,
                    (
                        self.x * Constants.CELL_SIZE,
                        self.y * Constants.CELL_SIZE,
                        self.size,
                        self.size,
                    ),
                )

    def update_previous_cells(self):
        if self.previous_x == -1 and self.previous_y == -1:
            pass
        else:
            if (self.x, self.y) not in self.previous_cells:
                self.previous_cells[(self.x, self.y)] = 1
            else:
                self.previous_cells[(self.x, self.y)] += 1

    def get_cell_history(self):
        for cell in self.previous_cells:
            if self.previous_cells[cell] >= 1:
                pass
                #print(cell, self.previous_cells[cell])

    def move(self, direction):
        self.previous_x = self.x
        self.previous_y = self.y

        # Keep agent in bounds
        # Up
        if direction == 0:
            if self.y - 1 >= 0:
                self.y -= 1
        # Left
        elif direction == 1:
            if self.x - 1 >= 0:
                self.x -= 1
        # Down
        elif direction == 2:
            if self.y + 1 < Constants.CELL_HEIGHT:
                self.y += 1
        # Right
        elif direction == 3:
            if self.x + 1 < Constants.CELL_WIDTH:
                self.x += 1

        return (self.x, self.y)

    def revert_move(self):
        if (self.x, self.y) in self.previous_cells:
            self.previous_cells[(self.x, self.y)] -= 1
        self.x = self.previous_x
        self.y = self.previous_y

    def get_type(self):
        return "agent"
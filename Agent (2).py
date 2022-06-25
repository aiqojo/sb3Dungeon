import pygame
import constants
import random


class Agent:
    def __init__(self, board, id):

        self.board = board
        self.id = id

        # pygame.sprite.Sprite.__init__(self)
        self.initialize_agent_image()

        self.x = 0
        self.y = 0
        self.previous_x = 0
        self.previous_y = 0
        self.alive = True
        self.score = 0

        # STATISTICS
        self.health = 100
        self.strength = random.randint(1, 20)

        # Dictionary that stores the previous cells of the agent as well as how many times it has been in that cell
        self.previous_cells = {}

    def initialize_agent_image(self):
        pygame.sprite.Sprite.__init__(self)
        # Specific agent image
        self.agent_specific_image = pygame.Surface(
            (constants.CELL_SIZE - 5, constants.CELL_SIZE - 5)
        )
        self.color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )
        self.agent_specific_image.fill(self.color)

        # Universal agent image
        self.universal_agent = pygame.Surface(
            (constants.CELL_SIZE, constants.CELL_SIZE)
        )
        self.universal_agent_color = constants.AGENT_COLOR
        self.universal_agent.fill(self.universal_agent_color)

    # Draws a cell to fill the agent's previous position and draws the agent's current position
    def draw(self):
        if self.previous_x == self.x and self.previous_y == self.y:
            return
        else:
            if self.alive:
                # Drawing the previous cell
                prev_cell = self.board.cells[self.previous_x // constants.CELL_SIZE][
                    self.previous_y // constants.CELL_SIZE
                ]
                prev_cell.draw(self.board.screen)

                # Creates a border square to help show that this cell is occupied by an agent
                self.board.screen.blit(self.universal_agent, (self.x, self.y))
                # Then draws individual agent's color
                self.board.screen.blit(
                    self.agent_specific_image, (self.x + 3, self.y + 3)
                )

    # Returns the amount of times the agent has been in the cell
    def get_cell_history(self, cell):
        if (
            cell.x // constants.CELL_SIZE,
            cell.y // constants.CELL_SIZE,
        ) in self.previous_cells:
            print("CELL:", cell.x // constants.CELL_SIZE, cell.y // constants.CELL_SIZE)
            print("PREVIOUS CELLS:", self.previous_cells)
            # Only returns if agent has been in cell more than once, because the value will be one when the agent has moved into the cell for the first time
            if (
                self.previous_cells.get(
                    (cell.x // constants.CELL_SIZE, cell.y // constants.CELL_SIZE)
                )
                > 1
            ):
                return self.previous_cells.get(
                    (cell.x // constants.CELL_SIZE, cell.y // constants.CELL_SIZE)
                )
        else:
            print(
                "CELL ELSE:",
                cell.x // constants.CELL_SIZE,
                cell.y // constants.CELL_SIZE,
            )
            print("RETUNRNING 0")
            return 0

    def update_previous_cells(self):
        if (
            self.x // constants.CELL_SIZE,
            self.y // constants.CELL_SIZE,
        ) not in self.previous_cells:
            self.previous_cells[
                (self.x // constants.CELL_SIZE, self.y // constants.CELL_SIZE)
            ] = 1
        else:
            self.previous_cells[
                (self.x // constants.CELL_SIZE, self.y // constants.CELL_SIZE)
            ] += 1

    # Moves the agent in the given direction and keeps in bounds
    def move(self, x, y):
        # print("AGENT X AND Y: ", self.x // constants.CELL_SIZE, self.y // constants.CELL_SIZE)
        # print("MOVE:", x // constants.CELL_SIZE, y // constants.CELL_SIZE)
        # print("CELL X AND Y:", self.x // constants.CELL_SIZE, self.y // constants.CELL_SIZE)
        # print("AGENT:", self.board.cells[self.x // constants.CELL_SIZE][self.y // constants.CELL_SIZE].agent)

        # Adds current cell to previous cells
        self.update_previous_cells()

        if self.alive:
            self.board.cells[self.x // constants.CELL_SIZE][
                self.y // constants.CELL_SIZE
            ].agent.remove(self)
            # Changing coordinates
            self.previous_x = self.x
            self.previous_y = self.y
            x *= constants.CELL_SIZE
            y *= constants.CELL_SIZE

            # Moves the agents x position but keeps it in bounds
            if self.x + x < 0:
                self.x = 0
            elif self.x + x > constants.WINDOW_WIDTH - constants.CELL_SIZE:
                self.x = constants.WINDOW_WIDTH - constants.CELL_SIZE
            else:
                self.x += x

            # Moves the agents y position but keeps it in bounds
            if self.y + y < 0:
                self.y = 0
            elif self.y + y > constants.WINDOW_HEIGHT - constants.CELL_SIZE:
                self.y = constants.WINDOW_HEIGHT - constants.CELL_SIZE
            else:
                self.y += y

            # Adds agent to next cell
            self.board.cells[self.x // constants.CELL_SIZE][
                self.y // constants.CELL_SIZE
            ].agent.append(self)

            # Checks if move is valid
            other_cell = self.board.cells[self.x // constants.CELL_SIZE][
                self.y // constants.CELL_SIZE
            ]
            # Collision checks
            # self.check_collision(other_cell)
            # Have to re-enter self.x and self.y because the agent could've been moved to another cell, and not into other_cell
            self.terrain_check(
                self.board.cells[self.x // constants.CELL_SIZE][
                    self.y // constants.CELL_SIZE
                ]
            )

            # Draws the agent
            self.draw()
            self.board.draw_grid()

    # Method checks if the agent is in the same cell as another agent

    def check_collision(self, cell):
        if cell.agent:
            for other_agent in cell.agent:
                if other_agent != self:
                    # If collision remove agent at its current cell
                    if self.health > 0:
                        self.board.cells[self.x // constants.CELL_SIZE][
                            self.y // constants.CELL_SIZE
                        ].agent.remove(self)
                    # Move it back to its previous cell
                    self.x = self.previous_x
                    self.y = self.previous_y
                    # Add it back to the previous cell
                    self.board.cells[self.x // constants.CELL_SIZE][
                        self.y // constants.CELL_SIZE
                    ].agent.append(self)

    # Checks the current terrain and changes the agent's health accordingly the calls check_collision
    def terrain_check(self, cell):
        if cell.get_terrain() == "lava":
            self.change_health(-constants.LAVA_DAMAGE)
            # score -= 50
            # print("DAMAGE TAKEN AT:", self.x // constants.CELL_SIZE, self.y // constants.CELL_SIZE)
            # print("HEALTH: ", self.health)
            if self.health <= 0:
                self.die()
                # print("DEAD AT:" + str(self.x // constants.CELL_SIZE) + "," + str(self.y // constants.CELL_SIZE))
        # Checks if the agent is in the same cell as another agent

    # Kills the agent
    def die(self):
        # Gets cell
        curr_cell = self.board.cells[self.x // constants.CELL_SIZE][
            self.y // constants.CELL_SIZE
        ]
        # Draws red square to show that the agent is dead
        curr_cell.draw(self.board.screen)

        curr_cell.draw(self.board.screen)
        # Removes the agent from the cell
        curr_cell.agent.remove(self)

        # Removes the agent from the board
        prev_cell = self.board.cells[self.previous_x // constants.CELL_SIZE][
            self.previous_y // constants.CELL_SIZE
        ]
        prev_cell.draw(self.board.screen)

        if self in prev_cell.agent:
            prev_cell.agent.remove(self)

        self.alive = False

        # Removes from board list
        self.board.alive_agents -= 1

    # This method returns a list of all of the adajcent cells terrain
    def get_adjacent_terrain(self):
        # Rock is 0, lava is 1, wood is 2, not exist/wall = 3
        dir = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        adjacent_terrain = []
        for x, y in dir:
            try:
                adjacent_terrain.append(
                    self.board.cells[(self.x // constants.CELL_SIZE) + x][
                        (self.y // constants.CELL_SIZE) + y
                    ].get_terrain()
                )
            except:
                adjacent_terrain.append("wall")

        adj_arr = []
        for cell in adjacent_terrain:
            if cell == "rock" or "wood":
                adj_arr.append(0)
            elif cell == "lava":
                adj_arr.append(1)
            else:
                adj_arr.append(2)

        return adj_arr

    # Checks if the agent has reached the exit
    def reached_exit(self):
        if (
            "exit"
            in self.board.cells[self.x // constants.CELL_SIZE][
                self.y // constants.CELL_SIZE
            ].get_terrain()
        ):
            self.die()
            # print("Reached exit!")
            return True
        else:
            return False

    def set_stats(self):
        self.health = 100
        self.strength = random.randint(1, 20)

    def change_health(self, health):
        self.health += health
        if (self.health / 100) < 1:
            for i in self.color:
                i *= self.health / 100

    def random_move(self):
        self.move(random.randint(-1, 1), random.randint(-1, 1))

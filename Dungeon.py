import time
import numpy as np
import Constants
import Cell
import pygame
import random
import Goblin


class Dungeon:
    def __init__(self, agent, screen):
        self.done = False
        self.agent = agent
        # Create the np array used for the cells of the dungeon
        self.cells = np.empty(
            (Constants.CELL_WIDTH, Constants.CELL_HEIGHT),
            dtype=Cell.Cell,
        )
        # Initialize pygame to actually use it
        pygame.init()
        # Create screen/window
        self.screen = screen
        self.create_window()

        # Get cell count
        self.cell_count = Constants.CELL_WIDTH * Constants.CELL_HEIGHT

        # Find empty spawn cells, spawn the agent and create the exit
        self.empty_spawn_cells = self.get_empty_spawn_cells()
        self.agent_spawn = random.choice(self.empty_spawn_cells)
        self.goblins = []

    def get_state(self):
        grid = self.create_numbered_grid()
        # print(grid)
        # returning flattened array of the Constants.VISION_RANGE x Constants.VISION_RANGE grid around the agent,
        # x, y, and distance to exit
        # return grid[
        #     self.agent.x - Constants.VISION_RANGE : self.agent.x + Constants.VISION_RANGE + 1,
        #     self.agent.y - Constants.VISION_RANGE : self.agent.y + Constants.VISION_RANGE + 1,
        # ].flatten()
        cur_x = self.agent.x
        cur_y = self.agent.y
        distance_to_exit = abs(self.exit_coords[0] - cur_x) + abs(
            self.exit_coords[1] - cur_y
        )
        return_grid = np.empty(
            (Constants.VISION_RANGE, Constants.VISION_RANGE),
            dtype=np.float32,
        )

        for i in range(Constants.VISION_RANGE):
            for j in range(Constants.VISION_RANGE):
                return_grid[i][j] = grid[cur_x - Constants.VISION_RANGE + i][
                    cur_y - Constants.VISION_RANGE + j
                ]

        return_grid = return_grid.flatten()
        return_grid = np.append(return_grid, cur_x)
        return_grid = np.append(return_grid, cur_y)
        return_grid = np.append(return_grid, distance_to_exit)
        return return_grid


    def get_reward(self):
        # If the agent is at the exit it gets 100 points
        if self.cells[self.agent.x][self.agent.y].terrain == "exit":
            return 500
        elif self.agent.alive == False:
            return -500
        else:
            return 25 / (
                1
                + abs(self.agent.x - self.exit_coords[0])
                + abs(self.agent.y - self.exit_coords[1])
            )

    def build_goblins(self):
        for i in range(Constants.GOBLIN_COUNT):
            while True:
                cell = np.random.choice(self.cells.flatten())
                if (
                    cell.terrain == "empty"
                    and cell.creature is None
                    and cell.brownian_path is True
                ):
                    self.goblins.append(Goblin.Goblin(cell.x, cell.y))
                    self.cells[cell.x][cell.y].creature = self.goblins[i]
                    # print("Goblin spawned at: " + str(cell.x) + ", " + str(cell.y))
                    self.cells[cell.x][cell.y].draw()
                    if (cell.x, cell.y) != self.put_in_bounds(cell.x, cell.y):
                        # print("Goblin spawned out of bounds")
                        self.goblins.pop()
                    else:
                        break

    def update(self):
        for goblin in self.goblins:
            # Checks if goblin and agent are in the same cell
            if goblin.x == self.agent.x and goblin.y == self.agent.y:
                # print("Goblin killed the agent")
                self.agent.alive = False
                self.done = True
                return "lose"

            # Only moves goblin if the agent is not in the safe zone or exit zone
            if (self.agent is not None) and (
                self.agent.x > int(len(self.cells) * Constants.SAFE_ZONE_RATIO)
                and self.agent.x < int(len(self.cells) * Constants.END_ZONE_RATIO)
            ):
                goblin.move(
                    self.cells, self.create_numbered_grid(), self.agent.x, self.agent.y
                )

                if self.is_collision(goblin):
                    goblin.revert_move()
                else:
                    if goblin.previous_x != goblin.x or goblin.previous_y != goblin.y:
                        # print(
                        #     "Goblin moved",
                        #     goblin.x,
                        #     goblin.y,
                        #     "from",
                        #     goblin.previous_x,
                        #     goblin.previous_y,
                        # )
                        self.cells[goblin.previous_x][goblin.previous_y].creature = None
                        self.cells[goblin.x][goblin.y].creature = goblin
                        self.cells[goblin.previous_x][goblin.previous_y].draw()
                        self.cells[goblin.x][goblin.y].draw()
                        self.draw_grid()

                    # print(goblin.x, goblin.y, self.agent.x, self.agent.y)

                    if goblin.x == self.agent.x and goblin.y == self.agent.y:
                        # print("Goblin killed the agent")
                        self.agent.alive = False
                        self.done = True
                        return "lose"

    def create_numbered_grid(self, gym_return=False):
        return_grid = np.empty(
            (Constants.CELL_WIDTH, Constants.CELL_HEIGHT),
            dtype=np.float32,
        )
        for i in range(Constants.CELL_WIDTH):
            for j in range(Constants.CELL_HEIGHT):
                if self.cells[i][j].terrain == "empty":
                    return_grid[i][j] = 0
                elif self.cells[i][j].terrain == "rock":
                    return_grid[i][j] = 1
                elif self.cells[i][j].terrain == "exit":
                    return_grid[i][j] = 2
                if self.cells[i][j].creature is not None:
                    if self.cells[i][j].creature.get_type() == "agent":
                        return_grid[i][j] = 3
                    elif self.cells[i][j].creature.get_type() == "goblin":
                        return_grid[i][j] = 4

        return return_grid

    def move_goblins(self):
        dungeon_cells = self.create_numbered_grid()
        for goblin in self.goblins:
            goblin.move(self.cells, dungeon_cells, self.agent.x, self.agent.y)
            goblin.x, goblin.y = self.put_in_bounds(goblin.x, goblin.y)
            if self.is_collision(goblin):
                goblin.revert_move()
            self.cells[goblin.previous_x][goblin.previous_y].creature = None
            self.cells[goblin.x][goblin.y].creature = goblin
            self.cells[goblin.previous_x][goblin.previous_y].draw()
            self.cells[goblin.x][goblin.y].draw()
            self.draw_grid()

    def create_window(self):
        for i in range(Constants.WINDOW_WIDTH // Constants.CELL_SIZE):
            for j in range(Constants.WINDOW_HEIGHT // Constants.CELL_SIZE):
                self.cells[i][j] = Cell.Cell(i, j, screen=self.screen)
                self.cells[i][j].draw()
        self.draw_grid()

    def create_exit(self):
        exit_cell_x = random.randint(
            int((len(self.cells)) * Constants.END_ZONE_RATIO), len(self.cells) - 1
        )
        exit_cell_y = random.randint(0, len(self.cells[0]) - 1)
        self.cells[exit_cell_x][exit_cell_y].terrain = "exit"
        self.cells[exit_cell_x][exit_cell_y].color = Constants.EXIT_COLOR
        self.cells[exit_cell_x][exit_cell_y].draw()
        self.draw_grid()
        self.exit_coords = (exit_cell_x, exit_cell_y)

    def get_empty_spawn_cells(self):
        empty_spawn_cells = []
        for i in range(0, int(len(self.cells) * Constants.SAFE_ZONE_RATIO)):
            for j in range(0, len(self.cells[0])):
                if self.cells[i][j].terrain == "empty":
                    empty_spawn_cells.append(self.cells[i][j])
        return empty_spawn_cells

    def add_agent(self, agent):
        agent.x = self.agent_spawn.x
        agent.y = self.agent_spawn.y
        self.agent_spawn.creature = agent
        self.cells[agent.x][agent.y].draw()
        self.draw_grid()

    def move_agent(self, agent, direction):
        agent.move(direction)
        agent.x, agent.y = self.put_in_bounds(agent.x, agent.y)
        if self.is_collision(agent):
            agent.revert_move()
        self.cells[agent.previous_x][agent.previous_y].creature = None
        self.cells[agent.x][agent.y].creature = agent
        self.cells[agent.previous_x][agent.previous_y].draw()
        self.cells[agent.x][agent.y].draw()
        self.draw_grid()

        # update agent distance frm exit
        agent.dist = abs(self.exit_coords[0] - agent.x) + abs(
            self.exit_coords[1] - agent.y
        )


        if self.check_for_exit(agent):
            self.done = True
            return "win"
        else:
            if (agent.x, agent.y) != (agent.previous_x, agent.previous_y):
                return "continue"
            else:
                return "no_move"

    def check_for_exit(self, agent):
        if self.cells[agent.x][agent.y].terrain == "exit":
            # print("You won!")
            return True
        else:
            return False

    def is_collision(self, creature):
        if (
            creature.x < 0
            or creature.x >= len(self.cells)
            or creature.y < 0
            or creature.y >= len(self.cells[0])
        ):
            return True
        elif self.cells[creature.x][creature.y].terrain == "rock":
            return True
        else:
            return False

    def put_in_bounds(self, x, y, exclude_zone=False):
        if exclude_zone == False:
            if x < 0:
                x = 0
            elif x >= len(self.cells):
                x = len(self.cells) - 1
            if y < 0:
                y = 0
            elif y >= len(self.cells[0]):
                y = len(self.cells[0]) - 1
            return x, y
        else:
            if x < int(len(self.cells) * Constants.SAFE_ZONE_RATIO):
                x = int(len(self.cells) * Constants.SAFE_ZONE_RATIO)
            elif x > int(len(self.cells) * Constants.END_ZONE_RATIO):
                x = int(len(self.cells) * Constants.END_ZONE_RATIO) - 1
            if y < 0:
                y = 0
            elif y >= len(self.cells[0]):
                y = len(self.cells[0]) - 1
            return x, y

    # Creates clusters of rocks in the dungeon that make the agent have to avoid
    # Doesn't put rocks in safe or end zone, or any tile that is apart of the
    # brownian paths
    def create_rocks(self):
        # print("creating rocks")
        rock_spawns = []
        i = 0
        while i < Constants.CLUSTER_COUNT:
            rock_x = random.randint(
                int((len(self.cells)) * Constants.SAFE_ZONE_RATIO),
                int((len(self.cells)) * Constants.END_ZONE_RATIO) - 1,
            )
            rock_y = random.randint(0, len(self.cells[0]) - 1)
            if self.cells[rock_x][rock_y].brownian_path == False:
                rock_spawns.append((rock_x, rock_y))
                i += 1

        for rock_x, rock_y in rock_spawns:
            self.put_in_bounds(rock_x, rock_y, exclude_zone=True)
            cluster_size = int(
                np.random.normal(Constants.CLUSTER_MEAN, Constants.CLUSTER_SD)
            )
            if cluster_size < 1:
                cluster_size = 1
            if self.cells[rock_x][rock_y].terrain == "empty":
                self.build_rock_cluster(rock_x, rock_y, cluster_size)

    def build_rock_cluster(self, x, y, cluster_size):
        cur = 0
        # Creates a set for the rocks in this current cluster and sets the origin as a rock
        rock_cells = set()
        x, y = self.put_in_bounds(x, y, exclude_zone=True)
        rock_cells.add((x, y))

        # Creates set for boundaries of the cluster
        boundaries = set()
        temp_boundaries = set()
        # Adds boundaries of origin
        temp_boundaries = self.get_cell_boundaries(x, y)
        boundaries = boundaries.union(temp_boundaries)

        # Adds boundaries of all other rocks in the cluster
        while len(rock_cells) < cluster_size and cur < cluster_size:
            # If there are no more rocks to add, break out of the loop
            if len(boundaries) == 0:
                break
            # Randomly select a boundary cell
            temp_rock = random.choice(tuple(boundaries))
            if (
                # Check if it is not in rock_cells and it isn't a rock to avoid wasting time
                temp_rock not in rock_cells
                and self.cells[temp_rock[0]][temp_rock[1]].terrain != "rock"
            ):
                # Add the rock to the set
                rock_cells.add(temp_rock)
                boundaries.remove(temp_rock)
                boundaries = boundaries.union(
                    self.get_cell_boundaries(temp_rock[0], temp_rock[1])
                )
            # Use cur as a counter to keep track of how many rocks have been added
            # and cut the loop off if there have been enough failed attempts
            cur += 1

        # Actually set the cells to rocks
        for rock_x, rock_y in rock_cells:
            self.put_in_bounds(rock_x, rock_y, exclude_zone=True)
            self.cells[rock_x][rock_y].terrain = "rock"
            self.cells[rock_x][rock_y].color = Constants.ROCK_COLOR
            self.cells[rock_x][rock_y].draw()

        self.draw_grid()

    def get_cell_boundaries(self, x, y):
        cell_boundaries = set()
        dx = [-1, 0, 1, 0]
        dy = [0, 1, 0, -1]
        for x, y in [(x + dx[i], y + dy[i]) for i in range(4)]:
            if (
                x >= int((len(self.cells)) * Constants.SAFE_ZONE_RATIO)
                and x < int((len(self.cells)) * Constants.END_ZONE_RATIO)
                and y >= 0
                and y < len(self.cells[0])
                and self.cells[x][y].brownian_path == False
            ):
                x, y = self.put_in_bounds(x, y, exclude_zone=True)
                cell_boundaries.add((x, y))
        return cell_boundaries

    def create_brownian_path(self):
        # How far the path will move up or down if value further away than min_border or max_border
        extreme_distance = 2

        # Sets the percentages the path will have to go up or down
        # If the value is between these two, it will go straight
        down_border = -0.35
        up_border = 0.35
        # If the value is between this and down_border, it will go down 1
        # If the value is below down_border, it will go down by extreme_distance
        min_border = -1.25
        # If the value is between this and up_border, it will go up 1
        # If the value is above up_border, it will go up by extreme_distance
        max_border = 1.25

        # These values are used to change the values above if the path spawns further away from the center
        single_multiply_ratio = 0.35
        double_multiply_ratio = single_multiply_ratio * 2

        # Get the width of the dungeon and spawn points for the paths
        dungeon_cell_width = len(self.cells)
        curr_x = int(Constants.SAFE_ZONE_RATIO * len(self.cells))
        curr_y = self.agent_spawn.y
        brown_coords = []

        brown_coords.append((curr_x, curr_y))

        for path in range(Constants.BROWNIAN_PATH_COUNT):
            if path > 0:
                curr_y = int(curr_y * np.random.normal(0, 1))
                curr_x, curr_y = self.put_in_bounds(curr_x, curr_y)

            # If the spawn is in the top 20% of the dungeon give higher chance to move down
            if curr_y > int(len(self.cells[0]) * 0.25):
                down_border = down_border * single_multiply_ratio
                max_border = max_border * double_multiply_ratio
            # If the spawn is in the bottom 20% of the dungeon give higher chance to move up
            if curr_y < int(len(self.cells[0]) * 0.75):
                up_border = up_border * single_multiply_ratio
                min_border = min_border * double_multiply_ratio

            # time.sleep(0.4)
            # Create list of normally distributed random numbers
            brown_list = np.random.normal(0, 1, dungeon_cell_width)
            end_x = int(Constants.END_ZONE_RATIO * len(self.cells))
            for i in range(int(Constants.SAFE_ZONE_RATIO * len(self.cells)), end_x - 1):
                # If between -0.5 and 0.5, then move forward one
                if down_border < brown_list[i] < up_border:
                    brown_coords.append((curr_x, curr_y))
                    curr_x += 1
                    brown_coords.append((curr_x, curr_y))
                    self.draw_grid()

                # If below -1.25, then move up two and forward one
                elif brown_list[i] < min_border:
                    for i in range(extreme_distance):
                        curr_y += 1
                        curr_x, curr_y = self.put_in_bounds(curr_x, curr_y)
                        brown_coords.append((curr_x, curr_y))
                    curr_x += 1
                    brown_coords.append((curr_x, curr_y))

                # If above 1.25, then move down two and forward one
                elif brown_list[i] > max_border:
                    for i in range(extreme_distance):
                        curr_y -= 1
                        curr_x, curr_y = self.put_in_bounds(curr_x, curr_y)
                        brown_coords.append((curr_x, curr_y))
                    curr_x += 1
                    brown_coords.append((curr_x, curr_y))

                # If between -1.25 and -.5, then move down one and forward one
                elif min_border < brown_list[i] < up_border:
                    curr_y -= 1
                    curr_x, curr_y = self.put_in_bounds(curr_x, curr_y)
                    brown_coords.append((curr_x, curr_y))
                    curr_x += 1
                    brown_coords.append((curr_x, curr_y))

                # If between 0.5 and 1.25, then move up one and forward one
                elif up_border < brown_list[i] < max_border:
                    curr_y += 1
                    curr_x, curr_y = self.put_in_bounds(curr_x, curr_y)
                    brown_coords.append((curr_x, curr_y))
                    curr_x += 1
                    brown_coords.append((curr_x, curr_y))

            curr_x = int(Constants.SAFE_ZONE_RATIO * len(self.cells))
            curr_y = self.agent_spawn.y

            for brown in brown_coords:
                for i in range(Constants.BROWNIAN_PATH_THICKNESS):
                    brown_x, brown_y = self.put_in_bounds(brown[0], brown[1] + i)
                    self.make_brown(brown_x, brown_y)

            brown_list = []

        self.draw_grid()

    def make_brown(self, x, y):
        # print("Making brown at: " + str(x) + ", " + str(y))
        self.cells[x][y].brownian_path = True
        self.cells[x][y].color = Constants.BROWN
        self.cells[x][y].draw()

    def draw_grid(self):
        return
        safe_zone = False
        exit_zone = False
        for i in range(0, Constants.WINDOW_WIDTH, Constants.CELL_SIZE):
            # Drawing a blue line for the safe zone to show how far it goes out
            if safe_zone == False and i // Constants.CELL_SIZE >= int(
                len(self.cells) * Constants.SAFE_ZONE_RATIO
            ):
                safe_zone = True
                pygame.draw.line(
                    self.screen, Constants.BLUE, (i, 0), (i, Constants.WINDOW_HEIGHT)
                )
            # Drawing a red line for the exit zone to show how far it goes out
            elif exit_zone == False and i // Constants.CELL_SIZE >= int(
                len(self.cells) * Constants.END_ZONE_RATIO
            ):
                exit_zone = True
                pygame.draw.line(
                    self.screen, Constants.RED, (i, 0), (i, Constants.WINDOW_HEIGHT)
                )
            else:
                pygame.draw.line(
                    self.screen, Constants.BLACK, (i, 0), (i, Constants.WINDOW_HEIGHT)
                )
        for j in range(0, Constants.WINDOW_HEIGHT, Constants.CELL_SIZE):
            pygame.draw.line(
                self.screen, Constants.BLACK, (0, j), (Constants.WINDOW_WIDTH, j)
            )

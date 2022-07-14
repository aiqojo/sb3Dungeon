import pygame
import Constants
import time
import random


class Goblin:
    def __init__(
        self, x=0, y=0, size=Constants.CELL_SIZE, color=Constants.GOBLIN_COLOR
    ):
        self.x = x
        self.y = y

        self.previous_x = 0
        self.previous_y = 0
        self.previous_cells = {}

        self.size = size
        self.color = color
        self.cur_a_star_path = []

    def draw(self, screen):
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

    def a_star(self, dungeon, dungeon_cells, agent_x, agent_y):

        # This resets the color of all of the cells that were in the previous path
        if len(self.cur_a_star_path) > 0:
            for cell in self.cur_a_star_path:
                if dungeon[cell[0]][cell[1]].brownian_path == False:
                    dungeon[cell[0]][cell[1]].color = Constants.EMPTY
                    dungeon[cell[0]][cell[1]].draw()
                else:
                    dungeon[cell[0]][cell[1]].color = Constants.BROWN
                    dungeon[cell[0]][cell[1]].draw()

        # Checks if the agent and goblin are in the same cell
        if agent_x == self.x and agent_y == self.y:
            return []

        # Initialize
        open_set = set()
        closed_set = set()
        came_from = {}
        g_score = {}
        f_score = {}

        # Add start node to open set
        open_set.add((self.x, self.y))
        g_score[(self.x, self.y)] = 0
        f_score[(self.x, self.y)] = self.get_manhattan_distance(agent_x, agent_y)

        #print("F score", f_score[(self.x, self.y)])

        # If the agent is out of range just return
        if f_score[(self.x, self.y)] >= Constants.GOBLIN_RANGE:
            return []

        # This is while the the agent is within range of the goblin
        # Loop until open set is empty
        while len(open_set) > 0:
            # Get node with lowest f_score
            current = min(open_set, key=lambda x: f_score[x])

            # Check if current node is goal
            if current == (agent_x, agent_y):
                break

            # Remove current node from open set
            open_set.remove(current)
            closed_set.add(current)

            # Loop through neighbors
            for neighbor in self.get_cell_boundaries(
                dungeon_cells, current[0], current[1]
            ):
                # Check if neighbor is in closed set
                if neighbor in closed_set:
                    continue

                # Check if neighbor is in open set
                if neighbor not in open_set:
                    open_set.add(neighbor)
                # Check if neighbor is on the path
                if (neighbor[0], neighbor[1]) in came_from:
                    continue

                # Calculate tentative g score
                tentative_g_score = g_score[current] + 1

                # Check if tentative g score is better than current g score
                if tentative_g_score < g_score.get(neighbor, float("inf")):
                    # Update came from
                    came_from[neighbor] = current
                    # Update g score
                    g_score[neighbor] = tentative_g_score
                    # Update f score
                    f_score[neighbor] = tentative_g_score + self.get_manhattan_distance(
                        agent_x, agent_y
                    )

        # Get path
        path = []
        current = (agent_x, agent_y)
        while current in came_from:
            path.append(current)
            current = came_from[current]
        path.append(current)
        path.reverse()


        # Make the path red and draw it
        for cell in path[1:]:
            self.cur_a_star_path.append(cell)
            dungeon[cell[0]][cell[1]].color = Constants.RED
            dungeon[cell[0]][cell[1]].draw()

        # Return the closest tile so it knows where to move
        # path[0] is current tile so we want path[1]
        #print("path", path) 
        if len(path) > 1:
            return path[1]
        else:
            return []

    def get_manhattan_distance(self, agent_x, agent_y):
        return abs(self.x - agent_x) + abs(self.y - agent_y)

    def get_cell_boundaries(self, dungeon_cells, x, y):
        cell_boundaries = set()
        dx = [-1, 0, 1, 0]
        dy = [0, 1, 0, -1]
        for x, y in [(x + dx[i], y + dy[i]) for i in range(4)]:
            if (
                x >= int((len(dungeon_cells)) * Constants.SAFE_ZONE_RATIO)
                and x < int((len(dungeon_cells)) * Constants.END_ZONE_RATIO)
                and y >= 0
                and y < len(dungeon_cells[0])
                and 
                (dungeon_cells[x][y] != 1)
            ):
                x, y = self.put_in_bounds(dungeon_cells, x, y, exclude_zone=True)
                cell_boundaries.add((x, y))
        return cell_boundaries

    def put_in_bounds(self, dungeon_cells, x, y, exclude_zone=False):
        while(True):
            if exclude_zone == False:
                if x < 0:
                    x = 0
                elif x >= len(dungeon_cells):
                    x = len(dungeon_cells) - 1
                if y < 0:
                    y = 0
                elif y >= len(dungeon_cells[0]):
                    y = len(dungeon_cells[0]) - 1
                return x, y
            else:
                if x < int(len(dungeon_cells) * Constants.SAFE_ZONE_RATIO):
                    x = int(len(dungeon_cells) * Constants.SAFE_ZONE_RATIO)
                elif x > int(len(dungeon_cells) * Constants.END_ZONE_RATIO):
                    x = int(len(dungeon_cells) * Constants.END_ZONE_RATIO) - 1
                if y < 0:
                    y = 0
                elif y >= len(dungeon_cells[0]):
                    y = len(dungeon_cells[0]) - 1
            # Check if the cell is not a wall
            if dungeon_cells[x][y] != 1:
                # If not return, this is a location you can move to
                return x, y
            # If it is a wall, move to the next cell
            else:
                y += random.randint(-1, 1)

            return x, y

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

    def move(self, dungeon, dungeon_cells, agent_x, agent_y):
        self.previous_x = self.x
        self.previous_y = self.y

        cell = self.a_star(dungeon, dungeon_cells, agent_x, agent_y)

        direction = -1

        if len(cell) == 0:
            direction = random.randint(0, 3)
        else:
            #print(self.x, self.y, cell[0], cell[1])
            if cell[0] == self.x and cell[1] == self.y + 1:
                direction = 0
            elif cell[0] == self.x and cell[1] == self.y - 1:
                direction = 1
            elif cell[0] == self.x + 1 and cell[1] == self.y:
                direction = 2
            elif cell[0] == self.x - 1 and cell[1] == self.y:
                direction = 3
            elif cell[0] == self.x and cell[1] == self.y:
                return (self.x, self.y)

        # Keep agent in bounds
        # Up
        if direction == 0:
            #print("goblin up")
            self.y += 1
            self.update_previous_cells()
        elif direction == 1:
            #print("goblin down")
            self.y -= 1
            self.update_previous_cells()
        elif direction == 2:
            #print("goblin right")
            self.x += 1
            self.update_previous_cells()
        elif direction == 3:
            #print("goblin left")
            self.x -= 1
            self.update_previous_cells()

        self.x, self.y = self.put_in_bounds(dungeon_cells, self.x, self.y)

        return (self.x, self.y)

    def revert_move(self):
        #print("REVERIN GOBBY MOVE")
        if (self.x, self.y) in self.previous_cells:
            self.previous_cells[(self.x, self.y)] -= 1
        self.x = self.previous_x
        self.y = self.previous_y

    def get_type(self):
        return "goblin"
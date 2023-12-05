import numpy as np
import Constants
import gymnasium as gym
from gymnasium import spaces
import Cell
import pygame
import Agent
import Dungeon


class sb3DungeonEnv(gym.Env):
    metadata = {"render.modes": ["human"]}

    def __init__(self):
        self.passive_loss = 1
        self.frames = 0
        # THE MAX FRAMES SHOULD PROB BE CHANGED TO SOMETHING LIKE:
        # Constants.CELL_WIDTH * 4
        if Constants.WINDOW_WIDTH == 1280:
            # this is how it shold be from now on
            # self.max_frames = (Constants.CELL_WIDTH) * 8  # model <= 14
            self.max_frames = (Constants.CELL_WIDTH) * 16  # model 15
        else:
            # this stays cause legacy form older models
            self.max_frames = (Constants.CELL_HEIGHT * Constants.CELL_WIDTH) / 2

        pygame.init()
        self.screen = pygame.display.set_mode(
            (Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT)
        )

        self.reward = 0
        self.done = False

        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(
            low=0,
            high=255,
            # +1 for max location for backtracking
            # shape=(Constants.VISION_RANGE * Constants.VISION_RANGE + 5,),  # model 6
            shape=(Constants.VISION_RANGE * Constants.VISION_RANGE + 6,),
            dtype=np.float32,
        )
        self.agent = Agent.Agent()
        self.dungeon = Dungeon.Dungeon(self.agent, self.screen)
        self.dungeon.create_exit()
        self.dungeon.add_agent(self.agent)

        self.dungeon.create_brownian_path()
        self.dungeon.create_rocks()
        self.dungeon.build_goblins()
        self.dungeon.update()
        # pygame.display.flip()

    def step(self, action):
        self.reward = 0
        self.frames += 1
        if self.frames > self.max_frames:
            self.done = True

            # reward for how close the agent is to the exit
            # for models 4-9
            # self.reward += -100 * (self.agent.dist / Constants.CELL_WIDTH) + 1
            # for models 10+
            dist_reward = -200 * (self.agent.dist / Constants.CELL_WIDTH) + 1
            self.reward += dist_reward

            # reward for time spent in the dungeon
            time_reward = -100 * (self.frames / self.max_frames) + 1
            self.reward += time_reward

            # negative reward for the largest number of times the agent has been in the same cell
            # stuck_reward = -1 * (max(self.agent.previous_cells.values())) # for models < 13
            stuck_reward = (
                -200 * (max(self.agent.previous_cells.values()) / self.max_frames) + 1
            )  # for models 13+
            self.reward += stuck_reward

            # to keep it mostly positive
            # self.reward += 300  # for models 10-12
            self.reward += 500  # for models 13+

            # print(
            #     "\ndist reward: \t\t",
            #     "{:010.4f}".format(dist_reward),
            # )
            # print(
            #     "time reward: \t\t",
            #     "{:010.4f}".format(time_reward),
            # )
            # print(
            #     "previous cells reward: \t",
            #     "{:010.4f}".format(stuck_reward),
            # )
            # if self.reward >= 0:
            #     print("total reward: \t\t", " {:09.4f}".format(round(self.reward, 4)))
            # else:
            #     print(
            #         "total reward: \t\t",
            #         "{:010.4f}".format(round(self.reward, 4)),
            #     )

        # add the current x and y to the agent's previous cells
        if (self.agent.x, self.agent.y) not in self.agent.previous_cells:
            self.agent.previous_cells[(self.agent.x, self.agent.y)] = 1
        else:
            self.agent.previous_cells[(self.agent.x, self.agent.y)] += 1

        agent_status = self.dungeon.move_agent(self.agent, action)
        goblin_status = None
        if agent_status != "no_move":
            goblin_status = self.dungeon.update()
        if agent_status == "no_move":
            self.reward += 0
        if agent_status == "win":
            self.done = True
            win_reward = 1000
            self.reward += win_reward

            # below rewards for model 13+
            # reward for time spent in the dungeon
            time_reward = -100 * (self.frames / self.max_frames) + 1
            self.reward += time_reward

            # to keep it mostly positive
            self.reward += 100  # for models 13+

            # print(
            #     "\ntime reward: \t\t",
            #     "{:010.4f}".format(time_reward),
            # )
            # print(
            #     "previous cells reward: \t",
            #     "{:010.4f}".format(stuck_reward),
            # )
            # print(
            #     "win reward: \t\t",
            #     " {:09.4f}".format(win_reward),
            # )
            # if self.reward >= 0:
            #     print("total reward: \t\t", " {:09.4f}".format(round(self.reward, 4)))
            # else:
            #     print(
            #         "total reward: \t\t",
            #         "{:010.4f}".format(round(self.reward, 4)),
            #     )

        # if goblin_status == "lose":
        #     self.done = True

        return self.dungeon.get_state(), self.reward, self.done, {}, {}

    def reset(self, seed=None):
        self.done = False
        self.reward = 0
        self.passive_loss = 1
        self.frames = 0
        self.agent = Agent.Agent()
        self.dungeon = Dungeon.Dungeon(self.agent, self.screen)
        self.dungeon.create_exit()
        self.dungeon.add_agent(self.agent)

        self.dungeon.create_brownian_path()
        self.dungeon.create_rocks()
        self.dungeon.build_goblins()
        self.dungeon.update()
        # pygame.display.flip()
        return self.dungeon.get_state(), None

    def render(self, mode="human"):
        pygame.display.flip()

import numpy as np
import Constants
import gym
from gym import spaces
import Cell
import pygame
import Agent
import Dungeon


class sb3DungeonEnv(gym.Env):
    metadata = {"render.modes": ["human"]}
    reward = 0

    def __init__(self):
        pygame.init()

        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(
            low=0,
            high=255,
            shape=(Constants.CELL_WIDTH, Constants.CELL_HEIGHT),
            dtype=np.uint32,
        )
        self.agent, self.dungeon = self.reset()

    def step(self, action):
        agent_status = self.dungeon.move_agent(self.agent, action)
        if agent_status != "no_move":
            self.dungeon.update()
        self.reward += self.dungeon.get_reward()

        return self.dungeon.get_state(gym_return=True), self.reward, self.dungeon.done, {}

    def reset(self):
        agent = Agent.Agent()
        dungeon = Dungeon.Dungeon(agent)
        dungeon.create_exit()
        dungeon.add_agent(agent)

        dungeon.create_brownian_path()
        dungeon.create_rocks()
        dungeon.build_goblins()
        dungeon.update()
        pygame.display.flip()
        return agent, dungeon

    def render(self, mode="human"):
        pass

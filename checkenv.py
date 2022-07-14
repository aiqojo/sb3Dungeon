from sb3DungeonEnv import sb3DungeonEnv
import numpy as np
import time
import sys

# np.set_printoptions(threshold=sys.maxsize)
first = True
env = sb3DungeonEnv()
episodes = 50
# for i in range(10):
#     print(env.observation_space.sample())

delay = 0.01

for episode in range(episodes):
    if first:
        first = False
    else:
        print("resetting")
        observation = env.reset()
        delay = 0.01
    done = False
    while not done:
        time.sleep(delay)
        action = env.action_space.sample()
        env.render()
        observation, reward, done, info = env.step(action)
        print(np.fliplr(np.rot90(m=observation, k=3)))
        print(reward)
        print("DONE", done)
        print(info)
        print("\n")

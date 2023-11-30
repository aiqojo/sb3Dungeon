import gym
from stable_baselines3 import PPO, DQN
from sb3DungeonEnv import sb3DungeonEnv
import time
import numpy as np

logdir = "logs"


env = sb3DungeonEnv()
env.reset()

models_dir = "models/"
models_path = f"{models_dir}/50000.zip"

model = PPO.load(models_path, env = env)

reward_array = []

episodes = 100
for ep in range(episodes):
    obs = env.reset()
    done = False
    while not done:
        # time.sleep(.5)
        env.render()
        action, _ = model.predict(obs)
        obs, reward, done, info = env.step(action)
        #print(obs)
        # print(np.fliplr(np.rot90(m=obs, k=3)))
        print(reward)
    reward_array += [reward]

env.close()

print(reward_array)

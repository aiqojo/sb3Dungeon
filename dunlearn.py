import gymnasium as gym
from stable_baselines3 import PPO
import os
import time
from sb3DungeonEnv import sb3DungeonEnv

models_dir = f"models12-big"
logdir = f"logs12-big"

if not os.path.exists(models_dir):
    os.makedirs(models_dir)

if not os.path.exists(logdir):
    os.makedirs(logdir)

load = False
load_last = False
if load_last and load:
    # finding the largest model
    largest = 0
    for file in os.listdir(models_dir):
        filename = os.fsdecode(file)
        num = int(filename.split(".")[0])
        if num > largest:
            largest = num
    models_path = f"{models_dir}/{largest}.zip"
    print("Loading model: ", models_path)
elif load:
    models_path = f"{models_dir}/2075000.zip"
    print("Loading model: ", models_path)
# models_path = f"{models_dir}/3600000.zip"

# model = PPO.load(models_path, env = env)

TIMESTEPS = 250000

if not load:
    env = sb3DungeonEnv()
    env.reset()

    model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=logdir)

    for i in range(1, 1000000):
        obs, _ = env.reset()
        model.learn(
            total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name="PPO"
        )
        model.save(f"{models_dir}/{TIMESTEPS*i}")

else:
    env = sb3DungeonEnv()
    env.reset()
    model = PPO.load(models_path, env=env)

    for i in range(1, 1000000):
        obs, _ = env.reset()
        model.learn(
            total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name="PPO"
        )
        model.save(f"{models_dir}/{TIMESTEPS*i}")


env.close()

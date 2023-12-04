from stable_baselines3 import PPO, DQN
from sb3DungeonEnv import sb3DungeonEnv
import sys
import time
import os

logdir = "logs"


env = sb3DungeonEnv()
env.reset()

# models_dir = "models4/"
# models_dir = "models6-small_backtrack/"
# models_dir = "models11-big/"
# models_dir = "models12-big/"
# models_dir = "models13-big/"
models_dir = "models15-big/"
load_last = True
models_path = ""

if load_last:
    # finding the largest model
    largest = 0
    for file in os.listdir(models_dir):
        filename = os.fsdecode(file)
        num = int(filename.split(".")[0])
        if num > largest:
            largest = num
    models_path = f"{models_dir}/{largest}.zip"
    print("Loading model: ", models_path)
else:
    models_path = f"{models_dir}/2075000.zip"
    print("Loading model: ", models_path)

model = PPO.load(models_path, env=env)

reward_array = []

episodes = 100
for ep in range(episodes):
    obs, _ = env.reset()
    done = False
    while not done:
        time.sleep(0.0005)
        env.render()
        action, _ = model.predict(obs)
        obs, reward, done, _, info = env.step(action)
        # print(np.fliplr(np.rot90(m=obs, k=3)))
        if reward != 0:
            print(reward)
    reward_array += [reward]

env.close()

print(reward_array)
print(sum(reward_array) / len(reward_array))
print("Total wins:", len([i for i in reward_array if i >= 1000]))

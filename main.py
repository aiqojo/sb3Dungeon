import Dungeon
import Agent
import Constants
import pygame
import time


def main():
    while True:
        pygame.init()
        agent, dungeon = reset()
        print(
            "Rock count:",
            Constants.CLUSTER_COUNT,
            "Cluster mean:",
            Constants.CLUSTER_MEAN,
            "Cluster SD:",
            Constants.CLUSTER_SD,
        )

        while True:
            loop(dungeon, agent)
            agent, dungeon = reset()
        # break


def reset():
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


def loop(dungeon, agent):
    loop_time = time.time()
    cur_time = time.time()
    delay = Constants.DELAY
    agent_status = None
    agent_moved = False
    goblin_status = None
    key_held = False
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] and key_held:
            agent_status = dungeon.move_agent(agent, 0)
            print("Moving up", agent.x, agent.y)
            key_held = True
            loop_time = time.time()
            agent_moved = True
        elif keys[pygame.K_s] and key_held:
            agent_status = dungeon.move_agent(agent, 2)
            print("Moving down", agent.x, agent.y)
            key_held = True
            loop_time = time.time()
            agent_moved = True
        elif keys[pygame.K_a] and key_held:
            agent_status = dungeon.move_agent(agent, 1)
            print("Moving left", agent.x, agent.y)
            key_held = True
            loop_time = time.time()
            agent_moved = True
        elif keys[pygame.K_d] and key_held:
            agent_status = dungeon.move_agent(agent, 3)
            print("Mdoving right", agent.x, agent.y)
            key_held = True
            loop_time = time.time()
            agent_moved = True
        elif keys[pygame.K_ESCAPE]:
            break

        if agent_moved and agent_status != "no_move":
            goblin_status = dungeon.update()
            agent_moved = False

        if agent_status == "win":
            time.sleep(1)
            break
        elif goblin_status == "lose":
            time.sleep(1)
            print("you lose!")
            break

        if keys:
            # print("time elapsed:", cur_time - loop_time)
            if cur_time - loop_time > delay:
                key_held = True
                cur_time = time.time()
            else:
                key_held = False
                cur_time = time.time()

        pygame.display.flip()


if __name__ == "__main__":
    main()

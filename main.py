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
    dungeon.add_agent(agent)

    dungeon.create_brownian_path()
    dungeon.create_rocks()
    pygame.display.flip()
    return agent, dungeon


def loop(dungeon, agent):
    delay = Constants.DELAY
    agent_status = None
    key_held = False
    while True:
        if key_held:
            time.sleep(delay)
            key_held = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            agent_status = dungeon.move_agent(agent, 0)
            print("moving up", agent.x, agent.y)
            key_held = True
        elif keys[pygame.K_s]:
            agent_status = dungeon.move_agent(agent, 2)
            print("moving down", agent.x, agent.y)
            key_held = True
        elif keys[pygame.K_a]:
            agent_status = dungeon.move_agent(agent, 1)
            print("moving left", agent.x, agent.y)
            key_held = True
        elif keys[pygame.K_d]:
            agent_status = dungeon.move_agent(agent, 3)
            print("moving right", agent.x, agent.y)
            key_held = True
        elif keys[pygame.K_ESCAPE]:
            break

        if agent_status == "win":
            time.sleep(1)
            break

        pygame.display.flip()


if __name__ == "__main__":
    main()

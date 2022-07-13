# Sizes
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
CELL_SIZE = 40
CELL_WIDTH = WINDOW_WIDTH // CELL_SIZE
CELL_HEIGHT = WINDOW_HEIGHT // CELL_SIZE
BROWNIAN_PATH_COUNT = 3
BROWNIAN_PATH_THICKNESS = 2
CELL_COUNT = WINDOW_WIDTH // CELL_SIZE * WINDOW_HEIGHT // CELL_SIZE
CLUSTER_COUNT = 100
CLUSTER_MEAN = int(CELL_COUNT * 0.15)
CLUSTER_SD = CLUSTER_MEAN // 4
DELAY = 0.075
GOBLIN_COUNT = 1
GOBLIN_RANGE = 5

# The exit's y will be randomly chose
# The exit's x will be randomly be chose in the last % of the dungeon (right side)
END_ZONE_RATIO = 0.95
# Safe zone ratio is the ratio of the safe zone on the left side of the dungeon
# similar to the exit ratio
SAFE_ZONE_RATIO = 0.05

# Colors
BLACK = (0, 0, 0)
EMPTY = (39, 58, 77)
ROCK_COLOR = (18, 23, 28)
EXIT_COLOR = (0, 0, 0)
AGENT = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BROWN = (102, 51, 0)
GOBLIN_COLOR = (15, 117, 42)

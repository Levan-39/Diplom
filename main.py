import numpy as np
import pygame

GRID_WIDTH = 20
GRID_HEIGHT = 10

EMPTY = 0
PASSENGER = 1
PLATFORM = 2
OBSTACLE = 3

COLORS = {
    EMPTY: (255, 255, 255),
    PASSENGER: (0, 0, 255),
    PLATFORM: (0, 255, 0),
    OBSTACLE: (128, 128, 128),
    "GRID_LINES": (0, 0, 0)
}

grid = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=int)

grid[1:2, 0:1] = PASSENGER
grid[2:3, 1:2] = PASSENGER
grid[1:2, 2:3] = PASSENGER
grid[2:3, 3:4] = PASSENGER
grid[1:2, 4:5] = PASSENGER
grid[2:3, 5:6] = PASSENGER
grid[4:6, 0:1] = PASSENGER
grid[4:6, 2:3] = PASSENGER
grid[4:6, 4:5] = PASSENGER
grid[7:9, 0:1] = PASSENGER
grid[7:9, 2:3] = PASSENGER

grid[0:1, 0:20] = OBSTACLE
grid[1:3, 19:20] = OBSTACLE
grid[3, 0:1] = OBSTACLE
grid[3, 5:6] = OBSTACLE
grid[3, 10:11] = OBSTACLE
grid[3, 15:16] = OBSTACLE
grid[9:10, 0:20] = OBSTACLE
grid[7:9, 19:20] = OBSTACLE
grid[6, 0:1] = OBSTACLE
grid[6, 5:6] = OBSTACLE
grid[6, 10:11] = OBSTACLE
grid[6, 15:16] = OBSTACLE
grid[4:6, 14:15] = OBSTACLE
grid[2:8, 16] = OBSTACLE

grid[2:8, 17] = PLATFORM

pygame.init()
clock = pygame.time.Clock()
screen_width = GRID_WIDTH * 40
screen_height = GRID_HEIGHT * 40
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Passenger Flow Simulation")


def draw_grid():
    screen.fill((0, 0, 0))
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            cell_state = grid[y, x]
            color = COLORS[cell_state]
            pygame.draw.rect(screen, color, (x * 40, y * 40, 40, 40))
            pygame.draw.line(screen, COLORS["GRID_LINES"], (x * 40, y * 40), (x * 40, (y + 1) * 40))
            pygame.draw.line(screen, COLORS["GRID_LINES"], (x * 40, y * 40), ((x + 1) * 40, y * 40))

def passenger_traffic():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH - 1, -1, -1):
            if grid[y, x] == PASSENGER:
                if x < GRID_WIDTH - 1 and grid[y, x + 1] == EMPTY:
                    grid[y, x] = EMPTY
                    grid[y, x + 1] = PASSENGER
                elif x < GRID_WIDTH - 1 and grid[y, x + 1] == OBSTACLE:
                    if y < GRID_HEIGHT - 1 and grid[y + 1, x] == EMPTY:
                        grid[y, x] = EMPTY
                        grid[y + 1, x] = PASSENGER
                    elif y > 0 and grid[y - 1, x] == EMPTY:
                        grid[y, x] = EMPTY
                        grid[y - 1, x] = PASSENGER
                elif x < GRID_WIDTH - 2 and grid[y, x + 1] == EMPTY and grid[y, x + 2] == OBSTACLE:
                    grid[y, x] = EMPTY
                    grid[y, x + 1] = PASSENGER
                if x > 0 and grid[y, x - 1] == PLATFORM:
                    grid[y, x] = EMPTY
                    grid[y - 1, x] = EMPTY
                    grid[y + 1, x] = EMPTY


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    passenger_traffic()
    draw_grid()
    pygame.display.flip()
    clock.tick(2)

pygame.quit()

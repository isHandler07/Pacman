import heapq
import pygame
import random

# Constants
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
ROWS, COLS = HEIGHT // GRID_SIZE, WIDTH // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Maze layout (1 represents walls, 0 represents paths)
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Pacman and Ghost initial positions
pacman_pos = [1, 1]
ghost_pos = [6, 18]

def draw_maze(screen):
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            color = BLACK if maze[row][col] == 1 else WHITE
            pygame.draw.rect(screen, color, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def dijkstra(start, goal, maze):
    rows, cols = len(maze), len(maze[0])
    heap = [(0, start)]
    distances = {start: 0}
    previous = {start: None}
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    while heap:
        cost, current = heapq.heappop(heap)
        if current == goal:
            break
        
        for d in directions:
            neighbor = (current[0] + d[0], current[1] + d[1])
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and maze[neighbor[0]][neighbor[1]] == 0:
                new_cost = cost + 1
                if neighbor not in distances or new_cost < distances[neighbor]:
                    distances[neighbor] = new_cost
                    previous[neighbor] = current
                    heapq.heappush(heap, (new_cost, neighbor))
    
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = previous[current]
    path.reverse()
    return path[1:] if len(path) > 1 else []

def move_ghost():
    global ghost_pos
    path = dijkstra(tuple(ghost_pos), tuple(pacman_pos), maze)
    if path:
        ghost_pos[0], ghost_pos[1] = path[0]

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(BLACK)
        draw_maze(screen)
        
        pygame.draw.rect(screen, YELLOW, (pacman_pos[1] * GRID_SIZE, pacman_pos[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, RED, (ghost_pos[1] * GRID_SIZE, ghost_pos[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and maze[pacman_pos[0] - 1][pacman_pos[1]] == 0:
                    pacman_pos[0] -= 1
                elif event.key == pygame.K_DOWN and maze[pacman_pos[0] + 1][pacman_pos[1]] == 0:
                    pacman_pos[0] += 1
                elif event.key == pygame.K_LEFT and maze[pacman_pos[0]][pacman_pos[1] - 1] == 0:
                    pacman_pos[1] -= 1
                elif event.key == pygame.K_RIGHT and maze[pacman_pos[0]][pacman_pos[1] + 1] == 0:
                    pacman_pos[1] += 1
        
        move_ghost()
        pygame.display.flip()
        clock.tick(5)

    pygame.quit()

import pygame
pygame.init()
h = 1056
w = 960
screen = pygame.display.set_mode([w, h])
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 20)

run = True
while run:
    timer.tick(fps)
    screen.fill('black')
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            run = False
    pygame.display.flip()
pygame.quit()


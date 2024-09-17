from fileinput import close

import pygame, sys, random, time, json
from src.boid import Boid
from src.game_state import GameState
from src.utils import create_grid

f = open('config.json')
config = json.load(f)

# Constants
WIDTH, HEIGHT = config['window']['width'], config['window']['height']
WHITE, BLACK = (255, 255, 255), (0, 0, 0)
GRID_SIZE = config['optimization']['grid_size']

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Clock and Framerate
clock = pygame.time.Clock()
fps = config['optimization']['max_fps']

close()

game_state = GameState()
boids = []

dt_total = 0

# Main Loop
running = True

while running:
    dt = clock.tick(fps) / 1000
    dt_total += dt

    # Performance Timer Start
    start_framerate_time = time.time()
    start_one_second_count_time = time.time()

    # Event Detection
    for event in pygame.event.get():
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                if not game_state.mouse_button_3_down:
                    game_state.mouse_button_3_down = True

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                if game_state.mouse_button_3_down:
                    game_state.mouse_button_3_down = False
        if event.type == pygame.QUIT:
            running = False

    if game_state.mouse_button_3_down:
        mouse_pos = pygame.mouse.get_pos()
        boids.append(Boid(mouse_pos[0], mouse_pos[1], random.randrange(-150, 150, 50), random.randrange(-150, 150, 50), 0, 0, 0))

    # Create a grid
    grid, grid_width, grid_height = create_grid(WIDTH, HEIGHT, GRID_SIZE)

    for boid in boids:
        grid_x = int(boid.pos.x // GRID_SIZE) - 1
        grid_y = int(boid.pos.y // GRID_SIZE) - 1
        grid[grid_x][grid_y].append(boid)

    # Loop functions
    screen.fill(WHITE)

    for i, boid in enumerate(boids):
        boid.update(boids, grid, grid_width, grid_height, dt)
        boid.draw_self(screen)
    pygame.display.update()

    # Performance Timer End
    if dt_total >= 1:
        print(f"{1 // dt} fps, {len(boids)} boids, time delay: {dt * 1000}")
        dt_total = 0
pygame.quit()
sys.exit()
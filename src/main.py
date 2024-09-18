from fileinput import close

import pygame, sys, random, time, json
from src.boid import Boid
from src.game_state import GameState
from src.utils import create_grid
from gui import SideBar, Button, Slider

f = open('../src/config.json')
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

game_state = GameState()

side_bar_items = [
    Button(0, 150, 50, WHITE, 2, 'Choose Leaders', 'push', game_state.choose_leaders),
    Slider(1, 150, 10, 1, 10, config['behavior']['separation_force'], "Separation Force", game_state.change_separation_force),
    Slider(2, 150, 10, 20, 150, config['behavior']['separation_radius'], "Separation Radius", game_state.change_separation_radius),
    Slider(3, 150, 10, 0.005, 2, config['behavior']['cohesion_force'], "Cohesion Force", game_state.change_cohesion_force),
    Slider(4, 150, 10, 20, 150, config['behavior']['cohesion_radius'], "Cohesion Radius", game_state.change_cohesion_radius),
    Slider(5, 150, 10, 0.005, 2, config['behavior']['alignment_force'], "Alignment Force", game_state.change_alignment_force),
    Slider(6, 150, 10, 20, 150, config['behavior']['alignment_radius'], "Alignment Radius", game_state.change_alignment_radius),
    Slider(7, 150, 10, 20, 500, config['physics']['max_speed'], "Max Speed", game_state.change_max_speed)
]

close()

side_bar = SideBar(200, HEIGHT, side_bar_items)
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

    mouse_pos = pygame.mouse.get_pos()

    # Event Detection
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                if not game_state.mouse_button_3_down:
                    game_state.mouse_button_3_down = True
            if event.button == 1:
                action, value = side_bar.handle_item_interaction(event, mouse_pos)



        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                if game_state.mouse_button_3_down:
                    game_state.mouse_button_3_down = False
            if event.button == 1:
                action, value = side_bar.handle_item_interaction(event, mouse_pos)
                if action:
                    action(boids, value)
        if event.type == pygame.QUIT:
            running = False

    if game_state.mouse_button_3_down:
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
        boid.update(grid, grid_width, grid_height, dt)
        boid.draw_self(screen)

    side_bar.update_sliders(mouse_pos)

    side_bar.draw_self(screen)
    side_bar.draw_interactive_items(screen)



    pygame.display.update()

    # Performance Timer End
    if dt_total >= 1:
        print(f"{1 // dt} fps, {len(boids)} boids, time delay: {dt * 1000}")
        print(f'Leaders present: {game_state.num_leaders_present}')
        dt_total = 0
pygame.quit()
sys.exit()
import pygame, sys, random, time
from src.boid import Boid
from src.game_state import GameState

# Constants
WIDTH, HEIGHT = 800, 800
WHITE, BLACK = (255, 255, 255), (0, 0, 0)

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Clock and Framerate
clock = pygame.time.Clock()
fps = 60

game_state = GameState()
boids = []

one_second_count_total = 0

# Main Loop
running = True

while running:
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
            if event.button == 1:
                for boid in boids:
                    boid.selected = False
                    distance = boid.pos.distance_to(mouse_pos)
                    if distance < 25:
                        boid.selected = True

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                if game_state.mouse_button_3_down:
                    game_state.mouse_button_3_down = False
        if event.type == pygame.QUIT:
            running = False

    if game_state.mouse_button_3_down:
        mouse_pos = pygame.mouse.get_pos()
        boids.append(Boid(mouse_pos[0], mouse_pos[1], random.randint(-3, 3), random.randint(-3, 3), 0, 0, 0))

    # Loop functions
    screen.fill(WHITE)

    for i, boid in enumerate(boids):
        boid.update(boids)
        boid.draw_self(screen)
        boid.draw_line_to_neighbors(screen, boids)
    pygame.display.update()

    clock.tick(fps)

    # Performance Timer End
    end_framerate_time = time.time() - start_framerate_time
    end_one_second_count_time = time.time() - start_one_second_count_time
    one_second_count_total += end_one_second_count_time
    if one_second_count_total >= 1:
        print(f"{1 // end_framerate_time} fps, {len(boids)} boids, time delay: {end_framerate_time}")
        one_second_count_total = 0
pygame.quit()
sys.exit()
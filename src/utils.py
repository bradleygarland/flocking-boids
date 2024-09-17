import math

def create_grid(window_width, window_height, grid_size):
    grid_width = math.ceil(window_width / grid_size)
    grid_height = math.ceil(window_height / grid_size)
    return [[[] for _ in range(grid_height)] for _ in range(grid_width)], grid_width, grid_height
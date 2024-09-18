import pygame, math, json

f = open('config.json')
config = json.load(f)

# Constants
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Config <- config.json
SEPARATION_RADIUS = config['behavior']['separation_radius']
SEPARATION_FORCE = config['behavior']['separation_force']

COHESION_RADIUS = config['behavior']['cohesion_radius']
COHESION_FORCE = config['behavior']['cohesion_force']

ALIGNMENT_RADIUS = config['behavior']['alignment_radius']
ALIGNMENT_FORCE = config['behavior']['alignment_force']

SIMULATION_WIDTH = config['window']['width'] - config['side_bar']['width']
SIMULATION_HEIGHT = config['window']['height']
MAX_SPEED = config['physics']['max_speed']

# Load Boid image
image_size = config['window']['image_size']
images = {
    'boid': pygame.transform.scale(pygame.image.load(f'../resources/boid_arrow.png'), (image_size, image_size)),
    'blue_boid': pygame.transform.scale(pygame.image.load(f'../resources/blue_boid_arrow.png'), (image_size, image_size)),
    'red_boid': pygame.transform.scale(pygame.image.load(f'../resources/red_boid_arrow.png'), (image_size, image_size)),
    'green_boid': pygame.transform.scale(pygame.image.load(f'../resources/green_boid_arrow.png'), (image_size, image_size))
}


class Boid:
    def __init__(self, x_pos, y_pos, x_velocity, y_velocity, x_acceleration, y_acceleration, rotation):
        self.pos = pygame.Vector2(x_pos - image_size / 2, y_pos - image_size / 2)
        self.velocity = pygame.Vector2(x_velocity, y_velocity)
        self.acceleration = pygame.Vector2(x_acceleration, y_acceleration)
        self.rotation = rotation
        self.selected = False
        self.image = 'boid'
        self.separation_force = SEPARATION_FORCE
        self.separation_radius = SEPARATION_RADIUS
        self.cohesion_force = COHESION_FORCE
        self.cohesion_radius = COHESION_RADIUS
        self.alignment_force = ALIGNMENT_FORCE
        self.alignment_radius = ALIGNMENT_RADIUS
        self.max_speed = MAX_SPEED

    def update(self, grid, grid_width, grid_height, dt):

        neighbors = self.get_neighbors(grid, grid_width, grid_height)
        self.behavior(neighbors, dt)

        # Velocity change
        self.velocity += self.acceleration * dt

        # Limit the speed of the arrow
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        # Position change
        self.pos.x += self.velocity.x * dt
        self.pos.y -= self.velocity.y * dt

        if self.pos.x < 0:
            self.pos.x = SIMULATION_WIDTH
        elif self.pos.x > SIMULATION_WIDTH:
            self.pos.x = 0

        if self.pos.y < 0:
            self.pos.y = SIMULATION_HEIGHT
        elif self.pos.y > SIMULATION_HEIGHT:
            self.pos.y = 0


        # Rotation change
        self.rotation = math.degrees(math.atan2(self.velocity.y, self.velocity.x)) - 90

    def behavior(self, boids, dt):
        repulsion_force = pygame.Vector2(0, 0)

        center_of_mass = pygame.Vector2(0, 0)
        cohesion_total = 0

        avg_velocity = pygame.Vector2(0, 0)
        alignment_total = 0

        for other_boid in boids:
            if other_boid != self:
                distance = self.pos.distance_to(other_boid.pos)
                # Separation
                if self.separation_radius > distance > 0:
                    away_vector = self.pos - other_boid.pos
                    away_vector = away_vector.normalize() / distance
                    repulsion_force += away_vector
                # Cohesion
                if self.cohesion_radius > distance > 0:
                    center_of_mass += other_boid.pos
                    cohesion_total += 1
                # Alignment
                if self.alignment_radius > distance > 0:
                    avg_velocity += other_boid.velocity
                    alignment_total += 1

        repulsion_force *= self.separation_force
        cohesion_force = self.cohesion(center_of_mass, cohesion_total)
        alignment_force = self.alignment(avg_velocity, alignment_total)


        self.acceleration += repulsion_force * dt
        self.acceleration += cohesion_force * dt
        self.acceleration += alignment_force * dt

    def cohesion(self, center_of_mass, cohesion_total):
        if cohesion_total > 0:
            center_of_mass /= cohesion_total
            cohesion_vector = center_of_mass - self.pos
            cohesion_vector *= self.cohesion_force
            return cohesion_vector
        else:
            return pygame.Vector2(0, 0)

    def alignment(self, avg_velocity, alignment_total):
        if alignment_total > 0:
            avg_velocity /= alignment_total
            alignment_vector = avg_velocity - self.velocity
            alignment_vector *= self.alignment_force
            return alignment_vector
        else:
            return pygame.Vector2(0, 0)

    def draw_self(self, screen):

        rotated_boid_image = pygame.transform.rotate(images[self.image], self.rotation)
        screen.blit(rotated_boid_image, self.pos)

    def get_neighbors(self, grid, grid_width, grid_height):
        neighbors = []
        grid_x = int(self.pos.x / 100)
        grid_y = int(self.pos.y / 100)

        for dx in range(-1, 2):
            for dy in range(-1, 2):
                neighbor_x = grid_x + dx
                neighbor_y = grid_y + dy
                if 0 <= neighbor_x < grid_width and 0 <= neighbor_y < grid_height:
                    neighbors += grid[neighbor_x][neighbor_y]

        return neighbors

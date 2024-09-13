import pygame, math

# Constants
RED = (255, 0, 0)
GREEN = (0, 255, 0)

SEPARATION_RADIUS = 75
SEPARATION_FORCE = 0.3
COHESION_RADIUS = 150
COHESION_FORCE = 0.0005
ALIGNMENT_RADIUS = 100
ALIGNMENT_FORCE = 0.05
MAX_SPEED = 3

# Load Boid image
image_size = 25
boid_image = pygame.transform.scale(pygame.image.load('resources/boid_arrow.png'), (image_size, image_size))

class Boid:
    def __init__(self, x_pos, y_pos, x_velocity, y_velocity, x_acceleration, y_acceleration, rotation):
        self.pos = pygame.Vector2(x_pos - image_size / 2, y_pos - image_size / 2)
        self.velocity = pygame.Vector2(x_velocity, y_velocity)
        self.acceleration = pygame.Vector2(x_acceleration, y_acceleration)
        self.rotation = rotation
        self.selected = False

    def update(self, boids):
        # Apply separation
        separation_force = self.separation(boids)
        self.acceleration += separation_force

        # Apply Cohesion
        cohesion_force = self.cohesion(boids)
        self.acceleration += cohesion_force

        # Apply Alignment
        alignment_force = self.alignment(boids)
        self.acceleration += alignment_force

        # Velocity change
        self.velocity += self.acceleration

        # Limit the speed of the arrow
        if self.velocity.length() > MAX_SPEED:
            self.velocity.scale_to_length(MAX_SPEED)

        # Position change
        self.pos.x += self.velocity.x
        self.pos.y -= self.velocity.y

        if self.pos.x < 0:
            self.pos.x = 800
        elif self.pos.x > 800:
            self.pos.x = 0

        if self.pos.y < 0:
            self.pos.y = 800
        elif self.pos.y > 800:
            self.pos.y = 0


        # Rotation change
        self.rotation = math.degrees(math.atan2(self.velocity.y, self.velocity.x)) - 90

    def separation(self, boids):
        repulsion_force = pygame.Vector2(0, 0)
        for other_boid in boids:
            if other_boid != self:
                distance = self.pos.distance_to(other_boid.pos)
                if SEPARATION_RADIUS > distance > 0:
                    away_vector = self.pos - other_boid.pos
                    away_vector = away_vector.normalize() / distance
                    repulsion_force += away_vector

        repulsion_force *= SEPARATION_FORCE
        return repulsion_force

    def cohesion(self, boids):
        center_of_mass = pygame.Vector2(0, 0)
        total = 0

        for other_boid in boids:
            if other_boid != self:
                distance = self.pos.distance_to(other_boid.pos)
                if COHESION_RADIUS > distance > 0:
                    center_of_mass += other_boid.pos
                    total += 1

        if total > 0:
            center_of_mass /= total
            cohesion_vector = center_of_mass - self.pos
            cohesion_vector *= COHESION_FORCE
            return cohesion_vector
        else:
            return pygame.Vector2(0, 0)

    def alignment(self, boids):
        avg_velocity = pygame.Vector2(0, 0)
        total = 0

        for other_boid in boids:
            if other_boid != self:
                distance = self.pos.distance_to(other_boid.pos)
                if distance < ALIGNMENT_RADIUS:
                    avg_velocity += other_boid.velocity
                    total += 1

        if total > 0:
            avg_velocity /= total
            alignment_vector = avg_velocity - self.velocity
            alignment_vector *= ALIGNMENT_FORCE
            return alignment_vector
        else:
            return pygame.Vector2(0, 0)

    def draw_self(self, screen):
        rotated_boid_image = pygame.transform.rotate(boid_image, self.rotation)
        screen.blit(rotated_boid_image, self.pos)

    def draw_line_to_neighbors(self, screen, boids):
        if self.selected:
            for other_boid in boids:
                if other_boid != self:
                    distance = self.pos.distance_to(other_boid.pos)
                    # Separation Line
                    if SEPARATION_RADIUS > distance > 0:
                        pygame.draw.line(screen, RED, (self.pos.x + image_size / 2, self.pos.y + image_size / 2), (other_boid.pos.x + image_size / 2, other_boid.pos.y + image_size / 2), 3)

                    # Cohesion Line
                    if COHESION_RADIUS > distance > SEPARATION_RADIUS:
                        pygame.draw.line(screen, GREEN, (self.pos.x + image_size / 2, self.pos.y + image_size / 2), (other_boid.pos.x + image_size / 2, other_boid.pos.y + image_size / 2), 2)

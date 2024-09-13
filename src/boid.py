import pygame, math

# Load Boid image
image_size = 25
boid_image = pygame.transform.scale(pygame.image.load('../resources/boid_arrow.png'), (image_size, image_size))

class Boid:
    def __init__(self, x_pos, y_pos, x_vel, y_vel, rotation):
        self.x_pos = x_pos - image_size / 2
        self.y_pos = y_pos - image_size / 2
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.rotation = rotation

    def update(self):
        self.x_pos += self.x_vel
        self.y_pos += self.y_vel
        if self.x_pos < 0:
            self.x_pos = 800
        elif self.x_pos > 800:
            self.x_pos = 0

        if self.y_pos < 0:
            self.y_pos = 800
        elif self.y_pos > 800:
            self.y_pos = 0

        self.rotation = math.degrees(math.atan2(-self.y_vel, self.x_vel)) - 90

    def draw_self(self, screen):
        rotated_boid_image = pygame.transform.rotate(boid_image, self.rotation)
        screen.blit(rotated_boid_image, (self.x_pos, self.y_pos))
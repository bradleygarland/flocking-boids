import random

BOID_TYPES = [
    'green_boid',
    'red_boid',
    'blue_boid'
]

class GameState:
    def __init__(self):
        self.mouse_button_3_down = False
        self.num_types_leaders = 3
        self.num_leaders_select = 1
        self.num_leaders_present = 0

    def choose_leaders(self, boids):
        selected_boids = []


        while len(selected_boids) < self.num_leaders_select * self.num_types_leaders:
            random_boid = random.choice(boids)
            if random_boid.image == 'boid' and not random_boid in selected_boids:
                selected_boids.append(random_boid)

        boid_type_index = 0
        for i in range(len(selected_boids)):
                selected_boids[i].image = BOID_TYPES[boid_type_index]
                boid_type_index += 1
                self.num_leaders_present += 1
                if boid_type_index >= self.num_types_leaders:
                    boid_type_index = 0

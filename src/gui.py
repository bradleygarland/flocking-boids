import pygame, json, math

pygame.init()

f = open('config.json')
config = json.load(f)

# Constants <- config.json
WIDTH = config['window']['width']
HEIGHT = config['window']['height']
MAX_BUTTON_HEIGHT = config['side_bar']['max_button_height']
MAX_BUTTON_WIDTH = config['side_bar']['max_button_width']
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
LIGHT_GREY = (200, 200, 200)

font = pygame.font.SysFont(None, 20)

class SideBar:
    def __init__(self, width, height, items):
        self.width = width
        self.height = height
        self.bg_color = GREY
        self.items = items

        if (len(self.items) * MAX_BUTTON_HEIGHT) > self.height:
            for i in range(len(self.items) - (self.height // MAX_BUTTON_HEIGHT)):
                self.items.remove(self.items[-1])

    def draw_self(self, screen):
        pygame.draw.rect(screen, self.bg_color, (WIDTH - self.width, 0, self.width, self.height))

    def draw_interactive_items(self, screen):
        if len(self.items) > 0:
            for item in self.items:
                item.draw_self(screen)

    def update_sliders(self, mouse_pos):
        for item in self.items:
            if item.interaction_type == 'slider':
                item.update(mouse_pos)

    def handle_item_interaction(self, event, mouse_pos):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for item in self.items:
                if item.is_selected(mouse_pos):
                    item.update(mouse_pos)
        if event.type == pygame.MOUSEBUTTONUP:
            for item in self.items:
                if item.selected:
                    if item.is_selected(mouse_pos):
                        item.selected = False
                        item.update(mouse_pos)
                        if item.interaction_type == 'button':
                            return item.action, item.value
                    if item.interaction_type == 'slider':
                        return item.action, item.value
                    item.selected = False
                    item.update(mouse_pos)
        return None, None






class Button:
    def __init__(self, y_index, width, height, color, border_width, text, button_type, action=None):
        self.interaction_type = 'button'
        self.y_index = y_index if y_index >= 0 else 0
        self.width = width if width <= MAX_BUTTON_WIDTH else MAX_BUTTON_WIDTH
        self.height = height if height <= MAX_BUTTON_HEIGHT else MAX_BUTTON_HEIGHT
        self.color = color
        self.border_width = border_width
        self.x_pos = (WIDTH - 200) + (MAX_BUTTON_WIDTH - self.width) / 2
        self.y_pos = (self.y_index * MAX_BUTTON_HEIGHT) + (MAX_BUTTON_HEIGHT - self.height) / 2
        self.selected = False
        self.unselected_color = color
        self.selected_color = LIGHT_GREY
        self.button_type = button_type
        self.text = text
        self.action = action
        self.value = 1

    def draw_self(self, screen):
        pygame.draw.rect(screen, BLACK, (self.x_pos, self.y_pos, self.width, self.height))
        pygame.draw.rect(screen, self.color, (self.x_pos + self.border_width, self.y_pos + self.border_width, self.width - 2 * self.border_width, self.height - 2 * self.border_width))

        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=(self.x_pos + self.width // 2, self.y_pos + self.height // 2))
        screen.blit(text_surface, text_rect)

    def is_selected(self, mouse_pos):
        if self.x_pos <= mouse_pos[0] <= self.x_pos + self.width:
            if self.y_pos <= mouse_pos[1] <= self.y_pos + self.height:
                self.selected = True
                return True
        return False

    def update(self, mouse_pos):
        if self.selected:
            self.color = self.selected_color
        else:
            self.color = self.unselected_color

class Slider:
    def __init__(self, y_index, width, selector_radius, value_min, value_max, value, text, action=None):
        self.interaction_type = 'slider'
        self.y_index = y_index
        self.width = width
        self.bar_thickness = 4
        self.selector_radius = selector_radius
        self.unselected_radius = selector_radius
        self.selected_radius = selector_radius + 2
        self.selector_color = BLACK
        self.start_x_pos = (WIDTH - 200) + (MAX_BUTTON_WIDTH - self.width) / 2
        self.start_y_pos = (self.y_index * MAX_BUTTON_HEIGHT) + MAX_BUTTON_HEIGHT / 2
        self.end_x_pos = self.start_x_pos + self.width
        self.end_y_pos = self.start_y_pos
        self.click_tolerance = 10
        self.selected = False
        self.value_min = value_min
        self.value_max = value_max
        self.value = value
        if self.value_min <= self.value <= self.value_max:
            self.selector_x_pos = self.start_x_pos + self.width * ((self.value - self.value_min) / (self.value_max - self.value_min))
            print(f'start_x: {self.start_x_pos}, selector: {self.selector_x_pos - self.start_x_pos}')
        elif self.value < self.value_min:
            self.selector_x_pos = self.start_x_pos
        elif self.value > self.value_max:
            self.selector_x_pos = self.end_x_pos
        self.text = text
        self.action = action

    def is_selected(self, mouse_pos):
        if self.start_x_pos <= mouse_pos[0] <= self.end_x_pos and self.start_y_pos - self.click_tolerance <= mouse_pos[1] <= self.end_y_pos + self.click_tolerance:
            self.selected = True
            return True
        return False

    def draw_self(self, screen):
        pygame.draw.line(screen, BLACK,(self.start_x_pos, self.start_y_pos), (self.end_x_pos, self.end_y_pos), self.bar_thickness)
        pygame.draw.circle(screen, self.selector_color, (self.selector_x_pos, self.start_y_pos), self.selector_radius)

        label_text_surface = font.render(self.text, True, BLACK)
        label_text_rect = label_text_surface.get_rect(center=(self.start_x_pos + self.width // 2, self.start_y_pos - MAX_BUTTON_HEIGHT / 4))
        screen.blit(label_text_surface, label_text_rect)

        rounded_value = math.ceil(self.value * 100) / 100
        value_text_surface = font.render(str(rounded_value), True, BLACK)
        value_text_rect = value_text_surface.get_rect(center=(self.selector_x_pos, self.start_y_pos + MAX_BUTTON_HEIGHT / 4))
        screen.blit(value_text_surface, value_text_rect)


    def update(self, mouse_pos):
        if self.selected:
            value_step = (self.value_max - self.value_min) / self.width
            self.value = self.value_min + (self.selector_x_pos - self.start_x_pos) * value_step

            if self.start_x_pos <= mouse_pos[0] <= self.end_x_pos:
                self.selector_x_pos = mouse_pos[0]
            elif mouse_pos[0] < self.start_x_pos:
                self.selector_x_pos = self.start_x_pos
            elif mouse_pos[0] > self.end_x_pos:
                self.selector_x_pos = self.end_x_pos
            self.selector_radius = self.selected_radius
            self.selector_color = (50, 50, 50)
        else:
            self.selector_radius = self.unselected_radius
            self.selector_color = (0, 0, 0)










import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (169, 169, 169)

# Particle class
class Particle:
    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.velocity = [0, 0]
        self.dragging = False  # Flag to indicate if the particle is being dragged
        self.drag_offset = [0, 0]  # Offset to store the difference between the particle position and mouse position when dragging
        self.friction_on = False  # Flag to indicate whether friction is applied

    def update(self, particles):
        if self.dragging:
            # If particle is being dragged, set its position to the mouse cursor
            self.x, self.y = pygame.mouse.get_pos()
            # Apply the drag offset
            self.x -= self.drag_offset[0]
            self.y -= self.drag_offset[1]
            self.velocity = [0, 0]  # Reset velocity while dragging
        else:
            # Update particle position based on velocity
            self.x += self.velocity[0]
            self.y += self.velocity[1]

            # Bounce off walls
            if self.x - self.radius < 0:
                self.velocity[0] = abs(self.velocity[0])
                self.x = self.radius
            elif self.x + self.radius > WIDTH:
                self.velocity[0] = -abs(self.velocity[0])
                self.x = WIDTH - self.radius

            if self.y - self.radius < 0:
                self.velocity[1] = abs(self.velocity[1])
                self.y = self.radius
            elif self.y + self.radius > HEIGHT:
                self.velocity[1] = -abs(self.velocity[1])
                self.y = HEIGHT - self.radius

            # Apply gravity
            gravity = gravity_slider.get_value()
            self.velocity[1] += gravity

            # Apply friction
            if self.friction_on:
                self.velocity[0] *= 0.98
                self.velocity[1] *= 0.98

            # Damping to gradually reduce velocity
            self.velocity[0] *= 0.98
            self.velocity[1] *= 0.98

            # Check for collisions with other particles
            for other_particle in particles:
                if other_particle != self:
                    distance = pygame.math.Vector2(self.x - other_particle.x, self.y - other_particle.y).length()
                    if distance < self.radius + other_particle.radius:
                        # Calculate overlap and move particles away from each other
                        overlap = (self.radius + other_particle.radius) - distance
                        overlap_direction = pygame.math.Vector2(self.x - other_particle.x, self.y - other_particle.y)
                        overlap_direction.normalize_ip()

                        # Move particles away from each other
                        self.x += overlap_direction.x * (overlap / 2)
                        self.y += overlap_direction.y * (overlap / 2)
                        other_particle.x -= overlap_direction.x * (overlap / 2)
                        other_particle.y -= overlap_direction.y * (overlap / 2)

                        # Calculate the relative velocity
                        relative_velocity = [self.velocity[0] - other_particle.velocity[0],
                                             self.velocity[1] - other_particle.velocity[1]]

                        # Coefficient to control the strength of the collision response
                        collision_coefficient = 1.5
                        elasticity_coefficient = 0.8  # Control the elasticity of the collisions

                        # Calculate the impulse and update velocities based on collision response
                        impulse = 2 * self.mass * other_particle.mass / (self.mass + other_particle.mass) * \
                                  pygame.math.Vector2(relative_velocity[0], relative_velocity[1]).dot(overlap_direction) * \
                                  overlap_direction

                        self.velocity[0] -= impulse[0] / self.mass
                        self.velocity[1] -= impulse[1] / self.mass
                        other_particle.velocity[0] += impulse[0] / other_particle.mass
                        other_particle.velocity[1] += impulse[1] / other_particle.mass

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)


# Box class
# Add this part to define the Box class
class Box:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def update(self):
        pass  # Add any specific update logic for boxes here

# Wedge class
class Wedge:
    def __init__(self, x, y, radius, angle, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.angle = angle
        self.color = color

    def draw(self, screen):
        pygame.draw.polygon(screen, self.color, [
            (self.x, self.y),
            (self.x + self.radius * math.cos(self.angle), self.y + self.radius * math.sin(self.angle)),
            (self.x + self.radius * math.cos(self.angle + math.pi / 2), self.y + self.radius * math.sin(self.angle + math.pi / 2))
        ])
    def update(self):
        pass  # Add any specific update logic for boxes here

# Create additional objects
boxes = [
    Box(100, 400, 50, 50, BLUE),
    Box(400, 300, 80, 40, RED),
    Box(600, 200, 30, 70, GREEN)
]

wedges = [
    Wedge(200, 200, 50, math.pi / 4, RED),
    Wedge(500, 100, 40, -math.pi / 3, GREEN)
]


# Button class
class Button:
    def __init__(self, x, y, width, height, color, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.action = action

    def draw(self, screen, font):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

# Create buttons
add_box_button = Button(10, 80, 150, 50, RED, 'Add Box', lambda: boxes.append(Box(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50), 30, 30, BLUE)))
add_wedge_button = Button(180, 80, 150, 50, GREEN, 'Add Wedge', lambda: wedges.append(Wedge(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50), 30, math.pi / 4, RED)))

# Custom Slider class
class Slider:
    def __init__(self, x, y, width, height, color, min_value, max_value):
        self.rect = pygame.Rect(x, y, width, height)
        self.handle_width = 10
        self.handle_rect = pygame.Rect(self.rect.x, self.rect.y, self.handle_width, height)
        self.color = color
        self.min_value = min_value
        self.max_value = max_value
        self.value = min_value
        self.dragging = False  # Flag to indicate if the slider is being dragged

    def get_value(self):
        return self.value

    def set_value(self, new_value):
        self.value = max(self.min_value, min(new_value, self.max_value))

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.rect)
        handle_x = int(self.rect.x + (self.value - self.min_value) / (self.max_value - self.min_value) * (self.rect.width - self.handle_width))
        handle_x = max(self.rect.x, min(handle_x, self.rect.x + self.rect.width - self.handle_width))  # Ensure handle stays within slider boundaries
        self.handle_rect.x = handle_x
        pygame.draw.rect(screen, self.color, self.handle_rect)

# Create particles
particles = [
    Particle(WIDTH // 4, HEIGHT // 2, 20, RED, 1),
    Particle(3 * WIDTH // 4, HEIGHT // 2, 20, BLUE, 1)
]

# Create Pygame screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Physics Simulator (Menu)")

# Font
font = pygame.font.Font(None, 36)

# Add Particle Button
add_particle_button = pygame.Rect(10, 10, 150, 50)
add_particle_color = GREEN

# Friction Button
friction_button = pygame.Rect(180, 10, 150, 50)
friction_color = BLUE

# Gravity Slider
gravity_slider = Slider(350, 10, 150, 20, RED, -1, 1)

# Return to Normal Button
reset_button = pygame.Rect(520, 10, 150, 50)
reset_color = (255, 165, 0)

# Color dropdown menu
color_options = [('Red', RED), ('Green', GREEN), ('Blue', BLUE), ('Random', (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))]
dropdown_rect = pygame.Rect(690, 10, 100, 50)
dropdown_open = False
selected_color = color_options[0][1]

# Main loop
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            dropdown_open = not dropdown_open
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if gravity_slider.handle_rect.collidepoint(event.pos):
                gravity_slider.dragging = True
                offset_x = event.pos[0] - gravity_slider.handle_rect.x
            elif add_particle_button.collidepoint(event.pos):
                new_particle = Particle(WIDTH // 2, HEIGHT // 2, 20, selected_color, 1)
                particles.append(new_particle)
            elif friction_button.collidepoint(event.pos):
                for particle in particles:
                    particle.friction_on = not particle.friction_on
            elif reset_button.collidepoint(event.pos):
                gravity_slider.set_value(0)
                for particle in particles:
                    particle.friction_on = False
                    particle.velocity = [0, 0]
            elif add_box_button.rect.collidepoint(event.pos):
                boxes.append(Box(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50), 30, 30, BLUE))
            elif add_wedge_button.rect.collidepoint(event.pos):
                wedges.append(Wedge(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50), 30, 30, GREEN))

            else:
                # Check if any particle is being clicked
                for particle in particles:
                    if pygame.Rect(particle.x - particle.radius, particle.y - particle.radius, 2 * particle.radius, 2 * particle.radius).collidepoint(event.pos):
                        particle.dragging = True
                        particle.drag_offset = [event.pos[0] - particle.x, event.pos[1] - particle.y]
                # Check if color dropdown menu is being clicked
                if dropdown_rect.collidepoint(event.pos):
                    dropdown_open = not dropdown_open
                else:
                    dropdown_open = False
                    # Check if any color option is being clicked
                    for i, (_, color_option) in enumerate(color_options):
                        rect = pygame.Rect(dropdown_rect.x, dropdown_rect.y + 50 * (i + 1), dropdown_rect.width, dropdown_rect.height)
                        if rect.collidepoint(event.pos):
                            selected_color = color_option

    # Update particles, boxes, and wedges
    for particle in particles:
        particle.update(particles)
    for box in boxes:
        box.update()
    for wedge in wedges:
        wedge.update()

    # Clear the screen
    screen.fill(WHITE)

    # Draw particles
    for particle in particles:
        particle.draw(screen)

    # Draw boxes
    for box in boxes:
        box.draw(screen)

    # Draw wedges
    for wedge in wedges:
        wedge.draw(screen)

    # Draw Add Particle button
    pygame.draw.rect(screen, add_particle_color, add_particle_button)
    add_particle_text = font.render('Add Particle', True, WHITE)
    screen.blit(add_particle_text, (20, 20))

    # Draw buttons
    add_box_button.draw(screen, font)
    add_wedge_button.draw(screen, font)

    # Check if mouse is over the Add Particle button
    if add_particle_button.collidepoint(pygame.mouse.get_pos()):
        add_particle_color = (0, 200, 0)
    else:
        add_particle_color = GREEN

    # Check if mouse is over the Add Box button
    if add_box_button.rect.collidepoint(pygame.mouse.get_pos()):
        add_box_button.color = (0, 200, 0)
    else:
        add_box_button.color = RED

    # Check if mouse is over the Add Wedge button
    if add_wedge_button.rect.collidepoint(pygame.mouse.get_pos()):
        add_wedge_button.color = (0, 200, 0)
    else:
        add_wedge_button.color = GREEN

    # Draw Add Box button
    pygame.draw.rect(screen, add_box_button.color, add_box_button.rect)
    add_box_text = font.render('Add Box', True, WHITE)
    screen.blit(add_box_text, (20, 80))

    # Draw Add Wedge button
    pygame.draw.rect(screen, add_wedge_button.color, add_wedge_button.rect)
    add_wedge_text = font.render('Add Wedge', True, WHITE)
    screen.blit(add_wedge_text, (20, 150))

    # Draw Friction button
    pygame.draw.rect(screen, friction_color, friction_button)
    friction_text = font.render('Toggle Friction', True, WHITE)
    screen.blit(friction_text, (190, 20))

    # Check if mouse is over the Friction button
    if friction_button.collidepoint(pygame.mouse.get_pos()):
        friction_color = (0, 0, 200)
    else:
        friction_color = BLUE

    # Draw Gravity Slider
    gravity_slider.draw(screen)

    # Draw Return to Normal button
    pygame.draw.rect(screen, reset_color, reset_button)
    reset_text = font.render('Return to Normal', True, WHITE)
    screen.blit(reset_text, (530, 20))

    # Check if mouse is over the Return to Normal button
    if reset_button.collidepoint(pygame.mouse.get_pos()):
        reset_color = (255, 215, 0)
    else:
        reset_color = (255, 165, 0)

    # Draw color dropdown menu
    pygame.draw.rect(screen, GRAY, dropdown_rect)
    pygame.draw.rect(screen, selected_color, dropdown_rect.inflate(-2, -2))
    dropdown_text = font.render('Color', True, WHITE)
    screen.blit(dropdown_text, (dropdown_rect.x + 5, dropdown_rect.y + 5))

    # Draw color options if dropdown is open
    if dropdown_open:
        for i, (text, color) in enumerate(color_options):
            rect = pygame.Rect(dropdown_rect.x, dropdown_rect.y + 50 * (i + 1), dropdown_rect.width, dropdown_rect.height)
            pygame.draw.rect(screen, GRAY, rect)
            pygame.draw.rect(screen, color, rect.inflate(-2, -2))
            text_surface = font.render(text, True, WHITE)
            screen.blit(text_surface, (rect.x + 5, rect.y + 5))

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

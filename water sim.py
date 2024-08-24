import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Object class
class Object(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = random.randint(1, 5)

    def update(self, wave_height):
        self.rect.y += self.velocity
        if self.rect.top > HEIGHT - wave_height:
            self.rect.y = 0
            self.velocity = random.randint(1, 5)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Objects in Waves Simulation")
clock = pygame.time.Clock()

# Wave parameters
amplitude = 50
frequency = 0.01
time = 0

# Create sprites group
all_sprites = pygame.sprite.Group()

# Create objects
for _ in range(10):
    obj = Object(random.randint(0, WIDTH), random.randint(0, HEIGHT))
    all_sprites.add(obj)

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update wave parameters
    time += 1
    wave_height = int(amplitude * math.sin(frequency * time))

    # Update objects
    all_sprites.update(wave_height)

    # Draw
    screen.fill(WHITE)

    # Draw wave
    pygame.draw.line(screen, BLUE, (0, HEIGHT), (WIDTH, HEIGHT), 2)
    pygame.draw.line(screen, BLUE, (0, HEIGHT - wave_height), (WIDTH, HEIGHT - wave_height), 2)

    # Color the space below the wave
    pygame.draw.polygon(screen, BLUE, [(x, HEIGHT) for x in range(WIDTH)], 0)
    pygame.draw.polygon(screen, WHITE, [(x, HEIGHT - wave_height) for x in range(WIDTH)], 0)

    # Draw objects
    all_sprites.draw(screen)

    # Refresh display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()

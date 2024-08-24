import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PLAYER_SIZE = 50
PLATFORM_HEIGHT = 20
GRAVITY = 1
NORMAL_GRAVITY = 2  # Adjust the normal gravity value
JUMP_HEIGHT = -15
SCROLL_THRESHOLD = WIDTH // 2

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Scrolling Platformer")

# Load background image
background = pygame.image.load("background.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Create the player
player = pygame.Rect(WIDTH // 2 - PLAYER_SIZE // 2, HEIGHT // 2 - PLAYER_SIZE // 2, PLAYER_SIZE, PLAYER_SIZE)
player_speed = 5
player_jump = False
jump_count = 10  # Controls how high the player jumps

# Define starting level
current_level = [
    [0, HEIGHT - PLATFORM_HEIGHT, WIDTH, PLATFORM_HEIGHT],
    [200, 400, 200, PLATFORM_HEIGHT],
    [500, 300, 200, PLATFORM_HEIGHT],
    [700, 100, 100, PLATFORM_HEIGHT],
    [900, 200, 50, PLATFORM_HEIGHT],
]

# Viewport position
viewport_x = 0

# Falling platform variables
falling_platforms = [{"rect": pygame.Rect(1300, 500, 100, PLATFORM_HEIGHT), "falling": False, "fall_speed": 5}]

# Clock to control the frame rate
clock = pygame.time.Clock()

def generate_fixed_platforms():
    """Generate a fixed set of platforms."""
    platforms = [
        [0, HEIGHT - PLATFORM_HEIGHT, WIDTH, PLATFORM_HEIGHT],
        [200, 400, 200, PLATFORM_HEIGHT],
        [500, 300, 200, PLATFORM_HEIGHT],
        [700, 100, 100, PLATFORM_HEIGHT],
        [900, 200, 50, PLATFORM_HEIGHT],
        [1300, 500, 100, PLATFORM_HEIGHT],
    ]
    return platforms

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.left > 0:
        player.x -= player_speed
        if player.x < viewport_x + SCROLL_THRESHOLD and viewport_x > 0:
            viewport_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player.x += player_speed
        # Scrolling to the right

    if keys[pygame.K_SPACE] and not player_jump:
        player_jump = True

    # Jumping mechanics
    if player_jump:
        if jump_count >= -10:
            neg = 1
            if jump_count < 0:
                neg = -1
            player.y -= (jump_count ** 2) * 0.5 * neg
            jump_count -= 1
        else:
            player_jump = False
            jump_count = 10

    # Simulate gravity
    on_platform = False
    for platform in current_level:
        platform_rect = pygame.Rect(platform[:4])
        if player.colliderect(platform_rect):
            on_platform = True
            player.y = platform_rect.y - PLAYER_SIZE
            player_jump = False
            jump_count = 10

    if not on_platform:
        player.y += NORMAL_GRAVITY

    # Update falling platforms
    for platform in falling_platforms:
        platform_rect = platform["rect"]
        if player.colliderect(platform_rect) and not platform["falling"]:
            platform["falling"] = True
        if platform["falling"]:
            platform_rect.y += platform["fall_speed"]

    # Fill the screen with the background
    screen.blit(background, (0, 0))

    # Draw the player and the current level's platforms
    pygame.draw.rect(screen, GREEN, player)
    for platform in current_level:
        platform_rect = [x - viewport_x for x in platform[:4]]
        pygame.draw.rect(screen, GREEN, platform_rect)

    # Draw falling platforms
    for platform in falling_platforms:
        platform_rect = platform["rect"]
        pygame.draw.rect(screen, GREEN, platform_rect)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
GRAVITY = 0.5
FRICTION = 0.99

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Object class
class GameObject:
    def __init__(self, x, y, size, color, shape):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.shape = shape
        self.velocity = [0, 0]
        self.angular_velocity = 0
        self.dragging = False
        self.prev_mouse_pos = (0, 0)

    def draw(self):
        if self.shape == "circle":
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))
        elif self.shape == "rectangle":
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
        elif self.shape == "wedge":
            pygame.draw.polygon(screen, self.color, self.get_wedge_points())

    def apply_gravity(self):
        self.velocity[1] += GRAVITY

    def apply_friction(self):
        self.velocity[0] *= FRICTION
        self.velocity[1] *= FRICTION

        self.angular_velocity *= FRICTION

    def handle_ground_collision(self):
        if self.y + self.size > HEIGHT:
            self.y = HEIGHT - self.size
            self.velocity[1] = 0  # Stop vertical movement on ground collision
            self.angular_velocity = 0

    def get_wedge_points(self):
        points = []
        num_points = 3  # Number of points in the wedge
        for i in range(num_points):
            angle = (i / num_points) * 2 * math.pi
            x = self.x + self.size * math.cos(angle)
            y = self.y + self.size * math.sin(angle)
            points.append((x, y))
        return points

    def update(self):
        if self.dragging:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            dx = mouse_x - self.prev_mouse_pos[0]
            dy = mouse_y - self.prev_mouse_pos[1]

            self.x += dx
            self.y += dy

            self.angular_velocity = dx / 10.0  # Adjust this factor to control the throwing strength

            self.prev_mouse_pos = (mouse_x, mouse_y)

        else:
            self.x += self.velocity[0]
            self.y += self.velocity[1]

            self.apply_gravity()
            self.apply_friction()

            if self.x > WIDTH or self.x < 0:
                self.velocity[0] *= -1
                self.angular_velocity *= -1  # Reverse angular velocity on bouncing off the walls

            self.handle_ground_collision()

# Function to check collision between two objects (circles, rectangles, and wedges)
def is_collision(obj1, obj2):
    if obj1.shape == "circle" and obj2.shape == "circle":
        distance = math.sqrt((obj1.x - obj2.x)**2 + (obj1.y - obj2.y)**2)
        combined_radius = obj1.size + obj2.size
        return distance < combined_radius

    elif obj1.shape == "rectangle" and obj2.shape == "rectangle":
        return (
            obj1.x < obj2.x + obj2.size and
            obj1.x + obj1.size > obj2.x and
            obj1.y < obj2.y + obj2.size and
            obj1.y + obj1.size > obj2.y
        )

    elif obj1.shape == "wedge" and obj2.shape == "wedge":
        # For wedges, we can simplify and assume a circular shape for collision detection
        distance = math.sqrt((obj1.x - obj2.x)**2 + (obj1.y - obj2.y)**2)
        combined_radius = obj1.size + obj2.size
        return distance < combined_radius

    # Handling collisions between different shapes (e.g., circle and rectangle)
    elif obj1.shape == "circle" and obj2.shape == "rectangle":
        # Use circle-rectangle collision detection
        return is_collision_circle_rectangle(obj1, obj2)
    elif obj1.shape == "rectangle" and obj2.shape == "circle":
        return is_collision_circle_rectangle(obj2, obj1)

    # Add more cases for different shape combinations if needed

    return False

# Function to check collision between a circle and a rectangle
def is_collision_circle_rectangle(circle, rectangle):
    closest_x = max(rectangle.x, min(circle.x, rectangle.x + rectangle.size))
    closest_y = max(rectangle.y, min(circle.y, rectangle.y + rectangle.size))

    distance_x = circle.x - closest_x
    distance_y = circle.y - closest_y
    distance_squared = distance_x**2 + distance_y**2

    return distance_squared < circle.size**2

# Function to resolve collision between two objects
def resolve_collision(obj1, obj2):
    if obj1.shape == "circle" and obj2.shape == "circle":
        angle = math.atan2(obj2.y - obj1.y, obj2.x - obj1.x)
        total_mass = obj1.size**2 + obj2.size**2
        obj1_ratio = obj1.size**2 / total_mass
        obj2_ratio = obj2.size**2 / total_mass

        obj1.velocity[0], obj1.velocity[1] = (
            obj1_ratio * obj1.velocity[0] + obj2_ratio * obj2.velocity[0],
            obj1_ratio * obj1.velocity[1] + obj2_ratio * obj2.velocity[1]
        )

        obj2.velocity[0], obj2.velocity[1] = (
            obj1_ratio * obj2.velocity[0] + obj2_ratio * obj1.velocity[0],
            obj1_ratio * obj2.velocity[1] + obj2_ratio * obj1.velocity[1]
        )

    elif obj1.shape == "rectangle" and obj2.shape == "rectangle":
        # Handle rectangle-rectangle collisions
        overlap_x = (obj1.size + obj2.size) - (abs(obj1.x - obj2.x) + obj1.size + obj2.size)
        overlap_y = (obj1.size + obj2.size) - (abs(obj1.y - obj2.y) + obj1.size + obj2.size)

        if overlap_x > 0 and overlap_y > 0:
            if overlap_x < overlap_y:
                if obj1.x < obj2.x:
                    obj1.x -= overlap_x / 2
                    obj2.x += overlap_x / 2
                else:
                    obj1.x += overlap_x / 2
                    obj2.x -= overlap_x / 2
            else:
                if obj1.y < obj2.y:
                    obj1.y -= overlap_y / 2
                    obj2.y += overlap_y / 2
                else:
                    obj1.y += overlap_y / 2
                    obj2.y -= overlap_y / 2

    elif obj1.shape == "wedge" and obj2.shape == "wedge":
        # For wedges, we can simplify and assume a circular shape for collision resolution
        angle = math.atan2(obj2.y - obj1.y, obj2.x - obj1.x)
        total_mass = obj1.size**2 + obj2.size**2
        obj1_ratio = obj1.size**2 / total_mass
        obj2_ratio = obj2.size**2 / total_mass

        obj1.velocity[0], obj1.velocity[1] = (
            obj1_ratio * obj1.velocity[0] + obj2_ratio * obj2.velocity[0],
            obj1_ratio * obj1.velocity[1] + obj2_ratio * obj2.velocity[1]
        )

        obj2.velocity[0], obj2.velocity[1] = (
            obj1_ratio * obj2.velocity[0] + obj2_ratio * obj1.velocity[0],
            obj1_ratio * obj2.velocity[1] + obj2_ratio * obj1.velocity[1]
        )

    # Handle collisions between different shapes (e.g., circle and rectangle)
    elif obj1.shape == "circle" and obj2.shape == "rectangle":
        # Use circle-rectangle collision resolution
        resolve_collision_circle_rectangle(obj1, obj2)
    elif obj1.shape == "rectangle" and obj2.shape == "circle":
        resolve_collision_circle_rectangle(obj2, obj1)

    # Add more cases for different shape combinations if needed

# Function to resolve collision between a circle and a rectangle
def resolve_collision_circle_rectangle(circle, rectangle):
    closest_x = max(rectangle.x, min(circle.x, rectangle.x + rectangle.size))
    closest_y = max(rectangle.y, min(circle.y, rectangle.y + rectangle.size))

    distance_x = circle.x - closest_x
    distance_y = circle.y - closest_y
    distance_squared = distance_x**2 + distance_y**2

    if distance_squared < circle.size**2:
        distance = math.sqrt(distance_squared)
        overlap = circle.size - distance

        if distance > 0:
            ratio = overlap / distance

            circle.x -= distance_x * ratio / 2
            circle.y -= distance_y * ratio / 2

            rectangle.x += distance_x * ratio / 2
            rectangle.y += distance_y * ratio / 2

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Physics Simulator")

# Create objects
objects = []

# Create buttons
spawn_circle_button = pygame.Rect(10, 10, 100, 50)
spawn_rectangle_button = pygame.Rect(120, 10, 130, 50)
spawn_wedge_button = pygame.Rect(260, 10, 100, 50)

# Font
font = pygame.font.Font(None, 36)

# Game loop
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if spawn_circle_button.collidepoint(event.pos):
                size = random.randint(10, 50)
                color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                obj = GameObject(WIDTH // 2, HEIGHT // 2, size, color, "circle")
                objects.append(obj)

            elif spawn_rectangle_button.collidepoint(event.pos):
                size = random.randint(10, 50)
                color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                obj = GameObject(WIDTH // 2, HEIGHT // 2, size, color, "rectangle")
                objects.append(obj)

            elif spawn_wedge_button.collidepoint(event.pos):
                size = random.randint(20, 50)
                color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                obj = GameObject(WIDTH // 2, HEIGHT // 2, size, color, "wedge")
                objects.append(obj)

            for obj in objects:
                if obj.x < event.pos[0] < obj.x + obj.size and obj.y < event.pos[1] < obj.y + obj.size:
                    obj.dragging = True
                    obj.prev_mouse_pos = pygame.mouse.get_pos()

        elif event.type == pygame.MOUSEBUTTONUP:
            for obj in objects:
                obj.dragging = False

    screen.fill(WHITE)

    for obj in objects:
        obj.update()
        obj.draw()

    # Check collisions
    for i in range(len(objects)):
        for j in range(i + 1, len(objects)):
            if is_collision(objects[i], objects[j]):
                resolve_collision(objects[i], objects[j])

    pygame.draw.rect(screen, BLUE, spawn_circle_button)
    pygame.draw.rect(screen, BLUE, spawn_rectangle_button)
    pygame.draw.rect(screen, BLUE, spawn_wedge_button)

    spawn_circle_text = font.render('Spawn Circle', True, WHITE)
    spawn_rectangle_text = font.render('Spawn Rectangle', True, WHITE)
    spawn_wedge_text = font.render('Spawn Wedge', True, WHITE)

    screen.blit(spawn_circle_text, (spawn_circle_button.x + 10, spawn_circle_button.y + 10))
    screen.blit(spawn_rectangle_text, (spawn_rectangle_button.x + 10, spawn_rectangle_button.y + 10))
    screen.blit(spawn_wedge_text, (spawn_wedge_button.x + 10, spawn_wedge_button.y + 10))

    pygame.display.flip()
    clock.tick(FPS)

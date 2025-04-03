import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flight Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Player (airplane)
PLANE_WIDTH, PLANE_HEIGHT = 50, 30
plane = pygame.Rect(WIDTH // 2 - PLANE_WIDTH // 2, HEIGHT - 100, PLANE_WIDTH, PLANE_HEIGHT)
plane_speed = 7

# Obstacles
OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 50, 50
obstacles = []
obstacle_speed = 5
obstacle_spawn_delay = 30  # Frames between obstacle spawns
obstacle_timer = 0

# Score
score = 0
font = pygame.font.SysFont(None, 36)

# Draw player (airplane)
def draw_plane(surface, rect):
    pygame.draw.polygon(surface, (0, 255, 0), [
        (rect.centerx, rect.top),  # Top point
        (rect.left, rect.bottom),  # Bottom-left point
        (rect.right, rect.bottom)  # Bottom-right point
    ])

# Draw obstacles
def draw_obstacle(surface, rect):
    pygame.draw.rect(surface, RED, rect)

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and plane.left > 0:
        plane.move_ip(-plane_speed, 0)
    if keys[pygame.K_RIGHT] and plane.right < WIDTH:
        plane.move_ip(plane_speed, 0)

    # Spawn obstacles
    obstacle_timer += 1
    if obstacle_timer >= obstacle_spawn_delay:
        obstacle_timer = 0
        obstacle_x = random.randint(0, WIDTH - OBSTACLE_WIDTH)
        obstacle = pygame.Rect(obstacle_x, 0, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
        obstacles.append(obstacle)

    # Move obstacles
    for obstacle in obstacles[:]:
        obstacle.move_ip(0, obstacle_speed)
        if obstacle.top > HEIGHT:  # Remove obstacles that go off-screen
            obstacles.remove(obstacle)
            score += 1  # Increase score for avoiding an obstacle

    # Check for collisions
    for obstacle in obstacles:
        if plane.colliderect(obstacle):
            print("Game Over!")
            running = False

    # Draw player, obstacles, and score
    draw_plane(screen, plane)
    for obstacle in obstacles:
        draw_obstacle(screen, obstacle)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Update display
    pygame.display.flip()
    clock.tick(60)

# Ensure proper cleanup
pygame.quit()
sys.exit()

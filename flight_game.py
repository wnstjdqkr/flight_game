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

# Player (fighter jet)
PLANE_WIDTH, PLANE_HEIGHT = 50, 30
plane = pygame.Rect(WIDTH // 2 - PLANE_WIDTH // 2, HEIGHT - 100, PLANE_WIDTH, PLANE_HEIGHT)
plane_speed = 7

# Obstacles
OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 50, 50
obstacles = []
obstacle_speed = 5
obstacle_spawn_delay = 30  # Frames between obstacle spawns
obstacle_timer = 0

# Power-ups
POWERUP_WIDTH, POWERUP_HEIGHT = 30, 30
powerups = []
powerup_spawn_delay = 200  # Frames between power-up spawns
powerup_timer = 0
powerup_score_bonus = 5

# Bullets
BULLET_WIDTH, BULLET_HEIGHT = 5, 10
bullets = []
bullet_speed = -10

# Bullet firing delay
bullet_timer = 0
bullet_delay = 10  # Frames between bullet fires

# Explosion effects
explosions = []
EXPLOSION_LIFETIME = 20  # Frames for explosion to last

# Score
score = 0
font = pygame.font.SysFont(None, 36)

# Font for displaying messages
button_font = pygame.font.SysFont(None, 48)

# Draw player (fighter jet) with more detailed design
def draw_plane(surface, rect):
    # Main body
    pygame.draw.polygon(surface, (0, 255, 0), [
        (rect.centerx, rect.top),  # Nose
        (rect.left + 10, rect.centery),  # Left wing
        (rect.left, rect.centery + 10),  # Left tail
        (rect.left + 15, rect.bottom),  # Left bottom
        (rect.right - 15, rect.bottom),  # Right bottom
        (rect.right, rect.centery + 10),  # Right tail
        (rect.right - 10, rect.centery)  # Right wing
    ])
    
    # Cockpit
    pygame.draw.ellipse(surface, (0, 0, 255), (rect.centerx - 10, rect.top + 5, 20, 10))
    
    # Engine flames
    pygame.draw.polygon(surface, (255, 165, 0), [
        (rect.left + 15, rect.bottom),  # Left engine flame
        (rect.left + 25, rect.bottom + 10),
        (rect.left + 35, rect.bottom)
    ])
    pygame.draw.polygon(surface, (255, 165, 0), [
        (rect.right - 15, rect.bottom),  # Right engine flame
        (rect.right - 25, rect.bottom + 10),
        (rect.right - 35, rect.bottom)
    ])
    
    # Additional details
    # Left wing detail
    pygame.draw.line(surface, (255, 255, 255), (rect.left + 10, rect.centery), (rect.left + 30, rect.centery + 10), 2)
    # Right wing detail
    pygame.draw.line(surface, (255, 255, 255), (rect.right - 10, rect.centery), (rect.right - 30, rect.centery + 10), 2)
    # Centerline
    pygame.draw.line(surface, (255, 255, 255), (rect.centerx, rect.top), (rect.centerx, rect.bottom), 2)

# Draw obstacles as irregular meteor shapes
def draw_obstacle(surface, rect):
    points = [
        (rect.centerx, rect.top),  # Top point
        (rect.right, rect.top + rect.height // 4),  # Top-right
        (rect.right - rect.width // 4, rect.bottom),  # Bottom-right
        (rect.left + rect.width // 4, rect.bottom),  # Bottom-left
        (rect.left, rect.top + rect.height // 4)  # Top-left
    ]
    pygame.draw.polygon(surface, (139, 69, 19), points)  # Brown color for meteor
    # Add craters
    pygame.draw.circle(surface, (105, 105, 105), (rect.centerx, rect.centery), rect.width // 6)  # Center crater
    pygame.draw.circle(surface, (105, 105, 105), (rect.left + rect.width // 4, rect.top + rect.height // 4), rect.width // 8)  # Top-left crater
    pygame.draw.circle(surface, (105, 105, 105), (rect.right - rect.width // 4, rect.bottom - rect.height // 4), rect.width // 8)  # Bottom-right crater

# Draw power-up
def draw_powerup(surface, rect):
    pygame.draw.ellipse(surface, BLUE, rect)

# Draw bullets
def draw_bullet(surface, rect):
    pygame.draw.rect(surface, WHITE, rect)

# Draw explosion
def draw_explosion(surface, explosion):
    pygame.draw.circle(surface, RED, explosion["pos"], explosion["radius"])

# Draw button
def draw_button(surface, text, x, y, width, height, color, text_color):
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surface, color, button_rect)
    text_surface = button_font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=button_rect.center)
    surface.blit(text_surface, text_rect)
    return button_rect

# Reset game state
def reset_game():
    global plane, obstacles, powerups, bullets, score, obstacle_speed
    plane = pygame.Rect(WIDTH // 2 - PLANE_WIDTH // 2, HEIGHT - 100, PLANE_WIDTH, PLANE_HEIGHT)
    obstacles.clear()
    powerups.clear()
    bullets.clear()
    score = 0
    obstacle_speed = 5  # Reset obstacle speed

# Game over screen
def game_over_screen():
    while True:
        screen.fill(BLACK)
        game_over_text = button_font.render("Game Over!", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 100))

        # Draw restart button
        restart_button = draw_button(screen, "Restart", WIDTH // 2 - 100, HEIGHT // 2, 200, 50, RED, WHITE)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    reset_game()
                    return

        pygame.display.flip()
        clock.tick(60)

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

    # Bullet firing
    bullet_timer += 1
    if keys[pygame.K_SPACE] and bullet_timer >= bullet_delay:  # Fire bullet with delay
        bullet = pygame.Rect(plane.centerx - BULLET_WIDTH // 2, plane.top - BULLET_HEIGHT, BULLET_WIDTH, BULLET_HEIGHT)
        bullets.append(bullet)
        bullet_timer = 0  # Reset bullet timer

    # Spawn obstacles
    obstacle_timer += 1
    if obstacle_timer >= obstacle_spawn_delay:
        obstacle_timer = 0
        obstacle_x = random.randint(0, WIDTH - OBSTACLE_WIDTH)
        obstacle = pygame.Rect(obstacle_x, 0, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
        obstacles.append(obstacle)

    # Spawn power-ups
    powerup_timer += 1
    if powerup_timer >= powerup_spawn_delay:
        powerup_timer = 0
        powerup_x = random.randint(0, WIDTH - POWERUP_WIDTH)
        powerup = pygame.Rect(powerup_x, 0, POWERUP_WIDTH, POWERUP_HEIGHT)
        powerups.append(powerup)

    # Move bullets
    for bullet in bullets[:]:
        bullet.move_ip(0, bullet_speed)
        if bullet.bottom < 0:  # Remove bullets that go off-screen
            bullets.remove(bullet)

    # Move obstacles
    for obstacle in obstacles[:]:
        obstacle.move_ip(0, obstacle_speed)
        if obstacle.top > HEIGHT:  # Remove obstacles that go off-screen
            obstacles.remove(obstacle)
            score += 1  # Increase score for avoiding an obstacle

    # Move power-ups
    for powerup in powerups[:]:
        powerup.move_ip(0, obstacle_speed)
        if powerup.top > HEIGHT:  # Remove power-ups that go off-screen
            powerups.remove(powerup)

    # Check for collisions with obstacles
    for bullet in bullets[:]:
        for obstacle in obstacles[:]:
            if bullet.colliderect(obstacle):
                bullets.remove(bullet)
                obstacles.remove(obstacle)
                score += 10  # Increase score for destroying an obstacle
                # Add explosion effect
                explosions.append({"pos": obstacle.center, "radius": 10, "lifetime": EXPLOSION_LIFETIME})
                break

    for obstacle in obstacles:
        if plane.colliderect(obstacle):
            print("Game Over!")
            game_over_screen()
            running = False

    # Check for collisions with power-ups
    for powerup in powerups[:]:
        if plane.colliderect(powerup):
            powerups.remove(powerup)
            score += powerup_score_bonus  # Increase score for collecting a power-up

    # Increase difficulty over time
    obstacle_speed += 0.001  # Gradually increase obstacle speed

    # Update explosions
    for explosion in explosions[:]:
        explosion["radius"] += 2  # Increase explosion radius
        explosion["lifetime"] -= 1
        if explosion["lifetime"] <= 0:
            explosions.remove(explosion)

    # Draw player, bullets, obstacles, power-ups, explosions, and score
    draw_plane(screen, plane)
    for bullet in bullets:
        draw_bullet(screen, bullet)
    for obstacle in obstacles:
        draw_obstacle(screen, obstacle)
    for powerup in powerups:
        draw_powerup(screen, powerup)
    for explosion in explosions:
        draw_explosion(screen, explosion)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Update display
    pygame.display.flip()
    clock.tick(60)

# Ensure proper cleanup
pygame.quit()
sys.exit()

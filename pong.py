import pygame

# Start pygame
pygame.init()

# Create the game window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pong - Part 1")

# Create a clock to control frame rate
clock = pygame.time.Clock()

# Create the player paddle
player = pygame.Rect(750, 250, 10, 100)
player_speed = 0

# Create the ball
ball = pygame.Rect(390, 290, 20, 20)
ball_speed_x = 4
ball_speed_y = 4

# Game loop control
running = True

while running:
    # Read all events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_k:
                player_speed = -5
            if event.key == pygame.K_m:
                player_speed = 5

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_k or event.key == pygame.K_m:
                player_speed = 0

    # Move the player paddle
    player.y += player_speed

    # Keep paddle inside the screen
    if player.top < 0:
        player.top = 0
    if player.bottom > 600:
        player.bottom = 600

    # Move the ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Bounce ball off top and bottom walls
    if ball.top <= 0 or ball.bottom >= 600:
        ball_speed_y *= -1

    # Clear screen
    screen.fill((0, 0, 0))

    # Draw player paddle
    pygame.draw.rect(screen, (255, 255, 255), player)

    # Draw ball
    pygame.draw.rect(screen, (255, 255, 255), ball)

    # Update display
    pygame.display.update()

    # Run at 60 frames per second
    clock.tick(60)

# Safely close pygame
pygame.quit()
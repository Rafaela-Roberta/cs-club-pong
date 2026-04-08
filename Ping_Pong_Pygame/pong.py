import pygame
import random
import sys

# -----------------------------
# CONFIG
# -----------------------------
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (170, 170, 170)

PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
BALL_SIZE = 20

PLAYER_SPEED = 6
CPU_SPEED = 5   # slower on purpose, easier to beat
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

WIN_SCORE = 5

CPU_NAMES = ["Pixel", "Nova", "Byte", "Echo", "Bolt", "Orbit"]


# -----------------------------
# DRAW TEXT
# -----------------------------
def draw_text(screen, text, font, color, x, y, center=False):
    surface = font.render(text, True, color)
    rect = surface.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(surface, rect)


# -----------------------------
# NAME INPUT SCREEN
# -----------------------------
def get_player_name(screen, clock):
    font_title = pygame.font.SysFont("Consolas", 40)
    font_text = pygame.font.SysFont("Consolas", 28)
    input_box = pygame.Rect(SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 - 25, 360, 50)
    player_name = ""

    while True:
        screen.fill(BLACK)

        draw_text(screen, "Enter your name", font_title, WHITE, SCREEN_WIDTH // 2, 220, center=True)
        draw_text(screen, "Press ENTER to start", font_text, GRAY, SCREEN_WIDTH // 2, 280, center=True)

        pygame.draw.rect(screen, WHITE, input_box, 2)
        draw_text(screen, player_name, font_text, WHITE, input_box.x + 10, input_box.y + 10)

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if player_name.strip() != "":
                        return player_name.strip()
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    if len(player_name) < 14 and event.unicode.isprintable():
                        player_name += event.unicode


# -----------------------------
# PLAY AGAIN SCREEN
# -----------------------------
def play_again_screen(screen, clock, winner_text, final_score_text):
    font_big = pygame.font.SysFont("Consolas", 42)
    font_small = pygame.font.SysFont("Consolas", 28)

    while True:
        screen.fill(BLACK)

        draw_text(screen, winner_text, font_big, WHITE, SCREEN_WIDTH // 2, 250, center=True)
        draw_text(screen, final_score_text, font_small, WHITE, SCREEN_WIDTH // 2, 320, center=True)
        draw_text(screen, "Play again? Y / N", font_small, GRAY, SCREEN_WIDTH // 2, 390, center=True)

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    return True
                if event.key == pygame.K_n:
                    return False


# -----------------------------
# ONE MATCH
# -----------------------------
def play_match(screen, clock, player_name, cpu_name):
    font_score = pygame.font.SysFont("Consolas", 28)
    font_start = pygame.font.SysFont("Consolas", 30)

    # paddles
    cpu_paddle = pygame.Rect(40, SCREEN_HEIGHT // 2 - 50, PADDLE_WIDTH, PADDLE_HEIGHT)
    player_paddle = pygame.Rect(SCREEN_WIDTH - 50, SCREEN_HEIGHT // 2 - 50, PADDLE_WIDTH, PADDLE_HEIGHT)

    # ball
    ball = pygame.Rect(SCREEN_WIDTH // 2 - BALL_SIZE // 2,
                       SCREEN_HEIGHT // 2 - BALL_SIZE // 2,
                       BALL_SIZE, BALL_SIZE)

    ball_speed_x = random.choice([-BALL_SPEED_X, BALL_SPEED_X])
    ball_speed_y = random.choice([-BALL_SPEED_Y, BALL_SPEED_Y])

    player_score = 0
    cpu_score = 0
    player_move = 0

    started = False

    while True:
        screen.fill(BLACK)

        # middle line
        pygame.draw.line(screen, GRAY, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT), 2)

        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if not started and event.key == pygame.K_SPACE:
                    started = True

                if event.key == pygame.K_k:
                    player_move = -PLAYER_SPEED
                if event.key == pygame.K_m:
                    player_move = PLAYER_SPEED

            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_k, pygame.K_m]:
                    player_move = 0

        # start message
        if not started:
            draw_text(screen, "Press SPACE to start", font_start, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, center=True)

        # player movement
        player_paddle.y += player_move

        if player_paddle.top < 0:
            player_paddle.top = 0
        if player_paddle.bottom > SCREEN_HEIGHT:
            player_paddle.bottom = SCREEN_HEIGHT

        # easy CPU movement
        # only follows the ball if the ball is on the left half
        if started and ball.centerx < SCREEN_WIDTH // 2:
            if cpu_paddle.centery < ball.centery - 10:
                cpu_paddle.y += CPU_SPEED
            elif cpu_paddle.centery > ball.centery + 10:
                cpu_paddle.y -= CPU_SPEED

        if cpu_paddle.top < 0:
            cpu_paddle.top = 0
        if cpu_paddle.bottom > SCREEN_HEIGHT:
            cpu_paddle.bottom = SCREEN_HEIGHT

        # ball movement
        if started:
            ball.x += ball_speed_x
            ball.y += ball_speed_y

        # bounce top and bottom
        if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
            ball_speed_y *= -1

        # paddle collisions
        if ball.colliderect(cpu_paddle) and ball_speed_x < 0:
            ball_speed_x *= -1

        if ball.colliderect(player_paddle) and ball_speed_x > 0:
            ball_speed_x *= -1

        # score
        if ball.left <= 0:
            player_score += 1
            started = False
            ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            ball_speed_x = random.choice([-BALL_SPEED_X, BALL_SPEED_X])
            ball_speed_y = random.choice([-BALL_SPEED_Y, BALL_SPEED_Y])

        if ball.right >= SCREEN_WIDTH:
            cpu_score += 1
            started = False
            ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            ball_speed_x = random.choice([-BALL_SPEED_X, BALL_SPEED_X])
            ball_speed_y = random.choice([-BALL_SPEED_Y, BALL_SPEED_Y])

        # draw paddles and ball
        pygame.draw.rect(screen, WHITE, cpu_paddle)
        pygame.draw.rect(screen, WHITE, player_paddle)
        pygame.draw.rect(screen, WHITE, ball)

        # top names and score
        draw_text(screen, f"{cpu_name}: {cpu_score}", font_score, WHITE, 40, 20)
        draw_text(screen, f"{player_name}: {player_score}", font_score, WHITE, SCREEN_WIDTH - 250, 20)

        pygame.display.flip()
        clock.tick(60)

        # win condition
        if player_score == WIN_SCORE:
            return f"{player_name} wins!", f"Final Score: {cpu_name} {cpu_score} - {player_score} {player_name}"

        if cpu_score == WIN_SCORE:
            return f"{cpu_name} wins!", f"Final Score: {cpu_name} {cpu_score} - {player_score} {player_name}"


# -----------------------------
# MAIN
# -----------------------------
def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pong - CS Club")
    clock = pygame.time.Clock()

    player_name = get_player_name(screen, clock)

    while True:
        cpu_name = random.choice(CPU_NAMES)

        winner_text, final_score_text = play_match(screen, clock, player_name, cpu_name)

        again = play_again_screen(screen, clock, winner_text, final_score_text)

        if not again:
            pygame.quit()
            sys.exit()


if __name__ == "__main__":
    main()
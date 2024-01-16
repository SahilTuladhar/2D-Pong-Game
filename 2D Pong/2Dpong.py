import pygame
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Window dimensions
width, height = 800, 600

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)

# Set up the display
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Pong')

# Font for displaying UI
font = pygame.font.Font(None, 60)
small_font = pygame.font.Font(None, 36)

clock = pygame.time.Clock()

# Function to get player names
def get_player_names():
    player1_input = ""
    player2_input = ""
    active_input = "Player 1"
    input_finished = False

    while not input_finished:
        screen.fill(black)
        player1_name = font.render(f"Player 1: {player1_input}", True, white)
        player2_name = font.render(f"Player 2: {player2_input}", True, white)
        active_text = font.render(f"Enter Name for {active_input}", True, white)
        screen.blit(player1_name, (width - 300, height // 2 - 30))
        screen.blit(player2_name, (50, height // 2 - 30))
        screen.blit(active_text, (width // 2 - active_text.get_width() // 2, height // 3))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    if active_input == "Player 1":
                        active_input = "Player 2"
                    else:
                        input_finished = True
                elif event.key == K_BACKSPACE:
                    if active_input == "Player 1":
                        player1_input = player1_input[:-1]
                    else:
                        player2_input = player2_input[:-1]
                else:
                    if active_input == "Player 1" and len(player1_input) < 15:
                        player1_input += event.unicode
                    elif active_input == "Player 2" and len(player2_input) < 15:
                        player2_input += event.unicode

    return player1_input, player2_input

# Get player names
player1_name, player2_name = get_player_names()

# Define game objects
ball = pygame.Rect(width // 2 - 15, height // 2 - 15, 30, 30)
player1 = pygame.Rect(width - 20, height // 2 - 60, 10, 120)
player2 = pygame.Rect(10, height // 2 - 60, 10, 120)

# Define ball speed and score
ball_speed_x = 0
ball_speed_y = 0
player1_speed = 0
player2_speed = 0
player1_score = 0
player2_score = 0

# Load sound effects
hit_sound = pygame.mixer.Sound("Sounds/ball_hit.mp3")
game_over_sound = pygame.mixer.Sound("Sounds/game-over.mp3")

# Function to display the starting UI
def display_start_screen():
    screen.fill(black)
    title_text = font.render("Pong Game", True, white)
    instruction_text = small_font.render("Press Space to Start", True, white)
    screen.blit(title_text, (width // 2 - title_text.get_width() // 2, height // 3))
    screen.blit(instruction_text, (width // 2 - instruction_text.get_width() // 2, height // 2))
    pygame.display.flip()

# Game loop
running = True
game_started = False
ball_moving = False
winner = None

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                if not game_started:
                    game_started = True

    if game_started:
        keys = pygame.key.get_pressed()
        # Player 1 controls
        if keys[K_UP] and player1.top > 0:
            player1_speed = -5
        elif keys[K_DOWN] and player1.bottom < height:
            player1_speed = 5
        else:
            player1_speed = 0

        # Player 2 controls
        if keys[K_w] and player2.top > 0:
            player2_speed = -5
        elif keys[K_s] and player2.bottom < height:
            player2_speed = 5
        else:
            player2_speed = 0

        # Update player positions
        player1.y += player1_speed
        player2.y += player2_speed

        if ball_moving:
            ball.x += ball_speed_x
            ball.y += ball_speed_y

            # Ball collision with walls and paddles
            if ball.top <= 0 or ball.bottom >= height:
                ball_speed_y *= -1
            if ball.colliderect(player1) or ball.colliderect(player2):
                ball_speed_x *= -1
                hit_sound.play()

            # Increase scores and reset ball position if it goes off the sides
            if ball.left <= 0:
                player1_score += 1
                ball_speed_x *= -1
                ball.x = width // 2 - 15
                ball.y = height // 2 - 15
                ball_moving = False
            if ball.right >= width:
                player2_score += 1
                ball_speed_x *= -1
                ball.x = width // 2 - 15
                ball.y = height // 2 - 15
                ball_moving = False

            # Check if a player has reached five points (first to five)
            if player1_score == 5:
                winner = player1_name
            elif player2_score == 5:
                winner = player2_name

            if winner:
                game_over_sound.play()
                winner_text = font.render(f"{winner} wins! Press Space to Restart", True, white)
                screen.blit(winner_text, (width // 2 - winner_text.get_width() // 2, height // 2))
                pygame.display.flip()

                restart = False
                while not restart:
                 for event in pygame.event.get():
                  if event.type == QUIT:
                    running = False
                    restart = True
                  if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        restart = True
                        player1_score = 0
                        player2_score = 0
                        ball_speed_x = 0
                        ball_speed_y = 0
                        winner = None
                        game_started = False
                        ball_moving = False
                        break 

        screen.fill(black)
        pygame.draw.rect(screen, white, player1)
        pygame.draw.rect(screen, white, player2)
        pygame.draw.ellipse(screen, white, ball)

        player1_text = font.render(f"{player1_name}: {player1_score}", True, white)
        player2_text = font.render(f"{player2_name}: {player2_score}", True, white)
        screen.blit(player1_text, (width - 250, height // 2 - 30))
        screen.blit(player2_text, (50, height // 2 - 30))

        if winner:
            winner_text = font.render(f"{winner} wins!", True, white)
            screen.blit(winner_text, (width // 2 - winner_text.get_width() // 2, height // 2))

        if not ball_moving:
            ready_text = small_font.render("Press 'Enter' to Start the Ball", True, white)
            screen.blit(ready_text, (width // 2 - ready_text.get_width() // 2, height // 2 + 50))

            if keys[K_RETURN]:
                ball_speed_x = 7
                ball_speed_y = 7
                ball_moving = True
                winner = None

    else:
        display_start_screen()  # Display the starting UI

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

import pygame, sys, time, random

# Difficulty settings
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
# Harder    ->  60
# Impossible->  120
difficulty = 25

# Window size
frame_size_x = 720
frame_size_y = 480

# Checks for errors encountered
check_errors = pygame.init()
# pygame.init() example output -> (6, 0)
# second number in tuple gives number of errors
if check_errors[1] > 0:
    print(f"[!] Had {check_errors[1]} errors when initialising game, exiting...")
    sys.exit(-1)
else:
    print("[+] Game successfully initialised")

# Initialise game window
pygame.display.set_caption("Snake Eater")
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))

# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# FPS (frames per second) controller
fps_controller = pygame.time.Clock()

# Game variables
snake_pos = [[100, 50], [90, 50], [80, 50]]
snake_body = [[100, 50], [90, 50], [80, 50]]

snake2_pos = [
    [frame_size_x - 100, frame_size_y - 50],
    [frame_size_x - 90, frame_size_y - 50],
    [frame_size_x - 80, frame_size_y - 50],
]
snake2_body = [
    [frame_size_x - 100, frame_size_y - 50],
    [frame_size_x - 90, frame_size_y - 50],
    [frame_size_x - 80, frame_size_y - 50],
]

food_pos = [
    random.randrange(1, (frame_size_x // 10)) * 10,
    random.randrange(1, (frame_size_y // 10)) * 10,
]
food_spawn = True

direction = "RIGHT"
change_to = direction

direction2 = "LEFT"
change_to2 = direction2

score = 0
score2 = 0


# Game Over
def game_over():
    my_font = pygame.font.SysFont("times new roman", 90)
    game_over_surface = my_font.render("YOU DIED", True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x / 2, frame_size_y / 4)
    game_window.fill(black)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(0, red, "times", 20)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()


# Score
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render(
        "Score 1: " + str(score) + "  Score 2: " + str(score2), True, color
    )
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x / 10, 15)
    else:
        score_rect.midtop = (frame_size_x / 2, frame_size_y / 1.25)
    game_window.blit(score_surface, score_rect)


def is_safe(pos, other_snake):
    for block in other_snake:
        if pos[0] == block[0] and pos[1] == block[1]:
            return False
    return True


# Main logic
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Whenever a key is pressed down
        elif event.type == pygame.KEYDOWN:
            # Snake 1 controls
            if event.key == pygame.K_UP:
                if direction != "DOWN":
                    change_to = "UP"
            if event.key == pygame.K_DOWN:
                if direction != "UP":
                    change_to = "DOWN"
            if event.key == pygame.K_LEFT:
                if direction != "RIGHT":
                    change_to = "LEFT"
            if event.key == pygame.K_RIGHT:
                if direction != "LEFT":
                    change_to = "RIGHT"
            # Snake 2 controls
            if event.key == ord("w"):
                if direction2 != "DOWN":
                    change_to2 = "UP"
            if event.key == ord("s"):
                if direction2 != "UP":
                    change_to2 = "DOWN"
            if event.key == ord("a"):
                if direction2 != "RIGHT":
                    change_to2 = "LEFT"
            if event.key == ord("d"):
                if direction2 != "LEFT":
                    change_to2 = "RIGHT"
            # Esc -> Create event to quit the game
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    # Making sure the snake cannot move in the opposite direction instantaneously
    if change_to == "UP" and direction != "DOWN":
        direction = "UP"
    if change_to == "DOWN" and direction != "UP":
        direction = "DOWN"
    if change_to == "LEFT" and direction != "RIGHT":
        direction = "LEFT"
    if change_to == "RIGHT" and direction != "LEFT":
        direction = "RIGHT"

    if change_to2 == "UP" and direction2 != "DOWN":
        direction2 = "UP"
    if change_to2 == "DOWN" and direction2 != "UP":
        direction2 = "DOWN"
    if change_to2 == "LEFT" and direction2 != "RIGHT":
        direction2 = "LEFT"
    if change_to2 == "RIGHT" and direction2 != "LEFT":
        direction2 = "RIGHT"

    # Moving the snake 1
    if direction == "UP":
        snake_pos[0][1] -= 10
    if direction == "DOWN":
        snake_pos[0][1] += 10
    if direction == "LEFT":
        snake_pos[0][0] -= 10
    if direction == "RIGHT":
        snake_pos[0][0] += 10

    # Moving the snake 2
    if direction2 == "UP":
        snake2_pos[0][1] -= 10
    if direction2 == "DOWN":
        snake2_pos[0][1] += 10
    if direction2 == "LEFT":
        snake2_pos[0][0] -= 10
    if direction2 == "RIGHT":
        snake2_pos[0][0] += 10

    # Snake 1 body growing mechanism
    snake_body.insert(0, list(snake_pos[0]))
    if snake_pos[0][0] == food_pos[0] and snake_pos[0][1] == food_pos[1]:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()

    # Snake 2 body growing mechanism
    snake2_body.insert(0, list(snake2_pos[0]))
    if snake2_pos[0][0] == food_pos[0] and snake2_pos[0][1] == food_pos[1]:
        score2 += 1
        food_spawn = False
    else:
        snake2_body.pop()

    # Spawning food on the screen
    if not food_spawn:
        food_pos = [
            random.randrange(1, (frame_size_x // 10)) * 10,
            random.randrange(1, (frame_size_y // 10)) * 10,
        ]
    food_spawn = True

    # GFX
    game_window.fill(black)
    for pos in snake_body:
        # Snake 1 body
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

    for pos in snake2_body:
        # Snake 2 body
        pygame.draw.rect(game_window, blue, pygame.Rect(pos[0], pos[1], 10, 10))

    # Snake food
    pygame.draw.rect(game_window, white, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    # Game Over conditions
    # Snake 1 out of bounds
    if (
        snake_pos[0][0] < 0
        or snake_pos[0][0] > frame_size_x - 10
        or snake_pos[0][1] < 0
        or snake_pos[0][1] > frame_size_y - 10
    ):
        game_over()
    # Snake 2 out of bounds
    if (
        snake2_pos[0][0] < 0
        or snake2_pos[0][0] > frame_size_x - 10
        or snake2_pos[0][1] < 0
        or snake2_pos[0][1] > frame_size_y - 10
    ):
        game_over()
    # Snake 1 touching its own body
    for block in snake_body[1:]:
        if snake_pos[0][0] == block[0] and snake_pos[0][1] == block[1]:
            game_over()
    # Snake 2 touching its own body
    for block in snake2_body[1:]:
        if snake2_pos[0][0] == block[0] and snake2_pos[0][1] == block[1]:
            game_over()
    # Snake 1 touching Snake 2 body
    for block in snake2_body:
        if snake_pos[0][0] == block[0] and snake_pos[0][1] == block[1]:
            game_over()
    # Snake 2 touching Snake 1 body
    for block in snake_body:
        if snake2_pos[0][0] == block[0] and snake2_pos[0][1] == block[1]:
            game_over()

    show_score(1, white, "consolas", 20)
    # Refresh game screen
    pygame.display.update()
    # Refresh rate
    fps_controller.tick(difficulty)

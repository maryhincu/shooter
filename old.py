import pygame
import sys
from random import randint


pygame.init()

game_font = pygame.font.Font(None, 30)

screen_width, screen_height = 800, 600
screen_fill_color = (32, 52, 71)
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Awesome Shooter Game")

FIGHTER_STEP = 2
fighter_image = pygame.image.load('images/fighter.png')
fighter_width, fighter_height = fighter_image.get_size()
fighter_x = screen_width/2 - fighter_width/2
fighter_y = screen_height - fighter_height
fighter_is_moving_left, fighter_is_moving_right = False, False

rocket_image = pygame.image.load('images/rocket.png')
rocket_width, rocket_height = rocket_image.get_size()

ROCKET_STEP = 2
rocket_was_fired = False
rockets = []

alien_image = pygame.image.load('images/alien.png')
alien_width, alien_height = alien_image.get_size()

ALIEN_STEP = 0.3
alien_speed = ALIEN_STEP
alien_x = randint(0, screen_width - alien_width)
alien_y = 0

game_is_running = True

game_score = 0

while game_is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                fighter_is_moving_left = True
            if event.key == pygame.K_RIGHT:
                fighter_is_moving_right = True
            if event.key == pygame.K_SPACE and len(rockets) < 100:
                rockets.append([fighter_x + fighter_width / 2 - rocket_width / 2, fighter_y - rocket_height])
                rocket_was_fired = True
        print(rockets)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                fighter_is_moving_left = False
            if event.key == pygame.K_RIGHT:
                fighter_is_moving_right = False

    if fighter_is_moving_left and fighter_x >= FIGHTER_STEP:
        fighter_x -= FIGHTER_STEP
    if fighter_is_moving_right and screen_width - fighter_width - FIGHTER_STEP > fighter_x:
        fighter_x += FIGHTER_STEP

    alien_y += alien_speed

    for rocket in rockets:
        if rocket_was_fired:
            rocket[1] -= ROCKET_STEP

    screen.fill(screen_fill_color)
    screen.blit(fighter_image, (fighter_x, fighter_y))
    screen.blit(alien_image, (alien_x, alien_y))

    for rocket in rockets:
        if rocket_was_fired:
            screen.blit(rocket_image, (rocket[0], rocket[1]))

    game_score_text = game_font.render(f"Your score is: {game_score}", True, 'white')
    screen.blit(game_score_text, (20, 20))

    pygame.display.update()

    if alien_y + alien_height > fighter_y:
        game_is_running = False

    for rocket in rockets:
        if (rocket_was_fired and
                alien_x < rocket[0] < alien_x + alien_width - rocket_width and
                alien_y < rocket[1] < alien_y + alien_height - rocket_height):
            rocket_was_fired = False
            alien_x, alien_y = randint(0, screen_width - alien_width), 0
            alien_speed += ALIEN_STEP / 10
            game_score += 1

game_over_text = game_font.render("Game Over", True, 'white')
game_over_rectangle = game_over_text.get_rect()
game_over_rectangle.center = (screen_width / 2, screen_height / 2)
screen.blit(game_over_text, game_over_rectangle)
pygame.display.update()
pygame.time.wait(5000)

pygame.quit()

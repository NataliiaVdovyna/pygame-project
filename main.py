import random
import os

import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

FPS = pygame.time.Clock()

HEIGHT = 800
WIDTH = 1200

FONT = pygame.font.SysFont('Verdana', 20) 
FONT2 =  pygame.font.SysFont('Verdana', 100)



COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_RED = (255, 0, 0)

main_display = pygame.display.set_mode((WIDTH, HEIGHT))

bg = pygame.transform.scale(pygame.image.load('background.png'), (WIDTH, HEIGHT))
bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 5

IMAGE_PATH = "goose"
PLAYER_IMAGES = os.listdir(IMAGE_PATH)

player_size = (40, 40)
player = pygame.image.load('player.png').convert_alpha() 
player = pygame.transform.scale(player, player_size)
player_rect = player.get_rect()

player_move_down = [0, 6]
player_move_right = [6, 0]
player_move_up = [0, -6]
player_move_left = [-6, 0]

def create_enemy():
    enemy_size = (2, 2)
    enemy = pygame.image.load('enemy.png').convert_alpha() 
    enemy_rect = pygame.Rect(WIDTH, random.randint(0, HEIGHT - enemy_size[1]), *enemy_size)
    enemy_move = [random.randint(-8, -8), 0]
    return [enemy, enemy_rect, enemy_move]

def create_bonus():
    bonus_size = (20, 20)
    bonus = pygame.image.load('bonus.png').convert_alpha() 
    bonus_rect = pygame.Rect(random.randint(0, WIDTH), 0, *bonus_size)
    bonus_move = [0, random.randint(1, 7)]
    return [bonus, bonus_rect, bonus_move]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)
CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 3000)
CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMAGE, 200)

enemies = []
bonuses = []

score = 0

image_index = 0

playing = True

waiting_for_key = True

while playing:
    FPS.tick(220)

    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        if event.type == CHANGE_IMAGE:
            player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index]))
            image_index += 1
            if image_index >= len(PLAYER_IMAGES):
                image_index = 0
        elif event.type == pygame.KEYDOWN:
            if waiting_for_key:
                waiting_for_key = False
            else:
                if event.key == pygame.K_ESCAPE:
                    playing = True

    if waiting_for_key:
        start_text = FONT.render("Press 'SPACE' key to start", True, COLOR_WHITE)
        main_display.blit(start_text, (WIDTH / 2 - 120, HEIGHT / 2 - 20))
        pygame.display.flip()
        continue

    bg_X1 -= bg_move
    bg_X2 -= bg_move

    if bg_X1 < -bg.get_width():
        bg_X1 = bg.get_width()

    if bg_X2 < -bg.get_width():
        bg_X2 = bg.get_width()

    main_display.blit(bg, (bg_X1, 0))
    main_display.blit(bg, (bg_X2, 0))

    keys = pygame.key.get_pressed()

    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)

    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)

    if keys[K_UP] and player_rect.top > 0:
        player_rect = player_rect.move(player_move_up)

    if keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)

    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])

        if player_rect.colliderect(enemy[1]):
            playing = False

    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])

        if player_rect.colliderect(bonus[1]):
            score += 1
            bonuses.pop(bonuses.index(bonus))

    #main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH / 2, HEIGHT / 2))
    #main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH - FONT.size(str(score))[0], 10))
    margin_left = 10 
    margin_down = 10
    main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH - FONT.size(str(score))[0] - margin_left, margin_down))


    main_display.blit(player, player_rect)

    pygame.display.flip()

    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

    for bonus in bonuses:
        if bonus[1].bottom < 0:
            bonuses.pop(bonuses.index(bonus))

# Виведення "Game Over"
if not playing:
    game_over_text = FONT2.render("GAME OVER", True, COLOR_RED)
    #main_display.blit(game_over_text, (WIDTH / 2 - 120, HEIGHT / 2 - 20))
    text_rect = game_over_text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
main_display.blit(game_over_text, text_rect)
pygame.display.flip()

pygame.time.delay(500)  # Затримка перед завершенням програми (2000 мілісекунд або 2 секунди)
pygame.quit()

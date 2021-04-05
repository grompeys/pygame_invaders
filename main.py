# pylint: disable=import-error
import pygame
from pygame import mixer
# pylint: enable=import-error
import math
import random

pygame.init()

# Width, Height
screen = pygame.display.set_mode((800, 600))

# Title and icon
pygame.display.set_caption("Pygame Invaders")
icon = pygame.image.load('assets/ufo-outline.png')
pygame.display.set_icon(icon)

# Background
background = pygame.image.load('assets/wtm_blrd_800-600.png')
mixer.music.load('assets/background.wav')
mixer.music.play(-1)

# Player Sprite and coordinates
player_sprite = pygame.image.load('assets/ship_J.png')
playerX = 368
playerX_move = 0
playerY = 500

# Torpedo sprite
torpedo_sprite = pygame.image.load('assets/star_tiny.png')
torpedoX = 0
torpedoY = 500
torpedoY_move = 16
torpedo_state = 'ready'
torpedo_sound = mixer.Sound('assets/laser.wav')
collision_sound = mixer.Sound('assets/explosion.wav')

# Enemies
enemies_sprites = ['assets/enemy_A.png', 'assets/enemy_B.png',
                   'assets/enemy_C.png', 'assets/enemy_D.png', 'assets/enemy_E.png']

enemy_sprite = []
enemyX = []
enemyY = []
enemyX_move = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_sprite.append(pygame.image.load(random.choice(enemies_sprites)))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(0, 100))
    enemyX_move.append(1.2)


# Score
score_value = 0
score_font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game Over
go_font = pygame.font.Font('freesansbold.ttf', 64)


def player(x, y):
    # draw a sprite on the screen:
    # takes the image and the x,y to draw to
    screen.blit(player_sprite, (x, y))


def fire_torpedo(x, y):
    global torpedo_state
    torpedo_state = 'fire'
    screen.blit(torpedo_sprite, (x, y - 26))


def enemy(x, y, i):
    screen.blit(enemy_sprite[i], (x, y))


def isCollision(enemyX, enemyY, torpedoX, torpedoY):
    distance = math.sqrt(math.pow(enemyX - torpedoX, 2) +
                         math.pow(enemyY - torpedoY, 2))
    if distance < 27:
        return True
    return False


def show_score(x, y):
    score = score_font.render(F'Score: {score_value}', True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    game_over = go_font.render(F'Game Over', True, (255, 255, 255))
    screen.blit(game_over, (250, 250))


running = True
while running:
    screen.fill((0, 96, 100))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_move = -2
            if event.key == pygame.K_RIGHT:
                playerX_move = 2
            if event.key == pygame.K_SPACE:
                if torpedo_state == 'ready':
                    torpedo_sound.play()
                    torpedoX = playerX
                    fire_torpedo(torpedoX, torpedoY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_move = 0

    playerX += playerX_move

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movement

    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 468:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            mixer.music.stop()
            break

        enemyX[i] += enemyX_move[i]
        if enemyX[i] <= 0:
            enemyX[i] = 0
            enemyX_move[i] = 1.2
            enemyY[i] += 32
        elif enemyX[i] >= 736:
            enemyX[i] = 736
            enemyX_move[i] = -1.2
            enemyY[i] += 32

        collision = isCollision(enemyX[i], enemyY[i], torpedoX, torpedoY)
        if collision:
            collision_sound.play()
            torpedoY = 500
            torpedo_state = 'ready'
            score_value += 10
            enemy_sprite[i] = pygame.image.load(random.choice(enemies_sprites))
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(0, 100)

        enemy(enemyX[i], enemyY[i], i)

    if torpedoY <= 0:
        torpedoY = 500
        torpedo_state = 'ready'

    if torpedo_state == 'fire':
        fire_torpedo(torpedoX, torpedoY)
        torpedoY -= torpedoY_move

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()

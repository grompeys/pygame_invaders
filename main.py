# pylint: disable=import-error
import pygame
# pylint: enable=import-error
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

# Enemies
enemies = ['assets/enemy_A.png', 'assets/enemy_B.png',
            'assets/enemy_C.png', 'assets/enemy_D.png', 'assets/enemy_E.png']
enemy_sprite = pygame.image.load(random.choice(enemies))
enemyX = random.randint(0, 736)
enemyX_move = 1.2
enemyY = random.randint(0, 100)


def player(x, y):
    # draw a sprite on the screen:
    # takes the image and the x,y to draw to
    screen.blit(player_sprite, (x, y))


def fire_torpedo(x, y):
    global torpedo_state
    torpedo_state = 'fire'
    screen.blit(torpedo_sprite, (x + 26, y + 26))


def enemy(x, y):
    screen.blit(enemy_sprite, (x, y))


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
                fire_torpedo(playerX, torpedoY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_move = 0
        

    playerX += playerX_move
    enemyX += enemyX_move

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    
    if enemyX <= 0:
        enemyX = 0
        enemyX_move = 1.2
        enemyY += 32
    elif enemyX >= 736:
        enemyX = 736
        enemyX_move = -1.2
        enemyY += 32
    
    if torpedo_state is 'fire':
        fire_torpedo(playerX, torpedoY)
        torpedoY -= torpedoY_move

    player(playerX, playerY)
    enemy(enemyX, enemyY)
    pygame.display.update()

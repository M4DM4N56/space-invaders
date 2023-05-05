# Space Invaders
# started on Sept. 30, 2022
# finished on Oct. 2, 2022
import random
import pygame
from pygame import mixer
import math


# initialize pygame
pygame.init()

# creates screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('wallpaper 800 600.jpg')
mixer.music.load('Abstraction - Three Red Hearts - Pixel War 2 32.wav')
mixer.music.play(-1)

# title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo_icon.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('standard gunner 128.png')
playerX = 336
playerX_change_right = 0
playerX_change_left = 0
playerY = 480

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemyNum = 7

for i in range(enemyNum):
    enemyImg.append(pygame.image.load('enemy1_128.png'))
    enemyX.append(random.randrange(1, 672))
    enemyY.append(random.randrange(1, 120))
    enemyX_change.append(.3)
    enemyY_change.append(64)

# bullet
bulletImg = pygame.image.load('standard bullet 32.png')
bulletX = 0
bulletY = 480
bulletY_change = 1
bullet_state = "ready"

# show score
score = 0
font = pygame.font.Font('minecraft.ttf', 24)

textX = 40
textY = 40

# Game Over
over_font = pygame.font.Font('minecraft.ttf', 64)


def show_score(x, y):
    score_show = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_show, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, ii):
    screen.blit(enemyImg[ii], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 48, y))


def collision(enemyx, enemyy, bulletx, bullety):
    distance = math.sqrt(math.pow(enemyx - bulletx, 2) + (math.pow(enemyy - bullety, 2)))
    if distance < 40:
        return True
    else:
        return False


# game loop
running = True
while running:
    screen.fill((255, 150, 0))
    # background
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                playerX_change_right = 1
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                playerX_change_left = -1
            if event.key == pygame.K_SPACE:
                bulletSound = mixer.Sound('loud laser 32.wav')
                bulletSound.play()
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(playerX, bulletY)
            # resets game
            if event.key == pygame.K_r:
                score = 0
                player_x = 370
                player_y = 480
                for j in range(enemyNum):
                    enemyY[j] = random.randint(1, 120)

        # un-pressing key
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                playerX_change_right = 0
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                playerX_change_left = 0

    # player bounds check
    playerX += playerX_change_right
    playerX += playerX_change_left

    if playerX >= 672:
        playerX = 672

    if playerX <= 0:
        playerX = 0

    for i in range(enemyNum):
        # Game Over
        if enemyY[i] > 440:
            for j in range(enemyNum):
                enemyY[j] = 2000
            game_over_text()
            break

        # enemy movement
        enemyX[i] += enemyX_change[i]
        if enemyX[i] >= 672:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]

        isCollision = collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if isCollision:
            explosionSound = mixer.Sound('rumble3.wav')
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score += 100
            enemyX[i] = random.randrange(1, 672)
            enemyY[i] = random.randrange(1, 120)
        enemy(enemyX[i], enemyY[i], i)

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    # bullets
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)

    pygame.display.update()

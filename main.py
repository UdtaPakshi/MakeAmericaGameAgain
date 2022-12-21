import random
import math
import pygame

# intialise karlo
pygame.init()

# screen banalo
screen = pygame.display.set_mode((900, 700))

# background banalo
bg = pygame.image.load("statue_bg1.jpg")

# MAKE AMRIKA GREAT AGAIN (title + caption)
pygame.display.set_caption("Amrika ka dalal")
icon = pygame.image.load("united-states.png")
pygame.display.set_icon(icon)

# dolun trump (player)
player_img = pygame.image.load("donald2.png")
playerX = 400
playerY = 600
playerX_change = 0

# pulis (enemy)
pulis_img = []
pulisX = []
pulisY = []
pulisX_change = []
pulisY_change = []
num = 6

for i in range(num):
    pulis_img.append(pygame.image.load("policeman.png"))
    pulisX.append(random.randint(0, 835))
    pulisY.append(random.randint(30, 200))
    pulisX_change.append(0.5)
    pulisY_change.append(10)

# bullet (ghoos)
# read == cant see the bullet
# fire == bullet is moving

bullet_img = pygame.image.load("cash2.png")
bulletX = 0
bulletY = 600
bulletX_change = 0
bulletY_change = 1.5
bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font("vanilla whale.ttf", 40)
textX = 20
textY = 20

# game over text
game_over = pygame.font.Font("vanilla whale.ttf", 150)


def game_over_text():
    over_text = game_over.render("Game Over", True, (0, 0, 0))
    screen.blit(over_text, (200, 250))


def show_score(x, y):
    score = font.render("Score:" + str(score_value), True, (0, 0, 0))
    screen.blit(score, (x, y))


def player(x, y):  # blit == drawing
    screen.blit(player_img, (x, y))


def pulis(x, y, i):
    screen.blit(pulis_img[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))


def collide(enemyx, enemyy, bulletx, bullety):
    dist = math.sqrt((math.pow(enemyx - bulletx, 2)) + (math.pow(enemyy - bullety, 2)))
    if dist < 27:
        return True
    else:
        return False


# loop jisse chalta rahega
# anything that has to remain persistent(cont. running) goes into the while loop
run = True
while run:
    screen.fill((50, 100, 100))  # fill screen with colour
    screen.blit(bg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1
            if event.key == pygame.K_RIGHT:
                playerX_change = 1
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
                    # print(bullet_state)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change  # always call player after screen (iss order main draw hoga warna)

    if playerX <= 0:
        playerX = 0
    if playerX >= 835:
        playerX = 835

    for i in range(num):

        # game over code
        if pulisY[i] > 500:
            for j in range(num):
                pulisY[j] = 2000
            game_over_text()
            break

        pulisX[i] += pulisX_change[i]

        if pulisX[i] <= 0:
            pulisX_change[i] = 0.5
            pulisY[i] += pulisY_change[i]
        if pulisX[i] >= 835:
            pulisX_change[i] = -0.5
            pulisY[i] += pulisY_change[i]

        col = collide(pulisX[i], pulisY[i], bulletX, bulletY)
        if col:
            score_value += 1
            bulletY = 600
            bullet_state = "ready"
            pulisX[i] = random.randint(0, 835)
            pulisY[i] = random.randint(30, 200)

        pulis(pulisX[i], pulisY[i], i)

    if bulletY <= 0:
        bullet_state = "ready"
        bulletY = 600

    # bullet movement
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()  # har baar karna padega

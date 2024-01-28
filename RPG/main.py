import pygame
import random
import time
import os

pygame.init()


# Screen
Width = 720
Height = 360
screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("RPG by Swayam Dhungana")

# Background
background = pygame.image.load("assets/background.jpg")

# Player
playerImg = pygame.image.load("assets/Sword-Base-Right.png")
playerX = 330
playerY = 150
playerX_change = 0
playerY_change = 0
player_change = 0.0333
playerImgBaseRight = pygame.image.load("assets/Sword-Base-Right.png")
playerImgBaseLeft = pygame.image.load("assets/Sword-Base-Left.png")
playerImgSwingRight = pygame.image.load("assets/Sword-Swing-Right.png")
playerImgSwingLeft = pygame.image.load("assets/Sword-Swing-Left.png")

def player(x, y):
    screen.blit(playerImg, (x, y))

#Enemy 
enemyIMG = []
enemyRight = pygame.image.load("assets/Skeleton-Right.png")
enemyLeft = pygame.image.load("assets/Skeleton-Left.png")
enemyX = []
enemyY = []
num_of_enemies = 6 

for i in range(num_of_enemies): 
    enemyIMG.append(pygame.image.load("assets/Skeleton-Right.png"))
    enemyX.append(random.randint(0,640))
    enemyY.append(random.randint(0,280))
def enemy(x,y,i): 
    screen.blit(enemyIMG[i], (x,y))
   
def pixel_collision(obj1, obj2, offset1, offset2):
    rect1 = obj1.get_rect(topleft=offset1)
    rect2 = obj2.get_rect(topleft=offset2)

    mask1 = pygame.mask.from_surface(obj1)
    mask2 = pygame.mask.from_surface(obj2)

    if rect1.colliderect(rect2):
        overlap = mask1.overlap(mask2, (rect2.left - rect1.left, rect2.top - rect1.top))
        return overlap is not None

    return False

# Bullet
bulletImg = pygame.image.load("assets/bullet.png")
bulletX = 0
bulletY = 0
bullet_state = "ready"  # "ready" means the bullet is not on the screen, "fire" means it's moving
bullet_speed = 0.3

# Function to draw the bullet
def fire_bullet(start_x, start_y, target_x, target_y):
    global bullet_state, bulletX, bulletY
    bullet_state = "fire"
    bulletX = start_x
    bulletY = start_y
    direction = pygame.math.Vector2(target_x - start_x, target_y - start_y).normalize()
    bullet_velocity = direction * bullet_speed
    return bullet_velocity

# Variables for bullet shooting intervals
bullet_timer = time.time()
min_interval = 2  # in seconds
max_interval = 3 # in seconds

#Score and Lives
font = pygame.font.Font('freesansbold.ttf', 25)
score = 0
lives = 5 

collision_flag = False
hit = False 

game_over_font = pygame.font.Font('freesansbold.ttf', 64)

#Background Music 
pygame.mixer.music.load("Sounds/background.mp3")
pygame.mixer.play()

running = True
while running:
 # If lives reach zero, display game over screen
    if lives <= 0:
        screen.fill((0, 0, 0))  # Fill the screen with a black color

        game_over_text = game_over_font.render("Game Over", True, (255, 255, 255))
        screen.blit(game_over_text, (Width // 2 - 150, Height // 2 - 32))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        continue  # Skip the rest of the loop and restart it

    # Background
    screen.blit(background, (0, 0))
    # Quit Game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Player Movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerImg = playerImgBaseLeft
                playerX_change = -player_change
            if event.key == pygame.K_RIGHT:
                playerImg = playerImgBaseRight
                playerX_change = player_change
            if event.key == pygame.K_UP:
                playerY_change = -player_change
            if event.key == pygame.K_DOWN:
                playerY_change = player_change
            if event.key == pygame.K_SPACE:
                is_swinging = True
                hit = True
                if playerImg == playerImgBaseRight:
                    playerImg = playerImgSwingRight
                elif playerImg == playerImgBaseLeft:
                    playerImg = playerImgSwingLeft

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0
            if event.key == pygame.K_SPACE:
                is_swinging = False
                hit = False
                if playerImg == playerImgSwingRight:
                    playerImg = playerImgBaseRight
                elif playerImg == playerImgSwingLeft:
                    playerImg = playerImgBaseLeft

    # player movement change
    playerX += playerX_change
    playerY += playerY_change

    #enemy and player collision 
    for i in range(num_of_enemies): 
        if pixel_collision(playerImg, enemyIMG[i], (playerX, playerY), (enemyX[i], enemyY[i])):
            collision_flag = True
            
        # Stop player movement if there is a collision
        if collision_flag:
            playerX_change = 0
            playerY_change = 0

        #Kill Enemy and add score
        if collision_flag and hit: 
            enemyX[i] = (random.randint(0,640))
            enemyY[i] = (random.randint(0,280))
            hit = False
            score += 1 
        
        playerX += playerX_change
        playerY += playerY_change

        collision_flag = False  # Reset the collision flag

    #Screen Boundary 
    if playerX <= -10:
        playerX = -10
    elif playerX >= 660:
        playerX = 660
    if playerY <= 0:
        playerY = 0
    elif playerY >= 295:
        playerY = 295
        
    #Enemy Animation
    for i in range(num_of_enemies):    
        if enemyX[i] > playerX:
            enemyIMG[i] = enemyLeft
        else: 
            enemyIMG[i] = enemyRight

        enemy(enemyX[i], enemyY[i],i)
    
    # Shooting bullets from enemies
    current_time = time.time()
    for i in range(num_of_enemies):
        if current_time - bullet_timer > random.uniform(min_interval, max_interval):
            if bullet_state == "ready":
                bullet_velocity = fire_bullet(enemyX[i], enemyY[i], playerX, playerY)
                bullet_timer = current_time

    # Move the bullet
    if bullet_state == "fire":
        bulletX += bullet_velocity.x
        bulletY += bullet_velocity.y
        screen.blit(bulletImg, (bulletX, bulletY))

        # Collision detection with the player
        if pixel_collision(bulletImg, playerImg, (bulletX, bulletY), (playerX, playerY)):
            print("Player is hit!")
            lives -= 1 
            bullet_state = "ready"  # Reset the bullet
            

        # Reset the bullet when it goes off the screen
        if bulletX > Width or bulletX < 0 or bulletY > Height or bulletY < 0:
            bullet_state = "ready"

    #Lievs Display 
    player_lives_text = font.render("Lives: " + str(lives), True, (255,255,255))
    screen.blit(player_lives_text, (140,20))

    #Score Display 
    player_score_text = font.render("Score: " + str(score),True,(255,255,255))
    screen.blit(player_score_text,(10,20))
            
    player(playerX, playerY)
    pygame.display.update()
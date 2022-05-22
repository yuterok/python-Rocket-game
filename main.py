import winsound
import pygame
import random
import time

pygame.init()

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 30
high_score = 0

window = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('название пока не придумала')
clock = pygame.time.Clock()
bg = pygame.image.load('img/bg.png')
font = pygame.font.Font('Baloo.ttf', 45)
h_font = pygame.font.Font('Baloo.ttf', 25)

rocket = pygame.image.load('img/yellow.png')
rocket_x = SCREEN_WIDTH/2
rocket_y = 500
rocket_width = 122
rocket_height = 233
speed = 20

asteroids_speed = 10
asteroids_x = [100, 450, 800, 900, 200]
asteroids_y = [-100, 100, 400, 400, 700]
asteroid1 = pygame.image.load('img/asteroid1.png')
asteroid2 = pygame.image.load('img/asteroid2.png')
asteroid3 = pygame.image.load('img/asteroid3.png')
asteroid4 = pygame.image.load('img/asteroid4.png')
asteroid5 = pygame.image.load('img/asteroid5.png')

def drawWindow():

    window.blit(bg, (0,0))
    window.blit(rocket, (rocket_x,rocket_y))
    window.blit(asteroid1, (asteroids_x[0],asteroids_y[0]))
    window.blit(asteroid2, (asteroids_x[1],asteroids_y[1]))
    window.blit(asteroid3, (asteroids_x[2],asteroids_y[2]))
    window.blit(asteroid4, (asteroids_x[3],asteroids_y[3]))
    window.blit(asteroid5, (asteroids_x[4],asteroids_y[4]))
    window.blit(score_text, (20,10))
    window.blit(high_score_text, (20,70))


    pygame.display.update()

run = True
while run:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and rocket_x > 5:
        rocket_x -= speed
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and rocket_x < SCREEN_WIDTH-rocket_width:
        rocket_x += speed
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and rocket_y>100:
            rocket_y -= speed
    if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and rocket_y < SCREEN_HEIGHT-rocket_height:
            rocket_y += speed
    if (keys[pygame.K_ESCAPE]):
        clock.tick(0.01)
        

    for i in range(len(asteroids_y)):
            asteroids_y[i] += asteroids_speed
            asteroids_speed +=0.002
            if asteroids_y[i] > SCREEN_HEIGHT+10:
                asteroids_y[i] = random.randint(-200,-50)
                asteroids_x[i] = random.randint(0,SCREEN_WIDTH)
    # if asteroids_speed == 15:
    #     new_asteroid_x = random.randint(0,SCREEN_WIDTH)
    #     asteroids_x.append(new_asteroid_x)
    #     asteroids_y.append(50)
    #     window.blit(rocket, (new_asteroid_x,50))
    # if asteroids_speed == 20:
    #     new_asteroid_x = random.randint(0,SCREEN_WIDTH)
    #     asteroids_x.append(new_asteroid_x)
    #     asteroids_y.append(50)
    #     window.blit(rocket, (new_asteroid_x,50))

    score = round((pygame.time.get_ticks())/50 + asteroids_speed)
    score_text = font.render(f'Score: {score}', True, (251,246,121))
    high_score_text = h_font.render(f'High score: {high_score}', True, (251,246,121))
    

    # print(round((pygame.time.get_ticks())/50 + asteroids_speed))
    # print(asteroids_speed)
    drawWindow()

pygame.quit()
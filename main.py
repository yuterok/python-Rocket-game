import pygame
import random
import time
import os

pygame.init()

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 30
f = open('high_score.txt','r')
print(*f)
high_score = 0

window = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('название пока не придумала')
clock = pygame.time.Clock()
bg = pygame.image.load('img/bg.png')
font = pygame.font.Font('Baloo.ttf', 45)
h_font = pygame.font.Font('Baloo.ttf', 25)

rocket = pygame.image.load('img/pink.png')
rocket_x = SCREEN_WIDTH/2
rocket_y = 500
rocket_width = 100
rocket_height = 191
speed = 20

asteroids_speed = 10
asteroids_x = [100, 450, 200, 900, 200]
asteroids_y = [-100, 100, 400, 400, 700]
asteroids_list = pygame.sprite.Group()

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, x, y, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect(center=(x,y))

    def update(self, asteroids_speed):
        self.rect.y += asteroids_speed  
        if self.rect.y > SCREEN_HEIGHT+10:
           self.rect.y = random.randint(-200,-50)
           self.rect.x = random.randint(0,SCREEN_WIDTH)

asteroid1 = Asteroid(asteroids_x[0], asteroids_y[0], 'img/asteroid1.png')
asteroid2 = Asteroid(asteroids_x[1], asteroids_y[1], 'img/asteroid2.png')
asteroid3 = Asteroid(asteroids_x[2], asteroids_y[2], 'img/asteroid3.png')
asteroid4 = Asteroid(asteroids_x[3], asteroids_y[3], 'img/asteroid4.png')
asteroid5 = Asteroid(asteroids_x[4], asteroids_y[4], 'img/asteroid5.png')
asteroids_list.add(asteroid1,asteroid2,asteroid3,asteroid4,asteroid5)

def drawWindow():

    window.blit(bg, (0,0))
    window.blit(rocket, (rocket_x,rocket_y))
    asteroids_list.draw(window)
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
          
    asteroids_list.update(asteroids_speed)
    asteroids_speed += 0.02
    
    score = round((pygame.time.get_ticks())/100 + asteroids_speed*10)
    score_text = font.render(f'Score: {score}', True, (251,246,121))
    high_score_text = h_font.render(f'High score: {high_score}', True, (251,246,121))
    
    if score == 200:
        asteroids_list.add(Asteroid(random.randint(0,SCREEN_WIDTH), -50, 'img/asteroid1.png'))
    if score == 500:
        asteroids_list.add(Asteroid(random.randint(0,SCREEN_WIDTH), -50, 'img/asteroid2.png'))
    if score == 750:
        asteroids_list.add(Asteroid(random.randint(0,SCREEN_WIDTH), -50, 'img/asteroid3.png'))

    # print(round((pygame.time.get_ticks())/50 + asteroids_speed))
    # print(asteroids_speed)
    # print(asteroids_list)
    drawWindow()

pygame.quit()
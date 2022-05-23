import pygame
import random
import time
import os
from constants import *

pygame.init()

game_start = True
game_over = False

h = open('high_score.txt','r')
high_score = h.read()
h.close()

window = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('название пока не придумала')
clock = pygame.time.Clock()
bg = pygame.image.load('img/bg.png')
game_over_bg = pygame.image.load('img/game_over_bg.png')
font = pygame.font.Font('Baloo.ttf', 45)
h_font = pygame.font.Font('Baloo.ttf', 25)
explosion = pygame.image.load('img/explode.png')
color = 'img/yellow.png'
rocket_width = 100
rocket_height = 191

lifes = 3
time_score = 0
rocket_x = SCREEN_WIDTH/2
rocket_y = 500
collide_x = -500
collide_y = -500

class Rocket(pygame.sprite.Sprite):
    def __init__(self, x, y, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect(center=(x,y))

# без этого координаты rect ракеты не будут обновляться
    def update(self):
        self.rect.x = rocket_x
        self.rect.y = rocket_y

asteroids_speed = 10
asteroids_x = [100, 450, 200, 900, 200]
asteroids_y = [-100, 100, 400, 400, 700]
asteroids_list = pygame.sprite.Group()

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, x, y, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect(center=(x,y))

# бесконечная генерация астероидов при выходе за пределы экрана
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
    window.blit(rocket.image, (rocket_x,rocket_y))
    asteroids_list.draw(window)
    window.blit(score_text, (20,10))
    window.blit(high_score_text, (20,70))
    window.blit(lifes_text, (850,30))
    window.blit(explosion,(collide_x, collide_y))

run = True
while run:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if game_start:

        rocket = Rocket(rocket_x, rocket_y, color)
        speed = 20
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and rocket_x > 5:
            rocket_x -= speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and rocket_x < SCREEN_WIDTH-rocket_width:
            rocket_x += speed
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and rocket.rect.y>100:
            rocket_y -= speed
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and rocket_y < SCREEN_HEIGHT-rocket_height:
            rocket_y += speed
        if (keys[pygame.K_ESCAPE]):
            run = False

        rocket.update()
        asteroids_list.update(asteroids_speed)
        asteroids_speed += 0.02

        time_score +=1
        
        score = round(time_score + asteroids_speed*50)-500

        score_text = font.render(f'Score: {score}', True, (251,246,121))
        high_score_text = h_font.render(f'High score: {high_score}', True, (251,246,121))
        lifes_text = font.render(f'Lifes: {lifes}', True, (255, 107, 107))

    # усложнение игры по мере прохождения
        if score == 200:
            asteroids_list.add(Asteroid(random.randint(0,SCREEN_WIDTH), -50, 'img/asteroid1.png'))
        if score == 500:
            asteroids_list.add(Asteroid(random.randint(0,SCREEN_WIDTH), -50, 'img/asteroid2.png'))
        if score == 750:
            asteroids_list.add(Asteroid(random.randint(0,SCREEN_WIDTH), -50, 'img/asteroid3.png')) 

# взрыв при столкновении   
        if pygame.sprite.spritecollide(rocket, asteroids_list, False):
            collide_x = rocket_x-50
            collide_y = rocket_y-50
            print(collide_x, collide_y)     
        collide_y += asteroids_speed
# проверка столкновений
        asteroid_hit_list = pygame.sprite.spritecollide(rocket, asteroids_list, False)    
        for asteroid in asteroid_hit_list:
            lifes -=1
            asteroid.rect.y = SCREEN_HEIGHT+100
        
        crack1 = pygame.image.load('img/crack1.png')
        crack2 = pygame.image.load('img/crack2.png')
            
        if lifes == 2:
            rocket.image.blit(crack1,(0,0))
        
        if lifes == 1:
            rocket.image.blit(crack2,(0,0))

        if lifes == 0:
            game_over = True
            game_start = False

        drawWindow()

    if game_over:

        window.blit(game_over_bg, (0,0))
        asteroids_speed = 0
        speed = 0
        time_score = 0

        win_text = font.render('Ты установил новый рекорд!!', True, (251,246,121))
        
        if high_score =="" or score > int(high_score):
            h = open('high_score.txt','w')
            h.write(str(score))
            h.close()
            window.blit(win_text, (200,250))
            window.blit(score_text, (400,350))
        else:
            window.blit(score_text, (400,310))
            
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_ESCAPE]):
            run = False

        point = pygame.mouse.get_pos()
        rect = pygame.Rect(300,500,400,100)
        pygame.draw.rect(window, (25,67,139), rect)
        restart_text = font.render('Начать заново', True, (251,246,121))
        window.blit(restart_text, (350,520))

        if rect.collidepoint(point):
            restart_text = font.render('Начать заново', True, (255, 107, 107))
            window.blit(restart_text, (350,520))

        if rect.collidepoint(point) and event.type == pygame.MOUSEBUTTONDOWN or (keys[pygame.K_RETURN]):
            rocket_x = SCREEN_WIDTH/2
            rocket_y = 500
            collide_x = -500
            collide_y = -500
            asteroids_x = [100, 450, 200, 900, 200]
            asteroids_y = [-100, 100, 400, 400, 700]
            asteroids_speed = 10
            asteroids_list.empty()
            asteroids_list.add(asteroid1,asteroid2,asteroid3,asteroid4,asteroid5)
            lifes = 3
                        
            h = open('high_score.txt','r')
            high_score = h.read()
            h.close()

            game_start = True
            game_over = False

    pygame.display.update()

pygame.quit()
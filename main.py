import pygame, pygame_menu
import random
import time
import os
from const_sprites import *

pygame.init()

game_menu = True
game_start = False
game_over = False

h = open('high_score.txt','r')
high_score = h.read()
h.close()

window = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('Space Flyer')
clock = pygame.time.Clock()

font = pygame.font.Font('Baloo.ttf', 45)
h_font = pygame.font.Font('Baloo.ttf', 25)
frame = 0

def game_start_pack():
    global game_start
    game_start = True
    global game_over
    game_over = False
    global game_menu
    game_menu = False
    global rocket_x
    rocket_x = SCREEN_WIDTH/2-50
    global rocket_y
    rocket_y = 500
    global collide_x
    collide_x = -500
    global collide_y
    collide_y = -500
    global time_score
    time_score = 0
    global lifes
    lifes = 3
    global asteroids_list
    global asteroids_x
    global asteroids_y
    global asteroids_speed
    asteroids_list = pygame.sprite.Group()
    asteroids_list.empty()
    asteroids_list.clear(window, bg)
    asteroids_x = [100, 450, 200, 900, 200]
    asteroids_y = [-100, -200, -300, -500, -700]
    asteroids_speed = 10
    asteroid1 = Asteroid(asteroids_x[0], asteroids_y[0], 'img/asteroid1.png')
    asteroid2 = Asteroid(asteroids_x[1], asteroids_y[1], 'img/asteroid2.png')
    asteroid3 = Asteroid(asteroids_x[2], asteroids_y[2], 'img/asteroid3.png')
    asteroid4 = Asteroid(asteroids_x[3], asteroids_y[3], 'img/asteroid4.png')
    asteroid5 = Asteroid(asteroids_x[4], asteroids_y[4], 'img/asteroid5.png')
    asteroids_list.add(asteroid1,asteroid2,asteroid3,asteroid4,asteroid5)
                        
    h = open('high_score.txt','r')
    global high_score
    high_score = h.read()
    h.close()

class Rocket(pygame.sprite.Sprite):
    def __init__(self, x, y, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect(center=(x,y))

# без этого координаты rect ракеты не будут обновляться
    def update(self):
        self.rect.x = rocket_x
        self.rect.y = rocket_y

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, x, y, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect(center=(x,y))

# бесконечная генерация астероидов при выходе за пределы экрана
    def update(self, asteroids_speed):
        self.rect.y += asteroids_speed
        if self.rect.y > SCREEN_HEIGHT+10:
           self.rect.y = random.randint(-200,-70)
           self.rect.x = random.randint(0,SCREEN_WIDTH)

def drawGame():

    window.blit(bg, (0,0))
    window.blit(anim[frame], (rocket_x,rocket_y))
    window.blit(rocket.image, (rocket_x,rocket_y))
    if lifes == 2:
            window.blit(crack1,(rocket_x,rocket_y))    
    if lifes == 1:
            window.blit(crack2,(rocket_x,rocket_y))    
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

    if game_menu:
        theme = pygame_menu.Theme()
        menu_font = pygame.font.Font('Baloo.ttf', 52)

        theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
        theme.title_close_button = False
        theme.widget_selection_effect = pygame_menu.widgets.SimpleSelection()
        theme.background_color = pygame_menu.BaseImage('img/menu_bg.png')
        theme.widget_cursor = pygame_menu.locals.CURSOR_HAND
        theme.widget_font = menu_font
        theme.widget_font_color = (251,246,121)
        theme.selection_color = (255, 107, 107)

        menu = pygame_menu.Menu(
            height=SCREEN_HEIGHT,
            onclose=pygame_menu.events.EXIT,
            theme=theme,
            title="",
            width=SCREEN_WIDTH,
            center_content=False,
            mouse_motion_selection=True)

        settings_menu = pygame_menu.Menu(
            height=SCREEN_HEIGHT,
            theme=theme,
            title='',
            width=SCREEN_WIDTH)
        
        def yellow():
            global color
            color = 'img/yellow.png'

        def pink():
            global color
            color = 'img/pink.png'

        def green():
            global color
            color = 'img/green.png'
        
        def null_score():
            h = open('high_score.txt','w')
            h.write(str(0))
            h.close()

        s_1 = settings_menu.add.label('Выбрать цвет')
        s_1.translate(0, 100)

        color_1 = settings_menu.add.button('', yellow, background_color = (251,191,63), padding=(10,50), selection_color=(255,255,255), selection_effect=pygame_menu.widgets.HighlightSelection(border_width=6))
        color_1.translate(-200, 130)
        color_2 = settings_menu.add.button('', pink, background_color = (220, 161, 200), padding=(10,50), selection_color=(255,255,255),selection_effect=pygame_menu.widgets.HighlightSelection(border_width=6))
        color_2.translate(0, 30)
        color_3 = settings_menu.add.button('', green, background_color = (120, 194, 169), padding=(10,50), selection_color=(255,255,255),selection_effect=pygame_menu.widgets.HighlightSelection(border_width=6))
        color_3.translate(200, -70)

        s_2 = settings_menu.add.button('Сбросить рекорд', null_score)
        s_2.translate(0,-30)

        settings_menu.add.button('Назад', pygame_menu.events.BACK)

        def start_game():
            menu.disable()
            print('Game started')
            game_start_pack()
            
        b1 = menu.add.button('Начать игру', start_game)
        b1.translate(10, 250)
        b2 = menu.add.button('Настройки', settings_menu)
        b2.translate(10, 280)
        b3 = menu.add.button('Выход', pygame_menu.events.EXIT)
        b3.translate(10, 310)

        menu.mainloop(window)

    if game_start:

        frame = (frame + 1) % 6
        rocket = Rocket(rocket_x, rocket_y, color)
        speed = 20
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and rocket_x > 10:
            rocket_x -= speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and rocket_x < SCREEN_WIDTH-ROCKET_WIDTH-10:
            rocket_x += speed
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and rocket.rect.y>10:
            rocket_y -= speed
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and rocket_y < SCREEN_HEIGHT-ROCKET_HEIGHT:
            rocket_y += speed
        if (keys[pygame.K_ESCAPE]):
            run = False

        rocket.update()
        asteroids_list.update(asteroids_speed)
        asteroids_speed += 0.02

        time_score +=1
        
        score = round(time_score + asteroids_speed*20)-200

        score_text = font.render(f'Score: {score}', True, (251,246,121))
        high_score_text = h_font.render(f'High score: {high_score}', True, (251,246,121))
        lifes_text = font.render(f'Lifes: {lifes}', True, (255, 107, 107))
        
# усложнение игры по мере прохождения
        if score == 300:
            asteroids_list.add(Asteroid(random.randint(0,SCREEN_WIDTH), -50, 'img/asteroid1.png'))
        if score == 500:
            asteroids_list.add(Asteroid(random.randint(0,SCREEN_WIDTH), -50, 'img/asteroid2.png'))
        if score == 799 or score == 800:
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
            
        if lifes == 0:
            game_over = True
            game_start = False
        drawGame()

    if game_over:

        window.blit(game_over_bg, (0,0))
        asteroids_speed = 0
        speed = 0

        win_text = font.render('Ты установил новый рекорд!!', True, (255, 107, 107))
        
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
        rect = pygame.Rect(300,480,400,100)
        pygame.draw.rect(window, (24,68,139), rect)
        rect2 = pygame.Rect(300,630,400,100)
        pygame.draw.rect(window, (31,61,136), rect2)
        restart_text = font.render('Начать заново', True, (251,246,121))
        back_to_menu_text = font.render('Назад в меню', True, (251,246,121))
        window.blit(restart_text, (350,500))
        window.blit(back_to_menu_text, (350,650))

        if rect.collidepoint(point):
            restart_text = font.render('Начать заново', True, (255, 107, 107))
            window.blit(restart_text, (350,500))

        if rect2.collidepoint(point):
            back_to_menu_text = font.render('Назад в меню', True, (255, 107, 107))
            window.blit(back_to_menu_text, (350,650))

        if rect.collidepoint(point) and event.type == pygame.MOUSEBUTTONDOWN or (keys[pygame.K_RETURN]):
            game_start_pack()

        if rect2.collidepoint(point) and event.type == pygame.MOUSEBUTTONDOWN:
            game_over = False
            game_menu = True
    pygame.display.update()

pygame.quit()
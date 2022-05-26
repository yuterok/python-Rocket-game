import pygame
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 30

ROCKET_WIDTH = 100
ROCKET_HEIGHT = 191

bg = pygame.image.load('img/bg.png')
game_over_bg = pygame.image.load('img/game_over_bg.png')
menu_bg = pygame.image.load('img/menu_bg.png')
color = 'img/yellow.png'
anim = [pygame.image.load('img/anim/0.png'),
        pygame.image.load('img/anim/1.png'),
        pygame.image.load('img/anim/2.png'),
        pygame.image.load('img/anim/3.png'),
        pygame.image.load('img/anim/4.png'),
        pygame.image.load('img/anim/5.png')]

crack1 = pygame.image.load('img/crack1.png')
crack2 = pygame.image.load('img/crack2.png')
explosion = pygame.image.load('img/explode.png')

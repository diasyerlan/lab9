import pygame
from pygame.locals import *
import random, time

#initiliaze
pygame.init()

#making FPS variable 
FPS = 60
FramePerSec = pygame.time.Clock()

#make useful tuples of colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#making characteristics of screen
SCREEN_WIDTH = 840
SCREEN_HEIGHT = 650

#making speed, points variables
SPEED = 3
Points = 0
point = 100
cycle = 1
points = str(Points)

#making background of game
bg = pygame.image.load("racer/images/bg_racer.png")
DISPLAYSURF = pygame.display.set_mode((840,650))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Racer")
font = pygame.font.Font("racer/Fonts/Lato-Black.ttf", 60)
font_small = pygame.font.Font("racer/Fonts/Lato-Black.ttf", 40)
game_over = font.render("Game Over", True, BLUE)

class Coin(pygame.sprite.Sprite):
    #make coin with different weights
    def __init__(self, weight):
        super().__init__()
        self.weight = weight
        if self.weight == 3:
            self.image = pygame.image.load("racer/images/coin_gold_racer.png")
        elif self.weight == 2:
            self.image = pygame.image.load("racer/images/coin_silver_racer.png")
        else:
            self.image = pygame.image.load("racer/images/coin_bronze_racer.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(200,SCREEN_WIDTH-200),0)
    
    #move of coin
    def move(self):
        self.rect.move_ip(0,SPEED)
        if (self.rect.bottom > SCREEN_HEIGHT):
            self.rect.top = 0
            self.rect.center = (random.randint(180, 660), 0)
    
    #deleting coin
    def coin_kill(self):
        self.rect.top = 0
        self.rect.center = (random.randint(180, 660), 0)


 
class Enemy(pygame.sprite.Sprite):
      #it's like a coin without deleting
      def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("racer/images/Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center=(random.randint(200,SCREEN_WIDTH-200),0) 
 
      def move(self):
        self.rect.move_ip(0,SPEED)
        if (self.rect.bottom > SCREEN_HEIGHT):
            self.rect.top = 0
            self.rect.center = (random.randint(180, 660), 0)
 
 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("racer/images/Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
 
    def move(self):
        pressed_keys = pygame.key.get_pressed()
         
        if self.rect.left > 200:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH - 200:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)     

P1 = Player()
E1 = Enemy()
#creating coins with different weights
C1 = Coin(1) # gold coin
C2 = Coin(2) # silver coin
C3 = Coin(3) # bronze coin
coin1 = pygame.sprite.Group()
coin2 = pygame.sprite.Group()
coin3 = pygame.sprite.Group()
coin1.add(C1)
coin2.add(C2)
coin3.add(C3)

#add coins to the coins group
coins = pygame.sprite.Group()
coins.add(C1, C2, C3)

#creating useful groups to use our sprites
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1, C2, C3)

while True:     
    for event in pygame.event.get(): 
        if event.type == QUIT:
            exit()
    point_counter = font_small.render(points, True, BLUE)
 
    DISPLAYSURF.fill(WHITE)
    DISPLAYSURF.blit(bg, (0, 0))
    DISPLAYSURF.blit(point_counter, (10, 10))

    #cycle of movements of sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()
    
    #condition of collision
    if pygame.sprite.spritecollideany(P1, enemies):
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (270,250))
        last_point = font_small.render("Points: ", True, BLUE)
        DISPLAYSURF.blit(last_point, (300, 320))
        DISPLAYSURF.blit(point_counter, (430, 320))
        pygame.display.update()
        for entity in all_sprites:
            entity.kill() 
        time.sleep(2)
        exit()
    
    #condition of picking coin
    if pygame.sprite.spritecollideany(P1, coin1):
        Points += point
        C1.coin_kill()
    if pygame.sprite.spritecollideany(P1, coin2):
        Points += point + 50
        C2.coin_kill()
    if pygame.sprite.spritecollideany(P1, coin3):
        Points += point + 100
        C3.coin_kill()
    
    #it's for avoid creating coin on enemy
    if pygame.sprite.spritecollideany(E1, coin1):
        C1.coin_kill()
    if pygame.sprite.spritecollideany(E1, coin2):
        C2.coin_kill()
    if pygame.sprite.spritecollideany(E1, coin3):
        C3.coin_kill()
    points = str(Points)

    #make game more challenging
    if Points >= 1000 * cycle:
        SPEED += 2
        cycle += 1
    pygame.display.update()
    FramePerSec.tick(FPS)
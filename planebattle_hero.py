#coding:utf-8
import pygame, sys, time
from pygame.locals import *
import os, random
import numpy
import math

global FPSCLOCK, DISPLAYSURF, WIDTH, HEIGHT
path = os.getcwd()
pygame.init()
TILE_SIZE = 64
WIDTH = TILE_SIZE * 7 
HEIGHT = TILE_SIZE * 10 

def checkForQuit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)

def terminate():
    pygame.quit()
    sys.exit()
	
class HERO(pygame.sprite.Sprite): 
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.raw_image = pygame.image.load('.\\res\\pics\\P38.png')
        #self.raw_image = pygame.image.load('.\\res\\pics\\myplane.png')
        #self.raw_image = pygame.image.load(os.path.join('.\\res\\pics', 'myplane.png'))
        #self.raw_image = pygame.image.load(path + '\\res\\pics\\myplane.png')
        self.image = self.raw_image.subsurface(0, 0, 80, 60)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speed_x = 0
        self.speed_y = 0        
        self.old = 0
        self.alive = True

        self.shoot_delay = 60
        self.beam_delay = 10
        self.last_shot = 0

        self.shooting_sound = pygame.mixer.Sound(path + '\\res\\sounds\\pew.wav')
       
    def update(self):
        if self.alive == True:
            self.speed_x = 0
            self.speed_y = 0 
            self.acceleration = 4 
            self.key_state = pygame.key.get_pressed()
            if self.key_state[pygame.K_j]:
                self.shooting()
            if self.key_state[pygame.K_k]:
                self.spray_shooting()
            if self.key_state[pygame.K_w]:
                self.speed_y -= self.acceleration
            if self.key_state[pygame.K_s]:
                self.speed_y += self.acceleration
            if self.key_state[pygame.K_a]:
                self.speed_x -= self.acceleration     
            if self.key_state[pygame.K_d]:
                self.speed_x += self.acceleration

            if self.key_state[pygame.K_n]:
                self.image = self.raw_image.subsurface(0, 0, 80, 60)
            if self.key_state[pygame.K_m]:
                self.image = pygame.transform.scale(self.raw_image.subsurface(0, 0, 80, 60), (160, 120))


            self.rect.x += self.speed_x
            self.rect.y += self.speed_y

            if self.rect.top < 0:
                self.rect.top = 0
            if self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > WIDTH:
                self.rect.right = WIDTH

            #self.now = pygame.time.get_ticks()
            #if self.now - self.old > 50:
            #    self.image = self.raw_image.subsurface(0, 0, 70, 80)
            #    self.old = self.now
            #else:
            #    self.image = self.raw_image.subsurface(70, 0, 70, 80)


            if self.key_state[pygame.K_RETURN]:
                self.player_explosion = Player_Explosion(hero.rect.center)
                all_sprites.add(self.player_explosion)
                all_sprites.remove(hero)
                self.alive = False
                explosion_time = pygame.time.get_ticks()

        if self.alive == False:
            self.rect.center = (WIDTH + 100, HEIGHT + 100)
    
    def shooting(self):
        self.now = pygame.time.get_ticks()
        if self.now - self.last_shot > self.shoot_delay:
            self.last_shot = self.now
            self.bullet1 = Bullet(self.rect.center)
            all_sprites.add(self.bullet1)
            bullets.add(self.bullet1)
            self.shooting_sound.play()

    def spray_shooting(self): #散射弹效果
        self.now = pygame.time.get_ticks()
        if self.now - self.last_shot > self.shoot_delay:
            self.last_shot = self.now
            self.bullet1 = Bullet(self.rect.center)
            all_sprites.add(self.bullet1)
            bullets.add(self.bullet1)
            self.bullet2 = Bullet(self.rect.center, 2) 
            all_sprites.add(self.bullet2)
            bullets.add(self.bullet2)
            self.bullet3 = Bullet(self.rect.center, 3)
            all_sprites.add(self.bullet3)
            bullets.add(self.bullet3)
            self.shooting_sound.play()

    def beam(self):
        self.now = pygame.time.get_ticks()
        if self.now - self.last_shot > self.beam_delay:
            self.last_shot = self.now
            self.bullet = Beam(self.rect.center)
            all_sprites.add(self.bullet)
            bullets.add(self.bullet)
            self.shooting_sound.play()

    def respawn(self):
        self.rect.center = (WIDTH / 2, HEIGHT + 40)
        self.alive = True


class HeroExplosion(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.raw_image = pygame.image.load(path + '\\res\\pics\\Explosion.png')
        self.image = self.raw_image.subsurface(0, 0, 96, 96)
        self.player_expo_sound = pygame.mixer.Sound(path + '\\res\\sounds\\explosion3.wav')
        self.player_expo_sound.play()
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.last_update = 0 #帧数计数器
    
    def update(self):
        self.frame = 12 #动画帧数
        self.frame_last = 180 #动画持续帧数
        if self.last_update % int(self.frame_last / self.frame) == 0:
            self.image = self.raw_image.subsurface(self.last_update / int(self.frame_last / self.frame) * 96, 0, 96, 96)
        self.last_update += 1 
        if self.last_update == self.frame_last:
            self.kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, center, indicator=1):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path + '\\res\\pics\\bullet2.png') 
        self.rect = self.image.get_rect()
        self.rect.center = center 
        self.speed = -10
        self.speed_x = 2
        self.indicator = indicator
    
    def update(self):
        if self.indicator == 1:
            self.rect.y += self.speed
            if self.rect.bottom < 0:
                self.kill()
        if self.indicator == 2:
            self.rect.y += self.speed
            self.rect.x -= self.speed_x
            if self.rect.bottom < 0:
                self.kill()
        if self.indicator == 3:
            self.rect.y += self.speed
            self.rect.x += self.speed_x
            if self.rect.bottom < 0:
                self.kill()


class Beam(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.raw_image = pygame.image.load('.\\res\\pics\\M484BulletCollection1.png') 
        self.image = self.raw_image.subsurface(490, 85, 10, 49)
        self.rect = self.image.get_rect()
        self.rect.center = center 
        self.speed = -10
    
    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

class Mob(pygame.sprite.Sprite):
    def __init__(self, center, indicator = 1):
        pygame.sprite.Sprite.__init__(self)
        self.raw_image = pygame.image.load(path + '\\res\\pics\\small.png')        
        self.image = self.raw_image.subsurface(0, 0, 34, 28)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.indicator = indicator
        if self.indicator == 2 and self.rect.centerx > WIDTH / 2:
           self.indicator = 3
        if self.indicator == 3 and self.rect.centerx < WIDTH / 2:
            self.indicator = 2
        self.speed_y = 3 
        self.speed_x = 3

        self.shoot_delay = 800
        self.last_shot = 0

        self.angle = 0
        self.counter = 0

    def shooting(self):
        self.now = pygame.time.get_ticks()
        if self.now - self.last_shot > self.shoot_delay:
            self.last_shot = pygame.time.get_ticks()
            self.bullet = MobBullet(self.rect.center)
            all_sprites.add(self.bullet)
            mobbullets.add(self.bullet)
        #self.shooting_sound.play()

    def update(self):
        if self.indicator == 1:
            self.rect.y += self.speed_y
            if self.rect.top > HEIGHT:
                self.kill()

        if self.indicator == 2:
            self.rect.y += self.speed_y
            self.rect.x += self.speed_x
            if self.rect.top > HEIGHT:
                self.kill()

        if self.indicator == 3:
            self.rect.y += self.speed_y
            self.rect.x -= self.speed_x
            if self.rect.top > HEIGHT:
                self.kill()

        if self.indicator == 4:
            self.rect.y += self.speed_y
            if self.counter % 24 == 0:
                self.angle += 1 
                self.image = pygame.transform.rotate(self.image, self.angle)
            if self.rect.top > HEIGHT:
                self.kill()
            self.counter += 1

        #if self.rect.centery > HEIGHT / 2 and self.rect.centery < HEIGHT / 2 + 100:
        #   self.shooting()
        #if self.rect.centerx > WIDTH / 2 - 100 and self.rect.centerx < WIDTH / 2 + 100:
        #    self.shooting()


class MobBullet(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.raw_image = pygame.image.load('.\\res\\pics\\M484BulletCollection1.png') 
        self.image = self.raw_image.subsurface(10, 187, 8, 10)
        self.rect = self.image.get_rect()
        self.rect.center = center 
        self.speed = 8 
    
    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()


class MobExplosion(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.mob_expo_sound = pygame.mixer.Sound(path + '\\res\\sounds\\explosion2.wav')
        self.mob_expo_sound.play()

        self.raw_image = pygame.image.load(path + '\\res\\pics\\small.png')
        self.image = self.raw_image.subsurface(0, 0, 34, 28)        
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.last_update = 0 #帧数计数器 

    def update(self):
        self.frame = 3 #动画帧数
        self.frame_last = 30 #动画持续帧数
        if self.last_update % int(self.frame_last / self.frame) == 0:
            self.image = self.raw_image.subsurface(0, self.last_update / int(self.frame_last / self.frame) * 28, 34, 28)
        self.last_update += 1 
        if self.last_update == self.frame_last:
            self.kill()

class PowerUP(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.raw_image = pygame.image.load('.\\res\\pics\\icons-pow-up.png')
        self.image = self.raw_image.subsurface(0, 0, 78, 78)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randrange(10, WIDTH - 10), 0)
        self.speed_y = 1

    def update(self):
        self.rect.centery += self.speed_y
        if self.rect.bottom > HEIGHT:
            self.rect.center = (random.randrange(10, WIDTH - 10), 0)

def New_mob():
    mob_centerx = random.randrange(10, WIDTH - 10)
    mob_center = (mob_centerx, 0)
    indicator = 4 #random.randrange(1, 4)
    mob_element = Mob(mob_center, indicator)
    all_sprites.add(mob_element)
    mobs.add(mob_element)


class Background:
    def __init__(self):
        self.scroll_speed = 2 
        self.background_tile = pygame.image.load(path + '\\res\\pics\\ocean.png')
        self.background = pygame.Surface((WIDTH, HEIGHT + TILE_SIZE)).convert()
        self.offset = 2 
        self.update_counter = 0
        self.frame_last = 120
    
    def background_update(self):
        if self.update_counter % self.frame_last == 0:
            for x in range(WIDTH / TILE_SIZE):
                for y in range(HEIGHT / TILE_SIZE + 1): #创建背景图层，尺寸为HEIGHT+1，用于循环显示制作移动效果
                    self.background.blit(self.background_tile, (x * TILE_SIZE, y * TILE_SIZE))
        self.update_counter += 1 
        return self.background
    
    def background_offset(self): 
        self.offset = (self.offset - self.scroll_speed) % TILE_SIZE
        return (0, self.offset, WIDTH, HEIGHT)


class MobAction:
    def __init__(self, center = [(100,0),(100,-40),(100,-80),(100,-120)]):
        self.center = center
        self.counter = 0
        
    def mob_moving(self):
        if self.counter == 0:
            for i in range(len(self.center)):
                self.mob_element = Mob(self.center[i])
                all_sprites.add(self.mob_element)
                mobs.add(self.mob_element)
        self.counter = 1
    
    def mobs_moving(self):
        if self.counter == 0:
            for i in range(len(self.center)):
                for j in range(1, 5, 1):
                    self.mob_element = Mob((self.center[i][0], self.center[i][1] - j * TILE_SIZE))
                    all_sprites.add(self.mob_element)
                    mobs.add(self.mob_element)
        self.counter = 1
#--------------------------------------------------------------------------
DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('PlaneBattle')
pygame.mixer.init()
background_music = pygame.mixer.music.load(path + '\\res\\sounds\\The Good Fight (w intro).ogg')
pygame.mixer.music.play(-1)
FPS = 60 
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)
BRICKCOLOUR = (244,119,89)
FPSCLOCK = pygame.time.Clock()

background = Background()

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
mobbullets = pygame.sprite.Group()

hero = HERO((WIDTH / 2, HEIGHT + 40))
all_sprites.add(hero)
Score = 0
game_font = pygame.font.SysFont('arial', 24)
score_text = game_font.render('score:' + str(Score), True, BLACK)

#powup = PowerUP()
#all_sprites.add(powup)


old = 0

explosion_time = 0
respawn_time = 0

mob_pos = [(TILE_SIZE * 1, TILE_SIZE * 0),(TILE_SIZE * 6, TILE_SIZE * 0), \
           (TILE_SIZE * 2, TILE_SIZE * (-6)),(TILE_SIZE * 5, TILE_SIZE * (-6)), \
           (TILE_SIZE * 3, TILE_SIZE * (-12)),(TILE_SIZE * 4, TILE_SIZE * (-12)), \
           (TILE_SIZE * 2, TILE_SIZE * (-18)),(TILE_SIZE * 5, TILE_SIZE * (-18)), \
           (TILE_SIZE * 1, TILE_SIZE * (-24)),(TILE_SIZE * 6, TILE_SIZE * (-24)), \
           
           (TILE_SIZE * 1, TILE_SIZE * -30),(TILE_SIZE * 6, TILE_SIZE * (-30)), \
           (TILE_SIZE * 2, TILE_SIZE * (-36)),(TILE_SIZE * 5, TILE_SIZE * (-36)), \
           (TILE_SIZE * 3, TILE_SIZE * (-42)),(TILE_SIZE * 4, TILE_SIZE * (-42)), \
           (TILE_SIZE * 2, TILE_SIZE * (-48)),(TILE_SIZE * 5, TILE_SIZE * (-48)), \
           (TILE_SIZE * 1, TILE_SIZE * (-54)),(TILE_SIZE * 6, TILE_SIZE * (-54)), \
           
           (TILE_SIZE * 1, TILE_SIZE * (-60)),(TILE_SIZE * 6, TILE_SIZE * (-60)), \
           (TILE_SIZE * 2, TILE_SIZE * (-66)),(TILE_SIZE * 5, TILE_SIZE * (-66)), \
           (TILE_SIZE * 3, TILE_SIZE * (-72)),(TILE_SIZE * 4, TILE_SIZE * (-72)), \
           (TILE_SIZE * 2, TILE_SIZE * (-78)),(TILE_SIZE * 5, TILE_SIZE * (-78)), \
           (TILE_SIZE * 1, TILE_SIZE * (-84)),(TILE_SIZE * 6, TILE_SIZE * (-84)), \
           
           (TILE_SIZE * 1, TILE_SIZE * (-90)),(TILE_SIZE * 6, TILE_SIZE * (-90)), \
           (TILE_SIZE * 2, TILE_SIZE * (-96)),(TILE_SIZE * 5, TILE_SIZE * (-96)), \
           (TILE_SIZE * 3, TILE_SIZE * (-102)),(TILE_SIZE * 4, TILE_SIZE * (-102)), \
           (TILE_SIZE * 2, TILE_SIZE * (-108)),(TILE_SIZE * 5, TILE_SIZE * (-108)), \
           (TILE_SIZE * 1, TILE_SIZE * (-114)),(TILE_SIZE * 6, TILE_SIZE * (-114)), \
           ]

mob_action = MobAction(mob_pos)

start_time = pygame.time.get_ticks()
while True:
    run_time = pygame.time.get_ticks()
    game_time = run_time - start_time
    #if (game_time / 1000) % 10 == 0:
        #print u'game running time: ', game_time / 1000
    mob_action.mobs_moving()
    

    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        mob_explosion = MobExplosion(hit.rect.center) 
        all_sprites.add(mob_explosion)
        Score += 1
        score_text = game_font.render('score:' + str(Score), True, BLACK)

    if hero.alive ==True:
        hits = pygame.sprite.spritecollide(hero, mobs, True, pygame.sprite.collide_circle)
        for hit in hits:
            hero_explosion = HeroExplosion(hero.rect.center)
            all_sprites.add(hero_explosion)
            explosion_time = pygame.time.get_ticks()
            hero.alive = False
            Score = 0
            score_text = game_font.render('score:' + str(Score), True, BLACK)

    if hero.alive ==True:
        hits = pygame.sprite.spritecollide(hero, mobbullets, True, pygame.sprite.collide_circle)
        for hit in hits:
            hero_explosion = HeroExplosion(hero.rect.center)
            all_sprites.add(hero_explosion)
            explosion_time = pygame.time.get_ticks()
            hero.alive = False
            Score = 0
            score_text = game_font.render('score:' + str(Score), True, BLACK)
    
    if hero.alive == False:
        respawn_time = pygame.time.get_ticks()
        if respawn_time - explosion_time > 3000:
            hero.respawn()
            all_sprites.add(hero)

    #if respawn_now - respawn_old > 1500 and boss.alive == False:
    #    boss.respawn()
    #    all_sprites.add(boss)


    checkForQuit()
    DISPLAYSURF.blit(background.background_update(), (0, 0), background.background_offset())
    DISPLAYSURF.blit(score_text, (10, 10))
    all_sprites.update()
    all_sprites.draw(DISPLAYSURF)

    pygame.display.flip()
    FPSCLOCK.tick(FPS)



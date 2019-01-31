#coding:utf-8
import pygame, sys, time
from pygame.locals import *
import os, random
import numpy
import math

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
    def __init__(self, X, Y):
        pygame.sprite.Sprite.__init__(self)
        self.raw_image = pygame.image.load(path + '\\res\\pics\\myplane.png')
        self.image = self.raw_image.subsurface(0, 0, 70, 80)
        self.Pos = [X, Y]
        self.rect = Rect((self.Pos[0], self.Pos[1]), (70, 80))
        self.speed_x = 0
        self.speed_y = 0        
        self.old = 0
        self.alive = True

        self.shoot_delay = 150
        self.last_shot = 0

        self.shooting_sound = pygame.mixer.Sound(path + '\\res\\sounds\\pew.wav')

       
    def update(self):
        if self.alive == True:
            self.speed_x = 0
            self.speed_y = 0 
            self.acceleration = 8
            self.key_state = pygame.key.get_pressed()
            if self.key_state[pygame.K_j]:
                self.shooting()
            if self.key_state[pygame.K_w]:
                self.speed_y -= self.acceleration
            if self.key_state[pygame.K_s]:
                self.speed_y += self.acceleration
            if self.key_state[pygame.K_a]:
                self.speed_x -= self.acceleration     
            if self.key_state[pygame.K_d]:
                self.speed_x += self.acceleration            

            self.rect.x += self.speed_x
            self.rect.y += self.speed_y

            if self.rect.top < 0:
                self.rect.top = 0
            if self.rect.bottom > 800:
                self.rect.bottom = 800
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > 480:
                self.rect.right = 480

            self.now = pygame.time.get_ticks()
            if self.now - self.old > 50:
                self.image = self.raw_image.subsurface(0, 0, 70, 80)
                self.old = self.now
            else:
                self.image = self.raw_image.subsurface(70, 0, 70, 80)


            if self.key_state[pygame.K_RETURN]:
                self.alive = False

    
    def shooting(self):
        self.now = pygame.time.get_ticks()
        if self.now - self.last_shot > self.shoot_delay:
            self.last_shot = self.now
            self.bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(self.bullet)
            bullets.add(self.bullet)
            self.shooting_sound.play()

    def respawn(self):
        self.rect.center = (WIDTH / 2, HEIGHT + 40)
        self.alive = True

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path + '\\res\\pics\\bullet2.png') 
        self.rect = self.image.get_rect()
        self.rect.bottom = pos_y
        self.rect.centerx = pos_x
        self.speed = -10

        self.old = 0

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

class BossBullet(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path + '\\res\\pics\\bossbullet.png') 
        self.rect = self.image.get_rect()
        self.rect.bottom = pos_y
        self.rect.centerx = pos_x
        self.speed = 5 

        self.old = 0

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

class Boss(pygame.sprite.Sprite): 
    def __init__(self, X, Y):
        pygame.sprite.Sprite.__init__(self)
        self.raw_image = pygame.image.load(path + '\\res\\pics\\bossplane.png')
        self.image = self.raw_image.subsurface(0, 440, 149, 220)
        self.Pos = [X, Y]
        self.rect = self.image.get_rect()
        self.rect.x = self.Pos[0]
        self.rect.y = self.Pos[1]
        self.speed_x = 0
        self.speed_y = 0        
        self.old = 0
        self.alive = True
        self.life = 10

        self.shoot_delay = 10
        self.last_shot = 0
        self.moving_delay = 10
        self.last_move = 0
        self.direction = 1

        self.shooting_sound = pygame.mixer.Sound(path + '\\res\\sounds\\pew.wav')

       
    def update(self):
        self.now = pygame.time.get_ticks()
        if self.now - self.last_move > self.moving_delay and self.alive == True:
            self.last_move = self.now
            self.speed_x = 0
            self.acceleration = 1 

            if self.direction == 1:
                if self.rect.x < 300 or self.rect.x == 300:
                    self.speed_x += self.acceleration * self.direction
                if self.rect.x > 300:
                    self.direction = -1
            if self.direction == -1:
                if self.rect.x > 75 or self.rect.x == 75:
                    self.speed_x += self.acceleration * self.direction
                if self.rect.x < 90:
                    self.direction = 1

            self.rect.x += self.speed_x

        for i in range(80, 400, 4):
            if self.rect.centerx == i:
                #self.shooting()
                pass

    def shooting(self):
        self.now = pygame.time.get_ticks()
        if self.now - self.last_shot > self.shoot_delay:
            self.last_shot = self.now
            self.boss_bullet = BossBullet(self.rect.centerx, self.rect.bottom)
            all_sprites.add(self.boss_bullet)
            boss_bullets.add(self.boss_bullet)
            self.shooting_sound.play()

    def respawn(self):
        self.rect.center = (WIDTH / 2, 130)
        self.alive = True
        self.life = 10

class BossAttack(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path + '\\res\\pics\\bullet2.png')
        self.rect = self.image.get_rect()
        self.rect.x = 240
        self.rect.y = 400
        self.Radius = 120
        self.x = 0
        self.y = 0

    def First_attack(self):
        if self.x < 240:
            self.x += 1
            self.y = int(math.sqrt(math.pow(self.Radius, 2) - math.pow(self.Radius - self.x, 2)))
            self.rect.x += 1 
            self.rect.y = self.y + 400

    def update(self):
        self.First_attack()

class BossAttack2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path + '\\res\\pics\\bullet2.png')
        self.rect = self.image.get_rect()
        self.rect.x = 240
        self.rect.y = 400
        self.Radius = 120
        self.x = 0
        self.y = 0


    def First_attack(self):
        if self.x < 240:
            self.x += 1
            self.y = int(math.sqrt(math.pow(self.Radius, 2) - math.pow(self.Radius - self.x, 2)))
            self.rect.x -= 1 
            self.rect.y = 400 - self.y
            print self.rect.x, self.rect.y

    def update(self):
        self.First_attack()

class BossAttack3(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path + '\\res\\pics\\bullet2.png')
        self.rect = self.image.get_rect()
        self.rect.x = 240
        self.rect.y = 400
        self.Radius = 120
        self.x = 0
        self.y = 0

    def First_attack(self):
        if self.x < 240:
            self.x += 1
            self.y = int(math.sqrt(math.pow(self.Radius, 2) - math.pow(self.Radius - self.x, 2)))
            self.rect.y += 1 
            self.rect.x = self.y + 240

    def update(self):
        self.First_attack()

class BossAttack4(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path + '\\res\\pics\\bullet2.png')
        self.rect = self.image.get_rect()
        self.rect.x = 240
        self.rect.y = 400
        self.Radius = 120
        self.x = 0
        self.y = 0


    def First_attack(self):
        if self.x < 240:
            self.x += 1
            self.y = int(math.sqrt(math.pow(self.Radius, 2) - math.pow(self.Radius - self.x, 2)))
            self.rect.y -= 1 
            self.rect.x = 240 - self.y
            print self.rect.x, self.rect.y

    def update(self):
        self.First_attack()

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.raw_image = pygame.image.load(path + '\\res\\pics\\small.png')        
        self.image = self.raw_image.subsurface(0, 0, 34, 28)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = 0
        self.speed_y = 5

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > 800:
            self.kill()

class Player_Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.raw_explosion_img = pygame.image.load(path + '\\res\\pics\\myplaneexplosion.png')
        self.image = self.raw_explosion_img.subsurface(0, 0, 70, 80)
        self.player_expo_sound = pygame.mixer.Sound(path + '\\res\\sounds\\explosion3.wav')
        self.player_expo_sound.play()
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.last_update = pygame.time.get_ticks()
    
    def update(self):
        self.now = pygame.time.get_ticks()
        if self.now - self.last_update > 300:
            self.image = self.raw_explosion_img.subsurface(0, 0, 70, 80)
        if self.now - self.last_update > 600:
            self.image = self.raw_explosion_img.subsurface(70, 0, 70, 80)
        if self.now - self.last_update > 900:
            self.image = self.raw_explosion_img.subsurface(70, 0, 70, 80)
            self.kill()

class Boss_Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.raw_explosion_img = pygame.image.load(path + '\\res\\pics\\bossplanebomb.png')
        self.image = self.raw_explosion_img.subsurface(0, 0, 149, 220)
        self.player_expo_sound = pygame.mixer.Sound(path + '\\res\\sounds\\explosion3.wav')
        self.player_expo_sound.play()
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.last_update = pygame.time.get_ticks()
    
    def update(self):
        self.now = pygame.time.get_ticks()
        if self.now - self.last_update > 300:
            self.image = self.raw_explosion_img.subsurface(0, 0, 149, 220)
        if self.now - self.last_update > 600:
            self.image = self.raw_explosion_img.subsurface(0, 220, 149, 220)
        if self.now - self.last_update > 900:
            self.image = self.raw_explosion_img.subsurface(0, 440, 149, 220)
        if self.now - self.last_update > 1200:
            self.image = self.raw_explosion_img.subsurface(0, 660, 149, 220)
        if self.now - self.last_update > 1500:
            self.image = self.raw_explosion_img.subsurface(0, 880, 149, 220)
            self.kill()

class Mob_Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.mob_expo_sound = pygame.mixer.Sound(path + '\\res\\sounds\\explosion2.wav')
        self.mob_expo_sound.play()

        self.raw_image = pygame.image.load(path + '\\res\\pics\\small.png')
        self.image = self.raw_image.subsurface(0, 0, 34, 28)        
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.last_update = pygame.time.get_ticks()

    def update(self):
        self.now = pygame.time.get_ticks()
        if self.now - self.last_update > 80:
            self.image = self.raw_image.subsurface(0, 28, 34, 28)
        if self.now - self.last_update > 160:
            self.image = self.raw_image.subsurface(0, 56, 34, 28)
            self.kill()


def newmob():
    mob_element = Mob()
    all_sprites.add(mob_element)
    mobs.add(mob_element)

def firstattack():
    boss_attack = BossAttack()
    boss_attack2 = BossAttack2()
    boss_attack3 = BossAttack3()
    boss_attack4 = BossAttack4()
    all_sprites.add(boss_attack)
    all_sprites.add(boss_attack2)
    all_sprites.add(boss_attack3)
    all_sprites.add(boss_attack4)

##############################################################    
global FPSCLOCK,DISPLAYSURF
FPS = 30
##############################################################
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)
BRICKCOLOUR = (244,119,89)


path = os.getcwd()
pygame.init()

pygame.mixer.init()

background = pygame.image.load(path + '\\res\\pics\\bg_01.png')

FPSCLOCK = pygame.time.Clock()
WIDTH = 480
HEIGHT = 800
DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('PlaneBattle')

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
boss_bullets = pygame.sprite.Group()

hero = HERO(205, 720)
all_sprites.add(hero)

boss = Boss(166, 20)
all_sprites.add(boss)


old = 0
respawn_old = 0

while True:
    #now = pygame.time.get_ticks() #add mobs
    #if now - old > 1200:
    #    newmob()
    #    old = now

    now = pygame.time.get_ticks() #add mobs
    if now - old > 800:
        firstattack()
        old = now
    
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        mob_explosion = Mob_Explosion(hit.rect.center) 
        all_sprites.add(mob_explosion)
        newmob()

    if hero.alive == True:
        hits = pygame.sprite.spritecollide(hero, boss_bullets, True, pygame.sprite.collide_circle)
        for hit in hits:
            player_explosion = Player_Explosion(hero.rect.center)
            all_sprites.add(player_explosion)
            all_sprites.remove(hero)
            respawn_old = pygame.time.get_ticks()
            hero.alive = False

    if boss.alive == True:
        hits = pygame.sprite.spritecollide(boss, bullets, True, pygame.sprite.collide_circle)
        for hit in hits:
            boss.life -= 1
            if boss.life == 0:
                boss_explosion = Boss_Explosion(boss.rect.center)
                all_sprites.add(boss_explosion)
                all_sprites.remove(boss)
                respawn_old = pygame.time.get_ticks()
                boss.alive = False
    
    hits = pygame.sprite.spritecollide(hero, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player_explosion = Player_Explosion(hero.rect.center)
        all_sprites.add(player_explosion)
        all_sprites.remove(hero)
        respawn_old = pygame.time.get_ticks()
        hero.alive = False
    
    respawn_now = pygame.time.get_ticks()
    if respawn_now - respawn_old > 1500 and hero.alive == False:
        hero.respawn()
        all_sprites.add(hero)

    if respawn_now - respawn_old > 1500 and boss.alive == False:
        boss.respawn()
        all_sprites.add(boss)


    checkForQuit()
    DISPLAYSURF.blit(background, (0, 0), (0, 0, 480, 800))
    all_sprites.update()
    all_sprites.draw(DISPLAYSURF)
    pygame.display.flip()
    FPSCLOCK.tick(FPS)



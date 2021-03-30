import pygame
import random


from tkinter import *
from tkinter import messagebox

import os
import time


# pygame.locals for easier access to key coordinates

from pygame.locals import (

    RLEACCEL, #The RLEACCEL constant is an optional parameter that helps pygame render more quickly
            # on non-accelerated displays
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_SPACE



)

screen_width = 800
screen_height = 600


pygame.init()

screen = pygame.display.set_mode([screen_width, screen_height])
DIR =os.getcwd()+r"\Pygame\Benny_game"

score = 0



class Player(pygame.sprite.Sprite): #The class of character
    def __init__(self):
        super(Player, self).__init__()
        # This class will be superior to be run first in inheritance of class
        #self.surf = pygame.Surface((75, 25)) #it has a fixed resolution and pixel format
        #self.surf.fill((255, 255, 255))

        self.surf = pygame.image.load(DIR+"\jetfighter.png").convert()
        self.surf = pygame.transform.scale(self.surf,(60,30))
        #To scale the size of the sprite

        self.surf.set_colorkey((0,0,0),RLEACCEL)

        #self.surf.set_alpha(128)
        self.rect = self.surf.get_rect()
        self.rect = pygame.rect.Rect((0, 0), (10, 20))
        self.player_speed = 8





    def update(self,pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0,-self.player_speed )
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0,self.player_speed )
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.player_speed ,0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.player_speed ,0)

        if self.rect.left<0: #e.g rect.left: 725   =>the edge point of the rectangle
            self.rect.left = 0
        if self.rect.right>screen_width:
            self.rect.right = screen_width
        if self.rect.top<0:
            self.rect.top = 0
        if self.rect.bottom >screen_height:
            self.rect.bottom = screen_height


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy,self).__init__()
        self.surf = pygame.image.load(DIR+"\missile.png").convert()

        self.surf = pygame.transform.scale(self.surf,(80,20))
        self.surf = pygame.transform.rotate(self.surf,180)

        self.surf.set_colorkey((255,255,255),RLEACCEL)
        #set_colorkey to set the background colour the same with the game objects


        #Set the transparent colorkey set_colorkey(Color, flags=0)
        #pygame.RLEACCEL to provide better performance on non accelerated displays


        #self.surf = pygame.Surface((20,10))
        #self.surf.fill((255,255,255))

        self.rect =self.surf.get_rect(
            center =(
                random.randint(screen_width+20,screen_width+100),
                random.randint(0,screen_height),
            )


        )

        self.speed = random.randint(6,10)
        #To change the speed of the enemy
        #random float number 0 to 1 => random.random()

    def update(self):
        self.rect.move_ip(-self.speed,0)
        if self.rect.right<0:
            self.kill() #From stopping the enemy to further be processed in spirit group
            pass


class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud,self).__init__()
        self.surf = pygame.image.load(DIR+"\BadCloud.png")
        self.surf.set_colorkey((0,0,0),RLEACCEL)
        self.rect  = self.surf.get_rect(center=(random.randint(screen_width+20,screen_width+100),
                                           random.randint(0,screen_height)),
                                  )
        #The method get_rect() returns a Rect object from an image.
        #Collider Box

        self.surf= pygame.transform.scale(self.surf,(100,50))

        self.speed =random.randint(1,2)


    def update(self):
        self.rect.move_ip(-self.speed,0)
        if self.rect.right<0:
            self.kill()

class Bullet(pygame.sprite.Sprite):

    def __init__(self,x,y):
        super(Bullet,self).__init__()
        self.surf = pygame.image.load(DIR+"\Bullet.png")
        self.surf.set_colorkey((0,0,0),RLEACCEL)
        self.surf = pygame.transform.scale(self.surf, (60, 20))
        self.speed = random.randint(10,14)
        self.rect = self.surf.get_rect(
            center=(x,y),
        )

    def update(self):
        self.rect.move_ip(self.speed, 0)
        if self.rect.right>screen_width+20:
            self.kill()
        #if self.rect.right < 0:
        #    self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super(Explosion, self).__init__()
        self.surf = pygame.image.load(DIR + "\explosion.png")
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # if x or y:
        self.x = x
        self.y = y
        # else:
        #     self.x = 0
        #     self.y = 0
        self.rect = self.surf.get_rect(center=(x,y),)
        # The method get_rect() returns a Rect object from an image.
        # Collider Box

        self.surf = pygame.transform.scale(self.surf, (120 , 60))

        self.speed = random.randint(1, 2)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < self.x-20:
            self.kill()







#Sprites creation area






player1 = Player()  # initialization of player1 object



bullets = pygame.sprite.Group()

enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
explosion = pygame.sprite.Group()





all_sprites = pygame.sprite.Group()
#A container class to hold and manage multiple Sprite objects.
all_sprites.add(player1)

#For rendering game objects








running = True



ADDENEMY = pygame.USEREVENT+1
#The last event pygame reserves is called USEREVENT
pygame.time.set_timer(ADDENEMY,500) # every 250ms the time will give out a signal to instaniate enemies






ADDCLOUD = pygame.USEREVENT +2
pygame.time.set_timer(ADDCLOUD,4000)


clock = pygame.time.Clock()
#Setup the clock for a decent frame rate of the game

background = pygame.image.load(DIR+"/clear-blue-sky.jpg")
background = pygame.transform.scale(background,(screen_width,screen_height ))
while running:


    font = pygame.font.SysFont("arial", 30, True)
    text = font.render("Score: " +str(score), 1, (0, 0, 0))
    # Arguments are: text, anti-aliasing, color => It is a surface object for blit


    # pygame control the time message through event list
    # Joysticks will send events
    # after initialization of display module in pygame
    # and set display mode
    #screen.fill((135, 206, 250))  # (R,G,B) Backgroud

    screen.blit(background, (0, 0))

    screen.blit(text, (screen_width - 150, screen_height - 150))


    for event in pygame.event.get():
        # handling event queue => event handler
        # loc_x = screen_width / 2 + val_x
        # loc_y = screen_height / 2 + val_y

        if event.type == KEYDOWN:
            print("key down")
            if event.key == K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:

                bullet = Bullet(player1.rect.left, player1.rect.top)
                if bullet not in bullets:
                    bullets.add(bullet)
                    #all_sprites.add(bullet)
                    print("bullet")



        elif event.type == pygame.QUIT:
            # Event list
            running = False

        elif event.type == ADDENEMY:  #The signal to system for adding an enemy
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        elif event.type ==ADDCLOUD:
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)


    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)





    for bullet in bullets:
        screen.blit(bullet.surf, bullet.rect)
        for new_enemy in enemies:
            if pygame.sprite.spritecollideany(new_enemy, bullets):
                score +=1
                exp = Explosion(new_enemy.rect.right,new_enemy.rect.top)
                explosion.add(exp)
                all_sprites.add(exp)
                new_enemy.kill()
                bullet.kill()





    if pygame.sprite.spritecollideany(player1,enemies): #Collide with enemies sprites group
        player1.kill()
        Tk().wm_withdraw() #To hide the main window
        messagebox.showinfo('Game Over','OK')
        running = False


    #screen.fill((0, 0, 0))
    screen.blit(player1.surf, player1.rect)  # draw a surface on the background surface
    pressed_keys = pygame.key.get_pressed()


    player1.update(pressed_keys)

    enemies.update()
    clouds.update()
    #If the player
    bullets.update()
    explosion.update()


    pygame.display.flip()
    clock.tick(30)
    #flip() =>update the whole display     vs update() => can update the specific area with argument

print("Exit!")
pygame.quit()



#Collision detection checks if the spirit object .rect collides with .rect of another object


#all_sprites =>add player1,enemies and clouds for rendering and instantiation
"""
player1 => player object and function
enemies =>enemies collision detection and positioning
clouds => positioning



"""


"""
Rendering is done using all_sprites.
Position updates are done using clouds and enemies.
Collision detection is done using enemies.

"""
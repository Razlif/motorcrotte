## main game script

# import some packages
from Pygame_Functions.pygame_functions import *
import pygame
import os
import controls
import collectibles
import refactoring as obstacles
import refactoring_sidewalk as sidewalk
from sound_elements import *
import game_configuration as settings
import functions

setAutoUpdate(False)


# set screen
screen = screenSize(settings.screen_size_x, settings.screen_size_y)


# set scrolling background
bg = setBackgroundImage( [  ["media/images/city3.png", "media/images/city4.png"]  ])


#init frames
frame=0
nextFrame = clock()


# Game Music Loop Begins:
pygame.mixer.music.load('media/sounds/BGM16.mid')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(loops=-1)


# init player
hero = controls.Player()
bullets = controls.bullets

# set up empty lists for game elements
vehicle_list = []
poop_list = []
sidewalk_element_list = []


#main game loop
while True:
    if clock() > nextFrame:                         
        frame = (frame+1)%8                      
        nextFrame += 80   # animate a new frame every 80 milisec
    
    scrollBackground((int(hero.speed)*-1),0)   # scroll the background by negative ratio to the player's speed
    
    hero.update()   # update the player's actions
    
    obstacles.update_display(vehicle_list, hero, bullets) # update the traffic
    
    sidewalk.update_display(sidewalk_element_list, hero, bullets) # update the sidewalk
    
    collectibles.update_display(poop_list, hero)  # update the poop
     
    # sort the spriteGroup based on the y position of the bottom of each sprite
    layer_order = sorted(spriteGroup, key=lambda sprite: (sprite.rect.y+sprite.rect.height))   
    for i, sprite in enumerate(layer_order):
        if sprite != hero and hero.jump == False:
        # rearrange the spriteGroup based on the new order
            spriteGroup.change_layer(sprite, i)   
    
    updateDisplay()
    tick(120)

endWait()







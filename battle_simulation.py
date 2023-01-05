## main game script

# import some packages
from Pygame_Functions.pygame_functions import *
import pygame
import os
import controls
import collectibles
import traffic as obstacles
import sidewalk
from sound_elements import *
import game_configuration as settings
import functions
import enemies

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
enemy_list = []



#main game loop
while True:
    if clock() > nextFrame:                         
        frame = (frame+1)%8                      
        nextFrame += 80   # animate a new frame every 80 milisec
    
    scrollBackground((int(hero.speed)*-1),0)   # scroll the background by negative ratio to the player's speed
    
    hero.update()   # update the player's actions
    
    enemies.update_display(enemy_list, hero) 
    
    # sort the spriteGroup based on the y position of the bottom of each sprite
    #functions.sort_sprites_by_pseudo_location_y(spriteGroup, vehicle_list, sidewalk_element_list, poop_list, hero)
        
    updateDisplay()
    tick(120)

endWait()








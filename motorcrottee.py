## main game script

# import some packages
from Pygame_Functions.pygame_functions import *
import pygame
import os
import controls2 as controls
import collectibles
import traffic as obstacles
import sidewalk
from sound_elements import *

setAutoUpdate(False)


# set screen
screen = screenSize(1200,550)


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
car_list = []
scooter_list = []
bicycle_list = []
dog_list = []
person_list = []
poop_list = []


#man game loop
while True:
    if clock() > nextFrame:                         
        frame = (frame+1)%8                      
        nextFrame += 80   # animate a new frame every 80 milisec
    

    scrollBackground((int(hero.speed)*-1),0)   # scroll the background by negative ratio to the player's speed
    
    hero.update()   # update the player's actions
    
    collectibles.spawn_poop(poop_list)   # spawn the poop if the list is lower than N
    for i,poop in enumerate(poop_list):   
        if poop.update(hero) == False:   # remove the poop from the list if it has been collected or passed
            poop_list.pop(i)
    
    sidewalk.spawn_person(person_list)   
    for i,person in enumerate(person_list):
        if person.update(hero, bullets, dog_list, person_list) == False:   
            person_list.pop(i)
    
    sidewalk.spawn_dogs(dog_list)   
    for i,dog in enumerate(dog_list):
        if dog.update(hero, dog_list, person_list) == False:   
            dog_list.pop(i)
    
    sidewalk.spawn_bicycle(bicycle_list)   
    for i,bicycle in enumerate(bicycle_list):
        if bicycle.update(hero, bullets, dog_list, person_list) == False:   
            bicycle_list.pop(i)
    
    obstacles.spawn_cars(car_list)
    for i,car in enumerate(car_list):
        if car.update(hero, bullets, car_list, scooter_list) == False:
            car_list.pop(i)
            
    obstacles.spawn_scooters(scooter_list)
    for i,scooter in enumerate(scooter_list):
        if scooter.update(hero, bullets, scooter_list, car_list) == False:
            scooter_list.pop(i)
     
    # sort the spriteGroup based on the y position of the bottom of each sprite
    layer_order = sorted(spriteGroup, key=lambda sprite: (sprite.rect.y+sprite.rect.height))   
    for i, sprite in enumerate(layer_order):
        # rearrange the spriteGroup based on the new order
        if sprite.jump == True:
            print("jump")
        else:
            spriteGroup.change_layer(sprite, i)   
    
    updateDisplay()
    tick(120)

endWait()



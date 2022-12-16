## main game script

# import some packages
from Pygame_Functions.pygame_functions import *
import pygame
import os
import controls
import collectibles
import one_way as obstacles
import dogs
from sound_elements import *

setAutoUpdate(False)


# set screen
screen = screenSize(1000,500)


# set scrolling background
bg = setBackgroundImage( [  ["media/images/city1.png", "media/images/city2.png"]  ])



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
top_car_list = []
bottom_car_list = []
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
    
    dogs.spawn_person(person_list)   
    for i,person in enumerate(person_list):
        if person.update(hero, bullets) == False:   
            person_list.pop(i)
    
    dogs.spawn_dogs(dog_list)   
    for i,dog in enumerate(dog_list):
        if dog.update(hero) == False:   
            dog_list.pop(i)
    
    obstacles.spawn_top_cars(top_cars_list)
    for i,car in enumerate(top_cars_list):
        if car.update(hero, bullets, top_cars_list) == False:
            top_cars_list.pop(i)
    
    obstacles.spawn_bottom_cars(bottom_cars_list)
    for i,car in enumerate(bottom_cars_list):
        if car.update(hero, bullets, bottom_cars_list) == False:
            bottom_cars_list.pop(i)
            
    obstacles.spawn_scooters(scooter_list)
    for i,scooter in enumerate(scooter_list):
        if scooter.update(hero, bullets, scooter_list, top_cars_list, bottom_cars_list) == False:
            scooter_list.pop(i)
    
    obstacles.spawn_bicycle(bicycle_list)
    for i,bicycle in enumerate(bicycle_list):
        if bicycle.update(hero, bullets, scooter_list, top_cars_list, bottom_cars_list) == False:
            bicycle_list.pop(i)
            
    layer_order = sorted(spriteGroup, key=lambda sprite: (sprite.rect.y+sprite.rect.height))   # sort the spriteGroup based on the y position of the bottom of each sprite
    for i, sprite in enumerate(layer_order):
        spriteGroup.change_layer(sprite, i)   # rearrange the actual spriteGroup based on the new order
    
    
    updateDisplay()
    tick(120)

endWait()

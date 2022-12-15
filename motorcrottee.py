from Pygame_Functions.pygame_functions import *
import pygame
import os
import controls as player
import collectibles
import one_way as obstacles2
import dogs
from sound_elements import *
#from pygame.sprite import LayeredUpdates

frame=0

screen = screenSize(1000,500)

setAutoUpdate(False)

bg = setBackgroundImage( [  ["images/city1.png", "images/city2.png"]  ])

nextFrame = clock()

def sort_by_y(sprite):
    return sprite.y

# Game Music Loop Begins:

pygame.mixer.music.load('sounds/BGM16.mid')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(loops=-1)

# init
hero = player.Player()
bullets = player.bullets
top_cars_list = []
bottom_cars_list = []
scooter_list = []
bicycle_list = []
dog_list = []
person_list = []
poop_list = []


    
while True:
    if clock() > nextFrame:                         
        frame = (frame+1)%8                         
        nextFrame += 80
    scrollBackground((int(hero.speed)*-1),0)
    hero.update()
    
    collectibles.spawn_poop(poop_list)
    for i,poop in enumerate(poop_list):
        if poop.update(hero) == False:
            poop_list.pop(i)
    
    dogs.spawn_person(person_list)
    for i,person in enumerate(person_list):
        if person.update(hero, bullets) == False:
            person_list.pop(i)
    
    dogs.spawn_dogs(dog_list)
    for i,dog in enumerate(dog_list):
        if dog.update(hero) == False:
            dog_list.pop(i)
    
    obstacles2.spawn_top_cars(top_cars_list)
    for i,car in enumerate(top_cars_list):
        if car.update(hero, bullets, top_cars_list) == False:
            top_cars_list.pop(i)
    
    obstacles2.spawn_bottom_cars(bottom_cars_list)
    for i,car in enumerate(bottom_cars_list):
        if car.update(hero, bullets, bottom_cars_list) == False:
            bottom_cars_list.pop(i)
            
    obstacles2.spawn_scooters(scooter_list)
    for i,scooter in enumerate(scooter_list):
        if scooter.update(hero, bullets, scooter_list, top_cars_list, bottom_cars_list) == False:
            scooter_list.pop(i)
    
    obstacles2.spawn_bicycle(bicycle_list)
    for i,bicycle in enumerate(bicycle_list):
        if bicycle.update(hero, bullets, scooter_list, top_cars_list, bottom_cars_list) == False:
            bicycle_list.pop(i)
            
    layer_order = sorted(spriteGroup, key=lambda sprite: (sprite.rect.y+sprite.rect.height))    
    for i, sprite in enumerate(layer_order):
        spriteGroup.change_layer(sprite, i)
    
    
    updateDisplay()
    tick(120)

endWait()

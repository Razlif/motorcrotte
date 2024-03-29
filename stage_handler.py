## main game script

# import some packages
from Pygame_Functions.pygame_functions import *
import pygame
import os
import player as controls
import collectibles
import traffic as obstacles
import sidewalk
from sound_elements import *
import game_configuration as settings
import enemies

setAutoUpdate(False)

def stage_1(vehicle_list, hero, bullets, enemy_list, sidewalk_element_list, poop_list):
    
    if hero.score <1 and hero.poop<99:
        current_wave = 0
        if hero.stages[0] == False:
            hero.notifications.append("Collect 100 Poop!")
            hero.stages[0] = True
    elif hero.score < 55:
        current_wave = 1
        if hero.stages[1]  == False:
            hero.notifications.append("Here We Go!")
            hero.stages[1]  = True
    elif hero.score < 200:
        current_wave = 2
    elif hero.score < 400:
        current_wave = 3
    elif hero.score < 600:
        current_wave = 4
        if hero.stages[4]  == False:
            hero.notifications.append("Beware the Danger!")
            hero.stages[4]  = True
    else:
        current_wave = 'end_level'

    if current_wave != 'end_level':

        scrollBackground((int(hero.x_velocity) * -1), 0)  # scroll the background by negative ratio to the player's speed

        hero.move(enemy_list, vehicle_list)  # update the player's actions

        obstacles.update_display(vehicle_list, hero, bullets, enemy_list, 1, current_wave)  # update the traffic

        sidewalk.update_display(sidewalk_element_list, hero, bullets)  # update the sidewalk

        collectibles.update_display(poop_list, hero)  # update the poop

        enemies.update_display(enemy_list, hero, bullets, 1, current_wave)
    return current_wave
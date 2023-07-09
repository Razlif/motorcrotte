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

    if hero.score < 30:
        current_wave = 0
    elif hero.score < 50:
        current_wave = 1
    elif hero.score < 80:
        current_wave = 2
    elif hero.score < 120:
        current_wave = 3
    elif hero.score < 150:
        current_wave = 4
    else:
        current_wave = 'end_level'

    if current_wave != 'end_level':

        scrollBackground((int(hero.x_velocity) * -1), 0)  # scroll the background by negative ratio to the player's speed

        hero.move()  # update the player's actions

        obstacles.update_display(vehicle_list, hero, bullets, enemy_list, 1, current_wave)  # update the traffic

        sidewalk.update_display(sidewalk_element_list, hero, bullets)  # update the sidewalk

        collectibles.update_display(poop_list, hero)  # update the poop

        enemies.update_display(enemy_list, hero, bullets, 1, current_wave)
    return current_wave
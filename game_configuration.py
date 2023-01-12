# game configuration file
from Pygame_Functions.pygame_functions import *
import math, random

# # load impact pic
impact_picture = pygame.image.load("media/images/poop.png")

# game settings

screen_size_x = 1200

screen_size_y = 550

gravity = 10

# poop settings

max_poop_number = 3

max_enemy_number = 1

# traffic settings

max_car_number = 10

max_scooter_number = 3

car_deceleration_on_player_collision = 0.8

scooter_deceleration_on_player_collision = 0.9

traffic_clear_distance = 500  # far enough in front or behind other vehicle

behind_distance = 250

close_behind_distance = 50

collision_pixel_range = 50  # range of collision from bottom of sprite and up

front_car_acceleration = 0.001  # acceleration when in front

gas_acceleration = 0.03  # general accelearation when running

breaking_deceleration = 0.03  # deceleration when breaking

natural_deceleration = 0.001

lane_1_top = 440

lane_1_bottom = 465

lane_2_top = 520

lane_2_bottom = 540

cars_speed_limit = 1.25  # ratio to player's top speed

max_precent_of_XL_cars = 15

max_precent_of_L_cars = 45

out_of_bounds_x = 2800

vehicle_slowdown_when_close_behind = 0.02

vehicle_slowdown_when_overlap = 0.05

vehicle_y_adjustment = 0.05  # move vehicle up or down when hitting another vehicle

front_x_adjustment_when_overlap = 0.3


# sidewalk settings

max_dog_number = 0

max_people_number = 0

max_bicycle_number = 0

sidewalk_bottom = 340

sidewalk_top = 380


# hero settings

hero_speed_limit = 20

move_hero_on_collision  = 2  # move hero up or down when hitting a car
# game configuration file
from Pygame_Functions.pygame_functions import *
import math, random
import os
import sys

# Determine the base directory (either the directory of the script or the executable)
if getattr(sys, 'frozen', False):
    # Executable mode
    base_dir = os.path.dirname(sys.executable)
else:
    # Script mode
    base_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path to the image
image_path = os.path.join(base_dir, 'media', 'images', 'poopimpact.png')

# Load the image using the absolute path
impact_picture = pygame.image.load(image_path)

# game settings

screen_size_x = 1200

screen_size_y = 686

# set screen
screen = screenSize(screen_size_x, screen_size_y)

gravity = 0.5

# poop settings

max_poop_number = 3

max_enemy_number = 3

spawn_x_range = [1200,1600]

# traffic settings

max_car_number = 5

max_scooter_number = 0

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

side_walk_top = 350

side_walk_bottom = 385

lane_1_top = 410

lane_1_bottom = 480

lane_2_top = 490

lane_2_bottom = 580

lane_3_top = 600

lane_3_bottom = 680

cars_speed_limit = 1.25  # ratio to player's top speed

max_precent_of_XL_cars = 15

max_precent_of_L_cars = 35

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

hero_top_speed = 20

move_hero_on_collision  = 2  # move hero up or down when hitting a car

hero_natural_deceleration = 0.005

hero_breaking_angle = -5

hero_move_back_on_break = 4

hero_back_border = 100

hero_break = 0.04

hero_gas = 0.05

hero_health = 1000

bullet_damage = 10


# notifications

enemy_down_notifications = [
    "Enemy down!",
    "Target neutralized!",
    "One less to worry about!",
    "Got 'em!",
    "That's another one!",
    "Boom, headshot!",
    "Nailed it!",
    "poop master",
    "poop master craftsman",
    "poop extravaganza"
]

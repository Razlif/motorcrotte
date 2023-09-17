from Pygame_Functions.pygame_functions import *
from sound_elements import *
import math, random
import game_configuration as settings

setAutoUpdate(False)

def collision_list_handler(main_sprite, sprite_list):
    for other_sprite in sprite_list:
        collision_handler(main_sprite, other_sprite)
def collision_handler(main_sprite, other_sprite):

    # hero collisions
    if main_sprite.type == "hero":
        # vehicle collisions
        if other_sprite.type == "car" or other_sprite.type == "bike" or other_sprite.type == "boss":
            # check for sprite overlap
            if abs((main_sprite.ground_position) - (other_sprite.ground_position)) < (
                    main_sprite.height * 0.25) and pygame.sprite.collide_mask(main_sprite.sprite, other_sprite.sprite):

                # if hero not on the ground
                if main_sprite.ground == False:
                    if main_sprite.sprite.rect.bottom < other_sprite.sprite.rect.center[1]:  # Check if player is on the roof of the car
                        main_sprite.roof = True
                        main_sprite.ground_position = other_sprite.ground_position
                        main_sprite.y_velocity = 0
                        if keyPressed("q"):
                            main_sprite.ground = False
                            # self.roof = False
                            changeSpriteImage(main_sprite.sprite, main_sprite.frame)
                            transformSprite(main_sprite.sprite, -45, main_sprite.scale, hflip=False, vflip=False)
                            main_sprite.y_velocity -= main_sprite.jump_size
                            main_sprite.jump = False
                    else:
                        main_sprite.roof = False
                        if main_sprite.sprite.rect.center[0] < other_sprite.sprite.rect.left: # if on left side decelerate by -1
                            main_sprite.x_velocity -= 1
                        if main_sprite.sprite.rect.center[0] > other_sprite.sprite.rect.right: # if on right side accelerate by 1
                            main_sprite.x_velocity += 1

                # if hero on the ground
                else:
                    main_sprite.roof = False
                    if main_sprite.ground_position < other_sprite.ground_position:
                        main_sprite.sprite.rect.bottom -= 2
                    else:
                        main_sprite.sprite.rect.bottom += 2

            else:
                main_sprite.roof = False


        # sidewalk collisions
        elif other_sprite.type == "dog" or other_sprite.type == "person":
            # check for sprite overlap
            if abs((main_sprite.ground_position) - (other_sprite.ground_position)) < (
                    main_sprite.height * 0.25) and pygame.sprite.collide_mask(main_sprite.sprite, other_sprite.sprite):
                if main_sprite.ground_position < other_sprite.ground_position:
                    main_sprite.sprite.rect.bottom -= 2
                else:
                    main_sprite.sprite.rect.bottom += 2

        # enemy collisions
        elif other_sprite.type == "enemy":
            # check for sprite overlap
            if abs((main_sprite.ground_position) - (other_sprite.ground_position)) < (
                    main_sprite.height * 0.25) and pygame.sprite.collide_mask(main_sprite.sprite, other_sprite.sprite) and other_sprite.dead == False:

                # if hero not on ground
                if main_sprite.ground == False:
                    if main_sprite.sprite.rect.bottom < other_sprite.sprite.rect.center[1]:  # Check if player is on the roof of the car
                        main_sprite.jump = True
                        main_sprite.ground_position = other_sprite.ground_position
                        transformSprite(other_sprite.sprite, 0, other_sprite.scale, hflip=False, vflip=True)
                        other_sprite.dead = True
                    else:
                        main_sprite.hit = True
                        main_sprite.health -= other_sprite.damage

                # if hero on the ground
                else:
                    main_sprite.hit = True
                    main_sprite.health -= other_sprite.damage


    # car collisions
    elif (main_sprite.type == "car" or main_sprite.type == "bike") and other_sprite.type != "hero":
        if abs((main_sprite.ground_position) - (other_sprite.ground_position)) < (
                main_sprite.height * 0.5):  # in possible range for collision
            if main_sprite.sprite.rect.right < other_sprite.sprite.rect.left - settings.traffic_clear_distance or main_sprite.sprite.rect.left > other_sprite.sprite.rect.right + settings.traffic_clear_distance:
                # far enough back or front
                main_sprite.gas = True


            elif main_sprite.sprite.rect.right < other_sprite.sprite.rect.left - settings.behind_distance:
                # getting close to car in front
                if main_sprite.speed_meter > other_sprite.speed_meter:
                    main_sprite.breaking = True


            elif main_sprite.sprite.rect.right < other_sprite.sprite.rect.left - settings.close_behind_distance:
                # getting very close to car in front
                main_sprite.breaking = True
                main_sprite.speed_meter -= main_sprite.speed_meter * settings.vehicle_slowdown_when_close_behind


            elif main_sprite.sprite.rect.left < other_sprite.sprite.rect.left and main_sprite.sprite.rect.right > other_sprite.sprite.rect.left:
                # overlapping with car in front
                main_sprite.speed_meter = 0

            else:
                main_sprite.gas = True  # in case in front speed up a little
                main_sprite.speed_meter += main_sprite.speed_meter * settings.front_car_acceleration



    # dog collisions
    elif main_sprite.type == "dog":
        if other_sprite.type == "hero":
            pass
        elif other_sprite.type == "car":
            pass
        elif other_sprite.type == "bike":
            pass
        elif other_sprite.type == "dog":
            pass
        elif other_sprite.type == "person":
            pass
        elif other_sprite.type == "enemy":
            pass
        elif other_sprite.type == "boss":
            pass


    # enemy collisions
    elif main_sprite.type == "enemy":
        if other_sprite.type == "enemy":

            if abs((main_sprite.ground_position) - (other_sprite.ground_position)) < (
                    main_sprite.height * 0.5):  # in possible range for collision
                if main_sprite.sprite.rect.right < other_sprite.sprite.rect.left - settings.traffic_clear_distance or main_sprite.sprite.rect.left > other_sprite.sprite.rect.right + settings.traffic_clear_distance:
                    # far enough back or front
                    pass
                elif main_sprite.sprite.rect.right < other_sprite.sprite.rect.left - settings.behind_distance:
                    # getting close to car in front
                    if main_sprite.speed_meter > other_sprite.speed_meter:
                        main_sprite.breaking = True

                elif main_sprite.sprite.rect.right < other_sprite.sprite.rect.left - settings.close_behind_distance:
                    # getting very close to car in front
                    main_sprite.breaking = True
                    main_sprite.speed_meter -= main_sprite.speed_meter * settings.vehicle_slowdown_when_close_behind


                elif main_sprite.sprite.rect.left < other_sprite.sprite.rect.left and main_sprite.sprite.rect.right > other_sprite.sprite.rect.left:
                    # overlapping with car in front
                    main_sprite.speed_meter = 0


        elif other_sprite.type != "hero":
            if abs((main_sprite.ground_position) - (other_sprite.ground_position)) < (
                    main_sprite.height * 0.25) and pygame.sprite.collide_mask(main_sprite.sprite, other_sprite.sprite):
                if main_sprite.ground_position < other_sprite.ground_position:
                    main_sprite.sprite.rect.bottom -= 2
                else:
                    main_sprite.sprite.rect.bottom += 2


    # person collisions
    elif main_sprite.type == "person":
        if other_sprite.type == "hero":
            pass
        elif other_sprite.type == "car":
            pass
        elif other_sprite.type == "bike":
            pass
        elif other_sprite.type == "dog":
            pass
        elif other_sprite.type == "person":
            pass
        elif other_sprite.type == "enemy":
            pass
        elif other_sprite.type == "boss":
            pass

    # boss collisions
    elif main_sprite.type == "boss":
        if other_sprite.type == "hero":
            pass
        elif other_sprite.type == "car":
            pass
        elif other_sprite.type == "bike":
            pass
        elif other_sprite.type == "dog":
            pass
        elif other_sprite.type == "person":
            pass
        elif other_sprite.type == "enemy":
            pass


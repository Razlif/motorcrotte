from Pygame_Functions.pygame_functions import *
import math, random
from sound_elements import *
import game_configuration as settings

setAutoUpdate(False)

# # load impact pic
impact_picture = pygame.image.load("media/images/poop.png")

def sort_sprites_by_pseudo_location_y(spriteGroup, vehicle_list, sidewalk_element_list, poop_list,hero):
    # Sort the sprites based on their bottom Y position
    my_private_sprite_group = vehicle_list + sidewalk_element_list + poop_list
    my_private_sprite_group.append(hero)  
    layer_order = sorted(my_private_sprite_group, key=lambda sprite: sprite.pseudo_location_y)
    
    # Add the sprites back to the sprite group in the correct order
    for i, sprite in enumerate(layer_order):
        spriteGroup.change_layer(sprite.sprite, i)
    

# to update bullet impact on different elements
def when_hit(sprite, bullets):
    for bullet in bullets:
        if sprite.sprite in allTouching(bullet.sprite):
            if bullet.impact == False:
                sprite.hit = True
                hit_position_x = random.randint(65,150)
                hit_position_y = random.randint(0,20)
                sprite.sprite.image.blit(impact_picture, (hit_position_x, hit_position_y)) 
                killSprite(bullet.sprite)
                



# function to randomize variation selection and get variation details
def get_variation_details(element_type):
    if element_type == "car":
        # determine car size
        probability = random.randint(1,100)   
        if probability < settings.max_precent_of_XL_cars:
                size = "XL"
                intial_speed = random.randint(4,8)
                sprite_number = random.randint(18,20)   # determine exact variation and get it's variables
                if sprite_number == 18:
                    sprite_scale = 2.9
                elif sprite_number == 19:
                    sprite_scale = 2.5
                else:
                    sprite_scale = 2.25
        elif probability < settings.max_precent_of_L_cars:
            size = "L"
            intial_speed = random.randint(5,10)
            sprite_number = random.randint(12,17)   # determine exact variation and get it's variables
            if sprite_number == 13:
                sprite_scale = 2.5
            else:
                sprite_scale = 2
        else:
            sprite_number = random.randint(1,11)   # determine exact variation and get it's variables
            if sprite_number < 2:
                size = "special"   # special fast car
                sprite_scale = 2.25
                intial_speed = 20
            else:
                size = "regular"
                intial_speed = random.randint(5,15)
                if sprite_number < 7:
                    sprite_scale = 2.25
                elif sprite_number < 11:
                    sprite_scale = 2.92
                else:
                    sprite_scale = 2.7
        number_of_frames_to_animate = settings.car_number_of_frames_to_animate
        sprite = makeSprite("media/images/cars/"+str(size)+"/car_"+str(sprite_number)+".png", number_of_frames_to_animate)
        deceleration_on_player_collision = settings.car_deceleration_on_player_collision
        
    
    elif element_type == "scooter":
        sprite_number = random.randint(1,19) 
        sprite = makeSprite("media/images/cars/bikes/"+str(sprite_number)+"_1.png",1)
        for i in range(2,5):
            addSpriteImage(sprite, "media/images/cars/bikes/"+str(sprite_number)+"_"+str(i)+".png")
        sprite_scale = 1.75
        intial_speed = random.randint(10,20)
        number_of_frames_to_animate = settings.scooter_number_of_frames_to_animate
        deceleration_on_player_collision = settings.scooter_deceleration_on_player_collision
        size = "small"
    
    elif element_type == "dog":
        number_of_frames_to_animate = 9
        intial_speed = 1
        sprite_number= random.randint(1,6)
        if sprite_number ==2 or sprite_number == 6:
            sprite_scale = 1.7
        elif sprite_number == 4 or sprite_number == 5:
            sprite_scale = 1.2
        else:
            sprite_scale = 1.4
        sprite = makeSprite("media/images/dogs/dog_"+ str(sprite_number)+".png",number_of_frames_to_animate)
        deceleration_on_player_collision = 0.5
        size = "small"

    
    elif element_type == "person":
        intial_speed = random.randint(1,2)
        sprite_number = random.randint(5,7)        
        if sprite_number == 5:
            number_of_frames_to_animate = 9
            sprite_scale = 1.6
        elif sprite_number == 6:
            number_of_frames_to_animate = 6
            sprite_scale = 0.5
        else:
            number_of_frames_to_animate = 19
            sprite_scale = 1.5
        sprite = makeSprite("media/images/people/person"+ str(sprite_number)+".png",number_of_frames_to_animate)
        deceleration_on_player_collision = 0.5
        size = "small"

    else: # in case of bicycle
        sprite_number = 1
        intial_speed = random.randint(2,3)
        number_of_frames_to_animate = 4
        sprite_scale = 1
        sprite = makeSprite("media/images/bicycle_flip.png",number_of_frames_to_animate)
        deceleration_on_player_collision = 0.5
        size = "small"

    return sprite, size, sprite_number, sprite_scale, intial_speed, number_of_frames_to_animate, deceleration_on_player_collision





# function to check for collision between non hero elements
def check_for_collision(sprite1, sprite2):

    car1= sprite1
    car2= sprite2
        
    if abs((car1.pseudo_location_y)-(car2.pseudo_location_y)) < (car1.height*0.5):  # in possible range for collision
        if car1.xpos+car1.width < car2.xpos - settings.traffic_clear_distance or car1.xpos > car2.xpos+car2.width + settings.traffic_clear_distance:             
            # far enough back or front
            car1.gas = True
            car1.state = "default"
            
        elif car1.xpos+car1.width < car2.xpos - settings.behind_distance:
            # getting close to car in front           
            if car1.speed_meter > car2.speed_meter:
                car1.breaking = True
            car1.state = "behind"
            
        elif car1.xpos+car1.width < car2.xpos - settings.close_behind_distance:
            # getting very close to car in front
            car1.breaking = True
            car1.speed_meter -= car1.speed_meter * settings.vehicle_slowdown_when_close_behind
            car1.state = "close behind"
            
        elif car1.xpos + car1.width < car2.xpos + car2.width:
            # overlapping with car in front
            car1.breaking = True
            car1.speed_meter -= car1.speed_meter * settings.vehicle_slowdown_when_overlap
            car2.xpos += settings.front_x_adjustment_when_overlap
            car1.state = "overlap"
            if car1.pseudo_location_y > car2.pseudo_location_y:   # move cars away from each other
                car1.ypos += settings.vehicle_y_adjustment_when_overlap
                car2.ypos -= settings.vehicle_y_adjustment_when_overlap
            else:
                car1.ypos -= settings.vehicle_y_adjustment_when_overlap
                car2.ypos += settings.vehicle_y_adjustment_when_overlap
            
        else:
            car1.gas = True  # in case in front speed up a little
            car1.state = "in front"
            car1.speed_meter += car1.speed_meter * settings.front_car_acceleration


        

# vehicle.sprite in allTouching(hero.sprite) and

# function to check for collision with hero
def check_for_player_collision(sprite1, hero):
    if sprite1.type == "car" or sprite1.type == "scooter":
        vehicle = sprite1
        # in possible range for collision with player otherwise ignore overlap
        if abs((hero.pseudo_location_y)-(vehicle.pseudo_location_y)) < (hero.height*0.15):
            if vehicle.sprite in allTouching(hero.sprite):  # when touching hero
                if vehicle.collision == False:
                    vehicle.collision = True
                if vehicle.ypos -15 < hero.pseudo_location_y < vehicle.ypos:
                    hero.pseudo_location_y = vehicle.pseudo_location_y
                    hero.ypos = vehicle.ypos - hero.height
                    #print("roof")
                else:
                    hero.speed = hero.speed * settings.car_deceleration_on_player_collision
                    # move hero slightly up or down
                    if hero.pseudo_location_y > vehicle.pseudo_location_y:
                        hero.ypos += settings.move_hero_on_collision
                    else:
                        hero.ypos -= settings.move_hero_on_collision
                            
        else:
            vehicle.collision = False
            
    elif sprite1.type == "dog":
        dog = sprite1
        if dog.sprite in allTouching(hero.sprite) and abs((hero.pseudo_location_y)-(dog.pseudo_location_y)) < 5 and hero.jump==False:
            hero.speed = hero.speed * 0.5
            if hero.pseudo_location_y > dog.pseudo_location_y:
                dog.ypos -= 1
            else:
                dog.ypos += 1
        
    elif sprite1.type == "person":
        person = sprite1
        if person.sprite in allTouching(hero.sprite) and abs((hero.pseudo_location_y)-(person.ypos + person.pseudo_location_y)) < 5 and hero.jump==False:
            hero.speed = hero.speed * 0.5
            if hero.pseudo_location_y > person.pseudo_location_y:
                person.ypos -= 1
            else:
                person.ypos += 1

    elif sprite1.type == "bicycle":
        bicycle = sprite1
        if bicycle.sprite in allTouching(hero.sprite) and abs((hero.pseudo_location_y)-(bicycle.pseudo_location_y)) < 5 and hero.jump==False:
            hero.speed = hero.speed * 0.5
            if hero.pseudo_location_y > bicycle.pseudo_location_y:
                bicycle.ypos -= 1
            else:
                bicycle.ypos += 1
    
    else: # sprite 1 == poop
        poop = sprite1
        if poop.sprite in allTouching(hero.sprite) and abs((hero.pseudo_location_y)-(poop.pseudo_location_y)) < 5 and hero.jump==False:
            hero.speed = hero.speed * 0.5
            if hero.pseudo_location_y > poop.pseudo_location_y:
                poop.ypos -= 1
            else:
                poop.ypos += 1


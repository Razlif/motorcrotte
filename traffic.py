from Pygame_Functions.pygame_functions import *
import math, random
from sound_elements import *
import game_configuration as settings

setAutoUpdate(False)


# function to update display on main loop
def update_display(vehicle_list, hero, bullets):
    spawn_vehicles(vehicle_list)
    for i, vehicle in enumerate(vehicle_list):
        if update_state(vehicle, hero, bullets, vehicle_list) == False:
            vehicle_list.pop(i)

    
    
    
# function to spawn the vehicles
def spawn_vehicles(vehicle_list):
    
    # count existing cars and scooters
    car_number = sum(car.type == "car" for car in vehicle_list)
    scooter_number = len(vehicle_list) - car_number
    
    if car_number < settings.max_car_number:   # if cars are under the max number make new car and append to list
        car = Car()
        vehicle_list.append(car)

    
    if scooter_number < settings.max_scooter_number:   # if scooters are under the max number make new scooter and append to list
        scooter = Scooter()
        vehicle_list.append(scooter)





# the main vehicle class
class Vehicle:
    def __init__(self, sprite, scale, intial_speed):
        
        # set to correct scale
        transformSprite(self.sprite, 0, self.scale, hflip=False, vflip=False)
        
        # get sprite dimensions
        self.height = self.sprite.rect.height
        self.width =  self.sprite.rect.width
        
        # randomize intial Y position between lanes
        self.ypos = random.randint(settings.lane_1_top, settings.lane_2_bottom) - self.height 
        
        # randomize initial x position front or back
        self.xpos = random.randint(1650,2150) + (random.randint(1,10) * 53.38)
        front_or_back = random.randint(1,2)
        if front_or_back == 1:
            self.xpos = self.xpos*-1
        

        # set state to default
        self.state = "default"
        self.lane = False
        self.health = 100 
        self.frame = 0
        self.gas = True
        self.breaking = False
        self.collision = False
        self.hit = False
        self.label = False
        self.speed = intial_speed
        self.bottom = self.ypos + self.height
        self.ground_position = self.bottom
        
        # set speed meter to inital speed var
        self.speed_meter = self.speed
        
        # frame counter
        self.timeOfNextFrame = clock()
        
        # show sprite and add to spriteGroup
        showSprite(self.sprite)





# subclass for cars
class Car(Vehicle):
    def __init__(self):
        # set base vars
        self.type = "car"
        
        self.sprite, self.car_size, self.sprite_number, self.scale, self.intial_speed, self.number_of_frames, self.deceleration_on_player_collision = get_variation_details(self.type)
        
        super().__init__(self.sprite, self.scale, self.intial_speed)




#subclass for scooters   
class Scooter(Vehicle):
    def __init__(self):
        # set base vars
        self.type = "scooter"
        
        self.sprite, self.car_size, self.sprite_number, self.scale, self.intial_speed, self.number_of_frames, self.deceleration_on_player_collision = get_variation_details(self.type)
        
        super().__init__(self.sprite, self.scale, self.intial_speed)
        
        
 # moving and general interactions

def update_state(vehicle, hero, bullets, vehicle_list):
    
    # rotate frames in modulu of 'frame number var' every 80 milisec
    if clock() > vehicle.timeOfNextFrame:  
        vehicle.frame = (vehicle.frame + 1) % vehicle.number_of_frames 
        vehicle.timeOfNextFrame += 80
    
    # update bottom location coordinate for sprite drawing order
    vehicle.bottom = vehicle.ypos + vehicle.height
    vehicle.ground_position = vehicle.bottom
        
    # in case of collision with player        
    collision = check_for_player_collision(vehicle, hero)
    
    # update state based on other cars
    for other_car in vehicle_list:   
        collision = check_for_collision(vehicle, other_car)
        
    # manage bullet impact
    for bullet in bullets:
        when_hit(vehicle, bullets)
        
    # when gas
    if vehicle.gas == True:
            
        # increase speed up to self.speed var
        if vehicle.speed_meter < vehicle.speed:
            vehicle.speed_meter += settings.gas_acceleration
                
        # check for lane
        if settings.lane_1_top < vehicle.ground_position < settings.lane_1_bottom:
            vehicle.lane = 1
        elif settings.lane_2_top > vehicle.ground_position > settings.lane_2_bottom :
            vehicle.lane = 2
        else:
            vehicle.lane = "no lane"
            if vehicle.state != "overlap":  # if not in collision and between lanes - gravitate to closest lane
                if settings.lane_2_top > vehicle.ground_position > settings.lane_1_bottom:
                    if abs(vehicle.ground_position - settings.lane_1_bottom) > abs(vehicle.ground_position -settings.lane_2_top) :
                        vehicle.ypos += 0.1
                    else:
                        vehicle.ypos -= 0.1
            
    # when breaking    
    elif vehicle.breaking == True:
        # decrease speed
        vehicle.speed_meter -= settings.breaking_deceleration 
    else:
        vehicle.speed_meter -= settings.natural_deceleration 
        # natural deceleration
            
            
        
    # when in collision with player status 
    if vehicle.collision == True:
        vehicle.breaking = True
        runing_sound.stop()
        idle_sound.stop()
        probability = random.randint(1,100)   # probability for horn sound
        if probability == 1:
            horn_sound.play()
        if probability == 2:
            horn_sound.play()
            horn_sound.play()
                          
     
     
    if vehicle.hit == False:
        changeSpriteImage(vehicle.sprite,  0*vehicle.number_of_frames + vehicle.frame) 
    else:
        vehicle.speed_meter = vehicle.speed_meter * 0.95
        
    
    
    ## move
    if vehicle.speed_meter < 0:  # low speed boundry
        vehicle.speed_meter = 0
        
    if hero.speed > settings.hero_speed_limit and vehicle.speed_meter > hero.speed * settings.cars_speed_limit:  # high speed boundry
        vehicle.speed_meter = hero.speed * settings.cars_speed_limit
        
    vehicle.xpos += vehicle.speed_meter * (random.randint(7,9)* 0.1)  # change  X position by speed meter
    vehicle.xpos += int(hero.speed)*-1   # adapt to background scroll
 
 
    # keep Y position boundries
    if vehicle.ground_position > settings.lane_2_bottom:
        vehicle.ypos = settings.lane_2_bottom - vehicle.height
    if vehicle.ground_position < settings.lane_1_top:
        vehicle.ypos = settings.lane_1_top - vehicle.height
        

    # when far enough in front or behind kill car sprite
    if vehicle.xpos - hero.xpos > settings.out_of_bounds_x or vehicle.xpos - hero.xpos < settings.out_of_bounds_x * -1:
        killSprite(vehicle.sprite)
        return False

    # update actual postiion on screen
    moveSprite(vehicle.sprite, vehicle.xpos, vehicle.ypos)
  


# to update bullet impact on different elements
def when_hit(sprite, bullets):
    for bullet in bullets:
        if sprite.sprite in allTouching(bullet.sprite):
            if bullet.impact == False:
                sprite.hit = True
                hit_position_x = random.randint(65,150)
                hit_position_y = random.randint(0,20)
                sprite.sprite.image.blit(settings.impact_picture, (hit_position_x, hit_position_y)) 
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
        
    
    else:
        sprite_number = random.randint(1,19) 
        sprite = makeSprite("media/images/cars/bikes/"+str(sprite_number)+"_1.png",1)
        for i in range(2,5):
            addSpriteImage(sprite, "media/images/cars/bikes/"+str(sprite_number)+"_"+str(i)+".png")
        sprite_scale = 1.75
        intial_speed = random.randint(10,20)
        number_of_frames_to_animate = settings.scooter_number_of_frames_to_animate
        deceleration_on_player_collision = settings.scooter_deceleration_on_player_collision
        size = "small"
    
    
    return sprite, size, sprite_number, sprite_scale, intial_speed, number_of_frames_to_animate, deceleration_on_player_collision





# function to check for collision between non hero elements
def check_for_collision(sprite1, sprite2):

    car1= sprite1
    car2= sprite2
        
    if abs((car1.ground_position)-(car2.ground_position)) < (car1.height*0.5):  # in possible range for collision
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
            if car1.ground_position > car2.ground_position:   # move cars away from each other
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

def check_for_player_collision(sprite1, hero):
    vehicle = sprite1
    # Check if hero is within range of vehicle for collision
    if abs((hero.ground_position) - (vehicle.ground_position)) < (hero.height * 0.2):
        # Check if hero is touching vehicle
        if vehicle.sprite in allTouching(hero.sprite):
            # Set vehicle collision to True
            vehicle.collision = True
            
            # Check if hero is on top of vehicle
            if vehicle.ypos + 25 > hero.bottom:
                hero.bottom = vehicle.ypos + 15
                hero.ypos = hero.bottom - hero.height
                hero.ground_position = vehicle.ground_position
                hero.xpos += vehicle.speed_meter

            else:
                # Update hero's speed based on collision with vehicle
                hero.speed = hero.speed * settings.car_deceleration_on_player_collision
                # Move hero slightly up or down based on collision with vehicle
                if hero.ground_position > vehicle.ground_position:
                    hero.ypos += settings.move_hero_on_collision
                else:
                    hero.ypos -= settings.move_hero_on_collision
    else:
        # Set vehicle collision to False if hero is not within range
        vehicle.collision = False
from Pygame_Functions.pygame_functions import *
import math, random
from sound_elements import *
import game_configuration as settings
import functions

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
        self.pseudo_location_y = self.ypos + self.height
        
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
        
        self.sprite, self.car_size, self.sprite_number, self.scale, self.intial_speed, self.number_of_frames_to_animate, self.deceleration_on_player_collision = functions.get_variation_details(self.type)
        
        super().__init__(self.sprite, self.scale, self.intial_speed)




#subclass for scooters   
class Scooter(Vehicle):
    def __init__(self):
        # set base vars
        self.type = "scooter"
        
        self.sprite, self.car_size, self.sprite_number, self.scale, self.intial_speed, self.number_of_frames_to_animate, self.deceleration_on_player_collision = functions.get_variation_details(self.type)
        
        super().__init__(self.sprite, self.scale, self.intial_speed)
        
        
 # moving and general interactions

def update_state(vehicle, hero, bullets, vehicle_list):
    
    # rotate frames in modulu of 'frame number var' every 80 milisec
    if clock() > vehicle.timeOfNextFrame:  
        vehicle.frame = (vehicle.frame + 1) % vehicle.number_of_frames_to_animate  
        vehicle.timeOfNextFrame += 80
    
    # update bottom location coordinate for sprite drawing order
    vehicle.pseudo_location_y = vehicle.ypos + vehicle.height
        
    # in case of collision with player        
    collision = functions.check_for_player_collision(vehicle, hero)
    
    # update state based on other cars
    for car2 in vehicle_list:   
        collision = functions.check_for_collision(vehicle, car2)
        
    # manage bullet impact
    for bullet in bullets:
        functions.when_hit(vehicle, bullets)
        
    # when gas
    if vehicle.gas == True:
            
        # increase speed up to self.speed var
        if vehicle.speed_meter < vehicle.speed:
            vehicle.speed_meter += settings.gas_acceleration
                
        # check for lane
        if   settings.lane_1_top < vehicle.pseudo_location_y < settings.lane_1_bottom:
            vehicle.lane = 1
        elif settings.lane_2_top > vehicle.pseudo_location_y > settings.lane_2_bottom :
            vehicle.lane = 2
        else:
            vehicle.lane = "no lane"
            if vehicle.state != "overlap":  # if not in collision and between lanes - gravitate to closest lane
                if settings.lane_2_top > vehicle.pseudo_location_y > settings.lane_1_bottom:
                    if abs(vehicle.pseudo_location_y - settings.lane_1_bottom) > abs(vehicle.pseudo_location_y -settings.lane_2_top) :
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
        changeSpriteImage(vehicle.sprite,  0*vehicle.number_of_frames_to_animate + vehicle.frame) 
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
    if vehicle.pseudo_location_y > settings.lane_2_bottom:
        vehicle.ypos = settings.lane_2_bottom - vehicle.height
    if vehicle.pseudo_location_y < settings.lane_1_top:
        vehicle.ypos = settings.lane_1_top - vehicle.height
        

    # when far enough in front or behind kill car sprite
    if vehicle.xpos - hero.xpos > settings.out_of_bounds_x or vehicle.xpos - hero.xpos < settings.out_of_bounds_x * -1:
        killSprite(vehicle.sprite)
        return False

    # update actual postiion on screen
    moveSprite(vehicle.sprite, vehicle.xpos, vehicle.ypos)
  



from Pygame_Functions.pygame_functions import *
import math, random
from sound_elements import *
import game_configuration as settings

setAutoUpdate(False)


# function to update display on main loop
def update_display(vehicle_list, hero, bullets, enemy_list):
    spawn_vehicles(vehicle_list)
    for i, vehicle in enumerate(vehicle_list):
        if update_state(vehicle, hero, bullets, vehicle_list, enemy_list) == False:
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
    def __init__(self, sprite, scale):
        
        # set to correct scale
        transformSprite(self.sprite, 0, self.scale, hflip=False, vflip=False)
        
        # get sprite dimensions
        self.height = self.sprite.rect.height
        self.width =  self.sprite.rect.width
        
        # randomize intial Y position between lanes
        self.sprite.rect.y = random.randint(settings.lane_1_top, settings.lane_3_bottom) - self.height 
        
        # randomize initial x position front or back
        self.sprite.rect.x = random.randint(settings.spawn_x_range[0], settings.spawn_x_range[1])
        front_or_back = random.randint(1,2)
        if front_or_back == 1:
            self.sprite.rect.x = self.sprite.rect.x*-1
        

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
        self.bottom = self.sprite.rect.y + self.height
        self.ground_position = self.sprite.rect.bottom
        self.previous_position = self.sprite.rect.copy()
        
        # frame counter
        self.timeOfNextFrame = clock()
        
        # show sprite and add to spriteGroup
        showSprite(self.sprite)





# subclass for cars
class Car(Vehicle):
    def __init__(self):
        # set base vars
        self.type = "car"
        
        # number of rames to animate
        self.number_of_frames = variation_data[self.type]["number_of_frames"]
        
        self.deceleration_on_player_collision = settings.car_deceleration_on_player_collision
        
        # determine size
        size_probability = random.randint(1,100)   
        if size_probability < settings.max_precent_of_XL_cars:
            self.size = "XL"
            self.variation_number = random.randint(1, variation_data[self.type][self.size]["number_of_variations"])

            
        elif size_probability < settings.max_precent_of_L_cars:
            self.size = "L"
            self.variation_number = random.randint(1, variation_data[self.type][self.size]["number_of_variations"])

        else:
            self.size = "regular"
            self.variation_number = random.randint(1, variation_data[self.type][self.size]["number_of_variations"])

            
        #set scale
        self.scale = variation_data[self.type][self.size]["sprite_scale"][self.variation_number]
        
        #set speed
        self.intial_speed = random.randint(variation_data[self.type][self.size]["initial_speed"][0],variation_data[self.type][self.size]["initial_speed"][1])
        
        self.speed_meter = self.intial_speed
        
        #create the actual sprite
        sprite_path = "media/images/cars/"+ self.size +"/car_"+ str(self.variation_number) +".png"
        
        self.sprite = makeSprite(sprite_path, self.number_of_frames)
        
        #inherint from main vehicle class
        super().__init__(self.sprite, self.scale)




#subclass for scooters   
class Scooter(Vehicle):
    def __init__(self):
        # set base vars
        self.type = "scooter"
        
        self.size = "small"
        
        self.number_of_frames = variation_data[self.type]["number_of_frames"]
        
        self.deceleration_on_player_collision = settings.scooter_deceleration_on_player_collision
        
        self.variation_number = random.randint(1, variation_data[self.type][self.size]["number_of_variations"]) 
        
        self.scale = variation_data[self.type][self.size]["sprite_scale"]
        
        self.intial_speed = random.randint(variation_data[self.type][self.size]["initial_speed"][0],variation_data[self.type][self.size]["initial_speed"][1])
        
        self.speed_meter = self.intial_speed
        
        sprite_path = "media/images/cars/bikes/"+str(self.variation_number)
        self.sprite = makeSprite(sprite_path+"_1.png", 1)
        for i in range(2,5):
            addSpriteImage(self.sprite, sprite_path+"_"+str(i)+".png")
            
        super().__init__(self.sprite, self.scale)
        
        
        
 # moving and general interactions
def update_state(vehicle, hero, bullets, vehicle_list, enemy_list):
    
    vehicle.previous_position = vehicle.sprite.rect.copy()
    
    vehicle.ground_position = vehicle.sprite.rect.bottom
    
    # rotate frames in modulu of 'frame number var' every 80 milisec
    if clock() > vehicle.timeOfNextFrame:  
        vehicle.frame = (vehicle.frame + 1) % vehicle.number_of_frames 
        vehicle.timeOfNextFrame += 80
        
    # manage bullet impact
    for bullet in bullets:
        when_hit(vehicle, bullets)
        
    # when gas
    if vehicle.gas == True:

        # increase speed up to self.speed var
        vehicle.speed_meter += settings.gas_acceleration

                
        # check for lane
        if settings.lane_1_top < vehicle.ground_position < settings.lane_1_bottom:
            vehicle.lane = 1
        elif settings.lane_2_top > vehicle.ground_position > settings.lane_2_bottom :
            vehicle.lane = 2
        elif settings.lane_3_top > vehicle.ground_position > settings.lane_3_bottom :
            vehicle.lane = 3
        else:
            vehicle.lane = "no lane"
            if vehicle.state != "overlap":  # if not in collision and between lanes - gravitate to closest lane
                if settings.lane_2_top > vehicle.ground_position > settings.lane_1_bottom:
                    if abs(vehicle.ground_position - settings.lane_1_bottom) > abs(vehicle.ground_position -settings.lane_2_top) :
                        vehicle.sprite.rect.y += settings.vehicle_y_adjustment
                    else:
                        vehicle.sprite.rect.y -= settings.vehicle_y_adjustment
                if settings.lane_3_top > vehicle.ground_position > settings.lane_2_bottom:
                    if abs(vehicle.ground_position - settings.lane_2_bottom) > abs(vehicle.ground_position -settings.lane_3_top) :
                        vehicle.sprite.rect.y += settings.vehicle_y_adjustment
                    else:
                        vehicle.sprite.rect.y -= settings.vehicle_y_adjustment
            
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
        vehicle.speed_meter = vehicle.speed_meter * vehicle.deceleration_on_player_collision
        
    
    
    ## move
    if vehicle.speed_meter > vehicle.intial_speed:
        vehicle.speed_meter = vehicle.intial_speed
    if vehicle.speed_meter < 0:  # low speed boundry
        vehicle.speed_meter = 0
        
    #if hero.x_velocity > settings.hero_top_speed and vehicle.speed_meter > hero.x_velocity * settings.cars_speed_limit:  # high speed boundry
    #    vehicle.speed_meter = hero.x_velocity * settings.cars_speed_limit
    
    vehicle.sprite.rect.x += vehicle.speed_meter  # change  X position by speed meter
    vehicle.sprite.rect.x += int(hero.x_velocity)*-1   # adapt to background scroll
 
    
    # update state based on other cars
    for other_car in vehicle_list:   
        collision = check_for_collision(vehicle, other_car)

    # update state based on other cars
    for enemy in enemy_list:   
        collision = check_for_player_collision(vehicle, enemy)
    
    # in case of collision with player        
    collision = check_for_player_collision(vehicle, hero)
    
        
    # keep Y position boundries
    if vehicle.sprite.rect.bottom > settings.lane_3_bottom:
        vehicle.sprite.rect.bottom = settings.lane_3_bottom
    if vehicle.sprite.rect.bottom < settings.lane_1_bottom - 25:
        vehicle.sprite.rect.bottom = settings.lane_1_bottom - 25
        

    # when far enough in front or behind kill car sprite
    if vehicle.sprite.rect.x - hero.sprite.rect.x> settings.out_of_bounds_x or vehicle.sprite.rect.x - hero.sprite.rect.x < settings.out_of_bounds_x * -1:
        killSprite(vehicle.sprite)
        return False

    # update actual postiion on screen
    moveSprite(vehicle.sprite, vehicle.sprite.rect.x, vehicle.sprite.rect.y)
  


# to update bullet impact on different elements
def when_hit(sprite, bullets):
    for bullet in bullets:
        if bullet.sprite in allTouching(sprite.sprite) and abs((bullet.ground_position)-(sprite.ground_position)) < (sprite.height*0.2):
            if bullet.impact == False:
                sprite.hit = True
                hit_position_x = random.randint(65,150)
                hit_position_y = random.randint(0,20)
                sprite.sprite.image.blit(settings.impact_picture, (hit_position_x, hit_position_y)) 
                killSprite(bullet.sprite)
                


# function to check for collision between non hero elements
def check_for_collision(sprite1, sprite2):

    car1= sprite1
    car2= sprite2
        
    if abs((car1.ground_position)-(car2.ground_position)) < (car1.height*0.5):  # in possible range for collision
        if car1.sprite.rect.right < car2.sprite.rect.left - settings.traffic_clear_distance or car1.sprite.rect.left > car2.sprite.rect.right + settings.traffic_clear_distance:             
            # far enough back or front
            car1.gas = True
            car1.state = "default"
            
        elif car1.sprite.rect.right < car2.sprite.rect.left - settings.behind_distance:
            # getting close to car in front           
            if car1.speed_meter > car2.speed_meter:
                car1.breaking = True
            car1.state = "behind"
            
        elif car1.sprite.rect.right < car2.sprite.rect.left - settings.close_behind_distance:
            # getting very close to car in front
            car1.breaking = True
            car1.speed_meter -= car1.speed_meter * settings.vehicle_slowdown_when_close_behind
            car1.state = "close behind"
            
        elif car1.sprite.rect.left < car2.sprite.rect.left and car1.sprite.rect.right > car2.sprite.rect.left:
            # overlapping with car in front
            car1.speed_meter = 0
            car1.state = "overlap"
            
        else:
            car1.gas = True  # in case in front speed up a little
            car1.state = "in front"
            car1.speed_meter += car1.speed_meter * settings.front_car_acceleration


        

# check_for_player_collision
def check_for_player_collision(sprite1, hero):
    vehicle = sprite1
    # Check if hero is within range of vehicle for collision
    if abs((hero.ground_position) - (vehicle.ground_position)) < (hero.height * 0.25) and pygame.sprite.collide_mask(hero.sprite, vehicle.sprite):
        if hero.ground == False:
            hero.obstacle = True
            hero.y_velocity = -1.5
            hero.ground_position = vehicle.ground_position
            
            if hero.sprite.rect.left < vehicle.sprite.rect.left:
                hero.x_velocity = -1
            
            elif hero.sprite.rect.right > vehicle.sprite.rect.right:
                hero.x_velocity += 0.7
            
            else:
                hero.x_velocity += 0.1

        else:
            if hero.ground_position < vehicle.ground_position:
                hero.sprite.rect.bottom -= 2
            else:
                hero.sprite.rect.bottom += 2
            
    else:
        # Set vehicle collision to False if hero is not within range
        vehicle.collision = False
        hero.obstacle = False

        


variation_data = {
    "scooter": {
        "number_of_frames":4,
        "small": {
            "number_of_variations":19,
            "initial_speed": [4, 8],
            "sprite_scale": 1.75,
            }
        },
    "car": {
        "number_of_frames":2,
        "XL": {
            "number_of_variations":3,
            "initial_speed": [4, 8],
            "sprite_scale": {
                1: 2.9,
                2: 2.5,
                3: 2.2
            }
        },
        "L": {
            "number_of_variations":6,
            "initial_speed": [5, 10],
            "sprite_scale": {
                1: 2.5,
                2: 2.5,
                3: 2.5,
                4: 2.5,
                5: 2.5,
                6: 2.5
            }
        },
        "regular": {
            "number_of_variations":11,
            "initial_speed": [5, 15],
            "sprite_scale": {
                1: 2.5,
                2: 2.4,
                3: 2.4,
                4: 2.4,
                5: 2.6,
                6: 2.6,
                7: 3,
                8: 3,
                9: 3.3,
                10: 3,
                11: 2.8
            }
        },
        "special": {
            "initial_speed": 20,
            "sprite_scale": 2.25
        }
    }
}  
from Pygame_Functions.pygame_functions import *
import math, random
from sound_elements import *
import game_configuration as settings
import functions

setAutoUpdate(False)


# function to update display on main loop
def update_display(sidewalk_element_list, hero, bullets):
    spawn_sidewalk_element(sidewalk_element_list)
    for i, sidewalk_element in enumerate(sidewalk_element_list):
        if update_state(sidewalk_element, hero, bullets, sidewalk_element_list) == False:
            sidewalk_element_list.pop(i)




# function to spawn the dogs, pedestrians and bicycles
def spawn_sidewalk_element(sidewalk_element_list):
    
    # count existing sidwalk elemets
    dog_number = sum(sidewalk_element.type == "dog" for sidewalk_element in sidewalk_element_list)
    
    people_number = sum(sidewalk_element.type == "person" for sidewalk_element in sidewalk_element_list)

    bicycle_number = len(sidewalk_element_list) - dog_number - people_number

    
    if dog_number < settings.max_dog_number:   # if dogs are under the max number make new dog and append to list
        dog = Dog()
        sidewalk_element_list.append(dog)

    
    if people_number < settings.max_people_number:   
        person = Person()
        sidewalk_element_list.append(person)


    if bicycle_number < settings.max_bicycle_number:   
        bicycle = Bicycle()
        sidewalk_element_list.append(bicycle)




# main sidewalk element class
class Sidewalk_element():
    def __init__(self, sprite, scale, intial_speed):
        
        # set to correct scale
        transformSprite(self.sprite, 0, self.scale, hflip=False, vflip=False)
        
        # get sprite dimensions
        self.height = self.sprite.rect.height
        self.width =  self.sprite.rect.width
        
        # randomize intial Y position
        self.ypos = random.randint(settings.sidewalk_bottom, settings.sidewalk_top) - self.height 
        
        # randomize initial x position
        self.xpos = random.randint(3,4) * 400
        
        # set state to default
        self.state = "default"
        self.health = 100 
        self.frame = 0
        self.gas = True
        self.breaking = False
        self.collision = False
        self.hit = False
        self.speed = intial_speed
        self.pseudo_location_y = self.ypos + self.height
        # set speed meter to inital speed var
        self.speed_meter = self.speed
        
        # frame counter
        self.timeOfNextFrame = clock()
        
        # show sprite and add to spriteGroup
        showSprite(self.sprite)
        



# dog subclass
class Dog(Sidewalk_element):
    def __init__(self):
        # set base vars
        self.type = "dog"
        
        self.sprite, self.size, self.sprite_number, self.scale, self.intial_speed, self.number_of_frames_to_animate, self.deceleration_on_player_collision = functions.get_variation_details(self.type)
        
        super().__init__(self.sprite, self.scale, self.intial_speed)




# person subclass
class Person(Sidewalk_element):
    def __init__(self):
        # set base vars
        self.type = "person"
        
        self.sprite, self.size, self.sprite_number, self.scale, self.intial_speed, self.number_of_frames_to_animate, self.deceleration_on_player_collision = functions.get_variation_details(self.type)
        
        super().__init__(self.sprite, self.scale, self.intial_speed)
        


# bicycle subclass
class Bicycle(Sidewalk_element):
    def __init__(self):
        # set base vars
        self.type = "bicycle"
        
        self.sprite, self.size, self.sprite_number, self.scale, self.intial_speed, self.number_of_frames_to_animate, self.deceleration_on_player_collision = functions.get_variation_details(self.type)
        
        super().__init__(self.sprite, self.scale, self.intial_speed)
        


# moving and general interactions
def update_state(sidewalk_element, hero, bullets, sidewalk_element_list):
    
    # rotate frames in modulu of 'frame number var' every 80 milisec
    if clock() > sidewalk_element.timeOfNextFrame:  
        sidewalk_element.frame = (sidewalk_element.frame + 1) % sidewalk_element.number_of_frames_to_animate  
        sidewalk_element.timeOfNextFrame += 80
    
    # update bottom location coordinate for sprite drawing order
    sidewalk_element.pseudo_location_y = sidewalk_element.ypos + sidewalk_element.height
        
    # in case of collision with player        
    collision = functions.check_for_player_collision(sidewalk_element, hero)
        
    # update state based on other cars
    for sidewalk_element2 in sidewalk_element_list:   
        collision = functions.check_for_collision(sidewalk_element, sidewalk_element2)

    # manage bullet impact
    for bullet in bullets:
        functions.when_hit(sidewalk_element, bullets)
                 
    
    
    # when in collision with player status 
    if sidewalk_element.collision == True:
        sidewalk_element.breaking = True
        runing_sound.stop()
        idle_sound.play()
        
    if sidewalk_element.hit == False:
        changeSpriteImage(sidewalk_element.sprite,  0*sidewalk_element.number_of_frames_to_animate + sidewalk_element.frame) 
    else:
        sidewalk_element.speed_meter = sidewalk_element.speed_meter * 0.95
        
    
    
    # when gas
    if sidewalk_element.gas == True:
            
        # increase speed up to self.speed var
        if sidewalk_element.speed_meter < sidewalk_element.speed:
            sidewalk_element.speed_meter += settings.gas_acceleration
            
    # when breaking    
    elif sidewalk_element.breaking == True:
        # decrease speed
        sidewalk_element.speed_meter -= settings.breaking_deceleration 
    else:
        sidewalk_element.speed_meter -= settings.natural_deceleration 
        # natural deceleration
            
                
        
    ## move
    if sidewalk_element.speed_meter < 0:  # low speed boundry
        sidewalk_element.speed_meter = 0
        
        
    sidewalk_element.xpos -= sidewalk_element.speed_meter * (random.randint(7,9)* 0.1)  # change  X position by speed meter
    sidewalk_element.xpos += int(hero.speed)*-1   # adapt to background scroll

 
    # keep Y position boundries
    if sidewalk_element.pseudo_location_y < settings.sidewalk_bottom:
        sidewalk_element.ypos = settings.sidewalk_bottom + sidewalk_element.height
    if sidewalk_element.pseudo_location_y > settings.sidewalk_top:
        sidewalk_element.ypos = settings.sidewalk_top - sidewalk_element.height
        
        
    # when far enough in front or behind kill car sprite
    if sidewalk_element.xpos - hero.xpos > settings.out_of_bounds_x or sidewalk_element.xpos - hero.xpos < settings.out_of_bounds_x * -1:
        killSprite(sidewalk_element.sprite)
        return False

    # update actual postiion on screen
    moveSprite(sidewalk_element.sprite, sidewalk_element.xpos, sidewalk_element.ypos)

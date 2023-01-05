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
        self.bottom = self.ypos + self.height
        self.ground_position = self.bottom
        
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
        
        self.sprite, self.size, self.sprite_number, self.scale, self.intial_speed, self.number_of_frames, self.deceleration_on_player_collision = functions.get_variation_details(self.type)
        
        super().__init__(self.sprite, self.scale, self.intial_speed)




# person subclass
class Person(Sidewalk_element):
    def __init__(self):
        # set base vars
        self.type = "person"
        
        self.sprite, self.size, self.sprite_number, self.scale, self.intial_speed, self.number_of_frames, self.deceleration_on_player_collision = functions.get_variation_details(self.type)
        
        super().__init__(self.sprite, self.scale, self.intial_speed)
        


# bicycle subclass
class Bicycle(Sidewalk_element):
    def __init__(self):
        # set base vars
        self.type = "bicycle"
        
        self.sprite, self.size, self.sprite_number, self.scale, self.intial_speed, self.number_of_frames, self.deceleration_on_player_collision = functions.get_variation_details(self.type)
        
        super().__init__(self.sprite, self.scale, self.intial_speed)
        


# moving and general interactions
def update_state(sidewalk_element, hero, bullets, sidewalk_element_list):
    
    # rotate frames in modulu of 'frame number var' every 80 milisec
    if clock() > sidewalk_element.timeOfNextFrame:  
        sidewalk_element.frame = (sidewalk_element.frame + 1) % sidewalk_element.number_of_frames 
        sidewalk_element.timeOfNextFrame += 80
    
    # update bottom location coordinate for sprite drawing order
    sidewalk_element.bottom = sidewalk_element.ypos + sidewalk_element.height
    sidewalk_element.ground_position = sidewalk_element.bottom
        
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
        changeSpriteImage(sidewalk_element.sprite,  0*sidewalk_element.number_of_frames + sidewalk_element.frame) 
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
    if sidewalk_element.ground_position < settings.sidewalk_bottom:
        sidewalk_element.ypos = settings.sidewalk_bottom + sidewalk_element.height
    if sidewalk_element.ground_position > settings.sidewalk_top:
        sidewalk_element.ypos = settings.sidewalk_top - sidewalk_element.height
        
        
    # when far enough in front or behind kill car sprite
    if sidewalk_element.xpos - hero.xpos > settings.out_of_bounds_x or sidewalk_element.xpos - hero.xpos < settings.out_of_bounds_x * -1:
        killSprite(sidewalk_element.sprite)
        return False

    # update actual postiion on screen
    moveSprite(sidewalk_element.sprite, sidewalk_element.xpos, sidewalk_element.ypos)


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
    if element_type == "dog":
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
        
    if abs((sprite1.pseudo_location_y)-(sprite2.pseudo_location_y)) < (sprite1.height*0.5):  # in possible range for collision
        if sprite1.xpos+sprite1.width < sprite2.xpos - settings.traffic_clear_distance or sprite1.xpos > sprite2.xpos+car2.width + settings.traffic_clear_distance:             
            # far enough back or front
            sprite1.gas = True
            sprite1.state = "default"
            
        elif sprite1.xpos+sprite1.width < sprite2.xpos - settings.behind_distance:
            # getting close to car in front           
            if sprite1.speed_meter > sprite2.speed_meter:
                sprite1.breaking = True
            sprite1.state = "behind"
            
        elif sprite1.xpos+sprite1.width < sprite2.xpos - settings.close_behind_distance:
            # getting very close to car in front
            sprite1.breaking = True
            sprite1.speed_meter -= sprite1.speed_meter * settings.vehicle_slowdown_when_close_behind
            sprite1.state = "close behind"
            
        elif sprite1.xpos + sprite1.width < sprite2.xpos + sprite2.width:
            # overlapping with car in front
            sprite1.breaking = True
            sprite1.speed_meter -= sprite1.speed_meter * settings.vehicle_slowdown_when_overlap
            sprite2.xpos += settings.front_x_adjustment_when_overlap
            sprite1.state = "overlap"
            if sprite1.pseudo_location_y > sprite2.pseudo_location_y:   # move cars away from each other
                sprite1.ypos += settings.vehicle_y_adjustment_when_overlap
                sprite2.ypos -= settings.vehicle_y_adjustment_when_overlap
            else:
                sprite1.ypos -= settings.vehicle_y_adjustment_when_overlap
                sprite2.ypos += settings.vehicle_y_adjustment_when_overlap
            
        else:
            sprite1.gas = True  # in case in front speed up a little
            sprite1.state = "in front"
            sprite1.speed_meter += sprite1.speed_meter * settings.front_car_acceleration


        

# vehicle.sprite in allTouching(hero.sprite) and

# function to check for collision with hero
def check_for_player_collision(sprite1, hero):
            
    if sprite1.type == "dog":
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

    else:
        bicycle = sprite1
        if bicycle.sprite in allTouching(hero.sprite) and abs((hero.pseudo_location_y)-(bicycle.pseudo_location_y)) < 5 and hero.jump==False:
            hero.speed = hero.speed * 0.5
            if hero.pseudo_location_y > bicycle.pseudo_location_y:
                bicycle.ypos -= 1
            else:
                bicycle.ypos += 1



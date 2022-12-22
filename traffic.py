from Pygame_Functions.pygame_functions import *
import math, random
from sound_elements import *

setAutoUpdate(False)


def spawn_cars(car_list):   # if no cars in the list create a car and append to list 
    if len(car_list) < 10:
        car = Car()
        car_list.append(car)


def spawn_scooters(scooter_list):   # if no scooters in the list create a scooter and append to list 
    if len(scooter_list) < 2:
        scooter = Scooter()
        scooter_list.append(scooter)
 
 
# function to check for other car proximity   
def check_for_other_cars(car1, car2):
    # in possible range for collision
    if abs((car1.ypos+car1.height)-(car2.ypos+car2.height)) < 50:
        # far enough back or front
        if car1.xpos+car1.width < car2.xpos - 500 or car1.xpos > car2.xpos+car2.width + 500:             
            car1.gas = True
            car1.state = "default"
        elif car1.xpos+car1.width < car2.xpos - 250:
            # getting close to car in front           
            if car1.speed_meter > car2.speed_meter:
                car1.breaking = True
            car1.state = "behind"
        elif car1.xpos+car1.width < car2.xpos - 100:
            # getting very close to car in front
            car1.breaking = True
            car1.speed_meter -= car1.speed_meter * 0.01
            car1.state = "close behind"
        elif car1.xpos + car1.width < car2.xpos + car2.width:
            # overlapping with car in front
            car1.breaking = True
            car1.speed_meter -= car1.speed_meter * 0.05
            car2.xpos += 0.3
            car1.state = "overlap"
            if car1.ypos+car1.height > car2.ypos+car2.height:   # move cars away from each other
                car1.ypos += 0.05
                car2.ypos -= 0.05
            else:
                car1.ypos -= 0.05
                car2.ypos += 0.05
        else:
            car1.gas = True  # in case in front speed up a little
            car1.state = "in front"
            car1.speed_meter += car1.speed_meter * 0.001



# function to randomize car style generation
def get_car_type():
    number_of_frames_to_animate = 2
    # determine car size
    probability = random.randint(1,100)   
    if probability < 15:
        car_type = "XL"
        sprite_number = random.randint(18,20)   # determine exact variation and get it's variables
        if sprite_number == 18:
            sprite_scale = 2.9
        elif sprite_number == 19:
            sprite_scale = 2.5
        else:
            sprite_scale = 2.25
        intial_speed = 5
    elif probability < 45:
        car_type = "L"
        sprite_number = random.randint(12,17)   # determine exact variation and get it's variables
        if sprite_number == 13:
            sprite_scale = 2.5
        else:
            sprite_scale = 2
        intial_speed = 8
    else:
        sprite_number = random.randint(1,11)   # determine exact variation and get it's variables
        if sprite_number < 2:
            car_type = "special"   # special fast car
            sprite_scale = 2.25
            intial_speed = 20
        else:
            car_type = "regular"
            if sprite_number < 7:
                sprite_scale = 2.25
            elif sprite_number < 11:
                sprite_scale = 2.92
            else:
                sprite_scale = 2.7
            intial_speed = 12
            
    return car_type, sprite_number, sprite_scale, intial_speed, number_of_frames_to_animate



# creating the car class
class Car():
    def __init__(self):
        # call the get car type function
        self.type, self.sprite_number, self.scale, self.speed, self.num_frames = get_car_type()
        
        # create the actual sprite
        self.sprite = makeSprite("media/images/cars/"+str(self.type)+"/car_"+str(self.sprite_number)+".png", self.num_frames)
        
        # set to correct scale
        transformSprite(self.sprite, 0, self.scale, hflip=False, vflip=False)
        
        # # load impact pic
        self.impact_picture = pygame.image.load("media/images/poop.png") 
        
        # get sprite dimensions
        self.height = self.sprite.rect.height
        self.width =  self.sprite.rect.width
        
        # randomize intial Y position between lanes
        self.ypos = random.randint(435,540) - self.height 
        
        # randomize initial x position front or back
        self.xpos = random.randint(1650,2150) + (random.randint(1,10) * 53.38)
        front_or_back = random.randint(1,2)
        if front_or_back == 1 or self.type == "special":
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

        # set speed meter to inital speed var
        self.speed_meter = self.speed
        
        # frame counter
        self.timeOfNextFrame = clock()
        
        # show sprite and add to spriteGroup
        showSprite(self.sprite)
        
        
     
    # move function 
    def move(self, hero, bullets, car_list, scooter_list):
        
        # rotate frames in modulu of 'frame number var' every 80 milisec
        if clock() > self.timeOfNextFrame:  
            self.frame = (self.frame + 1) % self.num_frames  
            self.timeOfNextFrame += 80  
                
        
        # update state based on other cars
        for car in car_list:   
            collision = check_for_other_cars(self, car)
        
        # update state based on other scooters
        for scooter in scooter_list:   
            collision = check_for_other_cars(self, scooter)
        
        
        # when gas
        if self.gas == True:
            
            # increase speed up to self.speed var
            if self.speed_meter < self.speed:
                self.speed_meter += 0.03
                
            # check for lane
            if   440 < self.ypos+self.height < 465:
                self.lane = 1
            elif 540 > self.ypos+self.height > 520 :
                self.lane = 2
            else:
                self.lane = "no lane"
                if self.state != "overlap":  # if not in collision and between lanes - gravitate to closest lane
                    if 520 > self.ypos+self.height > 465:
                        if abs(self.ypos+self.height - 465) > abs(self.ypos+self.height -520) :
                            self.ypos += 0.1
                        else:
                            self.ypos -= 0.1
            
        # when breaking    
        elif self.breaking == True:
            # decrease speed
            self.speed_meter -= 0.03 
        else:
            self.speed_meter -= 0.01
            # natural deceleration
            
                
        
            
        # in case of collision with player
        if self.sprite in allTouching(hero.sprite) and abs((hero.ypos + hero.height)-(self.ypos + self.height)) < 25:
            if self.collision == False:
                hero.speed = hero.speed * 0.8
                self.collision = True
        else:
            self.collision = False
        
        # when in collision with player status 
        if self.collision == True:
            self.breaking = True
            if hero.ypos+hero.height > self.ypos+self.height:
                # move hero slightly up or down
                hero.ypos += 1.8
                if hero.jump == True:
                    hero.ypos += 2

                    
            else:
                hero.ypos -= 1.8
                if hero.jump == True:
                    hero.ypos -= 2

            runing_sound.stop()
            idle_sound.stop()
            probability = random.randint(1,100)   # probability for horn sound
            if probability == 1:
                horn_sound.play()
            if probability == 2:
                horn_sound.play()
                horn_sound.play()
                    

        
        ## move
        if self.speed_meter < 0:  # low speed boundry
            self.speed_meter = 0
        
        if hero.speed > 20 and self.speed_meter>hero.speed*1.5:  # high speed boundry
            self.speed_meter = hero.speed*1.2
        
        self.xpos += self.speed_meter * (random.randint(7,9)* 0.1)  # change  X position by speed meter
        self.xpos += int(hero.speed)*-1   # adapt to background scroll


        # when far enough in front or behind kill car sprite
        if self.xpos - hero.xpos > 2800 or self.xpos - hero.xpos < -2800:
            killSprite(self.sprite)
            return False
 
 
        # keep Y position boundries
        if self. ypos + self.height > 540:
            self.ypos = 540 - self.height
        if self. ypos + self.height < 440:
            self.ypos = 440 - self.height

        # manage bullet impact
        for bullet in bullets:
            if self.sprite in allTouching(bullet.sprite):
                if bullet.impact == False:
                    self.hit = True
                    hit_position_x = random.randint(65,150)
                    hit_position_y = random.randint(0,20)
                    self.sprite.image.blit(self.impact_picture, (hit_position_x, hit_position_y)) 
                    killSprite(bullet.sprite)

                 
        
        if self.hit == False:
            changeSpriteImage(self.sprite,  0*self.num_frames+self.frame) 
        else:
            self.speed_meter = self.speed_meter * 0.95

        # update actual postiion on screen
        moveSprite(self.sprite, self.xpos, self.ypos)
        
        # show car data for testing
        #hideLabel(self.label)
        #self.label = makeLabel(str(self.lane) + " " + str(int(self.speed_meter)) + " " +  str(self.state), 40, self.xpos+50, self.ypos+40 , "blue")
        #showLabel(self.label)

        
    def update(self, hero, bullets, car_list, scooter_list):
        if self.move(hero, bullets, car_list, scooter_list) == False:
            return False        
        
# creating the scooter class
class Scooter():
    def __init__(self):
        # set base vars
        self.scale = 1.75
        self.speed = random.randint(10,20)
        self.num_frames = 4
        self.sprite_number = random.randint(1,19)
        
        # create the actual sprite
        self.sprite = makeSprite("media/images/bikes/"+str(self.sprite_number)+"_1.png",1)
        for i in range(2,5):
            addSpriteImage(self.sprite, "media/images/bikes/"+str(self.sprite_number)+"_"+str(i)+".png")
        
        # set to correct scale
        transformSprite(self.sprite, 1.75, self.scale, hflip=False, vflip=False)
        
        # # load impact pic
        self.impact_picture = pygame.image.load("media/images/poop.png") 
        
        # get sprite dimensions
        self.height = self.sprite.rect.height
        self.width =  self.sprite.rect.width
        
        # randomize intial Y position between lanes
        self.ypos = random.randint(435,540) - self.height 
        
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

        # set speed meter to inital speed var
        self.speed_meter = self.speed
        
        # frame counter
        self.timeOfNextFrame = clock()
        
        # show sprite and add to spriteGroup
        showSprite(self.sprite)
        
        
     
    # move function 
    def move(self, hero, bullets, car_list, scooter_list):
        
        # rotate frames in modulu of 'frame number var' every 80 milisec
        if clock() > self.timeOfNextFrame:  
            self.frame = (self.frame + 1) % self.num_frames  
            self.timeOfNextFrame += 80  
                
        
        # update state based on other cars
        for car in car_list:   
            collision = check_for_other_cars(self, car)
        
        # update state based on other scooters
        for scooter in scooter_list:   
            collision = check_for_other_cars(self, scooter)
        
        
        
        # when gas
        if self.gas == True:
            
            # increase speed up to self.speed var
            if self.speed_meter < self.speed:
                self.speed_meter += 0.04
                
            # check for lane
            if   440 < self.ypos+self.height < 465:
                self.lane = 1
            elif 540 > self.ypos+self.height > 520 :
                self.lane = 2
            else:
                self.lane = "no lane"
                if self.state != "overlap":  # if not in collision and between lanes - gravitate to closest lane
                    if 520 > self.ypos+self.height > 465:
                        if abs(self.ypos+self.height - 465) > abs(self.ypos+self.height -520) :
                            self.ypos += 0.1
                        else:
                            self.ypos -= 0.1
            
        # when breaking    
        elif self.breaking == True:
            # decrease speed
            self.speed_meter -= 0.03 
        else:
            self.speed_meter -= 0.01
            # natural deceleration
            
            
            
        
            
        # in case of collision with player
        if self.sprite in allTouching(hero.sprite) and abs((hero.ypos + hero.height)-(self.ypos + self.height)) < 20:
            if self.collision == False:
                hero.speed = hero.speed * 0.9
                self.collision = True
        else:
            self.collision = False
        
        # when in collision with player status 
        if self.collision == True:
            self.breaking = True
            if hero.ypos+hero.height > self.ypos+self.height:   # move hero slightly up or down
                hero.ypos += 1
            else:
                hero.ypos -= 1
                    

        
        ## move
        if self.speed_meter < 0:  # low speed boundry
            self.speed_meter = 0
        if hero.speed > 20 and self.speed_meter>hero.speed*1.5:  # high speed boundry
            self.speed_meter = hero.speed*1.2
        self.xpos += self.speed_meter * (random.randint(7,9)* 0.1)  # change  X position by speed meter
        self.xpos += int(hero.speed)*-1   # adapt to background scroll
        
        
        # when far enough in front or behind kill car sprite
        if self.xpos - hero.xpos > 2800 or self.xpos - hero.xpos < -2800:
            killSprite(self.sprite)
            return False
        
        
        # keep Y position boundries
        if self. ypos + self.height > 540:
            self.ypos = 540 - self.height
        if self. ypos + self.height < 440:
            self.ypos = 440 - self.height
        
        
        # manage bullet impact
        for bullet in bullets:
            if self.sprite in allTouching(bullet.sprite):
                if bullet.impact == False:
                    self.hit = True
                    hit_position_x = random.randint(10,20)
                    hit_position_y = random.randint(0,20)
                    self.sprite.image.blit(self.impact_picture, (hit_position_x, hit_position_y)) 
                    killSprite(bullet.sprite)

                 
        
        if self.hit == False:
            changeSpriteImage(self.sprite,  0*self.num_frames+self.frame) 
        else:
            self.speed_meter = self.speed_meter * 0.95

         
        # update actual postiion on screen
        moveSprite(self.sprite, self.xpos, self.ypos)
        
        # show car data for testing
        #hideLabel(self.label)
        #self.label = makeLabel(str(self.lane) + " " + str(int(self.speed_meter)) + " " +  str(self.state), 40, self.xpos+50, self.ypos+40 , "blue")
        #showLabel(self.label)

    
    def update(self, hero, bullets, scooter_list, car_list):
        if self.move(hero, bullets, scooter_list, car_list) == False:
            return False        
                

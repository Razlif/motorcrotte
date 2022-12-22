from Pygame_Functions.pygame_functions import *
import math, random
from sound_elements import *

setAutoUpdate(False)



def spawn_top_cars(top_car_list):   # if no cars in the list create a car and append to list 
    if len(top_car_list) < 8:
        car = top_car()
        top_car_list.append(car)

def spawn_bottom_cars(bottom_car_list):
    if len(bottom_car_list) < 0:
        car = bottom_car()
        bottom_car_list.append(car)

def spawn_scooters(scooter_list):
    if len(scooter_list) < 0:
        scooter = Scooter()
        scooter_list.append(scooter)
        
def spawn_bicycle(bicycle_list):
    if len(bicycle_list) < 0:
        probability = random.randint(1,100)
        if probability == 1:
            bicycle = Bicycle()
            bicycle_list.append(bicycle)
        
def check_for_collision(sprite1, sprite2):
    if sprite1.sprite in allTouching(sprite2.sprite):
        if abs((sprite1.ypos + sprite1.height)-(sprite2.ypos + sprite2.height)) < 50:
            if sprite1.xpos+sprite1.width <= sprite2.xpos+15:
                collision = "front_collision"
            elif sprite1.xpos +15 >= sprite2.xpos+sprite2.width:
                collision = "back_collision"
            elif sprite1.ypos+sprite1.height > sprite2.ypos+sprite2.height:
                collision = "top_collision"
            else:
                collision = "bottom_collision"
        else:
            collision = "overlap"
    else:
        collision = "none"
    return collision

class top_car():
    def __init__(self):       
        self.xpos = random.randint(1250, 2250)
        self.starting_lane = random.randint(1,2)
        if self.starting_lane == 1:
            self.ypos = random.randint(325,335)
        else:
            self.ypos = random.randint(385,395)
        self.speed = random.randint(1,10)
        self.speed_meter = self.speed
        self.health = 100 
        self.frame = 0
        self.running = True
        self.collision = False
        self.overlap = True
        self.hit = False
        self.timeOfNextFrame = clock()
        self.type = random.randint(1,11)
        self.sprite = makeSprite("media/images/cars/regular/car_"+str(self.type)+".png",2)
        if self.type < 7:
            transformSprite(self.sprite, 0, 2.25, hflip=False, vflip=False)
        elif self.type < 11:
            transformSprite(self.sprite, 0, 2.92, hflip=False, vflip=False)
        else:
            transformSprite(self.sprite, 0, 2.7, hflip=False, vflip=False)
        self.impact_picture = pygame.image.load("media/images/poop.png") 
        self.height = self.sprite.rect.height
        self.width =  self.sprite.rect.width
        showSprite(self.sprite)
        

    def move(self, hero, bullets, top_car_list):
             
        if clock() > self.timeOfNextFrame:  
            self.frame = (self.frame + 1) % 2  
            self.timeOfNextFrame += 80  
        changeSpriteImage(self.sprite,  0*2+self.frame)
        
        for car in top_car_list:   # when touching other cars
            collision = check_for_collision(self, car)
            if collision == "back_collision":
                self.xpos += 15
                probability = random.randint(1,500)
                if probability == 1:
                    horn_sound.play() 
                
            elif collision == "top_collision":
                self.ypos += 3
                
            elif collision == "bottom_collision":
                self.ypos -= 3
                
            elif collision == "front_collision":
                self.xpos -= 25
                self.speed_meter = car.speed_meter * 0.90
                probablity = random.randint(1,4)
                if self.ypos+self.height > car.ypos + car.height :
                    self.ypos += 5
                    self.speed_meter = car.speed_meter * 1.1
                else:
                    self.ypos -= 5
                    self.speed_meter = car.speed_meter * 1.1

                
            elif collision == "overlap":
                self.overlap = True
                if self.ypos+self.height > car.ypos + car.height :
                    self.ypos += 10
                    car.ypos -= 10
                    self.speed_meter = car.speed_meter * 1.05

                        
                    

            else:
                self.overlap = False

                        

                    
                        
                    

        # in case of collision with player
        if self.sprite in allTouching(hero.sprite) and abs((hero.ypos + hero.height)-(self.ypos + self.height)) < 10 and hero.jump == False:
            if self.xpos < hero.xpos:
                horn_sound.play()
            self.collision = True
        else:
            self.collision = False
        
         
        # when in collision status 
        if self.collision == True:
            if self.running == True:
                hero.speed = hero.speed * 0.90
                if hero.ypos > self.ypos:
                    hero.ypos += 3
                else:
                    hero.ypos -= 3
                runing_sound.stop()
                idle_sound.stop()
                horn_sound.play()
                self.running = False
            
            else:
                if hero.speed > 1:
                    self.running = True
        else:
            self.running = True
        
        
        # manage bullet impact
        for bullet in bullets:
            if self.sprite in allTouching(bullet.sprite):
                if bullet.impact == False:   
                    self.hit = True
                    hit_position_x = 0
                    hit_position_y = 0
                    
                    # paint the impact picture in the hit location to all frames of the sprite
                    for frame in range(1):
                        changeSpriteImage(self.sprite, frame)
                        self.sprite.image.blit(self.impact_picture, (hit_position_x, hit_position_y))                                        
                    
                    # kill the bullet sprite
                    killSprite(bullet.sprite)
        
        
        #When hit by bullet 
        if self.hit == True:
            horn_sound.play()
            self.running = False
            self.hit = False
        
                                
        
        # when running (not hit or collision)
        if self.running == True and self.overlap == False:
            if hero.speed < 10:
                self.speed_meter = self.speed * (random.randint(7,9)*0.1)
            else: 
                self.speed_meter = hero.speed * (random.randint(7,9)*0.1)
                if self.speed_meter < hero.speed * 0.5:
                    self.speed_meter = hero.speed * 0.5
                else:
                    if self.speed_meter > hero.speed * 1.2:
                        self.speed_meter = hero.speed * 1.2 
        else:
            self.speed_meter = 0        

        
        ## move
        self.xpos += self.speed_meter
        self.xpos += int(hero.speed)*-1
        
        # when out of bounds kill car sprite
        if self.xpos - hero.xpos > 1200 or self.xpos - hero.xpos < -1200:
            killSprite(self.sprite)
            return False
            
        
        # keep car in play boundries
        if self.ypos < 335:
            self.ypos = 335
        if self.ypos > 420:
            self.ypos = 420
            
        moveSprite(self.sprite, self.xpos, self.ypos)
        
    
    def update(self, hero, bullets, top_car_list):
        if self.move(hero, bullets, top_car_list) == False:
            return False
            
        
                     

class bottom_car():
    def __init__(self):       
        probability = random.randint(1,4)
        if probability == 1:   # create special fast car behind the player
            self.xpos = -300
            self.ypos = random.randint(340,380)
            self.special = True
        else:   # create regular car infront of the player
            self.xpos = random.randint(5,7) * 200
            self.ypos = random.randint(360,380)
            self.special = False
        
        self.speed = random.randint(2,4)
        self.health = 100 
        self.frame = 0
        self.running = True
        self.collision = False
        self.hit = False
        self.overlap = False
        self.timeOfNextFrame = clock()
        self.type = random.randint(1,20)
        self.sprite = makeSprite("media/images/cars/Asset_Car_"+str(self.type)+".png",2)
        transformSprite(self.sprite, 0, 2, hflip=False, vflip=False)
        self.impact_picture = pygame.image.load("media/images/poop.png") 
        showSprite(self.sprite)
        

    def move(self, hero, bullets, bottom_car_list):
             
        if clock() > self.timeOfNextFrame:  
            self.frame = (self.frame + 1) % 2  
            self.timeOfNextFrame += 80  
        changeSpriteImage(self.sprite,  0*2+self.frame)
        
        for car in bottom_car_list:
            if self.sprite in allTouching(car.sprite):
                if self.xpos < car.xpos:
                    self.xpos -= 1
                    car.xpos += 1
                    car.speed +=0.25
                    if abs((car.ypos + car.sprite.rect.height)-(self.ypos + self.sprite.rect.height)) < 20:
                        probability = random.randint(1,3)
                        if probability == 1:
                            horn_sound.play()
                        self.xpos -= 5
                        car.xpos += 10
                        if car.ypos > self.ypos:
                            self.ypos-=11
                        else:
                            self.ypos+=11
                            
                    
        
        if self.sprite in allTouching(hero.sprite) and abs((hero.ypos + hero.sprite.rect.height)-(self.ypos + self.sprite.rect.height)) < 15  and hero.jump == False:
            if self.xpos < hero.xpos:
                horn_sound.play()
            self.collision = True
        else:
            self.collision = False
        
              
        if self.collision == True:
            if self.running == True:
                hero.speed = hero.speed * 0.5
                if hero.ypos > self.ypos:
                    hero.ypos += 3
                else:
                    hero.ypos -= 3
                runing_sound.stop()
                idle_sound.stop()
                horn_sound.play()
                self.running = False
            
            else:
                self.speed = hero.speed
                if hero.speed > 1:
                    self.running = True
        else:
            self.running = True
        
        
        for bullet in bullets:
            if self.sprite in allTouching(bullet.sprite):
                if bullet.impact == False:
                    self.hit = True
                    hit_position_x = random.randint(65,150)
                    hit_position_y = random.randint(0,20)
                    for frame in range(2):
                        changeSpriteImage(self.sprite, frame)
                        self.sprite.image.blit(self.impact_picture, (hit_position_x, hit_position_y))                                        
                    killSprite(bullet.sprite)
        
        
        if self.hit == True:
            horn_sound.play()
            self.running = False
            self.hit = False
        
                                
        if self.running == True:
            if self.special == True:
                if hero.speed > 0:
                    if self.xpos < (hero.xpos - 350) or self.xpos > (hero.xpos + 1000):
                        self.speed = hero.speed * (random.randint(11,15)*0.1)
                    else:
                        self.speed += 0.01
            else:
                if hero.speed > 5:
                    self.speed = hero.speed * (random.randint(5,9)*0.1)
                else:
                    self.speed = random.randint(1,5)
            self.xpos += self.speed
            self.xpos += int(hero.speed)*-1
            

        else:
            self.speed = 0
            self.xpos += int(hero.speed)*-1
        
        if self.xpos - hero.xpos > 1200 or self.xpos - hero.xpos < -1200:
            killSprite(self.sprite)
            return False
            
        if self.ypos < 280:
            self.ypos = 280
        if self.ypos > 380:
            self.ypos = 380
            
        moveSprite(self.sprite, self.xpos, self.ypos)
        
    
    def update(self, hero, bullets, bottom_car_list):
        if self.move(hero, bullets, bottom_car_list) == False:
            return False
            
        

class Scooter():
    def __init__(self):       
        probability = random.randint(1,4)
        if probability == 1:
            self.xpos = -300
            self.ypos = random.randint(340,380)
            self.special = True
        else:
            self.xpos = random.randint(5,7) * 200
            self.ypos = random.randint(330,395)
            self.special = False
        self.sound = False
        self.speed = random.randint(2,4)
        self.health = 100 
        self.frame = 0
        self.running = True
        self.collision = False
        self.hit = False
        self.timeOfNextFrame = clock()
        self.type = random.randint(1,19)
        self.sprite = makeSprite("media/images/bikes/"+str(self.type)+"_1.png",1)
        for i in range(2,5):
            addSpriteImage(self.sprite, "media/images/bikes/"+str(self.type)+"_"+str(i)+".png")
        transformSprite(self.sprite, 0, 1.75, hflip=False, vflip=False)
        #image_name = "bike"+str(self.type)
        #self.sprite = makeSprite("media/images/"+image_name+".png",4)
        self.impact_picture = pygame.image.load("media/images/poop.png") 
        showSprite(self.sprite)
        

    def move(self, hero, bullets, scooter_list, top_car_list, bottom_car_list):
             
        if clock() > self.timeOfNextFrame:  
            self.frame = (self.frame + 1) % 4  
            self.timeOfNextFrame += 80  
        changeSpriteImage(self.sprite,  0*4+self.frame)
        
        for scooter in scooter_list:
            if self.sprite in allTouching(scooter .sprite):
                if self.xpos < scooter .xpos:
                    self.xpos -= 1
                    scooter .xpos += 1
                    scooter .speed +=0.25
                    if abs((scooter .ypos + scooter .sprite.rect.height)-(self.ypos + self.sprite.rect.height)) < 20:
                        probability = random.randint(1,3)
                        if probability == 1:
                            horn_sound.play()
                        self.xpos -= 5
                        scooter .xpos += 10
                        if scooter .ypos > self.ypos:
                            self.ypos-=11
                        else:
                            self.ypos+=11
        
        
        for car in top_car_list:
            if self.sprite in allTouching(car.sprite):
                if self.xpos < car.xpos:
                    self.xpos -= 1
                    car.xpos += 1
                    car.speed +=0.25
                    if abs((car.ypos + car.sprite.rect.height)-(self.ypos + self.sprite.rect.height)) < 20:
                        probability = random.randint(1,3)
                        if probability == 1:
                            horn_sound.play()
                        self.xpos -= 5
                        car.xpos += 10
                        if car.ypos > self.ypos:
                            self.ypos-=11
                        else:
                            self.ypos+=11
        
        for car in bottom_car_list:
            if self.sprite in allTouching(car.sprite):
                if self.xpos < car.xpos:
                    self.xpos -= 1
                    car.xpos += 1
                    car.speed +=0.25
                    if abs((car.ypos + car.sprite.rect.height)-(self.ypos + self.sprite.rect.height)) < 20:
                        probability = random.randint(1,3)
                        if probability == 1:
                            horn_sound.play()
                        self.xpos -= 5
                        car.xpos += 10
                        if car.ypos > self.ypos:
                            self.ypos-=11
                        else:
                            self.ypos+=11
                            
        
        if self.sprite in allTouching(hero.sprite) and abs((hero.ypos + hero.sprite.rect.height)-(self.ypos + self.sprite.rect.height)) < 15  and hero.jump == False:
            if self.xpos < hero.xpos:
                horn_sound.play()
            self.collision = True
        else:
            self.collision = False
        
              
        if self.collision == True:
            if self.running == True:
                hero.speed = hero.speed * 0.5
                if hero.ypos > self.ypos:
                    hero.ypos += 3
                else:
                    hero.ypos -= 3
                runing_sound.stop()
                idle_sound.stop()
                horn_sound.play()
                self.running = False
            
            else:
                self.speed = hero.speed
                if hero.speed > 1:
                    self.running = True
        else:
            self.running = True
        
        
        for bullet in bullets:
            if self.sprite in allTouching(bullet.sprite):
                if bullet.impact == False:
                    self.hit = True
                    hit_position_x = 5
                    hit_position_y = 5
                    for frame in range(4):
                        changeSpriteImage(self.sprite, frame)
                        self.sprite.image.blit(self.impact_picture, (hit_position_x, hit_position_y))                                        
                    killSprite(bullet.sprite)
        
        if self.hit == True:
            if self.running == True:
                hit_sound.play()
                self.running = False
            else:
                hit_sound.stop
        
                                
        if self.running == True:
            if self.special == True:
                if hero.speed > 0:
                    if self.xpos < (hero.xpos - 350) or self.xpos > (hero.xpos + 1000):
                        self.speed = hero.speed * (random.randint(11,15)*0.1)
                    else:
                        self.speed += 0.01
            else:
                if hero.speed > 5:
                    self.speed = hero.speed * (random.randint(5,9)*0.1)
                else:
                    self.speed = random.randint(1,5)
            self.xpos += self.speed
            self.xpos += int(hero.speed)*-1
            

        else:
            self.speed = 0
            self.xpos += int(hero.speed)*-1
        
        if self.xpos - hero.xpos > 1200 or self.xpos - hero.xpos < -1200:
            killSprite(self.sprite)
            return False
            
        if self.ypos < 280:
            self.ypos = 280
        if self.ypos > 380:
            self.ypos = 380
            
        moveSprite(self.sprite, self.xpos, self.ypos)
        
    
    def update(self, hero, bullets, scooter_list, top_car_list, bottom_car_list):
        if self.move(hero, bullets, scooter_list, top_car_list, bottom_car_list) == False:
            return False
            




class Bicycle():
    def __init__(self):       
        probability = random.randint(1,4)
        if probability == 1:
            self.xpos = random.randint(3,5) * 400
            self.ypos = random.randint(260,280) 
            self.special = True
        else:
            self.xpos = random.randint(3,5) * 400
            self.ypos = random.randint(260,280) 
            self.special = False
        self.sound = False
        self.speed = 1
        self.health = 100 
        self.frame = 0
        self.running = True
        self.collision = False
        self.hit = False
        self.timeOfNextFrame = clock()
        self.sprite = makeSprite("media/images/bicycle_flip.png",4)
        self.impact_picture = pygame.image.load("media/images/poop.png") 
        showSprite(self.sprite)
        

    def move(self, hero, bullets, scooter_list, top_car_list, bottom_car_list):
             
        if clock() > self.timeOfNextFrame:  
            self.frame = (self.frame + 1) % 4  
            self.timeOfNextFrame += 80  
        changeSpriteImage(self.sprite,  0*4+self.frame)
                             

        
        if self.sprite in allTouching(hero.sprite) and abs((hero.ypos + hero.sprite.rect.height)-(self.ypos + self.sprite.rect.height)) < 5  and hero.jump == False:
            if self.xpos < hero.xpos:
                self.collision = True
        else:
            self.collision = False
        
              
        if self.collision == True:
            if self.running == True:
                hero.speed = hero.speed * 0.5
                if hero.ypos > self.ypos:
                    hero.ypos += 3
                else:
                    hero.ypos -= 3
                self.running = False
            
            else:
                self.speed = hero.speed
                if hero.speed > 1:
                    self.running = True
        else:
            self.running = True
        
        
        for bullet in bullets:
            if self.sprite in allTouching(bullet.sprite):
                if bullet.impact == False:
                    self.hit = True
                    hit_position_x = 5
                    hit_position_y = 5
                    for frame in range(4):
                        changeSpriteImage(self.sprite, frame)
                        self.sprite.image.blit(self.impact_picture, (hit_position_x, hit_position_y))                                        
                    killSprite(bullet.sprite)
        
        
        if self.hit == True:
            if self.running == True:
                hit_sound.play()
                self.running = False
            else:
                hit_sound.stop

                                
        if self.running == True:
            if self.special == True:
                if hero.speed > 0:
                    if self.xpos < (hero.xpos - 350) or self.xpos > (hero.xpos + 1000):
                        self.speed = hero.speed * (random.randint(11,15)*0.1)
                    else:
                        self.speed += 0.01
            else:
                if hero.speed > 5:
                    self.speed = hero.speed * (random.randint(5,9)*0.1)
                else:
                    self.speed = random.randint(1,5)
            self.xpos -= self.speed
            self.xpos += int(hero.speed)*-1
            

        else:
            self.speed = 0
            self.xpos += int(hero.speed)*-1
        
        if self.xpos - hero.xpos > 1200 or self.xpos - hero.xpos < -1200:
            killSprite(self.sprite)
            return False
            
        if self.ypos < 160:
            self.ypos = 160
        if self.ypos > 220:
            self.ypos = 220
            
            
        moveSprite(self.sprite, self.xpos, self.ypos)
        
    
    def update(self, hero, bullets, scooter_list, top_car_list, bottom_car_list):
        if self.move(hero, bullets, scooter_list, top_car_list, bottom_car_list) == False:
            return False
            

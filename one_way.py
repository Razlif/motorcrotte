from Pygame_Functions.pygame_functions import *
import math, random
from sound_elements import *

setAutoUpdate(False)



def spawn_top_cars(top_car_list):   # if no cars in the list create a car and append to list 
    if len(top_car_list) < 1:
        car = top_car()
        top_car_list.append(car)

def spawn_bottom_cars(bottom_car_list):
    if len(bottom_car_list) < 1:
        car = bottom_car()
        bottom_car_list.append(car)

def spawn_scooters(scooter_list):
    if len(scooter_list) < 1:
        scooter = Scooter()
        scooter_list.append(scooter)
        
def spawn_bicycle(bicycle_list):
    if len(bicycle_list) < 1:
        probability = random.randint(1,100)
        if probability == 1:
            bicycle = Bicycle()
            bicycle_list.append(bicycle)
        
        

class top_car():
    def __init__(self):       
        self.xpos = random.randint(5,7) * 200
        self.ypos = random.randint(290,315)
        self.speed = random.randint(2,4)
        self.health = 100 
        self.frame = 0
        self.running = True
        self.collision = False
        self.hit = False
        self.timeOfNextFrame = clock()
        self.type = random.randint(1,2)
        image_name = "car"+str(self.type)
        self.sprite = makeSprite("media/images/"+image_name+".png",4)
        self.impact_picture = pygame.image.load("media/images/poop.png") 
        showSprite(self.sprite)
        

    def move(self, hero, bullets, top_car_list):
             
        if clock() > self.timeOfNextFrame:  
            self.frame = (self.frame + 1) % 4  
            self.timeOfNextFrame += 80  
        changeSpriteImage(self.sprite,  0*4+self.frame)
        
        for car in top_car_list:   # in case of collision with other cars in the list 
            if self.sprite in allTouching(car.sprite):   # in case sprites are overlapping but necessarly in collision
                if self.xpos < car.xpos:
                    self.xpos -= 1
                    car.xpos += 1
                    car.speed +=0.25   # the back car will acclerate
                    if abs((car.ypos + car.sprite.rect.height)-(self.ypos + self.sprite.rect.height)) < 20:   # in case of collision
                        probability = random.randint(1,3)
                        if probability == 1:
                            horn_sound.play()   # only sometimes play the horn 
                        self.xpos -= 5
                        car.xpos += 10
                        if car.ypos > self.ypos:   # the back car will also move up or down to exit collision status 
                            self.ypos-=11
                        else:
                            self.ypos+=11
                    
                        
                    

        # in case of collision with player
        if self.sprite in allTouching(hero.sprite) and abs((hero.ypos + hero.sprite.rect.height)-(self.ypos + self.sprite.rect.height)) < 15  and hero.jump == False:
            if self.xpos < hero.xpos:
                horn_sound.play()
            self.collision = True
        else:
            self.collision = False
        
         
        # when in collision status 
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
        
        
        # manage bullet impact
        for bullet in bullets:
            if self.sprite in allTouching(bullet.sprite):
                if bullet.impact == False:   
                    self.hit = True
                    hit_position_x = random.randint(65,150)
                    hit_position_y = random.randint(0,20)
                    
                    # paint the impact picture in the hit location to all frames of the sprite
                    for frame in range(4):
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
        if self.running == True:
            if hero.speed > 5:
                self.speed = hero.speed * (random.randint(5,9)*0.1)
            else:
                self.speed = random.randint(2,5)
            self.xpos += self.speed
            self.xpos += int(hero.speed)*-1
        else:
            self.speed = 0
            self.xpos += int(hero.speed)*-1
        
        
        # when out of bounds kill car sprite
        if self.xpos - hero.xpos > 1200 or self.xpos - hero.xpos < -1200:
            killSprite(self.sprite)
            return False
            
        
        # keep car in play boundries
        if self.ypos < 280:
            self.ypos = 280
        if self.ypos > 380:
            self.ypos = 380
            
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
        self.timeOfNextFrame = clock()
        self.type = random.randint(1,2)
        image_name = "car"+str(self.type)
        self.sprite = makeSprite("media/images/"+image_name+".png",4)
        self.impact_picture = pygame.image.load("media/images/poop.png") 
        showSprite(self.sprite)
        

    def move(self, hero, bullets, bottom_car_list):
             
        if clock() > self.timeOfNextFrame:  
            self.frame = (self.frame + 1) % 4  
            self.timeOfNextFrame += 80  
        changeSpriteImage(self.sprite,  0*4+self.frame)
        
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
                    for frame in range(4):
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
        self.type = random.randint(1,3)
        image_name = "bike"+str(self.type)
        self.sprite = makeSprite("media/images/"+image_name+".png",4)
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
            
        if self.ypos  < 150:
            self.ypos = 150
        if self.ypos > 230:
            self.ypos = 230
            
            
        moveSprite(self.sprite, self.xpos, self.ypos)
        
    
    def update(self, hero, bullets, scooter_list, top_car_list, bottom_car_list):
        if self.move(hero, bullets, scooter_list, top_car_list, bottom_car_list) == False:
            return False
            

from Pygame_Functions.pygame_functions import *
import math, random
from sound_elements import *

setAutoUpdate(False)



def spawn_top_cars(top_cars_list):
    if len(top_cars_list) < 1:
        car = top_car()
        top_cars_list.append(car)

def spawn_bottom_cars(bottom_cars_list):
    if len(bottom_cars_list) < 1:
        car = bottom_car()
        bottom_cars_list.append(car)

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
        probability = random.randint(1,5)
        if probability == 1:
            self.xpos = -300
            self.special = False
        else:
            self.xpos = random.randint(5,7) * 200
            self.special = False
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
        self.sprite = makeSprite("images/"+image_name+".png",4)
        self.impact_picture = pygame.image.load("images/poop.png") 
        showSprite(self.sprite)
        

    def move(self, hero, bullets, top_cars_list):
             
        if clock() > self.timeOfNextFrame:  # We only animate our character every 80ms.
            self.frame = (self.frame + 1) % 4  # There are 8 frames of animation in each direction
            self.timeOfNextFrame += 80  # so the modulus 8 allows it to loop
        changeSpriteImage(self.sprite,  0*4+self.frame)
        
        for car in top_cars_list:
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
                    
                        
                    

        
        #sprite_group.change_layer(self.sprite, sprite_group.layers()[-1])
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
                    if self.xpos < (hero.xpos - 250) or self.xpos > (hero.xpos + 650):
                        self.speed += 0.15
                    else:
                        self.speed += 0.01
            else:
                if hero.speed > 5:
                    self.speed = hero.speed * (random.randint(5,9)*0.1)
                else:
                    self.speed = random.randint(2,5)
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
            
        #if hero.ypos > self.ypos:
        #    spriteGroup.move_to_front(hero.sprite)
        #else:
        #    spriteGroup.move_to_back(hero.sprite)
            
        moveSprite(self.sprite, self.xpos, self.ypos)
        
    
    def update(self, hero, bullets, top_cars_list):
        if self.move(hero, bullets, top_cars_list) == False:
            return False
            
        
                     

class bottom_car():
    def __init__(self):       
        probability = random.randint(1,4)
        if probability == 1:
            self.xpos = -300
            self.ypos = random.randint(340,380)
            self.special = True
        else:
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
        self.sprite = makeSprite("images/"+image_name+".png",4)
        self.impact_picture = pygame.image.load("images/poop.png") 
        showSprite(self.sprite)
        

    def move(self, hero, bullets, bottom_cars_list):
             
        if clock() > self.timeOfNextFrame:  # We only animate our character every 80ms.
            self.frame = (self.frame + 1) % 4  # There are 8 frames of animation in each direction
            self.timeOfNextFrame += 80  # so the modulus 8 allows it to loop
        changeSpriteImage(self.sprite,  0*4+self.frame)
        
        for car in bottom_cars_list:
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
                            
                    

        
        #sprite_group.change_layer(self.sprite, sprite_group.layers()[-1])
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
            
        
        #if hero.ypos > self.ypos:
        #    spriteGroup.move_to_front(hero.sprite)
        #else:
        #    spriteGroup.move_to_back(hero.sprite)
        if self.ypos < 280:
            self.ypos = 280
        if self.ypos > 380:
            self.ypos = 380
            
        moveSprite(self.sprite, self.xpos, self.ypos)
        
    
    def update(self, hero, bullets, top_cars_list):
        if self.move(hero, bullets, top_cars_list) == False:
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
        self.sprite = makeSprite("images/"+image_name+".png",4)
        self.impact_picture = pygame.image.load("images/poop.png") 
        showSprite(self.sprite)
        

    def move(self, hero, bullets, scooter_list, top_cars_list, bottom_cars_list):
             
        if clock() > self.timeOfNextFrame:  # We only animate our character every 80ms.
            self.frame = (self.frame + 1) % 4  # There are 8 frames of animation in each direction
            self.timeOfNextFrame += 80  # so the modulus 8 allows it to loop
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
        
        
        for car in top_cars_list:
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
        
        for car in bottom_cars_list:
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
                            
                    

        
        #sprite_group.change_layer(self.sprite, sprite_group.layers()[-1])
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
            
        #if hero.ypos > self.ypos:
        #    spriteGroup.move_to_front(hero.sprite)
        #else:
        #    spriteGroup.move_to_back(hero.sprite)
            
        moveSprite(self.sprite, self.xpos, self.ypos)
        
    
    def update(self, hero, bullets, scooter_list, top_cars_list, bottom_cars_list):
        if self.move(hero, bullets, scooter_list, top_cars_list, bottom_cars_list) == False:
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
        self.sprite = makeSprite("images/bicycle_flip.png",4)
        self.impact_picture = pygame.image.load("images/poop.png") 
        showSprite(self.sprite)
        

    def move(self, hero, bullets, scooter_list, top_cars_list, bottom_cars_list):
             
        if clock() > self.timeOfNextFrame:  # We only animate our character every 80ms.
            self.frame = (self.frame + 1) % 4  # There are 8 frames of animation in each direction
            self.timeOfNextFrame += 80  # so the modulus 8 allows it to loop
        changeSpriteImage(self.sprite,  0*4+self.frame)
                            
                    

        
        #sprite_group.change_layer(self.sprite, sprite_group.layers()[-1])
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
            
        #if hero.ypos > self.ypos:
        #    spriteGroup.move_to_front(hero.sprite)
        #else:
        #    spriteGroup.move_to_back(hero.sprite)
            
        moveSprite(self.sprite, self.xpos, self.ypos)
        
    
    def update(self, hero, bullets, scooter_list, top_cars_list, bottom_cars_list):
        if self.move(hero, bullets, scooter_list, top_cars_list, bottom_cars_list) == False:
            return False
            

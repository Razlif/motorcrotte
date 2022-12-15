from Pygame_Functions.pygame_functions import *
import math, random
from sound_elements import *

setAutoUpdate(False)



def spawn_top_cars(top_cars_list):
    if len(top_cars_list) <1:
        car = top_car()
        top_cars_list.append(car)

def spawn_bottom_cars(bottom_cars_list):
    if len(bottom_cars_list) < 2:
        car = bottom_car()
        bottom_cars_list.append(car)
        
        

class top_car():
    def __init__(self):
        self.xpos = random.randint(3,5) * 400
        self.ypos = random.randint(360,395)
        self.speed = random.randint(1,2)
        self.health = 100 
        self.frame = 0
        self.running = True
        self.collision = False
        self.hit = False
        self.timeOfNextFrame = clock()
        self.hornTime = clock()
        self.sprite = makeSprite("images/car_flip.png",4)
        self.impact_picture = pygame.image.load("images/poop.png") 
        showSprite(self.sprite)
        

    def move(self, hero, bullets, top_cars_list):
             
        if clock() > self.timeOfNextFrame:  # We only animate our character every 80ms.
            self.frame = (self.frame + 1) % 4  # There are 8 frames of animation in each direction
            self.timeOfNextFrame += 80  # so the modulus 8 allows it to loop
        changeSpriteImage(self.sprite,  0*4+self.frame)
        
        for car in top_cars_list:
            if self.sprite in allTouching(car.sprite):
                if abs((car.ypos + car.sprite.rect.height)-(self.ypos + self.sprite.rect.height)) < 15:
                    self.xpos += 5
                    car.xpos -= 5
                    if self.ypos > car.ypos:
                        car.ypos-=11
                    else:
                        car.ypos+=11
                else:
                    if self.xpos > car.xpos:
                        self.speed += 0.1

        
        #sprite_group.change_layer(self.sprite, sprite_group.layers()[-1])
        if self.sprite in allTouching(hero.sprite) and abs((hero.ypos + hero.sprite.rect.height)-(self.ypos + self.sprite.rect.height)) < 15  and hero.jump == False:
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
                self.hornTime = clock()
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
            runing_sound.stop()
            idle_sound.stop()
            horn_sound.play()
            self.running = False
            self.hit = False
        
                                
        if self.running == True:
            self.xpos += int(hero.speed)*-1
            self.xpos -= self.speed

        else:
            self.speed = 0
            self.xpos += int(hero.speed)*-1
            if clock() > self.hornTime + 5:
                horn_sound.play()
                self.hornTime  = clock()
            else:
                horn_sound.stop()
        
        if self.xpos - hero.xpos < -1200:
            killSprite(self.sprite)
            return False
            
        
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
        probability = random.randint(1,3)
        if probability == 1:
            self.xpos = -300
            self.special = True
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
        self.hornTime = clock()
        self.sprite = makeSprite("images/car.png",4)
        self.impact_picture = pygame.image.load("images/poop.png") 
        showSprite(self.sprite)
        

    def move(self, hero, bullets, bottom_cars_list):
             
        if clock() > self.timeOfNextFrame:  # We only animate our character every 80ms.
            self.frame = (self.frame + 1) % 4  # There are 8 frames of animation in each direction
            self.timeOfNextFrame += 80  # so the modulus 8 allows it to loop
        changeSpriteImage(self.sprite,  0*4+self.frame)
        
        for car in bottom_cars_list:
            if self.sprite in allTouching(car.sprite):
                if abs((car.ypos + car.sprite.rect.height)-(self.ypos + self.sprite.rect.height)) < 15:
                    self.xpos += 5
                    car.xpos -= 5
                    if self.ypos > car.ypos:
                        car.ypos-=11
                    else:
                        car.ypos+=11
                else:
                    if self.xpos > car.xpos:
                        self.speed += 0.1
                        
                    

        
        #sprite_group.change_layer(self.sprite, sprite_group.layers()[-1])
        if self.sprite in allTouching(hero.sprite) and abs((hero.ypos + hero.sprite.rect.height)-(self.ypos + self.sprite.rect.height)) < 15  and hero.jump == False:
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
                self.hornTime = clock()
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
            runing_sound.stop()
            idle_sound.stop()
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
                    self.speed = hero.speed * (random.randint(7,9)*0.1)
                else:
                    self.speed = random.randint(2,5)
            self.xpos += self.speed
            self.xpos += int(hero.speed)*-1
            

        else:
            self.speed = 0
            self.xpos += int(hero.speed)*-1
            if clock() > self.hornTime + 5:
                horn_sound.play()
                self.hornTime  = clock()
            else:
                horn_sound.stop()
        
        if self.xpos - hero.xpos > 1200 or self.xpos - hero.xpos < -1200:
            killSprite(self.sprite)
            return False
            
        
        #if hero.ypos > self.ypos:
        #    spriteGroup.move_to_front(hero.sprite)
        #else:
        #    spriteGroup.move_to_back(hero.sprite)
            
        moveSprite(self.sprite, self.xpos, self.ypos)
        
    
    def update(self, hero, bullets, top_cars_list):
        if self.move(hero, bullets, top_cars_list) == False:
            return False
            
        

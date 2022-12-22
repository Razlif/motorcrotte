from Pygame_Functions.pygame_functions import *
import math, random
from sound_elements import *

setAutoUpdate(False)

def spawn_dogs(dog_list):   # if no dogs in the list create a dog and append to list 
    if len(dog_list) < 2:
        dog = Dog()
        dog_list.append(dog)

def spawn_person(person_list):   # if no pedestrian in the list create a pedestrian and append to list 
    if len(person_list) < 1:
        person = Person()
        person_list.append(person)

def spawn_bicycle(bicycle_list):
    if len(bicycle_list) < 1:
        probability = random.randint(1,100)
        if probability == 1:
            bicycle = Bicycle()
            bicycle_list.append(bicycle)
        

class Dog():
    def __init__(self):
        self.xpos = random.randint(3,4) * 400
        self.ypos = random.randint(290,330)
        self.speed = random.randint(4,5) * 0.1
        self.health = 100 
        self.frame = 0
        self.number_of_frames = 9
        self.timeOfNextFrame = clock()
        self.type = random.randint(1,6)
        if self.type ==2 or self.type == 6:
            self.scale = 1.7
        elif self.type == 4 or self.type == 5:
            self.scale = 1.2
        else:
            self.scale = 1.4
        self.sprite = makeSprite("media/images/dogs/dog_"+ str(self.type)+".png",self.number_of_frames)
        transformSprite(self.sprite, 0, self.scale, hflip=False, vflip=False)
        self.height = self.sprite.rect.height
        self.width =  self.sprite.rect.width
        showSprite(self.sprite)

    def move(self, hero, dog_list, person_list):
        
        # animate by frame number every 80 milisec
        if clock() > self.timeOfNextFrame: 
            self.frame = (self.frame + 1) % self.number_of_frames  
            self.timeOfNextFrame += 80  
        changeSpriteImage(self.sprite,  0*self.number_of_frames+self.frame) 
        
        #for dog in dog_list:
         #   if self.sprite in allTouching(dog.sprite):
         #       print("meet dog")
                #
                # do something when meet other dog
                
        #for person in person_list:
        #    if self.sprite in allTouching(person.sprite):
        #        print("meet person")
                #
                # do something when meet person      
                
        # in case of collision with player
        if self.sprite in allTouching(hero.sprite) and abs((hero.ypos + hero.sprite.rect.height)-(self.ypos + self.sprite.rect.height)) < 5 and hero.jump==False:
            hero.speed = hero.speed * 0.5
            if hero.ypos+hero.height > self.ypos+self.height:
                self.ypos -= 1
            else:
                self.ypos += 1
        
        if self.xpos < hero.xpos -800:   # kill sprite if out of bounds
            killSprite(self.sprite)
            return False
        else:
            self.xpos -= self.speed   # move normally when in bounds
            self.xpos += int(hero.speed)*-1
            moveSprite(self.sprite, self.xpos, self.ypos)
            return True
            

    def update(self, hero, dog_list, person_list):
        if self.move(hero, dog_list, person_list) == False:
            return False
        else:
            return True


class Person():
    def __init__(self):       
        self.speed = random.randint(2,6) * 0.1
        self.health = 100 
        self.frame = 0
        self.running = True
        self.collision = False
        self.hit = False
        self.timeOfNextFrame = clock()
        self.type = random.randint(5,7)
        if self.type == 5:
            self.number_of_frames = 9
            self.scale = 1.6
        elif self.type == 6:
            self.number_of_frames = 6
            self.scale = 0.5
        else:
            self.number_of_frames = 19
            self.scale = 1.5
        self.sprite = makeSprite("media/images/people/person"+ str(self.type)+".png",self.number_of_frames)
        self.impact_picture = pygame.image.load("media/images/poop.png") 
        transformSprite(self.sprite, 0, self.scale, hflip=False, vflip=False)
        self.height = self.sprite.rect.height
        self.width =  self.sprite.rect.width
        self.xpos = random.randint(3,6) * 400
        self.ypos = random.randint(150,180) + self.height
        showSprite(self.sprite)
        

    def move(self, hero, bullets, dog_list, person_list):
             
        if clock() > self.timeOfNextFrame: 
            self.frame = (self.frame + 1) % self.number_of_frames 
            self.timeOfNextFrame += 80  
        changeSpriteImage(self.sprite,  0*self.number_of_frames+self.frame)
                            
        #for dog in dog_list:
        #    if self.sprite in allTouching(dog.sprite):
                #
                # do something when meet  dog
                
        #for person in person_list:
        #    if self.sprite in allTouching(person.sprite):
                #
                # do something when meet other person              

        if self.sprite in allTouching(hero.sprite) and abs((hero.ypos + hero.sprite.rect.height)-(self.ypos + self.sprite.rect.height+5)) < 5  and hero.jump == False:
            hero.speed = hero.speed * 0.5
            if hero.ypos > self.ypos:
                self.ypos -= 1
            else:
                self.ypos += 1
        
              
        if self.collision == True:
            if self.running == True:
                hero.speed = hero.speed * 0.5
                if hero.ypos > self.ypos:
                    self.ypos -= 3
                else:
                    self.ypos += 3
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
                    hit_sound.play()
                    hit_position_x = -15
                    hit_position_y = -15
                    for frame in range(1,6):
                        changeSpriteImage(self.sprite, frame)
                        self.sprite.image.blit(self.impact_picture, (hit_position_x, hit_position_y))                                        
                    killSprite(bullet.sprite)
    

                                
        if self.running == True:
            self.xpos -= self.speed
            self.xpos += int(hero.speed)*-1
            

        else:
            self.speed = 0
            self.xpos += int(hero.speed)*-1
        
        if self.xpos - hero.xpos > 1200 or self.xpos - hero.xpos < -1200:
            killSprite(self.sprite)
            return False
            
        if self.ypos+ self.height  < 340:
            self.ypos = 340 - self.height
        if self.ypos + self.height > 375:
            self.ypos = 375 - self.height
            
            
        moveSprite(self.sprite, self.xpos, self.ypos)
        
    
    def update(self, hero, bullets, dog_list, person_list):
        if self.move(hero, bullets, dog_list, person_list) == False:
            return False
            
class Bicycle():
    def __init__(self):       
        self.xpos = random.randint(3,5) * 400
        self.ypos = random.randint(240,280) 
        self.sound = False
        self.speed = random.randint(1,3)
        self.health = 100 
        self.frame = 0
        self.running = True
        self.collision = False
        self.hit = False
        self.timeOfNextFrame = clock()
        self.sprite = makeSprite("media/images/bicycle_flip.png",4)
        self.impact_picture = pygame.image.load("media/images/poop.png") 
        showSprite(self.sprite)
        

    def move(self, hero, bullets, dog_list, person_list):
             
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
            self.xpos -= self.speed
            self.xpos += int(hero.speed)*-1           
        else:
            self.speed = 0
            self.xpos += int(hero.speed)*-1
        
        
        if self.xpos - hero.xpos > 1200 or self.xpos - hero.xpos < -1200:
            killSprite(self.sprite)
            return False
            
        if self.ypos < 240:
            self.ypos = 240
        if self.ypos > 280:
            self.ypos = 280
            
            
        moveSprite(self.sprite, self.xpos, self.ypos)
        
    
    def update(self, hero, bullets, dog_list, person_list):
        if self.move(hero, bullets, dog_list, person_list) == False:
            return False
            

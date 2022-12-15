from Pygame_Functions.pygame_functions import *
import math, random
from sound_elements import *

setAutoUpdate(False)


def spawn_dogs(dog_list):
    if len(dog_list) < 1:
        dog = Dog()
        dog_list.append(dog)

def spawn_person(person_list):
    if len(person_list) < 1:
        person = Person()
        person_list.append(person)
        

class Dog():
    def __init__(self):
#        self.xpos = random.randint(0,1000)
        self.xpos = random.randint(3,5) * 400
        self.ypos = random.randint(260,280) 
        self.speed = 0.5
        self.health = 100 
        self.frame = 0
        self.timeOfNextFrame = clock()
        self.sprite = makeSprite("images/dog_walking.png",8)
        showSprite(self.sprite)

    def move(self, hero):
        if clock() > self.timeOfNextFrame:  # We only animate our character every 80ms.
            self.frame = (self.frame + 1) % 8  # There are 8 frames of animation in each direction
            self.timeOfNextFrame += 80  # so the modulus 8 allows it to loop
        changeSpriteImage(self.sprite,  0*8+self.frame) 
        if self.sprite in allTouching(hero.sprite) and abs((hero.ypos + hero.sprite.rect.height)-(self.ypos + self.sprite.rect.height)) < 15 and hero.jump==False:
            hero.speed = hero.speed * 0.5
            if hero.ypos > self.ypos:
                self.ypos -= 1
            else:
                self.ypos += 1
        
        if self.xpos < hero.xpos -800:
            killSprite(self.sprite)
            return False
        else:
            self.xpos -= self.speed
            self.xpos += int(hero.speed)*-1
            moveSprite(self.sprite, self.xpos, self.ypos)
            return True
            

    def update(self, hero):
        if self.move(hero) == False:
            return False
        else:
            return True


class Person():
    def __init__(self):       
        self.xpos = random.randint(3,5) * 400
        self.ypos = random.randint(240,270)
        self.speed = 0.5
        self.health = 100 
        self.frame = 0
        self.running = True
        self.collision = False
        self.hit = False
        self.timeOfNextFrame = clock()
        self.sprite = makeSprite("images/person2.png",12)
        self.impact_picture = pygame.image.load("images/poop.png") 
        showSprite(self.sprite)
        

    def move(self, hero, bullets):
             
        if clock() > self.timeOfNextFrame:  # We only animate our character every 80ms.
            self.frame = (self.frame + 1) % 4  # There are 8 frames of animation in each direction
            self.timeOfNextFrame += 80  # so the modulus 8 allows it to loop
        changeSpriteImage(self.sprite,  0*4+self.frame)
                            
                    

        #sprite_group.change_layer(self.sprite, sprite_group.layers()[-1])
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
                    hit_position_x = -15
                    hit_position_y = -15
                    for frame in range(4):
                        changeSpriteImage(self.sprite, frame)
                        self.sprite.image.blit(self.impact_picture, (hit_position_x, hit_position_y))                                        
                    killSprite(bullet.sprite)
        
        
        if self.hit == True:
            if self.running == True:
                hit_sound.play()
                #self.running = False
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
            
        if self.ypos  < 120:
            self.ypos = 120
        if self.ypos > 280:
            self.ypos = 280
            
        #if hero.ypos > self.ypos:
        #    spriteGroup.move_to_front(hero.sprite)
        #else:
        #    spriteGroup.move_to_back(hero.sprite)
            
        moveSprite(self.sprite, self.xpos, self.ypos)
        
    
    def update(self, hero, bullets):
        if self.move(hero, bullets) == False:
            return False
            

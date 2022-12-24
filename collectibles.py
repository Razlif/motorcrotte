from Pygame_Functions.pygame_functions import *
import math, random
from sound_elements import *
import game_configuration

setAutoUpdate(False)

# function to update display on main loop

def update_display(poop_list, hero):
    for i, poop in enumerate(poop_list):
        if poop.update_state(hero) == False:
            poop_list.pop(i)    
    
    if len(poop_list) < game_configuration.max_poop_number:
        poop = Poop()
        poop_list.append(poop)



# poop class
class Poop():
    def __init__(self):
        self.xpos = random.randint(3,5) * 400
        self.ypos = random.randint(280,460) 
        self.speed = 0
        self.health = 100 
        self.frame = 0
        self.timeOfNextFrame = clock()
        self.sprite = makeSprite("media/images/poop3.png",8)
        showSprite(self.sprite)

    def update_state(self, hero):
        if clock() > self.timeOfNextFrame:  
            self.frame = (self.frame + 1) % 8  
            self.timeOfNextFrame += 80  
        changeSpriteImage(self.sprite,  0*8+self.frame) 
        
        # if collected by player
        if self.sprite in allTouching(hero.sprite) and abs((hero.ypos + hero.sprite.rect.height)-(self.ypos + self.sprite.rect.height)) < 20 :
                idle_sound.stop()
                runing_sound.stop()
                collect_sound.play()
                hero.poop += 1
                killSprite(self.sprite)
                return False
        
        elif self.xpos < -100:  # kill if out of bounds
            killSprite(self.sprite)
            return False
        
        else:
            self.xpos += int(hero.speed)*-1   # just hang around
            moveSprite(self.sprite, self.xpos, self.ypos)
            return True

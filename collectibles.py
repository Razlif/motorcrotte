from Pygame_Functions.pygame_functions import *
import math, random
from sound_elements import *
import game_configuration as settings

setAutoUpdate(False)

# function to update display on main loop

def update_display(poop_list, hero):
    for i, poop in enumerate(poop_list):
        if poop.update_state(hero) == False:
            poop_list.pop(i)

    
    if len(poop_list) < settings.max_poop_number:
        poop = Poop()
        poop_list.append(poop)




# poop class
class Poop():
    def __init__(self):
        self.xpos = random.randint(settings.spawn_x_range[0],settings.spawn_x_range[1])
        self.ypos = random.randint(settings.side_walk_top,settings.lane_3_bottom)
        self.frame = 0
        self.timeOfNextFrame = clock()
        self.number_of_frames = 8
        self.sprite = makeSprite("media/images/poop3.png",self.number_of_frames)
        self.height = self.sprite.rect.height
        self.width =  self.sprite.rect.width
        self.ground_position = self.sprite.rect.bottom
        showSprite(self.sprite)

    def update_state(self, hero):
        
        self.ground_position = self.sprite.rect.bottom
        
        if clock() > self.timeOfNextFrame:  
            self.frame = (self.frame + 1) % self.number_of_frames  
            self.timeOfNextFrame += 80  
        changeSpriteImage(self.sprite,  self.frame) 
        
        # if collected by player
        if self.sprite in allTouching(hero.sprite) and abs(hero.sprite.rect.bottom - self.sprite.rect.bottom) < 20 :
                idle_sound.stop()
                runing_sound.stop()
                collect_sound.play()
                hero.poop += 10
                killSprite(self.sprite)
                return False
        
        elif self.xpos < -100:  # kill if out of bounds
            killSprite(self.sprite)
            return False
        
        else:
            self.xpos += int(hero.x_velocity)*-1   # just hang around
            moveSprite(self.sprite, self.xpos, self.ypos)
            return True

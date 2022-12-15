from Pygame_Functions.pygame_functions import *
import math, random
from sound_elements import *

setAutoUpdate(False)


def spawn_poop(poop_list):
    if len(poop_list) < 2:
        poop = Poop()
        poop_list.append(poop)

class Poop():
    def __init__(self):
#        self.xpos = random.randint(0,1000)
        self.xpos = random.randint(3,5) * 400
        self.ypos = random.randint(280,460) 
        self.speed = 0
        self.health = 100 
        self.frame = 0
        self.timeOfNextFrame = clock()
        self.sprite = makeSprite("images/poop3.png",8)
        showSprite(self.sprite)

    def move(self, hero):
        if clock() > self.timeOfNextFrame:  # We only animate our character every 80ms.
            self.frame = (self.frame + 1) % 8  # There are 8 frames of animation in each direction
            self.timeOfNextFrame += 80  # so the modulus 8 allows it to loop
        changeSpriteImage(self.sprite,  0*8+self.frame) 
        if self.sprite in allTouching(hero.sprite) and abs((hero.ypos + hero.sprite.rect.height)-(self.ypos + self.sprite.rect.height)) < 15 :

                idle_sound.stop()
                runing_sound.stop()
                collect_sound.play()
                killSprite(self.sprite)
                return False
        elif self.xpos < hero.xpos -800:
            killSprite(self.sprite)
            return False
        else:
            self.xpos += int(hero.speed)*-1
            moveSprite(self.sprite, self.xpos, self.ypos)
            return True
            

    def update(self, hero):
        if self.move(hero) == False:
            return False
        else:
            return True

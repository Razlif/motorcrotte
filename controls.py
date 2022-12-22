## player controls

# import pygame functions acript
from Pygame_Functions.pygame_functions import *
from sound_elements import *
import math, random

setAutoUpdate(False)

# empty list for bullets
bullets = []


# player class
class Player():
    def __init__(self):
        # Reset intial Vars
        self.xpos = 200
        self.ypos = 250
        self.speed = 0
        self.health = 100
        self.xdir = 0 # shooting direction
        self.ydir = 0 # currently unused
        self.jump = False
        self.jump_origin = 13 # the size of the jump in pixels
        self.jump_meter = self.jump_origin # reset jump meter to jump size var
        self.dash = False
        self.dash_origin = 13
        self.dash_meter = self.dash_origin
        self.gas = False
        self.breaking = False
        self.up = False
        self.down = False
        self.shoot = False
        self.special = False
        self.poop = 0
        
        # create sprite
        self.sprite = makeSprite("media/images/hero/hero_1.png",1) 
        for i in range(2,5):
            addSpriteImage(self.sprite, "media/images/hero/hero_"+str(i)+".png")
        
        # sclae to correct size
        self.scale = 1.75
        angle = 0
        transformSprite(self.sprite, angle, self.scale , hflip=False, vflip=False)
        
        # addirional vars
        self.height = self.sprite.rect.height
        self.width =  self.sprite.rect.width
        self.frame = 0
        self.number_of_frames = 2
        self.timeOfNextFrame = clock()
        self.lastBulletTime = clock()
        
        # show sprite and add to spriterGroup
        showSprite(self.sprite)
        
        #Score label
        self.label = makeLabel("Speed: " + str(int(self.speed)) + "<br>Poop: " + str(self.poop), 35, 0, 0 , "green")
        showLabel(self.label)
        

    def move(self):
        if clock() > self.timeOfNextFrame:  # We only animate our character every 80ms.
            self.frame = (self.frame + 1) % self.number_of_frames  # There are 8 frames of animation in each direction
            self.timeOfNextFrame += 80  # so the modulus 8 allows it to loop
        
        # GAS - ON / OFF
        if keyPressed("right"):
            self.gas = True
        else:
            self.gas = False
        
        # BREAK - ON / OFF
        if keyPressed("left"):
            self.breaking = True
        else:
            self.breaking = False
        
        # UP
        if keyPressed("up") and self.speed > 1:
            self.up = True
        else:
            self.up = False
        
        #DOWN
        if keyPressed("down") and self.speed > 1:
            self.down = True
        else:
            self.down = False
        
        #JUMP
        if keyPressed("q") and self.speed > 1:
            self.jump = True

        
        #DASH
        if keyPressed("e") and self.speed > 1:
            self.dash = True

            
        # SHOOTING 
        if keyPressed("w"):
            if self.poop > 0:
                self.xdir = 1   # set shot direction
                self.shoot = True
        else:
            self.shoot = False
            
        # Secert Move
        if keyPressed("k"):
            if self.special == False:
                hideSprite(self.sprite)
                self.special = True
                self.hero_num = random.randint(1,11)
                
                if self.hero_num == 3:
                    self.number_of_frames = 4
                else:
                    self.number_of_frames = 2
                    
                if self.hero_num == 1:
                    self.scale = 1.1
                elif self.hero_num == 2:
                    self.scale = 0.2
                elif self.hero_num == 3:
                    self.scale = 1.15
                elif self.hero_num == 4:
                    self.scale = 1.2
                elif self.hero_num == 5:
                    self.scale = 0.25
                elif self.hero_num == 6:
                    self.scale = 0.15
                elif self.hero_num == 7:
                    self.scale = 0.23
                elif self.hero_num == 8:
                    self.scale = 0.15
                elif self.hero_num == 9:
                    self.scale = 0.23
                elif self.hero_num == 10:
                    self.scale = 0.15
                else:
                    self.scale = 0.50

                self.frame = 0                
                self.sprite = makeSprite("media/images/hero/special/special_"+str(self.hero_num)+".png",self.number_of_frames)
                transformSprite(self.sprite, 0, self.scale, hflip=False, vflip=False)
                showSprite(self.sprite)
            
        if keyPressed("o"):
            if self.special == True:
                hideSprite(self.sprite)
                self.special = False
                self.scale = 1.75
                self.frame = 0
                self.number_of_frames = 4
                self.sprite = makeSprite("media/images/hero/hero_1.png",1) 
                for i in range(2,5):
                    addSpriteImage(self.sprite, "media/images/hero/hero_"+str(i)+".png")
                transformSprite(self.sprite, 0, self.scale, hflip=False, vflip=False)
                showSprite(self.sprite)
        
        # when gas
        if self.gas == True:  
            idle_sound.stop()
            runing_sound.play()
            changeSpriteImage(self.sprite,  0*self.number_of_frames+self.frame)    
            if self.speed < 20:  # speed limit - but can be sxceeded using the DASH move 
                self.speed +=0.06
        
        # when break
        elif self.breaking == True:  
            runing_sound.stop()
            idle_sound.play()
            if self.speed > 0:
                self.speed -=0.03
                if self.xpos > 100:   # if breaking while player position hogher than 100 player's position will move back on the screen
                    self.xpos -= 4
                    changeSpriteImage(self.sprite,0)
                    angle = -5
                    transformSprite(self.sprite, angle , self.scale, hflip=False, vflip=False)
        
        # when idle
        else:  
            changeSpriteImage(self.sprite,  0*self.number_of_frames+self.frame) 
            if self.speed > 0:
                self.speed -=0.002   # natural deceleration 
                runing_sound.stop()
                idle_sound.play()
        
        
        # when up
        if self.up == True:
            self.ypos -= 2
            if self.jump == False:
                if self.ypos < 290 and self.ypos > 275:  # skip the pavement when moving up the screen
                    self.ypos = 275                  
            else:
                self.ypos += 0.5


        # when down         
        if self.down == True:
            self.ypos += 2
            if self.jump == False:
                if self.ypos > 275 and self.ypos < 290:  # skip the pavement when moving down the screen
                    self.ypos = 290                  
            else:
                self.ypos -= 0.5

                                   
        # when jump    
        if self.jump == True:
            angle = -10
            self.ypos -= self.jump_meter
            self.jump_meter -= 0.5
            changeSpriteImage(self.sprite,0)   # switch to jump frame animation
            transformSprite(self.sprite, angle , self.scale, hflip=False, vflip=False)
            if self.jump_meter < (self.jump_origin*-1):
                self.jump = False
                self.jump_meter = self.jump_origin
            
                        
        
        # when dash
        if self.dash == True:
            if self.dash_meter < 1:
                changeSpriteImage(self.sprite,0)
                self.dash_meter -= 0.25
                angle = 2
                transformSprite(self.sprite, angle, self.scale, hflip=False, vflip=False)
            if self.dash_meter < (self.dash_origin*-1):
                self.dash = False
                self.dash_meter = self.dash_origin
            else:
                self.speed +=0.03   # increase speed when dash
                self.xpos += self.dash_meter
                self.dash_meter -= 0.25
                changeSpriteImage(self.sprite,0)   # switch to dash frame animation
                angle = 5
                transformSprite(self.sprite, angle, self.scale, hflip=False, vflip=False)

        
        
        if self.dash == False and self.jump == False and self.breaking == False:
            angle = 0
            transformSprite(self.sprite, angle, self.scale, hflip=False, vflip=False)
        
        # when shoot
        if self.shoot == True:
            if clock() > self.lastBulletTime + 240:   # limit shots to every 240 milisec
                bullets.append(Bullet(self.xpos + 20, self.ypos + 20, self.xdir * 5, 0))   # create a new bullet and append it to bullet list 
                self.lastBulletTime = clock()
                runing_sound.stop()
                idle_sound.stop()
                shoot_sound.play()
                self.poop -= 1
                
        
        
        # Make sure player position is inside play boundries 
        if self.jump == False:
            # keep Y position boundries
            if self. ypos + self.height > 560:
                self.ypos = 560 - self.height
            if self. ypos + self.height < 350:
                self.ypos = 350 - self.height
            # keep X position boundries
            if self.xpos > 1200:
                self.xpos = 1200
            
        # update player position to new location
        moveSprite(self.sprite, self.xpos, self.ypos)
        
        # update bullet list
        for bullet in bullets:
            if bullet.move(self) == False:
                bullets.remove(bullet)
        
        # update score
        self.label.update("Speed: " + str(int(self.speed)) + "<br>Poop: " + str(self.poop), None, None)
        
    def update(self):
        self.move()
                

# bullet class
class Bullet():
    def __init__(self, xpos, ypos, xspeed, damage):
        self.xpos = xpos
        self.ypos = ypos
        self.xspeed = xspeed
        self.damage = 0
        self.impact = False
        self.sprite = makeSprite("media/images/poop2.png")
        addSpriteImage(self.sprite, "media/images/poop.png")
        showSprite(self.sprite)        

    def move(self, hero):
        if self.impact == False:  # if impact is false move the bullet along the X axis based on it's speed
            self.xpos += self.xspeed
            changeSpriteImage(self.sprite,0)   # flying animation frame
        else:
            changeSpriteImage(self.sprite,1)   # impact animation frame
        
        if self.xpos < -100 or self.xpos > 1300 or self.ypos < -100 or self.ypos > 800:   # false when out of boundries
            return False
        
        moveSprite(self.sprite, self.xpos, self.ypos)
        return True




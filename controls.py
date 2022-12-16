## player controls

# import pygame functions acript
from Pygame_Functions.pygame_functions import *
from sound_elements import *

setAutoUpdate(False)

# empty list for bullets
bullets = []


# player class
class Player():
    def __init__(self):
        self.xpos = 200
        self.ypos = 240
        self.speed = 0
        self.health = 100
        self.xdir = 0
        self.ydir = 0
        self.currentWeapon = 0
        self.jump = False
        self.jump_origin = 13
        self.jump_meter = self.jump_origin
        self.dash = False
        self.dash_origin = 15
        self.dash_meter = self.dash_origin
        self.gas = False
        self.breaking = False
        self.up = False
        self.down = False
        self.shoot = False       
        self.sprite = makeSprite("media/images/links.png",32)
        addSpriteImage(self.sprite, "media/images/jump.png")
        addSpriteImage(self.sprite, "media/images/dash.png")
        showSprite(self.sprite)
        self.frame = 0
        self.timeOfNextFrame = clock()
        self.lastBulletTime = clock()

    def move(self):
        if clock() > self.timeOfNextFrame:  # We only animate our character every 80ms.
            self.frame = (self.frame + 1) % 8  # There are 8 frames of animation in each direction
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
            self.xdir = 1   # set shot direction
            self.shoot = True
        else:
            self.shoot = False
            
        
        # when gas
        if self.gas == True:  
            idle_sound.stop()
            runing_sound.play()
            changeSpriteImage(self.sprite,  0*8+self.frame)    
            if self.speed < 14:  # speed limit - but can be sxceeded using the DASH move 
                self.speed +=0.03
        
        # when break
        elif self.breaking == True:  
            runing_sound.stop()
            idle_sound.play()
            if self.speed > 0:
                self.speed -=0.02
                if self.xpos > 100:   # if breaking while player position hogher than 100 player's position will move back on the screen
                    changeSpriteImage(self.sprite,32)
                    self.xpos -= 4
        
        # when idle
        else:  
            changeSpriteImage(self.sprite,  0*8+self.frame) 
            if self.speed > 0:
                self.speed -=0.002   # natural deceleration 
                runing_sound.stop()
                idle_sound.play()
        
        
        # when up
        if self.up == True:
            self.ypos -= 1.1
            if self.jump == False:
                if self.ypos < 275 and self.ypos > 260:  # skip the pavement when moving up the screen
                    self.ypos = 260                  
            else:
                self.ypos -= 1.2


        # when down         
        if self.down == True:
            self.ypos += 1.1
            if self.jump == False:
                if self.ypos > 260 and self.ypos < 275:  # skip the pavement when moving down the screen
                    self.ypos = 275                  
            else:
                self.ypos += 1.2

                                   
        # when jump    
        if self.jump == True:
            self.ypos -= self.jump_meter
            self.jump_meter -= 0.5
            changeSpriteImage(self.sprite,32)   # switch to jump frame animation
            if self.jump_meter < (self.jump_origin*-1):
                self.jump = False
                self.jump_meter = self.jump_origin
                        
        
        # when dash
        if self.dash == True:
            if self.dash_meter < 1:
                changeSpriteImage(self.sprite,0)
                self.dash_meter -= 0.25
            if self.dash_meter < (self.dash_origin*-1):
                self.dash = False
                self.dash_meter = self.dash_origin
            else:
                self.speed +=0.03   # increase speed when dash
                self.xpos += self.dash_meter
                self.dash_meter -= 0.25
                changeSpriteImage(self.sprite,33)   # switch to dash frame animation



        # when shoot
        if self.shoot == True:
            if clock() > self.lastBulletTime + 240:   # limit shots to every 240 milisec
                bullets.append(Projectile(self.xpos + 20, self.ypos + 20, self.xdir * 5, 0))   # create a new bullet and append it to bullet list 
                self.lastBulletTime = clock()
                runing_sound.stop()
                idle_sound.stop()
                shoot_sound.play()
                
        
        
        # Make sure player position is inside play boundries 
        if self.jump == False:
            if self.ypos > 410:
                self.ypos = 410
            if self.ypos < 230:
                self.ypos = 230
            if self.xpos > 1000:
                self.xpos -= 1
            if self.xpos < -100:
                self.speed = self.speed*1.1
        
        # update player position to new location
        moveSprite(self.sprite, self.xpos, self.ypos)
        
        # update bullet list
        for bullet in bullets:
            if bullet.move(self) == False:
                bullets.remove(bullet)
                
    def update(self):
        self.move()
                

# bullet class
class Bullet():
    def __init__(self, xpos, ypos, xspeed, damage):
        self.xpos = xpos
        self.xspeed = xspeed
        self.yspeed = yspeed
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
        
        if self.xpos < 0 or self.xpos > 1000 or self.ypos < 0 or self.ypos > 800:   # false when out of boundries
            return False
        
        moveSprite(self.sprite, self.xpos, self.ypos)
        return True


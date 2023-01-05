# enemy class

# import pygame functions acript
from Pygame_Functions.pygame_functions import *
from sound_elements import *
import math, random
import game_configuration as settings

setAutoUpdate(False)


# function to update display on main loop
def update_display(enemy_list, hero):
    spawn_enemies(enemy_list)
    for i, enemy in enumerate(enemy_list):
        if update_state(enemy, hero) == False:
            enemy_list.pop(i)

    
    
    
# function to spawn the enemies
def spawn_enemies(enemy_list):

    if len(enemy_list) < settings.max_enemy_number:   # if cars are under the max number make new car and append to list
        enemy = Basic_enemy()
        enemy_list.append(enemy)

        
# enemy class
class Enemy():
    def __init__(self):
        # Reset intial Vars
        self.xpos = 400
        self.ypos = 400
        self.speed = 0
        self.health = 100
        self.xdir = 0 # shooting direction
        self.ydir = 0 # currently unused
        self.jump = False
        self.jump_size = 13 # the size of the jump in pixels
        self.jump_meter = self.jump_size # reset jump meter to jump size var
        self.dash = False
        self.dash_origin = 13
        self.dash_meter = self.dash_origin
        self.gas = False
        self.breaking = False
        self.up = False
        self.down = False
        self.shoot = False
        self.max_speed = 0
        
        # create sprite
        self.sprite = makeSprite("media/images/cars/bikes/5_1.png",1) 
        for i in range(2,5):
            addSpriteImage(self.sprite, "media/images/cars/bikes/5_"+str(i)+".png")
        
        # sclae to correct size
        self.scale = 1.75
        angle = 0
        transformSprite(self.sprite, angle, self.scale , hflip=False, vflip=False)
        
        # addirional vars
        self.height = self.sprite.rect.height
        self.width =  self.sprite.rect.width
        self.bottom = self.ypos + self.height
        self.ground_position = self.bottom
        self.frame = 0
        self.number_of_frames = 4
        self.timeOfNextFrame = clock()
        self.lastBulletTime = clock()
        self.state = "neutral"
        self.previous_position = (self.xpos, self.ypos)
        
        # show sprite and add to spriterGroup
        showSprite(self.sprite)
        
class Basic_enemy(Enemy):
    def __init__(self):
        super().__init__()
        self.type = "basic_enemy"
        
    
def update_state(enemy, hero):
        # rotate frames in modulu of 'frame number var' every 80 milisec
    if clock() > enemy.timeOfNextFrame:  
        enemy.frame = (enemy.frame + 1) % enemy.number_of_frames_to_animate  
        enemy.timeOfNextFrame += 80
    
    # update bottom location coordinate for sprite drawing order
    enemy.bottom = enemy.ypos + enemy.height
    enemy.ground_position = enemy.bottom
    
    distance = math.sqrt((hero.xpos - enemy.xpos)**2 + (hero.ypos - enemy.ypos)**2)

    # Check if hero is moving towards enemy
    hero_towards_enemy = hero.previous_position[0] < hero.xpos and hero.xpos < enemy.xpos or hero.previous_position[0] > hero.xpos and hero.xpos > enemy.xpos

    # Check if enemy is moving towards hero
    enemy_towards_hero = enemy.previous_position[0] < enemy.xpos and enemy.xpos < hero.xpos or enemy.previous_position[0] > enemy.xpos and enemy.xpos > hero.xpos


    if distance > 250:
        enemy.state = "attack"
    else:
        # Update state based on movement
        if hero_towards_enemy:
            enemy.state = "neutral"
        elif enemy_towards_hero:
            enemy.state = "attack"
        else:
            enemy.state = "attack"
    
    if enemy.state == "attack":
        if hero.ground_position > enemy.ground_position:
            enemy.up = False
            enemy.down = True
        else:
            enemy.down = False
            enemy.up = True
        
        if hero.xpos + hero.width > enemy.xpos + enemy.width:
            enemy.gas = True
        else:
            enemy.gas = False
    
    elif enemy.state == "defense":
        if hero.ground_position > enemy.ground_position:
            enemy.up = True
            enemy.down = False
        else:
            enemy.down = True
            enemy.up = False
        
        if hero.xpos + hero.width > enemy.xpos + enemy.width:
            enemy.gas = False
        else:
            enemy.gas = True
    else:
        enemy.speed = hero.speed *  random.randint(8,15) * 0.1

        

            
            
        # when gas
    if enemy.gas == True:  
        changeSpriteImage(enemy.sprite,  0*enemy.number_of_frames+enemy.frame)    
        enemy.speed +=0.3    
        # when idle
    else:
        enemy.speed -=0.5
        changeSpriteImage(enemy.sprite,  0*enemy.number_of_frames+enemy.frame)
        transformSprite(enemy.sprite, 0, enemy.scale , hflip=True, vflip=False)
        
        
        # when up
    if enemy.up == True:
        enemy.ypos -= 1
        if enemy.ypos < 290 and enemy.ypos > 275:  # skip the pavement when moving up the screen
            enemy.ypos = 275                  



        # when down         
    if enemy.down == True:
        enemy.ypos += 1
        if enemy.ypos > 275 and enemy.ypos < 290:  # skip the pavement when moving down the screen
            enemy.ypos = 290                  


    # move
    enemy.xpos += enemy.speed * (random.randint(7,9)* 0.1)  # change  X position by speed meter
    enemy.xpos += int(hero.speed)*-1   # adapt to background scroll
    
    if enemy.sprite in allTouching(hero.sprite):
        if hero.ground_position > enemy.ground_position:
            enemy.ypos -= 25
        else:
            enemy.ypos += 25

            # keep Y position boundries
    if enemy.ypos + enemy.height > 560:
        enemy.ypos = 560 - enemy.height
    if enemy.ypos + enemy.height < 350:
        enemy.ypos = 350 - enemy.height
            
            # keep X position boundries
    if enemy.xpos > 1200:
        enemy.xpos = 1200


                
    # update actual postiion on screen
    moveSprite(enemy.sprite, enemy.xpos, enemy.ypos)
    
    # Store previous position of hero and enemy
    hero.previous_position = (hero.xpos, hero.ypos)
    enemy.previous_position = (enemy.xpos, enemy.ypos)





def update_enemy_movement(enemy, hero):
    
    # rotate frames in modulu of 'frame number var' every 80 milisec
    if clock() > enemy.timeOfNextFrame:  
        enemy.frame = (enemy.frame + 1) % enemy.number_of_frames_to_animate  
        enemy.timeOfNextFrame += 80
    
    # update bottom location coordinate for sprite drawing order
    enemy.bottom = enemy.ypos + enemy.height
    enemy.ground_position = enemy.bottom
    enemy.max_speed = 0.5 
 
 
    # Calculate distance between enemy and hero
    distance = math.sqrt((hero.xpos - enemy.xpos)**2 + (hero.ypos - enemy.ypos)**2)
    # Calculate angle between enemy and hero
    angle = math.atan2(hero.ypos - enemy.ypos, hero.xpos - enemy.xpos)
    # Calculate speed based on distance to hero
    enemy.speed = min(distance / 10, enemy.max_speed)
    # Update enemy's position based on speed and angle
    enemy.xpos += enemy.speed * math.cos(angle)
    enemy.ypos += enemy.speed * math.sin(angle)


    # update actual postiion on screen
    moveSprite(enemy.sprite, enemy.xpos, enemy.ypos)

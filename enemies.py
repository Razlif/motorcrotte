# enemy class

# import pygame functions acript
from Pygame_Functions.pygame_functions import *
from sound_elements import *
import math, random
import game_configuration as settings

setAutoUpdate(False)


# function to update display on main loop
def update_display(enemy_list, hero, bullets):
    spawn_enemies(enemy_list)
    for i, enemy in enumerate(enemy_list):
        if update_state(enemy, hero, bullets) == False:
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

        self.x_velocity = 0
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
        self.sprite = makeSprite("media/images/enemies/basicEnemy_1.png",1) 
        for i in range(2,5):
            addSpriteImage(self.sprite, "media/images/enemies/basicEnemy_"+str(i)+".png")
        
        addSpriteImage(self.sprite, "media/images/enemies/front_attack.png")
        addSpriteImage(self.sprite, "media/images/enemies/back_attack.png")
        
        # sclae to correct size
        self.scale = 1.85
        angle = 0
        transformSprite(self.sprite, angle, self.scale , hflip=False, vflip=False)
        self.sprite.rect.x = 1400
        self.sprite.rect.y = 400
        
        # addirional vars
        self.height = self.sprite.rect.height
        self.width =  self.sprite.rect.width
        self.ground_position = self.sprite.rect.bottom
        self.frame = 0
        self.number_of_frames = 4
        self.timeOfNextFrame = clock()
        self.lastBulletTime = clock()
        self.state = "neutral"
        self.previous_position = (self.sprite.rect.x, self.sprite.rect.y)
        self.ground = True
        self.hit = False
        
        # show sprite and add to spriterGroup
        showSprite(self.sprite)
        
class Basic_enemy(Enemy):
    def __init__(self):
        
        self.type = "basic_enemy"
        super().__init__()
        
    
def update_state(enemy, hero, bullets):
        # rotate frames in modulu of 'frame number var' every 80 milisec
    if clock() > enemy.timeOfNextFrame:  
        enemy.frame = (enemy.frame + 1) % enemy.number_of_frames 
        enemy.timeOfNextFrame += 80
    
    # update bottom location coordinate for sprite drawing order
    enemy.ground_position = enemy.sprite.rect.bottom
    
    distance = math.sqrt((hero.sprite.rect.x - enemy.sprite.rect.x)**2 + (hero.sprite.rect.y - enemy.sprite.rect.y)**2)

    # Check if hero is moving towards enemy
    hero_towards_enemy = hero.previous_position[0] < hero.sprite.rect.x and hero.sprite.rect.x < enemy.sprite.rect.x or hero.previous_position[0] > hero.sprite.rect.x and hero.sprite.rect.x > enemy.sprite.rect.x

    # Check if enemy is moving towards hero
    enemy_towards_hero = enemy.previous_position[0] < enemy.sprite.rect.x and enemy.sprite.rect.x < hero.sprite.rect.x or enemy.previous_position[0] > enemy.sprite.rect.x and enemy.sprite.rect.x > hero.sprite.rect.x


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
        
        if hero.sprite.rect.x + hero.width > enemy.sprite.rect.x + enemy.width:
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
        
        if hero.sprite.rect.x + hero.width > enemy.sprite.rect.x + enemy.width:
            enemy.gas = False
        else:
            enemy.gas = True
    else:
        enemy.x_velocity = hero.x_velocity

        

            
            
        # when gas
    if enemy.gas == True:  
        enemy.x_velocity +=0.3    
        # when idle
    else:
        enemy.x_velocity -=0.5
        
        
        # when up
    if enemy.up == True:
        enemy.sprite.rect.y -= 1
                  



        # when down         
    if enemy.down == True:
        enemy.sprite.rect.y += 1
                 

    if enemy.x_velocity > hero.x_velocity*2 and hero.x_velocity > 1:
        enemy.x_velocity = hero.x_velocity*2
        
    # move
    enemy.sprite.rect.x += enemy.x_velocity  # change  X position by speed meter
    enemy.sprite.rect.x += int(hero.x_velocity)*-1   # adapt to background scroll
    
    
    for bullet in bullets:
        if bullet.sprite in allTouching(enemy.sprite) and abs((bullet.ground_position)-(enemy.ground_position)) < (enemy.height*0.2):
            if bullet.impact == False:
                enemy.hit = True
                enemy.sprite.image.blit(settings.impact_picture, (0, 0))
                killSprite(bullet.sprite)
    
    if enemy.hit == True:
        enemy.x_velocity = 0
    else:
        changeSpriteImage(enemy.sprite,  enemy.frame)
        if enemy.x_velocity < 0 or enemy.gas == False:
            transformSprite(enemy.sprite, 0 , enemy.scale, hflip=True, vflip=False)
    
    if abs((hero.ground_position) - (enemy.ground_position)) < (hero.height * 0.25) and enemy.sprite in allTouching(hero.sprite):
        if hero.dash == True:
            transformSprite(enemy.sprite, 0 , enemy.scale, hflip=False, vflip=True)
            enemy.hit = True
        else:
            changeSpriteImage(enemy.sprite,-2)
        
            # keep Y position boundries
    if enemy.sprite.rect.bottom > settings.lane_3_bottom:
        enemy.sprite.rect.bottom = settings.lane_3_bottom
    if enemy.sprite.rect.bottom  < settings.side_walk_top:
        enemy.sprite.rect.bottom = settings.side_walk_top
                
    # when far enough in front or behind kill car sprite
    if enemy.sprite.rect.x - hero.sprite.rect.x> settings.out_of_bounds_x or enemy.sprite.rect.x - hero.sprite.rect.x < settings.out_of_bounds_x * -1:
        killSprite(enemy.sprite)
        return False
                
    # update actual postiion on screen
    moveSprite(enemy.sprite, enemy.sprite.rect.x, enemy.sprite.rect.y)
    
    # Store previous position of hero and enemy
    hero.previous_position = (hero.sprite.rect.x, hero.sprite.rect.y)
    enemy.previous_position = (enemy.sprite.rect.x, enemy.sprite.rect.y)





def update_enemy_movement(enemy, hero):
    
    # rotate frames in modulu of 'frame number var' every 80 milisec
    if clock() > enemy.timeOfNextFrame:  
        enemy.frame = (enemy.frame + 1) % enemy.number_of_frames_to_animate  
        enemy.timeOfNextFrame += 80
    
    # update bottom location coordinate for sprite drawing order
    enemy.bottom = enemy.sprite.rect.y + enemy.height
    enemy.ground_position = enemy.bottom
    enemy.max_speed = 0.5 
 
 
    # Calculate distance between enemy and hero
    distance = math.sqrt((hero.sprite.rect.x - enemy.sprite.rect.x)**2 + (hero.sprite.rect.y - enemy.sprite.rect.y)**2)
    # Calculate angle between enemy and hero
    angle = math.atan2(hero.sprite.rect.y - enemy.sprite.rect.y, hero.sprite.rect.x - enemy.sprite.rect.x)
    # Calculate speed based on distance to hero
    enemy.x_velocity = min(distance / 10, enemy.max_speed)
    # Update enemy's position based on speed and angle
    enemy.sprite.rect.x += enemy.x_velocity * math.cos(angle)
    enemy.sprite.rect.y += enemy.x_velocity * math.sin(angle)


    # update actual postiion on screen
    moveSprite(enemy.sprite, enemy.sprite.rect.x, enemy.sprite.rect.y)

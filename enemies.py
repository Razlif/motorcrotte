# enemy class

# import pygame functions acript
from Pygame_Functions.pygame_functions import *
from sound_elements import *
import math, random
import game_configuration as settings
import time

setAutoUpdate(False)


def update_display(enemy_list, hero, bullets):
    spawn_enemies(enemy_list)
    new_enemy_list = []
    for enemy in enemy_list:
        if update_state(enemy, hero, bullets) != False:
            new_enemy_list.append(enemy)
    enemy_list[:] = new_enemy_list


def update_display_2(enemy_list, hero, bullets):
    spawn_enemies(enemy_list)
    for i, enemy in enumerate(enemy_list):
        if update_state(enemy, hero, bullets) == False:
            enemy_list.pop(i)



def spawn_enemies(enemy_list):
    if len(enemy_list) < settings.max_enemy_number:  # if cars are under the max number, make new car and append to the list
        enemy_type = random.choice(["simple", "advanced", "advanced"])
        if enemy_type == "simple":
            enemy = BossEnemy()
        else:
            enemy = BossEnemy()
        enemy_list.append(enemy)

# enemy class
class Enemy():
    def __init__(self):
        # Reset intial Vars

        self.x_velocity = 0
        self.y_velocity = 0
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


class SimpleEnemy(Enemy):
    def __init__(self):
        super().__init__()
        self.type = 'simple'
        self.variation_number = 5
        # create sprite
        sprite_path = "media/images/cars/bikes/"+str(self.variation_number)
        self.sprite = makeSprite(sprite_path+"_1.png", 1)
        for i in range(2,5):
            addSpriteImage(self.sprite, sprite_path+"_"+str(i)+".png")
        
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
        self.state = "close_distance"
        self.previous_position = (self.sprite.rect.x, self.sprite.rect.y)
        self.ground = True
        self.hit = False
        
        # show sprite and add to spriterGroup
        showSprite(self.sprite)

    def update_behavior(self, hero, bullets):
        distance = math.sqrt((hero.sprite.rect.x - self.sprite.rect.x)**2 + (hero.sprite.rect.y - self.sprite.rect.y)**2)

        if distance > 250:
            self.state = "attack"
        else:
            self.state = "attack"
        
        if self.state == "attack":
            if hero.ground_position > self.ground_position:
                self.up = False
                self.down = True
            else:
                self.down = False
                self.up = True
            
            if hero.sprite.rect.x + hero.width > self.sprite.rect.x + self.width:
                self.gas = True
            else:
                self.gas = False

        # Update the SimpleEnemy position based on the state
        self.update_position(hero)

        return True

    def update_position(self, hero):
        if self.gas == True:  
            self.x_velocity += 0.3    
        else:
            self.x_velocity -= 0.5
        
        if self.up == True:
            self.sprite.rect.y -= 1
        
        if self.down == True:
            self.sprite.rect.y += 1
        
        if self.x_velocity > hero.x_velocity * 2 and hero.x_velocity > 1:
            self.x_velocity = hero.x_velocity * 2
        
        # Move
        self.sprite.rect.x += self.x_velocity
        self.sprite.rect.x += int(hero.x_velocity) * -1

        # Keep Y position boundaries
        if self.sprite.rect.bottom > settings.lane_3_bottom:
            self.sprite.rect.bottom = settings.lane_3_bottom
        if self.sprite.rect.bottom  < settings.side_walk_top:
            self.sprite.rect.bottom = settings.side_walk_top

class AdvancedEnemy(Enemy):
    def __init__(self):
        super().__init__()
        self.type = 'advanced'
        self.safe_distance = 150
        self.blitz_cooldown = 5  # seconds
        self.last_blitz_time = clock()
        self.blitz_duration = 1  # seconds
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
        self.state = "close_distance"
        self.previous_position = (self.sprite.rect.x, self.sprite.rect.y)
        self.ground = True
        self.hit = False
        
        # show sprite and add to spriterGroup
        showSprite(self.sprite)

    def update_behavior(self, hero, bullets):
        distance = ((hero.sprite.rect.x - self.sprite.rect.x)**2 + (hero.sprite.rect.y - self.sprite.rect.y)**2)**0.5
        current_time = clock()
        time_since_last_blitz = current_time - self.last_blitz_time

        if distance > self.safe_distance:
            self.state = "close_distance"
            self.gas = True
            if hero.ground_position > self.ground_position:
                self.up = False
                self.down = True
            else:
                self.down = False
                self.up = True
        else:
            self.state = "retreat"
            self.gas = False

        if time_since_last_blitz > self.blitz_cooldown:
            self.state = "blitz"
            self.last_blitz_time = current_time
        elif self.state == "blitz" and time_since_last_blitz > self.blitz_duration:
            self.state = "retreat"

        self.update_position(hero)

        return True

    def update_position(self, hero):
        if self.state == "blitz":
            if hero.sprite.rect.x > self.sprite.rect.x:
                self.x_velocity += 0.1
            else:
                self.x_velocity -= 0.1
        else: # for states "close_distance" and "retreat"
            if self.gas == True:
                self.x_velocity += 0.05
            else:
                self.x_velocity -= 0.05

        if self.up == True:
            self.sprite.rect.y -= 1
        if self.down == True:
            self.sprite.rect.y += 1

        if self.x_velocity > hero.x_velocity * 2 and hero.x_velocity > 1:
            self.x_velocity = hero.x_velocity * 2

        self.sprite.rect.x += self.x_velocity
        self.sprite.rect.x += int(hero.x_velocity) * -1 

        # Keep Y position boundaries
        if self.sprite.rect.bottom > settings.lane_3_bottom:
            self.sprite.rect.bottom = settings.lane_3_bottom
        if self.sprite.rect.bottom < settings.side_walk_top:
            self.sprite.rect.bottom = settings.side_walk_top


class BossEnemy(Enemy):
    def __init__(self):
        super().__init__()
        self.type = 'boss'
        self.shoot_cooldown = 10  # seconds
        self.last_shoot_time = clock()
        # create sprite
        sprite_path = "media/images/cars/special/Asset_Tank_Shot.png"
        self.sprite = makeSprite(sprite_path, 4)

        # sclae to correct size
        self.scale = 2.85
        angle = 0
        transformSprite(self.sprite, angle, self.scale , hflip=False, vflip=False)
        self.sprite.rect.x = 1000
        self.sprite.rect.y = 400
        
        # addirional vars
        self.height = self.sprite.rect.height
        self.width =  self.sprite.rect.width
        self.ground_position = self.sprite.rect.bottom
        self.frame = 0
        self.number_of_frames = 4
        self.timeOfNextFrame = clock()
        self.lastBulletTime = clock()
        self.state = "close_distance"
        self.previous_position = (self.sprite.rect.x, self.sprite.rect.y)
        self.ground = True
        self.hit = False
        self.bullet = None
        
        # show sprite and add to spriterGroup
        showSprite(self.sprite)
        


    def update_behavior(self, hero, bullets):
        
        self.hit = False
        transformSprite(self.sprite, 0 , self.scale, hflip=True, vflip=False)
        # The boss moves up or down depending on the hero's position
        if hero.sprite.rect.bottom >= self.sprite.rect.bottom:
            self.y_velocity += 0.02
        else:
            self.y_velocity -= 0.02
        
        # Update x position
        self.sprite.rect.y += self.y_velocity
        
        # Update x position
        # The boss will stick to the right edge of the screen
        self.sprite.rect.right = settings.screen_size_x + 200
        
        # Keep Y position boundaries
        if self.sprite.rect.bottom > settings.lane_3_bottom:
            self.sprite.rect.bottom = settings.lane_3_bottom
        if self.sprite.rect.bottom < settings.side_walk_top:
            self.sprite.rect.bottom = settings.side_walk_top

        # The boss shoots at the hero if the cooldown has passed
        current_time = clock()
        if self.bullet is None and current_time - self.last_shoot_time > self.shoot_cooldown:
            self.shoot_projectile()
            self.last_shoot_time = current_time

        # Update the bullet
        if self.bullet is not None:
            if not self.bullet.update(hero):
                killSprite(self.bullet.sprite)
                self.bullet = None  # Destroy the bullet if it went off screen

    def shoot_projectile(self):
        self.bullet = Bullet((self.sprite.rect.x+55), (self.sprite.rect.y+55), -5, 10)  # Create new bullet


class Bullet:
    def __init__(self, xpos, ypos, xspeed, damage):
        self.xpos = xpos
        self.ypos = ypos
        self.xspeed = xspeed
        self.damage = damage
        self.sprite = makeSprite("media/images/poopfly.png")
        showSprite(self.sprite)
        moveSprite(self.sprite, self.xpos, self.ypos)
        
    def update(self, hero):
        self.xpos += self.xspeed
        moveSprite(self.sprite, self.xpos, self.ypos)

        # Check if the bullet is off screen. If so, return False to indicate it should be destroyed.
        if self.xpos < 0 or self.xpos > settings.screen_size_x:
            return False
        
        # Check for bullet impact
        if self.sprite in allTouching(hero.sprite):
            return False
        
        return True


def update_state(enemy, hero, bullets):
    # Common updates for all enemy types
    
    # Rotate frames in modulu of 'frame number var' every 80 milliseconds
    if clock() > enemy.timeOfNextFrame:  
        enemy.frame = (enemy.frame + 1) % enemy.number_of_frames 
        enemy.timeOfNextFrame += 80
    
    # Update bottom location coordinate for sprite drawing order
    enemy.ground_position = enemy.sprite.rect.bottom
    
    # Check for bullet impact
    for bullet in bullets:
        if (bullet.sprite in allTouching(enemy.sprite) and abs((bullet.ground_position)-(enemy.ground_position)) < (enemy.height*0.2)) and hero.sprite.rect.right < enemy.sprite.rect.left:
            if bullet.impact == False:
                enemy.hit = True
                enemy.sprite.image.blit(settings.impact_picture, (0, 0))
                bullet.impact = True
                

            
    if enemy.hit == True:
        if enemy.type != "boss":
            #transformSprite(enemy.sprite, 0 , enemy.scale, hflip=False, vflip=True)
            enemy.x_velocity = 0
            enemy.gas = False
    else:
        changeSpriteImage(enemy.sprite,  enemy.frame)
        if (enemy.x_velocity < 0 or enemy.gas == False) and enemy.type == 'simple':
            transformSprite(enemy.sprite, 0 , enemy.scale, hflip=True, vflip=False)

    if abs((hero.ground_position) - (enemy.ground_position)) < (hero.height * 0.25) and enemy.sprite in allTouching(hero.sprite):
        changeSpriteImage(enemy.sprite,-2)

    # Check if the enemy is out of bounds
    if enemy.sprite.rect.x - hero.sprite.rect.x > settings.out_of_bounds_x or enemy.sprite.rect.x - hero.sprite.rect.x < settings.out_of_bounds_x * -1:
        killSprite(enemy.sprite)
        return False
    
    # Call the specific update_behavior method for each enemy type
    result = enemy.update_behavior(hero, bullets)
    
    return result
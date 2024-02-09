# enemy class

# import pygame functions acript
from Pygame_Functions.pygame_functions import *
from sound_elements import *
import math, random
import game_configuration as settings
import time
from stage_config import *
import collisions

setAutoUpdate(False)


def update_display(enemy_list, hero, bullets, stage, wave):
    enemy_manager(enemy_list, stage, wave)
    new_enemy_list = []
    for enemy in enemy_list:
        if update_state(enemy, hero, bullets) != False:
            new_enemy_list.append(enemy)
    enemy_list[:] = new_enemy_list
    
def enemy_manager(enemy_list, stage, wave):

    if len(enemy_list) == 0:  # Only spawn new enemies if all previous enemies have been defeated
        wave_info = stage_configuration["stage_" + str(stage)]["waves"][wave]
        enemy_number = wave_info['enemy_count']
        enemy_types = wave_info['enemy_types']

        for _ in range(enemy_number):
            enemy_type = random.choice(enemy_types)
            if enemy_type == "simple":
                enemy = SimpleEnemy()
            elif enemy_type == "advanced":
                enemy = AdvancedEnemy()
            elif enemy_type == "boss":
                enemy = BossEnemy()
            enemy_list.append(enemy)




# enemy class
class Enemy():
    def __init__(self):
        # Reset intial Vars
        self.type = "enemy"
        self.x_velocity = 0
        self.speed_meter = self.x_velocity
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
        self.type = "enemy"
        self.level = 'simple'
        self.health = 10
        self.damage = 20
        self.score_reward = 10
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
        self.sprite.rect.y = random.randint(200,500)
        
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
        self.dead = False
        self.transparency = 255
        
        # show sprite and add to spriterGroup
        showSprite(self.sprite)

    def update_behavior(self, hero, bullets):
        if clock() > self.timeOfNextFrame:
            self.frame = (self.frame + 1) % self.number_of_frames
            self.timeOfNextFrame += 80

        if self.dead == False:
            changeSpriteImage(self.sprite, self.frame)
            if (self.x_velocity < 0 or self.gas == False):
                transformSprite(self.sprite, 0, self.scale, hflip=True, vflip=False)

        if (abs((hero.ground_position) - (self.ground_position)) < (hero.height * 0.25) and self.sprite in allTouching(
                hero.sprite)) and self.dead == False:
            hero.health -= self.damage
            hero.hit = True
            self.state = "defend"

        distance = math.sqrt(
            (hero.sprite.rect.x - self.sprite.rect.x) ** 2 + (hero.sprite.rect.y - self.sprite.rect.y) ** 2)

        if distance > 400:
            self.state = "attack"
        else:
            self.state = "defend"

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
        elif self.x_velocity > 0:
            self.x_velocity -= 0.5

        
        if self.up == True:
            self.sprite.rect.y -= 1
        
        if self.down == True:
            self.sprite.rect.y += 1
        
        if self.x_velocity > hero.x_velocity * 1.5:
            self.x_velocity = hero.x_velocity * 1.5
        
        # Move
        self.sprite.rect.x += self.x_velocity

        # adapting to screen scroll
        self.sprite.rect.x += int(hero.x_velocity) * -1

        # Keep Y position boundaries
        if self.sprite.rect.bottom > settings.lane_3_bottom:
            self.sprite.rect.bottom = settings.lane_3_bottom
        if self.sprite.rect.bottom  < settings.side_walk_top:
            self.sprite.rect.bottom = settings.side_walk_top

class AdvancedEnemy(Enemy):
    def __init__(self):
        super().__init__()
        self.type = "enemy"
        self.level = 'advanced'
        self.health = 10
        self.damage = 20
        self.score_reward = 25
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
        self.sprite.rect.y = random.randint(200,500)
        
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
        self.dead = False
        self.transparency = 255
        
        # show sprite and add to spriterGroup
        showSprite(self.sprite)

    def update_behavior(self, hero, bullets):

        if clock() > self.timeOfNextFrame:
            self.frame = (self.frame + 1) % self.number_of_frames
            self.timeOfNextFrame += 80

        
        if self.dead == False:
            changeSpriteImage(self.sprite, self.frame)
            if (self.x_velocity < 0 or self.gas == False):
                transformSprite(self.sprite, 0, self.scale, hflip=True, vflip=False)

        if (abs((hero.ground_position) - (self.ground_position)) < (hero.height * 0.25) and self.sprite in allTouching(
                hero.sprite)) and self.dead == False:
            changeSpriteImage(self.sprite, -2)

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
        self.health = 400
        self.score_reward = 250
        self.shoot_cooldown = 10  # seconds
        self.last_shoot_time = clock()
        # create sprite
        sprite_path = "media/images/cars/special/Tank.png"
        self.sprite = makeSprite(sprite_path, 6)

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
        self.previous_position = (self.sprite.rect.x, self.sprite.rect.y)
        self.ground = True
        self.dead = False
        self.bullet = None
        # ...
        self.state = "driving"  # Add this attribute to keep track of the tank state
        self.number_of_frames = 6  # Total number of frames
        self.frame = 0
        self.timeOfNextFrame = clock()
        self.lastBulletTime = clock()
        self.last_state_change_time = clock()


        # show sprite and add to spriterGroup
        showSprite(self.sprite)
        


    def update_behavior(self, hero, bullets):

        #print(self.state)
        if clock() > self.timeOfNextFrame:
            if self.state == "driving":
                # The driving frames are 0 and 1 (indices start from 0, so use 0 and 1)
                self.frame = (self.frame + 1) % 2
            elif self.state == "shooting":
                # The shooting frames are 2 to 5 (indices start from 0)
                # Reset self.frame to 2 when switching to shooting state
                if self.frame < 2 or self.frame > 5:
                    self.frame = 2
                else:
                    self.frame = (self.frame + 1) % 4 + 2

            self.timeOfNextFrame += 80
            # Update sprite image to the new frame
            changeSpriteImage(self.sprite, self.frame)

        if self.dead == False:
            self.sprite.rect.right = settings.screen_size_x + 200
            changeSpriteImage(self.sprite, self.frame)

        # The boss moves up or down depending on the hero's position
        if hero.sprite.rect.bottom >= self.sprite.rect.bottom:
            self.y_velocity += 0.02
        else:
            self.y_velocity -= 0.02
        
        # Update x position
        self.sprite.rect.y += self.y_velocity


        # Keep y position boundaries
        if self.sprite.rect.bottom > settings.lane_3_bottom:
            self.sprite.rect.bottom = settings.lane_3_bottom
        if self.sprite.rect.bottom < settings.side_walk_top:
            self.sprite.rect.bottom = settings.side_walk_top

        # The boss shoots at the hero if the cooldown has passed
        if self.bullet is None and clock() - self.last_shoot_time > self.shoot_cooldown:
            self.shoot_projectile()
            self.last_shoot_time = clock()
            self.last_state_change_time = clock()
            self.state = "shooting"
        else:
            # Assume the shooting animation lasts for a certain amount of time (e.g., 320 milliseconds for 4 frames)
            # Only change state if enough time has passed since the last state change
            if self.state == "shooting" and clock() - self.last_state_change_time > 320:
                self.state = "driving"
                self.last_state_change_time = clock()

        # Update the bullet
        if self.bullet is not None:
            if not self.bullet.update(hero):
                killSprite(self.bullet.sprite)
                self.bullet = None  # Destroy the bullet if it went off screen

    def shoot_projectile(self):
        self.bullet = Bullet((self.sprite.rect.x+55), (self.sprite.rect.y+55), -8, 10)  # Create new bullet


class Bullet:
    def __init__(self, xpos, ypos, xspeed, damage):
        self.xpos = xpos
        self.ypos = ypos
        self.xspeed = xspeed
        self.damage = damage
        self.sprite = makeSprite("media/images/tank_rocket.png")
        # sclae to correct size
        self.scale = 0.25
        angle = 0
        transformSprite(self.sprite, angle, self.scale , hflip=False, vflip=False)
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
            hero.hit = True
            hero.health -= self.damage
            return False
        
        return True


def update_state(enemy, hero, bullets):
    # Common updates for all enemy types
    enemy.speed_meter = enemy.x_velocity
    # Update bottom location coordinate for sprite drawing order
    enemy.ground_position = enemy.sprite.rect.bottom
    
    # Check for bullet impact
    for bullet in bullets:
        if (bullet.sprite in allTouching(enemy.sprite) and abs((bullet.ground_position)-(enemy.ground_position)) < (enemy.height*0.5)) and hero.sprite.rect.right < enemy.sprite.rect.left:
            if bullet.impact == False:
                #enemy.hit = True
                enemy.health -= bullet.damage
                #print(enemy.health)
                enemy.sprite.image.blit(settings.impact_picture, (0, 0))
                bullet.impact = True
                if enemy.health <= 0:
                    enemy.x_velocity = 0
                    enemy.gas = False
                    if enemy.dead == False:
                        enemy.dead = True
                        hero.score += enemy.score_reward
                        selected_phrase = random.choice(settings.enemy_down_notifications)
                        hero.notifications.append(selected_phrase)                       
                        killSprite(enemy.sprite)
                        return False

                    


    # Check if the enemy is out of bounds
    if enemy.sprite.rect.x - hero.sprite.rect.x > settings.out_of_bounds_x or enemy.sprite.rect.x - hero.sprite.rect.x < settings.out_of_bounds_x * -1:
        killSprite(enemy.sprite)
        return False
    
    # Call the specific update_behavior method for each enemy type
    result = enemy.update_behavior(hero, bullets)

    return result
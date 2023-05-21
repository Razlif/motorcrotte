# enemy class

# import pygame functions acript
from Pygame_Functions.pygame_functions import *
from sound_elements import *
import math, random
import game_configuration as settings

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
        enemy_type = random.choice(["simple", "advanced"])
        if enemy_type == "simple":
            enemy = SimpleEnemy()
        else:
            enemy = SimpleEnemy()
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


class SimpleEnemy(Enemy):
    def __init__(self):
        super().__init__()
        self.type = 'simple'

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
        self.type = "advanced_enemy"
        self.attack_distance = 150
        self.safety_distance = 100
        self.attack_cooldown = 2000
        self.last_attack_time = 0
        self.angular_velocity = 1  # Controls the speed of circling
        super().__init__()

        # Increase max_speed for better pursuit
        self.max_speed = 20

    def update_behavior(self, hero, bullets):
        distance = math.sqrt((hero.sprite.rect.x - self.sprite.rect.x) ** 2 + (hero.sprite.rect.y - self.sprite.rect.y) ** 2)

        if distance > self.safety_distance:
            angle = math.atan2(hero.sprite.rect.y - self.sprite.rect.y, hero.sprite.rect.x - self.sprite.rect.x)
            self.x_velocity = min(distance / 5, self.max_speed)
            self.sprite.rect.x += self.x_velocity * math.cos(angle)
            self.sprite.rect.y += self.x_velocity * math.sin(angle)
        else:
            angle_to_hero = math.atan2(hero.sprite.rect.y - self.sprite.rect.y, hero.sprite.rect.x - self.sprite.rect.x)
            circle_angle = angle_to_hero + self.angular_velocity
            self.sprite.rect.x = hero.sprite.rect.x + self.safety_distance * math.cos(circle_angle) - self.sprite.rect.width // 2
            self.sprite.rect.y = hero.sprite.rect.y + self.safety_distance * math.sin(circle_angle) - self.sprite.rect.height // 2

        if distance < self.attack_distance and clock() - self.last_attack_time > self.attack_cooldown:
            self.attack(hero)
            self.last_attack_time = clock()


        def attack(self, hero):
            # Implement the attack logic here
            pass

        def update(self, hero, bullets):
            super().update(hero, bullets)
            self.update_behavior(hero, bullets)



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

    # Check if the enemy is out of bounds
    if enemy.sprite.rect.x - hero.sprite.rect.x > settings.out_of_bounds_x or enemy.sprite.rect.x - hero.sprite.rect.x < settings.out_of_bounds_x * -1:
        killSprite(enemy.sprite)
        return False
    
    # Call the specific update_behavior method for each enemy type
    result = enemy.update_behavior(hero, bullets)
    
    return result

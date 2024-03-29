## player controls

# import pygame functions acript
from Pygame_Functions.pygame_functions import *
from sound_elements import *
import math, random
import game_configuration as settings
import collisions

setAutoUpdate(False)

# empty list for bullets
bullets = []


# player class
class Player():
    def __init__(self):
        # Reset intial Vars
        self.type = "hero"
        self.score = 0
        self.x_direction = "static"
        self.y_direction = "static"
        self.y_velocity = 0
        self.x_velocity = 0
        self.speed_meter = self.x_velocity
        self.health = settings.hero_health
        self.xdir = 1  # shooting direction
        self.ydir = 0  # currently unused
        self.jump = False
        self.jump_size = 15  # the size of the jump in pixels
        self.jump_meter = self.jump_size  # reset jump meter to jump size var
        self.dash = False
        self.dash_origin = 13
        self.dash_meter = self.dash_origin
        self.gas = False
        self.breaking = False
        self.up = False
        self.down = False
        self.shoot = False
        self.ground = True
        self.poop = 0
        self.obstacle = False
        self.hit = False
        self.roof = False
        self.font = pygame.font.Font('media/Ghoust_Solid.otf', 45)
        self.notifications = []
        self.notification_visible = False
        self.notification_time = clock()
        self.stages = [False,False,False,False,False]
        self.angle = 0
        self.trick = False
        # create sprite
        self.sprite = makeSprite("media/images/hero/hero_1.png", 1)
        for i in range(2, 5):
            addSpriteImage(self.sprite, "media/images/hero/hero_" + str(i) + ".png")

        # sclae to correct size
        self.scale = 1.85
        angle = 0
        transformSprite(self.sprite, angle, self.scale, hflip=False, vflip=False)

        # create rect from mask
        self.sprite.rect = pygame.mask.Mask.get_rect(self.sprite.mask)

        # addirional vars

        self.height = self.sprite.rect.height
        self.width = self.sprite.rect.width
        self.sprite.rect.x = 200
        self.sprite.rect.y = settings.side_walk_top - self.sprite.rect.height
        self.ground_position = self.sprite.rect.bottom
        self.frame = 0
        self.number_of_frames = 2
        self.timeOfNextFrame = clock()
        self.lastBulletTime = clock()
        self.previous_position = self.sprite.rect.copy()

        # show sprite and add to spriterGroup
        showSprite(self.sprite)

    def move(self, enemy_list, vehicle_list):

        # update last position before new changes
        self.previous_position = self.sprite.rect.copy()
        self.speed_meter = self.x_velocity
        # update frame number
        if clock() > self.timeOfNextFrame:  # We only animate our character every 80ms.
            self.frame = (self.frame + 1) % self.number_of_frames
            self.timeOfNextFrame += 80

        # update the frame
        changeSpriteImage(self.sprite, self.frame)

        sprite_list = enemy_list + vehicle_list
        # update state based on other cars
        collision = collisions.collision_list_handler(self, sprite_list)

        # update bottom location coordinate for sprite drawing order but not when hero is jumping
        if self.ground == True or self.roof == True:
            transformSprite(self.sprite, 0, self.scale, hflip=False, vflip=False)
            self.y_velocity = 0
            if self.roof == False:
                self.ground_position = self.sprite.rect.bottom
        else:
            if self.sprite.rect.bottom <= self.ground_position:
                self.y_velocity += settings.gravity
            else:
                self.sprite.rect.bottom = self.ground_position
                self.y_velocity = 0
                self.ground = True

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
        if keyPressed("up") and self.x_velocity > 1:
            self.up = True
        else:
            self.up = False

        # DOWN
        if keyPressed("down") and self.x_velocity > 1:
            self.down = True
        else:
            self.down = False

        # JUMP
        if keyPressed("q"):
            if self.ground == True or self.roof == True:
                self.jump = True

        # DASH
        if keyPressed("e") and self.x_velocity > 1:
            self.dash = True

        # SHOOTING
        if keyPressed("w"):
            if self.poop > 0:
                self.shoot = True
        else:
            self.shoot = False

        # when gas
        if self.gas == True:
            changeSpriteImage(self.sprite, self.frame)
            idle_sound.stop()
            runing_sound.play()
            if self.x_velocity < settings.hero_top_speed:  # speed limit - but can be exceeded using the DASH move
                self.x_velocity += settings.hero_gas

        # when break
        elif self.breaking == True:
            runing_sound.stop()
            idle_sound.play()
            if self.x_velocity > 0:
                self.x_velocity -= settings.hero_break
                if self.sprite.rect.x > settings.hero_back_border:  # if breaking while player position hogher than 100 player's position will move back on the screen
                    self.sprite.rect.x -= settings.hero_move_back_on_break
                    changeSpriteImage(self.sprite, 0)
                    angle = settings.hero_breaking_angle
                    transformSprite(self.sprite, -45, self.scale, hflip=False, vflip=False)

        # when idle
        else:
            changeSpriteImage(self.sprite, self.frame)
            if self.x_velocity > 0:
                self.x_velocity -= settings.hero_natural_deceleration  # natural deceleration
                runing_sound.stop()
                idle_sound.play()

        # when up
        if self.up == True:
            self.sprite.rect.bottom -= 1.5
            if self.ground == False:
                self.ground_position -= 1.5

        # when down
        if self.down == True:
            self.sprite.rect.bottom += 1.5
            if self.ground == False:
                self.ground_position += 1.5

        # when jump
        if self.jump == True:
            self.ground = False
            #self.roof = False
            changeSpriteImage(self.sprite, self.frame)
            transformSprite(self.sprite, -45, self.scale, hflip=False, vflip=False)
            self.y_velocity -= self.jump_size
            self.jump = False

        # when trick
        if self.trick== True:
            self.ground = False 
            #self.roof = False
            #changeSpriteImage(self.sprite, self.frame)

            if self.angle <=360:
                self.angle +=20
                transformSprite(self.sprite, self.angle, self.scale, hflip=False, vflip=False)
            else:
                self.trick = False
                selected_phrase = "Flidipi flip!"
                self.notifications.append(selected_phrase)


        # when dash
        if self.dash == True:
            if self.dash_meter < 1:
                changeSpriteImage(self.sprite, 0)
                self.dash_meter -= 0.25
                angle = 25
                transformSprite(self.sprite, angle, self.scale, hflip=False, vflip=False)
            if self.dash_meter < (self.dash_origin * -0.25):
                self.dash = False
                self.dash_meter = self.dash_origin
            else:
                self.x_velocity += 0.03  # increase speed when dash
                self.sprite.rect.x += self.dash_meter
                self.dash_meter -= 0.25
                changeSpriteImage(self.sprite, 0)  # switch to dash frame animation
                angle = 45
                transformSprite(self.sprite, angle, self.scale, hflip=False, vflip=False)

        # when shoot
        if self.shoot == True:
            if clock() > self.lastBulletTime + 240:  # limit shots to every 240 milisec
                new_bullet = Bullet(self.sprite.rect.x + 20, self.sprite.rect.y + 20, self.xdir * 5, 0, self)
                bullets.append(new_bullet)  # create a new bullet and append it to bullet list
                self.lastBulletTime = clock()
                runing_sound.stop()
                idle_sound.stop()
                shoot_sound.play()
                self.poop -= 1

        # Make sure player position is inside play boundries
        if self.ground == True:
            # keep Y position boundries
            if self.sprite.rect.bottom > settings.lane_3_bottom:
                self.sprite.rect.bottom = settings.lane_3_bottom
            if self.sprite.rect.bottom < settings.side_walk_top:
                self.sprite.rect.bottom = settings.side_walk_top
                # keep X position boundries
            if self.sprite.rect.x > 1000:
                self.sprite.rect.x = 1000

        if self.hit == True:
            # make transparent or opaque randomly when hit
            self.sprite.image.set_alpha(random.choice([0, 255]))
            self.hit = False
        else:
            # clear transparency if any
            self.sprite.image.set_alpha(255)

        # update Y value up or down based on Y velocity
        self.sprite.rect.y += self.y_velocity

        # verify min speed
        if self.x_velocity < 1:
            self.x_velocity = 1

        # update player position to new location
        moveSprite(self.sprite, self.sprite.rect.x, self.sprite.rect.y)

        # check for hero driection based on rpevious position
        if self.previous_position[0] < self.sprite.rect.x:
            self.x_direction = "right"
        elif self.previous_position[0] > self.sprite.rect.x:
            self.x_direction = "left"
        else:
            self.x_direction = "static"

        if self.previous_position[1] < self.sprite.rect.y:
            self.y_direction = "down"
        elif self.previous_position[1] > self.sprite.rect.y:
            self.y_direction = "up"
        else:
            self.y_direction = "static"

        # Create new bullets list
        new_bullets = []

        # Update bullet list
        for bullet in bullets:
            # If bullet is still active, append it to the new list
            if bullet.move(self):
                new_bullets.append(bullet)
            # If bullet is not active, kill its sprite
            else:
                killSprite(bullet.sprite)

        # Replace old bullets list with new one
        bullets[:] = new_bullets

    def draw_labels(self, screen, x, y):
        score_label = self.font.render("Score: " + str(self.score), 1, (255, 0, 0))  # Red
        speed_label = self.font.render("Speed: " + str(int(self.x_velocity)), 1, (0, 255, 0))  # Green
        poop_label = self.font.render("Poop: " + str(self.poop), 1, (0, 0, 255))  # Blue
        health_label = self.font.render("Health: " + str(int(self.health)), 1, (255, 255, 0))  # Yellow

        screen.blit(score_label, (x, y))
        screen.blit(speed_label, (x, y + 40))  # Adjust y for each label to prevent overlap
        screen.blit(poop_label, (x, y + 80))
        screen.blit(health_label, (x, y + 120))




# bullet class
class Bullet():
    def __init__(self, xpos, ypos, xspeed, damage, hero):
        self.xpos = xpos
        self.ypos = ypos
        self.xspeed = xspeed
        self.damage = settings.bullet_damage
        self.impact = False
        self.sprite = makeSprite("media/images/poopfly.png")
        addSpriteImage(self.sprite, "media/images/poopimpact.png")
        self.height = self.sprite.rect.height
        self.width = self.sprite.rect.width
        self.bottom = self.ypos + self.height
        self.ground_position = hero.ground_position
        self.angle = 0
        self.scale = 0.5
        self.score = 0
        showSprite(self.sprite)

    def move(self, hero):
        if self.impact == False:  # if impact is false move the bullet along the X axis based on it's speed
            self.xpos += self.xspeed
            changeSpriteImage(self.sprite, 0)  # flying animation frame
            self.bottom = self.ypos + self.height
            self.angle += 15
            transformSprite(self.sprite, self.angle, self.scale, hflip=False, vflip=False)
        else:
            changeSpriteImage(self.sprite, 1)  # impact animation frame
            return False
        if self.xpos < -100 or self.xpos > 1300 or self.ypos < -100 or self.ypos > 800:  # false when out of boundries
            return False

        moveSprite(self.sprite, self.xpos, self.ypos)
        return True


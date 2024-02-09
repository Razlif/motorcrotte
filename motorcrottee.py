## main game script
import stage_handler
# import some packages
from Pygame_Functions.pygame_functions import *
import pygame
import os
import player as controls
import collectibles
import traffic as obstacles
import sidewalk
from sound_elements import *
import game_configuration as settings
import enemies




setAutoUpdate(False)

def sort_sprites_by_ground_position(spriteGroup, vehicle_list, sidewalk_element_list, poop_list, enemy_list, bullets, hero):
    # Sort the sprites based on their bottom Y position
    my_private_sprite_group = vehicle_list + sidewalk_element_list + poop_list + enemy_list + bullets
    my_private_sprite_group.append(hero)  
    layer_order = sorted(my_private_sprite_group, key=lambda sprite: sprite.ground_position)
    
    # Add the sprites back to the sprite group in the correct order
    for i, sprite in enumerate(layer_order):
        try:
            spriteGroup.change_layer(sprite.sprite, i)
        except:
            pass
        
def draw_text(surface, text, size, x, y):
    # choose a font (you can choose another if you like)
    #font_name = pygame.font.match_font('arial')
    font = pygame.font.Font('media/Ghoust_Solid.otf', size)
    text_surface = font.render(text, True, 'WHITE')  # True stands for anti-aliasing, WHITE is the color of the text which is usually defined as (255, 255, 255)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def process_notifications(hero, screen, x=500, y=25, size=100, duration=6000, interval=1000):

    if hero.notifications:  # While there are notifications left
        message = hero.notifications[0]  # Get the first notification

        elapsed_time = clock() - hero.notification_time
        if elapsed_time < duration:
            if elapsed_time % (2 * interval) < interval:  # This gives a simple flickering effect
                draw_text(screen, message, size, x, y)
        else:
            hero.notifications.pop(0)
            hero.notification_time = clock()  # Reset the timer for the next notification




def show_start_screen():
    # Load the image
    background = pygame.image.load("media/images/main1.png")  # Replace 'background_image_path.png' with the path to your image file
    background = pygame.transform.scale(background, (settings.screen_size_x, settings.screen_size_y))  # Scale the image to fit the screen

    # Draw the image
    screen.blit(background, (0, 0))

    # Draw the text
    draw_text(screen, "MOTOCROTTE", 64, settings.screen_size_x / 2, settings.screen_size_y / 4)
    draw_text(screen, "Press any key to start", 45, settings.screen_size_x / 2, settings.screen_size_y / 2)

    # Update the display
    pygame.display.flip()

    # Start screen Music Loop Begins:
    pygame.mixer.music.load('media/mainRiff.wav')
    pygame.mixer.music.set_volume(0.8)
    pygame.mixer.music.play(loops=-1)

    # Wait for the player to press a key
    wait_for_key()

def wait_for_key():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False



# Show the start screen
show_start_screen()

# set scrolling background
bg = setBackgroundImage( [  ["media/images/new_background5.png", "media/images/new_background5.png"]  ])

#  Game Music Loop Begins:
pygame.mixer.music.load('media/sounds/BGM16.mid')
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(loops=-1)


# init player
hero = controls.Player()
bullets = controls.bullets

# set up empty lists for game elements
vehicle_list = []
poop_list = []
sidewalk_element_list = []
enemy_list = []
stage = 1


#main game loop
while True:
    
    if stage == 1:
        current_wave = stage_handler.stage_1(vehicle_list, hero, bullets, enemy_list, sidewalk_element_list, poop_list)
        # sort the spriteGroup based on the y position of the bottom of each sprite
        sort_sprites_by_ground_position(spriteGroup, vehicle_list, sidewalk_element_list, poop_list, enemy_list, bullets, hero)
        
        process_notifications(hero, screen, 500, 25, 85, 3000, 500)

        # update score
        hero.draw_labels(screen, 10, 10)
        
        if current_wave == 'end_level':
            # Display end of level screen
            # Load the image
            background = pygame.image.load(
                "media/images/main1.png")  # Replace 'background_image_path.png' with the path to your image file
            background = pygame.transform.scale(background, (
                settings.screen_size_x, settings.screen_size_y))  # Scale the image to fit the screen

            # Draw the image
            screen.blit(background, (0, 0))

            # use the font render function to create the end level text surfaces
            end_text = hero.font.render('Level Completed', True, (255, 255, 255))
            score_text = hero.font.render('Score: ' + str(hero.score), True, (255, 255, 255))

            # Compute performance grade based on whatever metric you prefer
            performance_grade = "S Rank"  # replace this with your actual function
            performance_text = hero.font.render('Performance: ' + performance_grade, True, (255, 255, 255))

            # blit the text surfaces onto the screen at desired positions
            screen.blit(end_text, (screen.get_width() // 2 - end_text.get_width() // 2, screen.get_height() // 3))
            screen.blit(score_text, (screen.get_width() // 2 - score_text.get_width() // 2, screen.get_height() // 2))
            screen.blit(performance_text,
                        (screen.get_width() // 2 - performance_text.get_width() // 2, screen.get_height() // 2 + 60))

            
    updateDisplay()
    tick(90)

endWait()
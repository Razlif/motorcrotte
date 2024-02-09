#from Pygame_Functions.pygame_functions import *
import pygame

idle_sound = pygame.mixer.Sound("media/sounds/idle.mp3")
pygame.mixer.Sound.set_volume(idle_sound, 0.5)

runing_sound = pygame.mixer.Sound("media/sounds/running.mp3")
pygame.mixer.Sound.set_volume(runing_sound, 0.8)

breaking_sound = pygame.mixer.Sound("media/sounds/break.mp3")
pygame.mixer.Sound.set_volume(breaking_sound, 0.3)

horn_sound = pygame.mixer.Sound("media/sounds/horn_sound.mp3")
pygame.mixer.Sound.set_volume(horn_sound, 0.3)

shoot_sound = pygame.mixer.Sound("media/sounds/poop.mp3")
pygame.mixer.Sound.set_volume(shoot_sound, 0.5)

hit_sound = pygame.mixer.Sound("media/sounds/oh_no.mp3")
pygame.mixer.Sound.set_volume(hit_sound, 2)

collect_sound = pygame.mixer.Sound("media/sounds/collect.mp3")
pygame.mixer.Sound.set_volume(collect_sound, 0.4)

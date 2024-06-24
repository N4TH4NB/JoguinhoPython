import pygame
from sys import *
from pytmx.util_pygame import load_pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
tmx_maps = load_pygame("C:\\Users\\nathanbc\\PycharmProjects\\pythonProject1\\Sprite2\\sem_título.tmx")
print(dir(tmx_maps))
print(tmx_maps.layers)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.update()

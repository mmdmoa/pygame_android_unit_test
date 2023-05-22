import pygame
from pygame._sdl2 import Renderer, Texture, Window
import os
here = os.path.abspath(".")+"/"
pygame.init()

screen = pygame.display.set_mode((0,0), flags=pygame.FULLSCREEN)
window = Window.from_display_module()
renderer = Renderer(window)

texture = Texture.from_surface(renderer, pygame.image.load(here+"Capture.PNG"))

print(list(pygame._sdl2.get_drivers()))

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    renderer.draw_color = (255, 255, 255, 255)
    renderer.clear()

    texture.draw(None, None)

    renderer.present()

    clock.tick()
    print(clock.get_fps(), end="\r")

pygame.quit()
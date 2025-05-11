import pgzrun
import pygame
from events import scene1, scene2, scene3, scene4
from config import WIDTH, HEIGHT
import time

# NO sé como ponerlo en pantalla completa :'v perdón

WIDTH = WIDTH
HEIGHT = HEIGHT
TITLE = "Capítulo 15"
FPS = 30 

current_scene = scene1

def update(dt):
    global current_scene
    current_scene.update(dt, keyboard)
    if keyboard.r:
        current_scene = scene1

def draw():
    current_scene.draw(screen)

def on_key_down(key):
    if hasattr(current_scene, 'on_key_down'):
        current_scene.on_key_down(key)

def switch_scene(new_scene):
    global current_scene
    current_scene = new_scene

# Pass the switch function to scenes so they can change scene
scene1.init(switch_scene)
scene2.init(switch_scene)
scene3.init(switch_scene)
scene4.init(switch_scene)

pgzrun.go()
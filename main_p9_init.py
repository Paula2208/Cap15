import pgzrun
import pygame
from events import p9_scene1
from config import WIDTH, HEIGHT
import time

WIDTH = WIDTH
HEIGHT = HEIGHT
TITLE = "Capítulo 15"
FPS = 30 

# Estado global del juego
started = False
current_scene = None

def start_game():
    global current_scene, started
    p9_scene1.init(switch_scene)
    current_scene = p9_scene1
    started = True

def update(dt):
    global current_scene
    if started and current_scene:
        current_scene.update(dt, keyboard)

def draw():
    screen.clear()
    if not started:
        screen.draw.text("Presiona S para comenzar", center=(WIDTH // 2, HEIGHT // 2), fontsize=50, color="white")
        screen.draw.text("Presiona E para salir", center=(WIDTH // 2, HEIGHT // 2 + 60), fontsize=30, color="gray")
    elif current_scene:
        current_scene.draw(screen)

def on_key_down(key):
    from pgzero.keyboard import keys
    global current_scene
    if key == keys.S and not started:
        start_game()
    elif key == keys.E:
        exit()
    elif started and hasattr(current_scene, 'on_key_down'):
        current_scene.on_key_down(key)

def switch_scene(new_scene):
    global current_scene
    new_scene.init(switch_scene)
    current_scene = new_scene

p9_scene1.init(switch_scene)

pgzrun.go()
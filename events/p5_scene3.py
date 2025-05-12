from pgzero.actor import Actor
import pygame
import time
from config import WIDTH, HEIGHT

# Fondo
background = pygame.image.load("images/farm.png").convert()

# Gallinas estáticas
hens_static = [
    Actor("henjail", (WIDTH - 300, HEIGHT - 230)),
    Actor("henjail", (WIDTH - 150, HEIGHT - 150)),
    Actor("henjail", (WIDTH - 470, HEIGHT - 160))
]

# Gallina animada
hen_sprites = [f"hen{i}" for i in range(1, 6)]
hen = Actor(hen_sprites[0], (WIDTH + 150, HEIGHT - 100))
hen_frame = 0
hen_direction = 1
hen_last_update = 0

# Perro animado
dog_sprites = [f"dog{i}" for i in range(1, 7)]
dog = Actor(dog_sprites[0], (WIDTH + 350, HEIGHT - 120))
dog_frame = 0
dog_last_update = 0

# Velocidades ajustadas
hen_speed = 2.6
dog_speed = 2.4

start_time = None
switch_scene = None

def init(switch_fn):
    global switch_scene, start_time
    switch_scene = switch_fn
    start_time = time.time()

def update(dt, keyboard):
    global hen_frame, hen_direction, hen_last_update
    global dog_frame, dog_last_update

    now = pygame.time.get_ticks()

    # Animar gallina (adelante y atrás)
    if now - hen_last_update > 100:
        hen_frame += hen_direction
        if hen_frame == len(hen_sprites) - 1 or hen_frame == 0:
            hen_direction *= -1
        hen.image = hen_sprites[hen_frame]
        hen_last_update = now

    # Animar perro (cíclico solo hacia adelante)
    if now - dog_last_update > 180:
        dog_frame = (dog_frame + 1) % len(dog_sprites)
        dog.image = dog_sprites[dog_frame]
        dog_last_update = now

    # Movimiento
    if dog.x > -300:
        hen.x -= hen_speed
        dog.x -= dog_speed
    else:
        exit()

def draw(screen):
    screen.blit(background, (0, 0))
    for h in hens_static:
        h.draw()
    hen.draw()
    dog.draw()
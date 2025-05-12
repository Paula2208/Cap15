import pygame
from pgzero.actor import Actor
import time
from config import WIDTH, HEIGHT, CENTER_ROBOT

# Robot
robot = Actor("rsh1", (400, CENTER_ROBOT + 100))

robot_images = ["rsh1", "rsh2", "rsh3", "rsh4"]
current_image_index = 0
animation_counter = 0
animation_direction = 1  # 1 for forward, -1 for backward
switch_scene = None
start_time = None
mode = "walking"
speed = 2

# Fondo
raw_bg = pygame.image.load("images/school2.png").convert()
background = raw_bg.copy()

# Imágenes
school_images = [f"sh2_{i}" for i in range(1, 8)]
school_actors = []
shown_images = 0
image_times = []
image_scale = []

baseh = HEIGHT // 3 - 180
basew = WIDTH // 2 - 380

# Posiciones para las imágenes
image_positions = [
    (basew - 100, baseh),
    (basew + 200, baseh + 100),
    (basew + 200, baseh + 180),
    (basew + 400, baseh + 260),
    (basew + 400, baseh + 340),
    (basew + 400, baseh + 420),
    (basew + 200, baseh + 500),
]

# Temporizador
start_time = None
switch_scene = None

def init(switch_fn):
    global switch_scene, start_time
    switch_scene = switch_fn
    start_time = time.time()

def update(dt, keyboard):
    global shown_images, image_times, image_scale, mode, start_time
    global current_image_index, animation_counter, animation_direction

    elapsed = time.time() - start_time

    animation_counter += 1
    if animation_counter % 15 == 0:
        current_image_index += animation_direction

        # Reverse direction at ends
        if current_image_index == len(robot_images) - 1 or current_image_index == 0:
            animation_direction *= -1

        robot.image = robot_images[current_image_index]

    # Mostrar imágenes progresivamente
    if shown_images < 7 and elapsed >= (shown_images + 1) * 2:
        school_actors.append(Actor(school_images[shown_images], image_positions[shown_images]))
        image_times.append(pygame.time.get_ticks())
        image_scale.append(0.1)  # Escala inicial del zoom
        shown_images += 1

    # Animar zoom-in
    for i in range(len(school_actors)):
        if image_scale[i] < 1.0:
            image_scale[i] += 0.05
            if image_scale[i] > 1.0:
                image_scale[i] = 1.0

    # Salir después de 5 segundos tras la última imagen
    if shown_images == 7:
        last_image_time = start_time + 2 * 7
        if time.time() - last_image_time >= 5:
            exit()

def draw(screen):
    screen.blit(background, (0, 0))
    robot.draw()

    # Dibujar imágenes con zoom
    for i, actor in enumerate(school_actors):
        img = pygame.image.load(f"images/{actor.image}.png").convert_alpha()
        scale = image_scale[i]
        scaled_img = pygame.transform.rotozoom(img, 0, scale)
        rect = scaled_img.get_rect(topleft=actor.pos)
        screen.surface.blit(scaled_img, rect.topleft)
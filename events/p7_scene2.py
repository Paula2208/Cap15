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
school_images = [f"sim{i}" for i in range(1, 4)]
school_images.append("simvoid")
school_actors = []
shown_images = 0
image_times = []
image_scale = []

baseh = HEIGHT // 3 - 200
basew = WIDTH // 2

# Posiciones para las imágenes
image_positions = [
    (basew - 100, baseh),
    (basew - 450, baseh + 300),
    (basew + 200, baseh + 400),
    (basew + 450, baseh + 180)
]

# Temporizador
start_time = None
switch_scene = None
show_bubble = False
bubble_start_time = None

bubble_phase = 0  # 0: no mostrada, 1: primer texto, 2: oculta, 3: segundo texto
bubble_switch_time = None

def init(switch_fn):
    global switch_scene, start_time
    switch_scene = switch_fn
    start_time = time.time()

def update(dt, keyboard):
    global shown_images, image_times, image_scale, mode, start_time
    global current_image_index, animation_counter, animation_direction
    global show_bubble, bubble_start_time, bubble_phase, bubble_switch_time
    global robot

    elapsed = time.time() - start_time

    animation_counter += 1
    if animation_counter % 15 == 0 and bubble_phase == 0:  # Solo animar si aún no está sorprendido
        current_image_index += animation_direction

        if current_image_index == len(robot_images) - 1 or current_image_index == 0:
            animation_direction *= -1
        robot.image = robot_images[current_image_index]

    # Mostrar imágenes progresivamente
    if shown_images < 4 and elapsed >= (shown_images + 1) * 2:
        school_actors.append(Actor(school_images[shown_images], image_positions[shown_images]))
        image_times.append(pygame.time.get_ticks())
        image_scale.append(0.1)
        shown_images += 1

    for i in range(len(school_actors)):
        if image_scale[i] < 1.0:
            image_scale[i] += 0.05
            if image_scale[i] > 1.0:
                image_scale[i] = 1.0

    if shown_images == 4:
        if bubble_phase == 0:
            if bubble_start_time is None:
                bubble_start_time = time.time()
            elif time.time() - bubble_start_time >= 1:
                show_bubble = True
                bubble_phase = 1
                bubble_switch_time = time.time()
        elif bubble_phase == 1:
            if time.time() - bubble_switch_time >= 4:
                robot.image = "rsurprisedbig"
                show_bubble = False
                bubble_phase = 2
                bubble_switch_time = time.time()
        elif bubble_phase == 2:
            if time.time() - bubble_switch_time >= 1:
                show_bubble = True
                bubble_phase = 3
                bubble_switch_time = time.time()
        elif bubble_phase == 3:
            if time.time() - bubble_switch_time >= 7:
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
    
        # Mostrar burbuja de texto
        # Mostrar burbuja de texto con imagen 'globe.png'
    if show_bubble:
        globe_img = pygame.image.load("images/globe_f.png").convert_alpha()
        globe_scale = 0.8  # ajusta este valor si es muy grande o pequeño
        scaled_globe = pygame.transform.rotozoom(globe_img, 0, globe_scale)
        globe_rect = scaled_globe.get_rect(topleft=(robot.x + 60, robot.y - 700))

        # Dibuja la burbuja
        screen.surface.blit(scaled_globe, globe_rect.topleft)

        # Dibuja texto encima de la burbuja
        font = pygame.font.SysFont("arial", 50, bold=True)
        if bubble_phase in [1, 2]:
            robot_lines = ["Siento que me", "hace falta algo"]
        elif bubble_phase == 3:
            robot_lines = ["¡Oh! Debo"," replantear", "el modelo"]

        for i, line in enumerate(robot_lines):
            text_surface = font.render(line, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(globe_rect.centerx, globe_rect.top + 100 + i * 55))
            screen.surface.blit(text_surface, text_rect)
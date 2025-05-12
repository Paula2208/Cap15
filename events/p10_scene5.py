import pygame
from pgzero.actor import Actor
import time
from config import WIDTH, HEIGHT, CENTER_ROBOT

# Robot
robot = Actor("r1", (-200, CENTER_ROBOT + 20))
robot_images = ["r1", "r2", "r3", "r4"]
current_image_index = 0
animation_counter = 0
animation_direction = 1
switch_scene = None
start_time = None
mode = "walking"
speed = 2

# Fondo
raw_bg = pygame.image.load("images/l5.png").convert()
background = raw_bg.copy()

# Libro
book_image = "b1"
book_actor = Actor(book_image, center=(WIDTH // 2, HEIGHT // 2))
book_scale = 0.1
book_zooming_in = True
book_start_time = None
book_already_shown = False  # ✅ NUEVA bandera

book_images = ["b1", "b2", "b3", "b4", "b5", "b6"]
book_frame_index = 0
last_book_frame_time = None
book_sequence_complete = False

def init(switch_fn):
    global switch_scene, start_time
    switch_scene = switch_fn
    start_time = time.time()

def update(dt, keyboard):
    global current_image_index, animation_counter, animation_direction
    global mode, start_time, book_scale, book_zooming_in
    global book_start_time, book_already_shown
    global book_frame_index, last_book_frame_time, book_image, book_sequence_complete

    elapsed = time.time() - start_time

    if book_already_shown and mode == "surprised":
        book_scale = 0
        if robot.x < WIDTH + 200:
            robot.x += speed
            animation_counter += 1
            if animation_counter % 5 == 0:
                current_image_index += animation_direction
                if current_image_index == len(robot_images) - 1 or current_image_index == 0:
                    animation_direction *= -1
                robot.image = robot_images[current_image_index]
        else:
            switch_scene(__import__('events.p10_scene6', fromlist=['scene']))

    if mode == "walking":
        if robot.x < 500:
            robot.x += speed
            animation_counter += 1
            if animation_counter % 5 == 0:
                current_image_index += animation_direction
                if current_image_index == len(robot_images) - 1 or current_image_index == 0:
                    animation_direction *= -1
                robot.image = robot_images[current_image_index]
        elif not book_already_shown:
            robot.image = "rsurprised"
            mode = "surprised"
            book_start_time = time.time()
            book_scale = 0.1
            book_zooming_in = True
            book_frame_index = 0
            book_image = book_images[0]
            last_book_frame_time = time.time()
            book_sequence_complete = False

    elif mode == "surprised":
        # Zoom in
        if book_zooming_in and book_scale < 1.0:
            book_scale += 0.05
            if book_scale >= 1.0:
                book_scale = 1.0

        if book_zooming_in and time.time() - book_start_time >= 2:
            book_zooming_in = False
            last_book_frame_time = time.time()

        # Cambio de imagen cada 2 segundos cuando ya se hizo zoom-in
        elif not book_zooming_in and not book_sequence_complete:
            now = time.time()
            if now - last_book_frame_time >= 2:
                book_frame_index += 1
                last_book_frame_time = now
                if book_frame_index < len(book_images):
                    book_image = book_images[book_frame_index]
                else:
                    book_sequence_complete = True
                    book_zooming_in = False  # Empieza el zoom-out

        # Zoom-out si ya terminó la secuencia
        elif book_sequence_complete and book_scale > 0.1:
            book_scale -= 0.05
            if book_scale <= 0.1:
                book_scale = 0.1
                book_already_shown = True
                start_time = time.time()

def draw(screen):
    if mode == "surprised" and not book_already_shown:
        # Crear una copia del fondo con opacidad baja
        faded_bg = background.copy()
        faded_bg.set_alpha(65)
        screen.blit(faded_bg, (0, 0))
        
        # Dibujar libro
        img = pygame.image.load(f"images/{book_image}.png").convert_alpha()
        scaled_img = pygame.transform.rotozoom(img, 0, book_scale)
        rect = scaled_img.get_rect(center=book_actor.pos)
        screen.surface.blit(scaled_img, rect.topleft)
    else:
        # Fondo con opacidad normal
        screen.blit(background, (0, 0))

    robot.draw()
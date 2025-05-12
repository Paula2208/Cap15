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
raw_bg = pygame.image.load("images/l7.png").convert()
background = raw_bg.copy()

# Bubble
bubble_img = pygame.image.load("images/globe_l.png").convert_alpha()
bubble_img_robot = pygame.image.load("images/globe_lf.png").convert_alpha()
bubble_visible = False
bubble_timer_start = None  # Tiempo en el que se mostró el bubble

# Fuente para el texto
pygame.font.init()
font = pygame.font.SysFont("Arial", 26, bold=True)

def init(switch_fn):
    global switch_scene, start_time
    switch_scene = switch_fn
    start_time = time.time()

def update(dt, keyboard):
    global current_image_index, animation_counter, animation_direction
    global mode, start_time
    global bubble_visible, bubble_timer_start

    animation_counter += 1

    if mode == "surprised":
        if not bubble_visible:
            bubble_visible = True
            bubble_timer_start = time.time()

        elif time.time() - bubble_timer_start >= 2:
            mode = "leaving"
            robot.image = "r1"
            animation_counter = 0

    # Movimiento después del bubble
    if mode == "leaving":
        if robot.x < WIDTH + 200:
            robot.x += speed
            if animation_counter % 5 == 0:
                current_image_index += animation_direction
                if current_image_index == len(robot_images) - 1 or current_image_index == 0:
                    animation_direction *= -1
                robot.image = robot_images[current_image_index]
        else:
            switch_scene(__import__('events.p10_scene8', fromlist=['scene8']))

    # Movimiento inicial caminando
    if mode == "walking":
        if robot.x < 250:
            robot.x += speed
            if animation_counter % 5 == 0:
                current_image_index += animation_direction
                if current_image_index == len(robot_images) - 1 or current_image_index == 0:
                    animation_direction *= -1
                robot.image = robot_images[current_image_index]
        else:
            robot.image = "rsurprised"
            mode = "surprised"

def draw(screen):
    screen.blit(background, (0, 0))


    if bubble_visible:
        bubble_x = robot.x + 20
        bubble_y = robot.y - 500
        screen.surface.blit(bubble_img_robot, (bubble_x, bubble_y))
        robot_lines = ["Hoy he aprendido", "a reflexionar"]
        for i, line in enumerate(robot_lines):
            text_surface_robot = font.render(line, True, (0, 0, 0))
            screen.surface.blit(text_surface_robot, (bubble_x + 30, bubble_y + 50 + i * 30))

    robot.draw()
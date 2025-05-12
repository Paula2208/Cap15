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
raw_bg = pygame.image.load("images/l2.png").convert()
background = raw_bg.copy()

# Línea de tiempo
timeline_img = pygame.image.load("images/timeline.png").convert_alpha()
timeline_x = WIDTH  # comienza fuera del lado derecho
timeline_y = HEIGHT // 2 - timeline_img.get_height() // 2
timeline_speed = 2
complete_timelapse = False

def init(switch_fn):
    global switch_scene, start_time
    switch_scene = switch_fn
    start_time = time.time()

def update(dt, keyboard):
    global current_image_index, animation_counter, animation_direction
    global mode, start_time, timeline_x, complete_timelapse

    if mode == "surprised":
        if timeline_x + timeline_img.get_width() > 0:
            timeline_x -= timeline_speed
        else:
            complete_timelapse = True

    if complete_timelapse:
        if robot.x < WIDTH + 200:
            robot.x += speed
            animation_counter += 1
            if animation_counter % 5 == 0:
                current_image_index += animation_direction
                if current_image_index == len(robot_images) - 1 or current_image_index == 0:
                    animation_direction *= -1
                robot.image = robot_images[current_image_index]
        else:
            switch_scene(__import__('events.p10_scene3', fromlist=['scene3']))

    if mode == "walking":
        if robot.x < 250:
            robot.x += speed
            animation_counter += 1
            if animation_counter % 5 == 0:
                current_image_index += animation_direction
                if current_image_index == len(robot_images) - 1 or current_image_index == 0:
                    animation_direction *= -1
                robot.image = robot_images[current_image_index]
        else:
            robot.image = "rsurprised"
            mode = "surprised"

def draw(screen):
    if mode == "surprised" and not complete_timelapse:
        faded_bg = background.copy()
        faded_bg.set_alpha(65)
        screen.blit(faded_bg, (0, 0))

        screen.surface.blit(timeline_img, (timeline_x, timeline_y))
    else:
        screen.blit(background, (0, 0))

    robot.draw()
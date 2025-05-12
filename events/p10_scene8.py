import pygame
from pgzero.actor import Actor
import time
from config import WIDTH, HEIGHT, CENTER_ROBOT

# Robot
robot = Actor("r1big", (-300, CENTER_ROBOT + 20))
robot_images = ["r1big", "r2big", "r3big", "r4big"]
robot_bye_images = ["bye1", "bye2", "bye3", "bye4"]
current_image_index = 0
animation_counter = 0
animation_direction = 1
switch_scene = None
start_time = None
mode = "walking"
speed = 2
bubble_timer_start = 0

# Fondo
raw_bg = pygame.image.load("images/l8.png").convert()
background = raw_bg.copy()
background.set_alpha(78)

def init(switch_fn):
    global switch_scene, start_time
    switch_scene = switch_fn
    start_time = time.time()

def update(dt, keyboard):
    global current_image_index, animation_counter, animation_direction
    global mode, start_time
    global bubble_timer_start

    animation_counter += 1

    if mode == "surprised":
        if time.time() - bubble_timer_start >= 5:
            mode = "leaving"
            robot.image = "r1big"
            animation_counter = 0
        else:
            if animation_counter % 5 == 0:
                current_image_index += animation_direction
                if current_image_index == len(robot_bye_images) - 1 or current_image_index == 0:
                    animation_direction *= -1
                robot.image = robot_bye_images[current_image_index]

    # Movimiento después del bubble
    if mode == "leaving":
        if robot.x < WIDTH + 300:
            robot.x += speed
            if animation_counter % 5 == 0:
                current_image_index += animation_direction
                if current_image_index == len(robot_images) - 1 or current_image_index == 0:
                    animation_direction *= -1
                robot.image = robot_images[current_image_index]
        else:
            exit()

    # Movimiento inicial caminando
    if mode == "walking":
        if robot.x < WIDTH // 2 - 200:
            robot.x += speed
            if animation_counter % 5 == 0:
                current_image_index += animation_direction
                if current_image_index == len(robot_images) - 1 or current_image_index == 0:
                    animation_direction *= -1
                robot.image = robot_images[current_image_index]
        else:
            robot.image = "bye1"
            mode = "surprised"
            bubble_timer_start = time.time()
            animation_counter = 0

def draw(screen):
    screen.blit(background, (0, 0))
    robot.draw()
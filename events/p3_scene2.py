from pgzero.actor import Actor
import pygame
from config import WIDTH, CENTER_ROBOT
import time

robot = Actor("r1", (100, CENTER_ROBOT + 20))

robot_images = ["r1", "r2", "r3", "r4"]
current_image_index = 0
animation_counter = 0
animation_direction = 1  # 1 for forward, -1 for backward
switch_scene = None
start_time = None
mode = "walking"
speed = 2

def init(switch_fn):
    global start_time, switch_scene
    start_time = time.time()
    switch_scene = switch_fn

def update(dt, keyboard):
    global current_image_index, animation_counter, animation_direction
    global start_time, mode

    if robot.x < WIDTH - 300:
        robot.x += speed
        animation_counter += 1
        if animation_counter % 5 == 0:
            current_image_index += animation_direction

            # Reverse direction at ends
            if current_image_index == len(robot_images) - 1 or current_image_index == 0:
                animation_direction *= -1

            robot.image = robot_images[current_image_index]

    elif mode == "walking":
        robot.image = "rsurprised"
        mode = "surprised"
        start_time = time.time()

    elif mode == "surprised" and time.time() - start_time > 2:
        switch_scene(__import__('events.p1_scene2', fromlist=['scene2']))

def draw(screen):
    screen.blit("bg1", (0, 0))
    robot.draw()
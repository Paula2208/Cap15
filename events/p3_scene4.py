from pgzero.actor import Actor
import pygame
from config import WIDTH, CENTER_ROBOT
import time

robot = Actor("r1", (100, CENTER_ROBOT + 20))
robot2 = Actor("r1", (-70, CENTER_ROBOT + 60))

robot_images = ["r1", "r2", "r3", "r4"]
current_image_index = 0
animation_counter = 0
animation_direction = 1  # 1 for forward, -1 for backward
switch_scene = None
start_time = None
mode = "walking"
speed = 6

def init(switch_fn):
    global start_time, switch_scene
    start_time = time.time()
    switch_scene = switch_fn

def update(dt, keyboard):
    global current_image_index, animation_counter, animation_direction
    global start_time, mode

    if robot.x < WIDTH + 300:
        robot.x += speed
        animation_counter += 1
        if animation_counter % 5 == 0:
            current_image_index += animation_direction

            # Reverse direction at ends
            if current_image_index == len(robot_images) - 1 or current_image_index == 0:
                animation_direction *= -1

            robot.image = robot_images[current_image_index]
    
    if robot2.x < WIDTH + 300:
        robot2.x += speed
        animation_counter += 1
        if animation_counter % 5 == 0:
            current_image_index += animation_direction

            # Reverse direction at ends
            if current_image_index == len(robot_images) - 1 or current_image_index == 0:
                animation_direction *= -1

            robot2.image = robot_images[current_image_index]

    if robot2.x >= WIDTH + 300 and robot.x >= WIDTH + 300:
        exit()

def draw(screen):
    screen.blit("bg2", (0, 0))
    robot.draw()
    robot2.draw()

    screen.draw.text("Agente 1", center=(robot.x, robot.y - 280), fontsize=50, color="white", ocolor="black", owidth=1.5)
    screen.draw.text("Agente 2", center=(robot2.x, robot2.y - 280), fontsize=50, color="white", ocolor="black", owidth=1.5)
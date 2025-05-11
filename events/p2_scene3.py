from pgzero.actor import Actor
from config import WIDTH, HEIGHT, CENTER_ROBOT
import pygame
import time
import math

max_value = [0.5, 0.2, 0.3]
prob = ["a", "b", "c"]
actual = 0
elapsed = 0.0
start_time = 0.0

bg1 = pygame.image.load("images/bg1.png").convert()
bg1.set_alpha(128)

robot_images = ["rtdone", "rtdonel", "rtdone", "rtdonel"]

robot_ok = ["rok1", "rok2", "rok3", "rok4"]

robot = Actor(robot_images[actual], (WIDTH // 2, CENTER_ROBOT + 130))
mode = "thinking"
switch_scene = None

animation_counter = 0
current_image_index = 0
animation_direction = 1

def init(switch_fn):
    global switch_scene, start_time, mode
    switch_scene = switch_fn
    start_time = time.time()
    mode = "thinking"

def update(dt, keyboard):
    global mode, elapsed, actual, start_time
    global animation_counter, current_image_index, animation_direction

    elapsed = time.time() - start_time

    if mode == "thinking" and elapsed > 3:
        if actual < 2:
            actual += 1
            robot.image = robot_images[actual]
            start_time = time.time()
        else:
            mode = "complete"
            actual = 0
            robot.image = robot_ok[0]
            start_time = time.time()

    if mode == "complete":
        animation_counter += 1
        if animation_counter % 15 == 0:
            current_image_index += animation_direction
            if current_image_index == len(robot_ok) - 1 or current_image_index == 0:
                animation_direction *= -1
            robot.image = robot_ok[current_image_index]
    
    if elapsed > 8 and mode == "complete":
        switch_scene(__import__('events.p2_scene4', fromlist=['scene4']))

def draw(screen):
    screen.surface.blit(bg1, (0, 0))
    robot.draw()

    if mode == "thinking":
        screen.draw.text("EU(a) = ∑ P(Result(a) = s')U(s')", center=(WIDTH//3 + 270, 200), fontsize=150, color="white")
        if actual % 2 == 0:
            text_x = robot.x + 300
        else:
            text_x = robot.x - 300

        font_size = 200
    elif mode == "complete":
        screen.draw.text("MEU: action = argmaxEU(a)", center=(WIDTH//3 + 270, 200), fontsize=150, color="white")

        text_x = robot.x - 300

        font_size = 210 + 30 * math.sin(time.time() * 4)
    else:
        return 

    screen.draw.text("P[" + prob[actual] + "] = " + f"{max_value[actual]:.1f}",
                     center=(text_x, robot.y - 500),
                     fontsize=int(font_size),
                     color="white")

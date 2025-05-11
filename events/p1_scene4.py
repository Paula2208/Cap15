from pgzero.actor import Actor
from config import WIDTH, HEIGHT, CENTER_ROBOT
import time
import pygame

# Globales
mode = "thinking"
actual = 0

switch_scene = None
start_time = None
vibration_offset = 0
vibration_dir = 1
number_value = 0.0
animation_counter = 0
current_image_index = 0
animation_direction = 1
speed = 5
max_value = [0.5, 0.2, 0.3]
bgs = ["images/bg2.png", "images/bg3.png", "images/bg4.png"]
bgs_e1 = ["bg2_e1", "bg3_e1", "bg4_e1"]
bgs_e2 = ["bg2_e2", "bg3_e2", "bg4_e2"]
prob = ["a", "b", "c"]

bg2 = pygame.image.load(bgs[actual]).convert()
bg2.set_alpha(180)

robot = Actor("rt1", (450, CENTER_ROBOT + 20))
robot_images = ["rt1", "rt2", "rt3", "rt4"]
robot_walking= ["r1big", "r2big", "r3big", "r4big"]

e1 = Actor(bgs_e1[actual], (1150, HEIGHT // 2))
e2 = Actor(bgs_e2[actual], (1600, HEIGHT // 2 + 150))

def init(switch_fn):
    global switch_scene, start_time, number_value
    switch_scene = switch_fn
    start_time = time.time()
    number_value = 0.0

def update(dt, keyboard):
    global vibration_offset, vibration_dir, number_value, bg2, actual, mode
    global start_time, animation_counter, current_image_index, animation_direction
    
    animation_counter += 1

    if actual == 2 and robot.x >= WIDTH - 300:
        switch_scene(__import__('events.p1_scene5', fromlist=['scene5']))
    else:
        vibration_offset += vibration_dir
        if abs(vibration_offset) > 5:
            vibration_dir *= -1

        e1.x += vibration_dir * 1
        e2.x -= vibration_dir * 1

        if mode == "thinking":
            if number_value <= max_value[actual]:
                number_value += 0.005

            if animation_counter % 15 == 0:
                current_image_index += animation_direction

                # Reverse direction at ends
                if current_image_index == len(robot_images) - 1 or current_image_index == 0:
                    animation_direction *= -1

                robot.image = robot_images[current_image_index]

            if number_value > max_value[actual]:
                mode = "walking"
        else:
            if robot.x < WIDTH - 300:
                robot.x += speed
                animation_counter += 1
                if animation_counter % 5 == 0:
                    current_image_index += animation_direction

                    # Reverse direction at ends
                    if current_image_index == len(robot_walking) - 1 or current_image_index == 0:
                        animation_direction *= -1

                    robot.image = robot_walking[current_image_index]
            else:
                mode = "thinking"
                robot.image = "rt1"
                robot.x = 450
                start_time = time.time()
                number_value = 0.0
                actual += 1
                bg2 = pygame.image.load(bgs[actual]).convert()
                bg2.set_alpha(180)
                e1.image = bgs_e1[actual]
                e2.image = bgs_e2[actual]

def draw(screen):
    screen.surface.blit(bg2, (0, 0))
    e1.draw()
    e2.draw()
    robot.draw()
    screen.draw.text("P[" + prob[actual]+ "] = "+ f"{number_value:.1f}", center=((WIDTH//3 )* 2 + 150, 300), fontsize=200, color="white")
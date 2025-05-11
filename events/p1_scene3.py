from pgzero.actor import Actor
from config import WIDTH, CENTER_ROBOT_BIG
import time

robot = Actor("rcrisis1", (WIDTH/2 + 80, CENTER_ROBOT_BIG))
robot_images = ["rcrisis1", "rcrisis2", "rcrisis3", "rcrisis4"]
background = "bg1"
switch_scene = None
start_time = None
animation_counter = 0
current_image_index = 0
animation_direction = 1
mode = "1"
blink_counter = 0
show_error = True  # Alterna visibilidad

def init(switch_fn):
    global switch_scene
    switch_scene = switch_fn

def update(dt, keyboard):
    global start_time, background, robot, mode, animation_counter
    global current_image_index, animation_direction, blink_counter, show_error

    if mode == "1":
        mode = "2"
        start_time = time.time()

    animation_counter += 1
    blink_counter += 1

    if blink_counter % 30 == 0:
        show_error = not show_error

    if animation_counter % 5 == 0:
        current_image_index += animation_direction

        # Reverse direction at ends
        if current_image_index == len(robot_images) - 1 or current_image_index == 0:
            animation_direction *= -1

        robot.image = robot_images[current_image_index]

    if mode == "2" and time.time() - start_time > 7:
        switch_scene(__import__('events.p1_scene4', fromlist=['scene4']))

def draw(screen):
    screen.blit(background, (0, 0))
    robot.draw()
    if show_error:
        screen.draw.text("¡ERROR EN SISTEMA!", center=(WIDTH / 2, 100), fontsize=70, color="red", owidth=1.0, ocolor="black")
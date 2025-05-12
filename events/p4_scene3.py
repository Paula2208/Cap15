from pgzero.actor import Actor
from config import CENTER_ROBOT_BIG, WIDTH, HEIGHT, CENTER_ROBOT
import pygame
import time
import math

max_value = [0.4, 0.3, 0.3]
prob = ["a", "b", "c"]
prob_exp = ["Está muy soleado", "Está muy frío", "Tiene rocas pronunciadas"]
actual = 0
elapsed = 0.0
start_time = 0.0

robot_images = ["rtdone", "rtdonel", "rtdone", "rtdonel"]
bgs = ["images/bg2.png", "images/bg3.png", "images/bg4.png"]
r_obs_images = ["robs1_big", "robs2_big", "robs3_big", "robs4_big"]

robot_ok = ["rok1", "rok2", "rok3", "rok4"]

robot = Actor(robot_images[actual], (WIDTH // 2, CENTER_ROBOT))
robotWait = Actor("robs1_big", (WIDTH - 600, HEIGHT - CENTER_ROBOT_BIG + 200))
mode = "waiting"
switch_scene = None

bg1 = pygame.image.load(bgs[actual]).convert()
bg1.set_alpha(128)

animation_counter = 0
current_image_index = 0
animation_direction = 1

def init(switch_fn):
    global switch_scene, start_time, mode
    switch_scene = switch_fn
    start_time = time.time()
    mode = "waiting"

def update(dt, keyboard):
    global mode, elapsed, actual, start_time, bg1
    global animation_counter, current_image_index, animation_direction

    elapsed = time.time() - start_time

    if mode == "waiting":
        bg1 = pygame.image.load("images/bg1.png").convert()
        bg1.set_alpha(128)
        animation_counter += 1
        if animation_counter % 15 == 0:
            current_image_index += animation_direction
            if current_image_index == len(r_obs_images) - 1 or current_image_index == 0:
                animation_direction *= -1
            robot.image = r_obs_images[current_image_index]
        if elapsed > 3:
            mode = "thinking"
            start_time = time.time()
            robot.image = robot_images[actual]
            bg1 = pygame.image.load(bgs[actual]).convert()
            bg1.set_alpha(128)
            actual = 0
            return

    if mode == "thinking" and elapsed > 3:
        if actual < 2:
            actual += 1
            robot.image = robot_images[actual]
            start_time = time.time()
            bg1 = pygame.image.load(bgs[actual]).convert()
            bg1.set_alpha(128)
        else:
            mode = "complete"
            actual = 0
            robot.image = robot_ok[0]
            start_time = time.time()
            elapsed = 0
            bg1 = pygame.image.load(bgs[actual]).convert()
            bg1.set_alpha(128)

    if mode == "complete":
        robot.x = WIDTH // 2 + 250
        animation_counter += 1
        if animation_counter % 15 == 0:
            current_image_index += animation_direction
            if current_image_index == len(robot_ok) - 1 or current_image_index == 0:
                animation_direction *= -1
            robot.image = robot_ok[current_image_index]
    
    if elapsed > 8 and mode == "complete":
        exit()

def draw(screen):
    screen.surface.blit(bg1, (0, 0))

    if mode == "waiting":
        robotWait.draw()
        screen.blit("globe", (robotWait.x - 750, robotWait.y - 700))
        screen.draw.text("¿Qué pasa si\ncambio los valores?",
                         topleft=(robotWait.x - 650, robotWait.y - 600),
                         fontsize=60,
                         color="black")

    if mode == "thinking":
        robot.draw()
        if actual % 2 == 0:
            text_x = robot.x + 300
        else:
            text_x = robot.x - 300

        font_size = 140  
    elif mode == "complete":
        robot.draw()
        text_x = robot.x - 500

        font_size = 160 + 30 * math.sin(time.time() * 4)
        screen.draw.text("U'(S) = aU(S) + b",
                     center=(text_x, robot.y - 200),
                     fontsize=int(font_size),
                     color="yellow", owidth=1.0, ocolor="black")
    else:
        return  # no dibujar nada si otro modo

    screen.draw.text(prob_exp[actual],
                     center=(text_x, robot.y - 600),
                     fontsize=int(font_size),
                     color="white")
    
    screen.draw.text("U(" + prob[actual]+ ") = " + str(max_value[actual]),
                     center=(text_x, robot.y - 400),
                     fontsize=int(font_size),
                     color="red", owidth=1.0, ocolor="black")

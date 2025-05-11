from pgzero.actor import Actor
import pygame
from config import WIDTH, CENTER_ROBOT, HEIGHT
import time

robot = Actor("r1", (100, CENTER_ROBOT + 20))
overlay = pygame.Surface((WIDTH, HEIGHT))
overlay.set_alpha(128)
overlay.fill((0, 0, 0)) 

robot_images = ["r1", "r2", "r3", "r4"]
current_image_index = 0
animation_counter = 0
animation_direction = 1  # 1 for forward, -1 for backward
switch_scene = None
start_time = None
speed = 2
elapse = 0

r_obs = Actor("robs1", (WIDTH // 4 - 200, HEIGHT // 2))
r_apr = Actor("rapr1", ((WIDTH // 4) * 2 + 30, HEIGHT // 2))
r_inf = Actor("rinf1", ((WIDTH // 4) * 3 + 200, HEIGHT // 2))

r_obs_images = ["robs1", "robs2", "robs3", "robs4"]
r_apr_images = ["rapr1", "rapr2", "rapr3", "rapr4"]
r_inf_images = ["rinf1", "rinf2", "rinf3", "rinf4"]
len_images = 4

def init(switch_fn):
    global start_time, switch_scene
    start_time = time.time()
    switch_scene = switch_fn

def update(dt, keyboard):
    global current_image_index, animation_counter, animation_direction
    global start_time, elapse

    elapse = time.time() - start_time
    animation_counter += 1

    if robot.x < WIDTH + 300:
        robot.x += speed
    else:
        exit()

    if animation_counter % 15 == 0:
        current_image_index += animation_direction

        # Reverse direction at ends
        if current_image_index == len_images - 1 or current_image_index == 0:
            animation_direction *= -1

        robot.image = robot_images[current_image_index]

        if elapse > 3:
            r_obs.image = r_obs_images[current_image_index]
            r_apr.image = r_apr_images[current_image_index]
            r_inf.image = r_inf_images[current_image_index]


def draw(screen):
    screen.blit("bg2", (0, 0))
    robot.draw()

    if elapse > 3:
        screen.surface.blit(overlay, (0, 0))
        
        r_obs.draw()
        screen.blit("table", (r_obs.x - 200, r_obs.y + 110))
        screen.draw.text("Observar", center=(r_obs.x, r_obs.y + 170), fontsize=70, color="black")

        if elapse > 4:
            r_apr.draw()
            screen.blit("table", (r_apr.x - 200, r_apr.y + 110))
            screen.draw.text("Aprender", center=(r_apr.x , r_apr.y + 170), fontsize=70, color="black")
        
        if elapse > 5:
            r_inf.draw()
            screen.blit("table", (r_inf.x - 200, r_inf.y + 110))
            screen.draw.text("Inferir", center=(r_inf.x , r_inf.y + 170), fontsize=70, color="black")
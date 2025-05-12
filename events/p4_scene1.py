from pgzero.actor import Actor
import pygame
import time
from config import WIDTH, HEIGHT, CENTER_ROBOT_BIG

robot = Actor("robs1_big", (WIDTH - 600, HEIGHT - CENTER_ROBOT_BIG + 200))
robot_start_y = robot.y
robot_target_y = HEIGHT - 100  # Posición final del robot

r_obs_images = ["robs1_big", "robs2_big", "robs3_big", "robs4_big"]
current_image_index = 0
animation_counter = 0
animation_direction = 1

# Cajas y sus posiciones
box1 = Actor("box", (WIDTH // 3 + 170, HEIGHT // 4))
box2 = Actor("box", (WIDTH // 3 - 340, (HEIGHT // 4) * 2 + 40))
box3 = Actor("box", (WIDTH // 3 - 80, (HEIGHT // 4) * 3 + 100))
boxes = [box1, box2, box3]
values = [0.4, 0.5, 0.1]

# Animación de cajas
shake_index = 0
shake_start_time = None
show_final = False
final_start = None
final_flash = False
robot_descending = False
robot_descend_start = None

# Control de texto que ya ha salido
revealed = [False, False, False]

switch_scene = None
elapsed = 0
bg1 = pygame.image.load("images/bg1.png").convert()
bg1.set_alpha(128)
mode = "play"
final = 0

def init(switch_fn):
    global switch_scene, start_time, shake_start_time
    switch_scene = switch_fn
    start_time = time.time()
    shake_start_time = time.time()

def update(dt, keyboard):
    global animation_counter, current_image_index, animation_direction, mode, final
    global elapsed, shake_index, shake_start_time, show_final, final_start, final_flash
    global robot_descending, robot_descend_start

    animation_counter += 1
    if animation_counter % 15 == 0:
        current_image_index += animation_direction
        if current_image_index == len(r_obs_images) - 1 or current_image_index == 0:
            animation_direction *= -1
        robot.image = r_obs_images[current_image_index]

    elapsed = time.time() - start_time

    # Secuencia de temblores
    if shake_index < len(boxes) and time.time() - shake_start_time > 3:
        revealed[shake_index] = True
        shake_index += 1
        shake_start_time = time.time()
        if shake_index == len(boxes):
            final_start = time.time()
            robot_descending = True
            mode = "ok"
            robot_descend_start = time.time()

    if robot_descending:
        duration = 2.0
        t = (time.time() - robot_descend_start) / duration
        if t >= 1.0:
            t = 1.0
            robot_descending = False
            show_final = True
            final_flash = True
            final_start = time.time()
            final = time.time()
        robot.y = robot_start_y + (robot_target_y - robot_start_y) * t

    if show_final and not robot_descending and time.time() - final_start > 0.3:
        final_flash = not final_flash
        final_start = time.time()

    if show_final and not robot_descending and (time.time() - final > 5):
        switch_scene(__import__('events.p4_scene2', fromlist=['scene2']))

def draw(screen):
    screen.surface.blit(bg1, (0, 0))
    robot.draw()

    if mode == "ok":
        screen.draw.text("∑ pi × U(Si)", center=(robot.x + 200, 300), fontsize=150, color="white")

    for i, box in enumerate(boxes):
        box_pos = (box.x - box.width // 2, box.y - box.height // 2)

        if i == shake_index - 1 and not show_final:
            offset = 5 if int(time.time() * 20) % 2 == 0 else -5
            screen.blit("box", (box_pos[0] + offset, box_pos[1]))
            text_y = box.y - (elapsed - 2 * i) * 20
            screen.draw.text(str(values[i]), center=(box.x, text_y), fontsize=100, color="white")

        elif show_final and i == values.index(max(values)):
            if final_flash:
                screen.blit("box", box_pos)
            screen.draw.text(str(values[i]), center=(box.x, box.y - box.height // 2 - 20), fontsize=100, color="white")

        else:
            screen.blit("box", box_pos)
            if revealed[i]:
                screen.draw.text(str(values[i]), center=(box.x, box.y - box.height // 2 - 20), fontsize=100, color="white")
from pgzero.actor import Actor
from config import WIDTH, CENTER_ROBOT
import time
import pygame

robot = Actor("rbackl", (WIDTH / 2, CENTER_ROBOT + 100))
background = pygame.image.load("images/bg5.png").convert()

# Posiciones objetivo
target_left_x = 310
target_right_x = 1580

# Elementos laterales iniciando fuera de pantalla
elem_left = Actor("bg3_e1", (-200, CENTER_ROBOT - 400))   # entra desde la izquierda
elem_right = Actor("bg4_e1", (WIDTH + 200, CENTER_ROBOT - 400))  # entra desde la derecha

# Control de animaciones y tiempos
switch_scene = None
start_time = None
shake_start_time = None
bubble1_shown = False
bubble2_shown = False
mode = "1"
elements_arrived = False

def init(switch_fn):
    global switch_scene
    switch_scene = switch_fn

def update(dt, keyboard):
    global start_time, shake_start_time, mode
    global bubble1_shown, bubble2_shown, elements_arrived

    if mode == "1":
        mode = "2"
        start_time = time.time()

    elif mode == "2" and time.time() - start_time >= 2:
        mode = "3"
        shake_start_time = time.time()
        background.set_alpha(178)

    elif mode == "3" and not elements_arrived:
        # Animación de entrada
        speed = 12
        if elem_left.x < target_left_x:
            elem_left.x += speed
        if elem_right.x > target_right_x:
            elem_right.x -= speed

        # Verificar si ambos han llegado
        if elem_left.x >= target_left_x and elem_right.x <= target_right_x:
            elements_arrived = True
            shake_start_time = time.time()  # reiniciamos tiempo de temblor

    elif mode == "3" and elements_arrived:
        if time.time() - shake_start_time >= 3 and not bubble1_shown:
            bubble1_shown = True
            start_time = time.time()

        elif bubble1_shown and not bubble2_shown and time.time() - start_time >= 2:
            bubble2_shown = True
            start_time = time.time()

        elif bubble1_shown and bubble2_shown and time.time() - start_time >= 5:
            exit()

def draw(screen):
    screen.blit(background, (0, 0))
    robot.draw()

    if mode in ["3", "4"]:
        # Si ya llegaron, tiemblan
        if elements_arrived:
            offset = 4 if int(time.time() * 10) % 2 == 0 else -4
        else:
            offset = 0

        screen.blit("bg3_e1", (elem_left.x + offset - elem_left.width // 2, elem_left.y - elem_left.height // 2))
        screen.blit("bg4_e1", (elem_right.x + offset - elem_right.width // 2, elem_right.y - elem_right.height // 2))

        # Burbujas de pensamiento
        if bubble1_shown:
            screen.blit("globe_f", (robot.x + 150, robot.y - 650))
            screen.draw.text("¿Qué es esto?",
                             center=(robot.x + 430, robot.y - 480),
                             fontsize=80, color="black")

        if bubble2_shown:
            screen.blit("globe", (robot.x - 700, robot.y - 650))
            screen.draw.text("¡Son muchas\nvariables!",
                             center=(robot.x - 440, robot.y - 480),
                             fontsize=80, color="black")
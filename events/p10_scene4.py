import pygame
from pgzero.actor import Actor
import time
from config import WIDTH, HEIGHT, CENTER_ROBOT

# Robot
robot = Actor("r1", (-200, CENTER_ROBOT + 20))
robot_images = ["r1", "r2", "r3", "r4"]
current_image_index = 0
animation_counter = 0
animation_direction = 1
switch_scene = None
start_time = None
mode = "walking"
speed = 2

# Persona (centro)
person = Actor("t1", (WIDTH // 2, CENTER_ROBOT + 20))
p_images = ["t1", "t2", "t3", "t4"]
current_image_index_p = 0
animation_counter_p = 0
animation_direction_p = 1

# Ruleta (base, rueda, resultado)
lottery_base = Actor("base", (1500, CENTER_ROBOT + 50))
lottery_wheel = Actor("lotery", (1500, CENTER_ROBOT - 250))
lottery_pic = Actor("pic", (1500, CENTER_ROBOT - 600))
rotation_speed = 0.1
angle = 0

complete_timelapse = False

# Fondo
raw_bg = pygame.image.load("images/l4.png").convert()
background = raw_bg.copy()

# Bubble
bubble_img = pygame.image.load("images/globe_l.png").convert_alpha()
bubble_img_robot = pygame.image.load("images/globe_lf.png").convert_alpha()
bubble_visible = False
bubble_timer_start = None  # Tiempo en el que se mostró el bubble

# Fuente para el texto
pygame.font.init()
font = pygame.font.SysFont("Arial", 26, bold=True)

def init(switch_fn):
    global switch_scene, start_time
    switch_scene = switch_fn
    start_time = time.time()

def update(dt, keyboard):
    global current_image_index, animation_counter, animation_direction
    global current_image_index_p, animation_counter_p, animation_direction_p
    global mode, start_time, complete_timelapse, angle
    global bubble_visible, bubble_timer_start

    animation_counter += 1
    animation_counter_p += 1

    # Rueda girando constantemente
    angle = (angle + rotation_speed) % 360
    lottery_wheel.angle = angle

    # Animación de la persona que espera
    if animation_counter_p % 10 == 0:
        current_image_index_p += animation_direction_p
        if current_image_index_p == len(p_images) - 1 or current_image_index_p == 0:
            animation_direction_p *= -1
        person.image = p_images[current_image_index_p]

    if mode == "surprised":
        # Mostrar globo de diálogo por 2 segundos
        if not bubble_visible:
            bubble_visible = True
            bubble_timer_start = time.time()

        elif time.time() - bubble_timer_start >= 3:
            mode = "leaving"
            robot.image = "r1"
            animation_counter = 0  # Reiniciar animación
            bubble_visible = False

    # Movimiento después del bubble
    if mode == "leaving" or complete_timelapse:
        if robot.x < WIDTH + 200:
            robot.x += speed
            if animation_counter % 5 == 0:
                current_image_index += animation_direction
                if current_image_index == len(robot_images) - 1 or current_image_index == 0:
                    animation_direction *= -1
                robot.image = robot_images[current_image_index]
        else:
            switch_scene(__import__('events.p10_scene5', fromlist=['scene5']))

    # Movimiento inicial caminando
    if mode == "walking":
        if robot.x < 250:
            robot.x += speed
            if animation_counter % 5 == 0:
                current_image_index += animation_direction
                if current_image_index == len(robot_images) - 1 or current_image_index == 0:
                    animation_direction *= -1
                robot.image = robot_images[current_image_index]
        else:
            robot.image = "rsurprised"
            mode = "surprised"

def draw(screen):
    screen.blit(background, (0, 0))

    # Dibujar actores
    person.draw()
    lottery_base.draw()
    lottery_wheel.draw()
    lottery_pic.draw()

    #Dibujar el bubble de la persona "Creo que jugaré  otra vez"
    bubble_x = person.x - 300
    bubble_y = person.y - 600
    screen.surface.blit(bubble_img, (bubble_x, bubble_y))
    person_lines = ["Creo que jugaré", "de nuevo"]
    for i, line in enumerate(person_lines):
        text_surface = font.render(line, True, (0, 0, 0))
        screen.surface.blit(text_surface, (bubble_x + 40, bubble_y + 60 + i * 30))

    # Dibujar el bubble con "globe.png" sobre el robot (no la persona)
    if bubble_visible:
        bubble_x = robot.x + 20
        bubble_y = robot.y - 500
        screen.surface.blit(bubble_img_robot, (bubble_x, bubble_y))
        robot_lines = ["¡No! Solo toma", "lo que ganaste"]
        for i, line in enumerate(robot_lines):
            text_surface_robot = font.render(line, True, (0, 0, 0))
            screen.surface.blit(text_surface_robot, (bubble_x + 30, bubble_y + 50 + i * 30))

    robot.draw()
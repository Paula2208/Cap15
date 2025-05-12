import pygame
from pgzero.actor import Actor
import time
from config import WIDTH, HEIGHT, CENTER_ROBOT

# Fondo con opacidad
raw_bg = pygame.image.load("images/bg5.png").convert()
background = raw_bg.copy()
background.set_alpha(65)

# Robot en el centro inferior con animación
robot_sprites = [f"rinf{i}" for i in range(1, 5)]
robot = Actor(robot_sprites[0], (WIDTH // 2, HEIGHT - 65))
robot_frame = 0
robot_direction = 1
robot_last_update = 0

# Fórmulas
formula_images = [f"h{i}" for i in range(1, 5)]
formulas = []
formulas_shown = 0
formula_times = []
formula_scale = []

baseh = HEIGHT // 3 - 100

# Posiciones para las fórmulas
formula_positions = [
    (WIDTH // 2, baseh),
    (WIDTH // 2, baseh + 150),
    (WIDTH // 2, baseh + (150 * 2)),
    (WIDTH // 2, baseh + (150 * 3)),
]

# Temporizador
start_time = None
switch_scene = None

def init(switch_fn):
    global switch_scene, start_time
    switch_scene = switch_fn
    start_time = time.time()

def update(dt, keyboard):
    global robot_frame, robot_direction, robot_last_update
    global formulas_shown, formula_times, formula_scale

    now = pygame.time.get_ticks()

    # Robot animación (adelante y atrás)
    if now - robot_last_update > 150:
        robot_frame += robot_direction
        if robot_frame == len(robot_sprites) - 1 or robot_frame == 0:
            robot_direction *= -1
        robot.image = robot_sprites[robot_frame]
        robot_last_update = now

    # Mostrar fórmulas progresivamente
    elapsed = time.time() - start_time
    if formulas_shown < 4 and elapsed >= (formulas_shown + 1) * 2:
        formulas.append(Actor(formula_images[formulas_shown], formula_positions[formulas_shown]))
        formula_times.append(pygame.time.get_ticks())
        formula_scale.append(0.1)  # Escala inicial del zoom
        formulas_shown += 1

    # Animar zoom-in
    for i in range(len(formulas)):
        if formula_scale[i] < 1.0:
            formula_scale[i] += 0.05  # Velocidad de zoom
            if formula_scale[i] > 1.0:
                formula_scale[i] = 1.0

    if formulas_shown == 4:
        last_formula_time = start_time + 2 * 4
        if time.time() - last_formula_time >= 5:
            exit()

def draw(screen):
    screen.blit(background, (0, 0))

    # Título
    screen.draw.text("Herramientas para Multiatributo",
                     center=(WIDTH // 2, 100),
                     fontsize=70, color="white", owidth=2.5, ocolor="black")

    # Dibujar fórmulas con zoom
    for i, formula in enumerate(formulas):
        img = pygame.image.load(f"images/{formula.image}.png").convert_alpha()
        scale = formula_scale[i]
        scaled_img = pygame.transform.rotozoom(img, 0, scale)
        rect = scaled_img.get_rect(center=formula.pos)
        screen.surface.blit(scaled_img, rect.topleft)

    # Dibujar robot
    robot.draw()
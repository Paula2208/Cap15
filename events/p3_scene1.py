from pgzero.actor import Actor
import pygame
import time
from config import WIDTH, HEIGHT, CENTER_ROBOT

# Elementos visuales
robot = Actor("rtdone", (400, CENTER_ROBOT - 100))
globe = Actor("globe_f", (robot.x + 250, robot.y - 500))

lottery_base = Actor("base", (1200, CENTER_ROBOT + 50))
lottery_wheel = Actor("lotery", (1200, CENTER_ROBOT - 250))
lottery_pic = Actor("pic", (1200, CENTER_ROBOT - 600))

# Lógica de animación
rotation_speed = 5  # grados por frame
start_time = None
switch_scene = None
angle = 0

def init(switch_fn):
    global start_time, switch_scene
    start_time = time.time()
    switch_scene = switch_fn

def update(dt, keyboard):
    global angle
    angle = (angle + rotation_speed) % 360
    lottery_wheel.angle = angle

    if time.time() - start_time >= 10:
        exit()

def draw(screen):
    screen.blit("bg2", (0, 0))

    lottery_base.draw()
    lottery_wheel.draw()
    lottery_pic.draw()

    robot.draw()
    globe.draw()
    screen.draw.text("¿Qué es peor,\nganar un poco o\n perder mucho?",
                     (globe.x - 240, globe.y - 140),
                     fontsize=80,
                     color="black")
from pgzero.actor import Actor
from config import WIDTH, CENTER_ROBOT
import time

robot = Actor("rbackl", (WIDTH/3, CENTER_ROBOT + 100))
robot2 = Actor("rbackl", ((WIDTH/3) * 2, CENTER_ROBOT + 100))
bubble1 = Actor("globe", (robot.x - 300, robot.y - 500))
bubble2 = Actor("globe_f", (robot2.x + 300, robot2.y - 500))

background = "bg2"
switch_scene = None
start_time = None
mode = "1"

def init(switch_fn):
    global switch_scene
    switch_scene = switch_fn

def update(dt, keyboard):
    global start_time, background, robot, mode

    if mode == "1":
        mode = "2"
        start_time = time.time()

    if time.time() - start_time >= 2 and mode == "2":
        if background == "bg2":
            background = "bg3"
            robot.image = "rbackr"
            robot2.image = "rbackr"
            start_time = time.time()
        elif background == "bg3":
            background = "bg4"
            robot.image = "rbackl"
            robot2.image = "rbackl"
            start_time = time.time()
        elif background == "bg4":
            switch_scene(__import__('events.p3_scene4', fromlist=['scene4']))

def draw(screen):
    screen.blit(background, (0, 0))
    robot.draw()
    robot2.draw()
    
    # Dibujar burbujas
    bubble1.draw()
    bubble2.draw()

    # Dibujar texto dentro de las burbujas
    screen.draw.text("A < B < C", (robot.x - 520, robot.y - 600), fontsize=140, color="black")
    screen.draw.text("A < C < B", (robot2.x + 90, robot2.y - 600), fontsize=140, color="black")
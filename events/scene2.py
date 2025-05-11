from pgzero.actor import Actor
from config import WIDTH, CENTER_ROBOT
import time

robot = Actor("rbackl", (WIDTH/2, CENTER_ROBOT + 100))
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
            start_time = time.time()
        elif background == "bg3":
            background = "bg4"
            robot.image = "rbackl"
            start_time = time.time()
        elif background == "bg4":
            switch_scene(__import__('events.scene3', fromlist=['scene3']))

def draw(screen):
    screen.blit(background, (0, 0))
    robot.draw()
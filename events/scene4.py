from pgzero.actor import Actor
from config import WIDTH, CENTER_ROBOT_BIG
import time


def init(switch_fn):
    global switch_scene
    switch_scene = switch_fn

def update(dt, keyboard):
    pass

def draw(screen):
    screen.blit("bg1", (0, 0))
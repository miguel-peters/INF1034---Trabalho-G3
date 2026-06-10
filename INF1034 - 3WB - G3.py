from pygame import *
import sys

clock = time.Clock()
init()
screen = display.set_mode((1200,800))
running = True


while running:
    for ev in event.get():
        if ev.type == QUIT:
            quit()
            sys.exit()
    
    display.update()

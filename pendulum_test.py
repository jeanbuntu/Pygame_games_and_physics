import pygame as pg
import numpy as np

sc_width, sc_height = 900, 500
win = pg.display.set_mode((sc_width, sc_height))
pg.display.set_caption('pendulum test1')

clock = pg.time.Clock()
FPS = 60

white = (255, 255, 255)
black = (0, 0, 0)

pendulum_length = 250
pendulum_base = (sc_width/2, 0)

gravity = 1


def rope_tip(angle):
    x = pendulum_length * np.sin(angle) + pendulum_base[0]
    y = pendulum_length * np.cos(angle) + pendulum_base[1]
    return x, y

def draw(angle):
    win.fill(white)
    pg.draw.line(win, black, pendulum_base, rope_tip(angle), 5) #rope
    pg.draw.circle(win, black, rope_tip(angle), 20)
    pg.display.update()

def main():
    run = True
    angle = np.pi/2
    angleV = 0
    angleA = 0
    while run:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        draw(angle)
        force = -1 * gravity * np.sin(angle)/pendulum_length
        angleA = force
        angleV += angleA
        angle += angleV
        angleV *= 0.99
        print(angle)


if __name__ == '__main__':
    main()
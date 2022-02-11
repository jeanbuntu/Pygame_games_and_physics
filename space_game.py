import pygame as p
import os
WIDTH, HEIGHT = 900, 500
WIN = p.display.set_mode((WIDTH, HEIGHT))
p.display.set_caption('First Game!')

white = (255, 255, 255)
black = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

border = p.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
FPS = 60
sp_width, sp_height = 55, 40

yellow_hit = p.USEREVENT + 1
red_hit = p.USEREVENT + 2
yspci = p.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
yspt = p.transform.rotate(p.transform.scale(yspci, (sp_width, sp_height)), 90)
rspci = p.image.load(os.path.join('Assets', 'spaceship_red.png'))
space = p.transform.scale(p.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))
rspt = p.transform.rotate(p.transform.scale(rspci, (sp_width, sp_height)), -90)


def draw_window(red, yellow, red_bullets, yellow_bullets):
    WIN.blit(space, (0, 0))
    p.draw.rect(WIN, black, border)
    WIN.blit(yspt, (yellow.x, yellow.y))
    WIN.blit(rspt, (red.x, red.y))

    for bullet in red_bullets:
        p.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        p.draw.rect(WIN, YELLOW, bullet)

    p.display.update()


def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[p.K_a] and yellow.x - VEL > 0:  # left
        yellow.x -= VEL
    if keys_pressed[p.K_d] and yellow.x + VEL + yellow.width < border.x:  # right
        yellow.x += VEL
    if keys_pressed[p.K_w] and yellow.y - VEL > 0:  # up
        yellow.y -= VEL
    if keys_pressed[p.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 20:  # down
        yellow.y += VEL


def red_handle_movement(keys_pressed, red):
    if keys_pressed[p.K_LEFT] and red.x - VEL > border.x + 10:  # left
        red.x -= VEL
    if keys_pressed[p.K_RIGHT] and red.x + VEL < WIDTH - red.width:  # right
        red.x += VEL
    if keys_pressed[p.K_UP] and red.y - VEL > 0:  # up
        red.y -= VEL
    if keys_pressed[p.K_DOWN] and red.y + VEL < HEIGHT - red.height - 15:  # down
        red.y += VEL


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            p.event.post(p.event.Event(red_hit))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            p.event.post(p.event.Event(yellow_hit))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def main():
    red = p.Rect(700, 300, sp_width, sp_height)
    yellow = p.Rect(100, 300, sp_width, sp_height)

    red_bullets = []
    yellow_bullets = []

    clock = p.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in p.event.get():
            if event.type == p.QUIT:
                run = False

            if event.type == p.KEYDOWN:
                if event.key == p.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = p.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                if event.key == p.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = p.Rect(red.x, red.y + yellow.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)

        keys_pressed = p.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        draw_window(red, yellow, red_bullets, yellow_bullets)
    p.quit()


if __name__ == '__main__':
    main()
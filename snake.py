import numpy as np
import pygame as pg
import random
import sys
import time
pg.init()
pg.font.init()

block_dim = 20 # body parts are squares with width of 20
screenscale = 20 # some multiple of 20 ?
size = width, height = screenscale*block_dim, screenscale*block_dim
speed = block_dim
saved_velocity = (0, 0) # velcoity as given by the keys pressed by the player
grey,red, col_head = (47, 79, 79), (255, 90, 0),(200, 255, 0)
start = [0]*2
xlines = width/block_dim
SURFACE = pg.display.set_mode(size)
pg.display.set_caption("Snake")
gameover = False


def newgame():
    global gameover, score,blocks, apple_y, apple_x, start,saved_velocity
    gameover = False
    score = 0
    start[0] = screenscale * random.randint((2 * block_dim) / 10, xlines) - 2 * block_dim  # x start
    start[1] = screenscale * random.randint((2 * block_dim) / 10, xlines) - 2 * block_dim  # y start

    pg.display.set_caption("Snake")
    blocks = np.array([[start[0], start[1]]])

    apple_x, apple_y = 0, 0
    saved_velocity = (0, 0)
    play()


def play():
    global blocks, saved_velocity
    new_spawn = True
    t= int(round(time.time() * 10))
    t_prev = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            getKeys(event)

        if t != t_prev:
            if not gameover:
                movesnake()
                checkcollisions()
                if new_spawn:
                    assignAppleCoords()
                    new_spawn = False

            SURFACE.fill(grey)
            for coord in blocks:
                pg.draw.rect(SURFACE, col_head, (coord[0] + 2, coord[1] + 2, block_dim - 2, block_dim - 2))
            pg.draw.circle(SURFACE, red, (apple_x, apple_y), int(block_dim/2), 0)

            if gameover:
                font = pg.font.SysFont('Calibri', 20)
                text = font.render("GAME OVER : score = %s" % score, True, (80, 10, 10))
                print("GAME OVER : score = %s" % score)
                SURFACE.blit(text, (width/2 - 100, height/2))
                pg.display.flip()
                secsStart = time.time()
                while time.time() - secsStart <= 2:
                    pass
                newgame()
            else:
                SURFACE.blit(SURFACE, (0, 0))
                pg.display.flip()
            t_prev = t
        t = int(round(time.time() * 10))


def getKeys(event):
    # gets the keys from the keyboard
    global saved_velocity,speed,gameover
    if event.type == pg.KEYDOWN and not gameover:
        if saved_velocity != (0, speed) and (event.key == pg.K_w or event.key == pg.K_UP):
            saved_velocity = (0, -speed)
        if saved_velocity != (speed, 0) and (event.key == pg.K_a or event.key == pg.K_LEFT):
            saved_velocity = (-speed, 0)
        if saved_velocity != ( 0, -speed) and (event.key == pg.K_s or event.key == pg.K_DOWN):
            saved_velocity = (0, speed)
        if saved_velocity != (-speed, 0) and (event.key == pg.K_d or event.key == pg.K_RIGHT):
            saved_velocity = (speed, 0)


def movesnake():
    # move the snake
    global blocks
    blocks = np.concatenate((np.array([blocks[0] + saved_velocity]), blocks), axis=0)
    blocks = np.delete(blocks, len(blocks) - 1, 0)


def checkcollisions():
    global blocks, saved_velocity, gameover, score
    # check if outside boundaries
    h = blocks[0]
    prev = h + saved_velocity
    if h[0] >= width - block_dim or h[0] <= 0 or h[1] >= height - block_dim or h[1] <= 0:
        gameover = True
    elif SURFACE.get_at((int(prev[0]), int(prev[1]))) == (200, 255, 0) and saved_velocity != (0, 0):
        gameover = True
    else:
        for b in blocks:
            if b[0] == apple_x - block_dim/2 and b[1] == apple_y-block_dim/2:
                # add to tail
                blocks = np.concatenate((np.array([[apple_x - block_dim/2, apple_y-block_dim/2]]), blocks), axis=0)
                assignAppleCoords()
                score += 1
    if gameover:
        saved_velocity = (0, 0)


def assignAppleCoords():
    global apple_x, apple_y
    x = [0] * 2
    redo = True
    while redo:
        redo = False
        x[0] = block_dim * random.randint((2 * block_dim) / 10, xlines) - int(block_dim / 2)  # x start
        x[1] = block_dim * random.randint((2 * block_dim) / 10, xlines) - int(block_dim / 2)  # y start
        if x[0] == start[0] or x[1] == start[1]:
            redo = True
        if x[0] + block_dim >= width or x[1] + block_dim >= height:
            redo = True

    if start[0] % 20 == x[0] % 20:
        x[0] = x[0] + int(block_dim / 2)

    if start[1] % 20 == x[1] % 20:
        x[1] = x[1] + int(block_dim / 2)

    if SURFACE.get_at((x[0], x[1])) == (200, 255, 0):
        assignAppleCoords()
    else:
        apple_x = x[0]
        apple_y = x[1]


newgame()


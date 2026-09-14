# Left click to draw black
# Right click to fill blue
import pygame as pg

from floodfill import floodfill

# Setup pygame
h = 40
w = 40
px_size = 20
fps = 60

pg.init()
screen = pg.display.set_mode((w*px_size, h*px_size))
myfont = pg.font.SysFont("monospace", 12)
clock = pg.time.Clock()


image = [[1]*w for _ in range(h)]

left_pressed = False

running = True
while running:
 
    for event in pg.event.get():
        if event.type == pg.QUIT:
            # Close window
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False

        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                left_pressed = True

            if event.button == 3:
                x, y = event.pos
                row = y//px_size
                col = x//px_size
                floodfill(image,row,col,2)

        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                left_pressed = False

    if left_pressed:
        x,y = pg.mouse.get_pos()
        row = y//px_size
        col = x//px_size
        image[row][col] = 2


    screen.fill((0,0,0))
    for row in range(h):
        for col in range(w):
            if image[row][col] == 0:
                pg.draw.rect(screen, (0,0,0), (col*px_size+1, row*px_size+1, px_size-1, px_size-1))
            elif image[row][col] == 1:
                pg.draw.rect(screen, (200,200,200), (col*px_size+1, row*px_size+1, px_size-1, px_size-1))
            elif image[row][col] == 2:
                pg.draw.rect(screen, (0,0,200), (col*px_size+1, row*px_size+1, px_size-1, px_size-1))

    pg.display.flip()
    clock.tick(fps)
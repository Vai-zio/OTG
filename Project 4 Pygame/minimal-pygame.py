import pygame as pg
import time

x=1900
y=50
screen = pg.display.set_mode((1440,740))
pg.display.set_caption("My Pygame Program")

ship_img = pg.image.load("Kachow.png")

running = True
while running:

    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            running = False
    #pg.draw.rect(screen, (r,g,b),(left,up,width,height))
    #pg.draw.rect(screen, (0,0,0), (500,500,500,500))
    #venter 1/60 af et sekund
    #time.sleep(1/60)

    x=x-4
    y=y-4
    screen.fill((0,0,0))
    pg.display.update()
    time.sleep(1/90)
    screen.blit(ship_img,(x,50))
    pg.display.update()
    time.sleep(1/90)
    if x<-1900:
        x=1900
    if y<-43:
        y=50

pg.quit()

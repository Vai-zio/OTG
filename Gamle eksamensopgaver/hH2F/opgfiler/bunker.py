import pygame as pg
import random
import math

# Setup pygame
width = 800
height = 600
lives = 5
pg.init()
screen = pg.display.set_mode((width, height))
myfont = pg.font.SysFont("monospace", 12)
clock = pg.time.Clock()

bullets = []
class Bullet:
    def __init__(self, x, y, dir):
        self.x = x
        self.y = y
        self.dir = dir

enemies = []
class Enemy:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

def draw_game(pos, direction):

    # Background
    pg.draw.rect(screen, (10,50,20), pg.Rect(0,0,width,height))

    # Bunker 
    pg.draw.circle(screen, (110,50,120), (width/2,height-20), 30)

    end_pos = [0,0]
    l = 100
    end_pos[0] = (width/2) - l*math.cos(direction)
    end_pos[1] = (height - 20) - l*math.sin(direction)
    pg.draw.line(screen, (110,50,120), (width/2,height - 20), (end_pos[0],end_pos[1]), 10)

    # Grass
    pg.draw.rect(screen, (10,150,20), pg.Rect(0,height - 20,width,100))

    # Text
    screen.blit(myfont.render("{} points".format(points), 0, (255,255,255)), (50,50))
    screen.blit(myfont.render("{} lives".format(lives), 0, (255,0,0)), (width-100,50))

    # Bullets
    for b in bullets:
        pg.draw.circle(screen, (200,200,200), (b.x,b.y), 4)

    # Enemies
    for e in enemies:
        pg.draw.circle(screen, (255,255,255), (e.x,e.y), e.size, width=1)

points = 0
state = "menu"
running = True

while running:
    if state == "menu":
    
        for event in pg.event.get():
            if event.type == pg.QUIT:
                # Close window
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                elif event.key == pg.K_s:
                    state = "game"
                elif event.key == pg.K_l:
                    state = "leaderboard"



        #TEXT and elements
        pg.draw.rect(screen, (0,0,0), pg.Rect(0,0,width,height))
        screen.blit(myfont.render("{} points".format(points), 0, (255,255,255)), (50,50))

   
    elif state == "game":

        pos = [0,0]
        pos[0] = (width/2) - pg.mouse.get_pos()[0]
        pos[1] = height - 20 - pg.mouse.get_pos()[1]
        direction = math.atan2(pos[1],pos[0])

        for event in pg.event.get():
            if event.type == pg.QUIT:
                # Close window
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False

            elif event.type == pg.MOUSEBUTTONDOWN:
                # Fire bullet
                x = (width/2) - 100*math.cos(direction)
                y = height - 20 -100*math.sin(direction)
                bullets.append(Bullet(x, y, direction))
                points -= 2 

        # Update bullets
        for b in bullets:
            b.x -= 6*math.cos(b.dir)
            b.y -= 6*math.sin(b.dir)
            if b.y < 0:
                bullets.remove(b)

        # Bullet collision check
        for b in bullets:
            for e in enemies:
                d = math.sqrt( (e.x-b.x)**2 + (e.y-b.y)**2)
                if d < e.size:
                    e.size -= 10
                    if e.size <= 0:
                        enemies.remove(e)
                        points += 20
                    else:
                        points += 2 

                    bullets.remove(b)
                    break


        #Update enemies
        if random.random() > 0.993:
            enemies.append(Enemy(random.randint(50, width-50), -50,50))

        for enemy in enemies:
            enemy.y += 1
            if enemy.y > height - 20 - enemy.size:
                enemies.remove(enemy)
                lives -= 1

            if lives <= 0:
                state = "gameover"


        draw_game(pos, direction)

    pg.display.flip()
    clock.tick(60)

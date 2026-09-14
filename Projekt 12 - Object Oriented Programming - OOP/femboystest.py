from femboys import femboy, twink
import pygame as pg
import sys
import random
import math

pg.init()
pg.font.init() # you have to call this at the start, 
                   # if you want to use this module.
my_font = pg.font.SysFont('Comic Sans MS', 30)

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
TITLE = "Pygame Starter Template"

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Setup screen
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption(TITLE)

# Clock for frame rate
clock = pg.time.Clock()

c1 = femboy(100,200,20)
c2 = twink(100,130,60)


circles = []
for i in range(20):
    c = femboy(random.randint(200,300),random.randint(100,500),random.randint(3,10),)
    circles.append(c)

circles2 = []
for i in range(random.randint(10,15)):
    c2 = twink(random.randint(200,300),random.randint(100,500),random.randint(3,10))
    circles2.append(c2)


# Keypress status
left_pressed = False
right_pressed = False
forward_pressed = False
backwards_pressed = False
shift_pressed = False

Movefactor = float(random.randint(-200,200)/100)

state = "START"

running = True
while running:
    if state == "START":
        # --- Event handling ---
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                running = False
        
            # Keypresses
            elif event.type == pg.KEYDOWN:

                if event.key == pg.K_r:
                    state = "RUN"
                if event.key == pg.K_l:
                    state = "leaderboard"
        
        for c in circles:
            if c.x-c.r <= 0 or c.x+c.r >= 800:
                c.MoveDirectionX *= -1
                #print("Circles(c).MovedirectionX:", c.MoveDirectionX)
            if c.y-c.r <= 0 or c.y+c.r >= 600:
                c.MoveDirectionY *= -1
                #print("Circles(c).MovedirectionY:", c.MoveDirectionY)
            c.move()

        for c2 in circles2:
            if c2.x-c2.r <= 0 or c2.x+c2.r >= 800:
                c2.MoveDirectionX *= -1
                #print("Circles2(c).MovedirectionX:", c.MoveDirectionX)
            if c2.y-c2.r <= 0 or c2.y+c2.r >= 600:
                c2.MoveDirectionY *= -1
                #print("Circles2(c).MovedirectionY:", c.MoveDirectionY)
            c2.move()

        """
        for c in circles:
            if c.collide(c2):
                c.MoveDirectionY *= -1 
                c.MoveDirectionX *= -1
        """

        """ SOME FORM OF MOVEMENT WITHOUT CLASSES
        if c1.x-c1.r <= 0 or c1.x+c1.r >= 800:
            MovedirectionX *= -1
            print("MoveDirectionX:", MovedirectionX)
        if c1.y-c1.r <= 0 or c1.y+c1.r >= 600:
            MovedirectionY *= -1
            print("MoveDirectionY:", MovedirectionY)
        c1.move(MovedirectionX,MovedirectionY)

        if c2.x-c2.r <= 0 or c2.x+c2.r >= 800:
            MovedirectionX *= -1
            print("MoveDirectionX:", MovedirectionX)
        if c2.y-c2.r <= 0 or c2.y+c2.r >= 600:
            MovedirectionY *= -1
            print("MoveDirectionY:", MovedirectionY)
        c2.move(((-MovedirectionX)*Movefactor),((-MovedirectionY)*Movefactor))
        print("Movefactor:", Movefactor)
        """

        screen.fill(WHITE)
        for c in circles:
            pg.draw.circle(screen,(c.color),(c.x,c.y),c.r)
        for c in circles2:
            pg.draw.circle(screen,(c.color),(c.x,c.y),c.r)
        # Source - https://stackoverflow.com/a
        # Posted by Bartlomiej Lewandowski, modified by community. See post 'Timeline' for change history
        #  Retrieved 2025-11-18, License - CC BY-SA 4.0

        text = my_font.render('Press R to Start', False, (0, 0, 0))
        screen.blit(text,((SCREEN_WIDTH/2-text.get_width()/2),(SCREEN_HEIGHT/2-text.get_height()/2)))

    elif state == "RUN":
        # --- Event handling ---
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                running = False
        
            # Keypresses
            elif event.type == pg.KEYDOWN:

                if event.key == pg.K_w:
                    forward_pressed = True
                if event.key == pg.K_s:
                    backwards_pressed = True
                if event.key == pg.K_LSHIFT:
                    shift_pressed = True
                elif event.key == pg.K_LEFT:
                    left_pressed = True
                elif event.key == pg.K_RIGHT:
                    right_pressed = True

            # Keyreleases
            elif event.type == pg.KEYUP:

                if event.key == pg.K_LSHIFT:
                    shift_pressed = False
                elif event.key == pg.K_LEFT:
                    left_pressed = False
                elif event.key == pg.K_RIGHT:
                    right_pressed = False

        # Normal movement speed
        movement_speed = 6

        # Apply boost if SHIFT is pressed
        if shift_pressed:
            movement_speed = 12

        # Spaceship
        if left_pressed:
            c1.x -= movement_speed
        if right_pressed:
            c1.x += movement_speed
        if forward_pressed:
            c1.y -= movement_speed
        if backwards_pressed:
            c1.y += movement_speed


        for c in circles:
            if c.x-c.r <= 0 or c.x+c.r >= 800:
                c.MoveDirectionX *= -1
                #print("Circles(c).MovedirectionX:", c.MoveDirectionX)
            if c.y-c.r <= 0 or c.y+c.r >= 600:
                c.MoveDirectionY *= -1
                #print("Circles(c).MovedirectionY:", c.MoveDirectionY)
            c.move()

        for c in circles2:
            if c.x-c.r <= 0 or c.x+c.r >= 800:
                c.MoveDirectionX *= -1
                #print("Circles(c).MovedirectionX:", c.MoveDirectionX)
            if c.y-c.r <= 0 or c.y+c.r >= 600:
                c.MoveDirectionY *= -1
                #print("Circles(c).MovedirectionY:", c.MoveDirectionY)
            c.move()


        for c in circles:
            if c.collide(c):
                c1.r += c.r
                circles.remove(c)
                c = femboy(random.randint(100,700),random.randint(100,500),5)
                circles.append(c)

        for c2 in circles2:
            if c1.collide(c):
                c1.r += c.r
                circles2.remove(c2)
                c = femboy(random.randint(100,700),random.randint(100,500),10)
                circles2.append(c)

        screen.fill(WHITE)
        pg.draw.circle(screen,BLACK,(c1.x,c1.y),c1.r)
        pg.draw.circle(screen,BLACK,(c2.x,c2.y),c2.r)
        for c in circles:
            pg.draw.circle(screen,BLACK,(c.x,c.y),c.r) 

        for d in circles:
            pg.draw.circle(screen,(255,0,0),(d.x,d.y),d.r)


    pg.display.flip()  # Update the display

    # --- Frame rate ---
    clock.tick(FPS)

pg.quit()
sys.exit()


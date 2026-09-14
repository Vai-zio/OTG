import pygame as pg
import os
import time


# Screen setup
pg.init()
screen = pg.display.set_mode((600,600))

# Game loop
running = True
tick = 0 
#player
x = 200
y = 200
w1 = 30
h1 = 30
#zone
x2 = 400
y2 = 400
w2 = 100
h2 = 100
#zone colors
zone_colors = [200,200,200]
#player colors
player_colors = [200,0,0]

zone = [x2,y2,w2,h2]
player = [x,y,w1,h1]
def rect_collision(x,y,w1,h1,x2,y2,w2,h2):
    if x2 < x+w1 and x < x2+w2:
        if y2 < y+h1 and y < y2+h2:
            return True
    else:
        return False

while running:

    # Event loop
    for event in pg.event.get():
        if event.type == pg.QUIT:
            # Close window
            running = False

        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False

            elif event.key == pg.K_LEFT:
                player[0] -= 5
            elif event.key == pg.K_RIGHT:
                player[0] += 5
            elif event.key == pg.K_UP:
                player[1] -= 5 
            elif event.key == pg.K_DOWN:
                player[1] += 5

            elif event.key == pg.K_a:
                zone[0] -= 5
            elif event.key == pg.K_d:
                zone[0] += 5
            elif event.key == pg.K_w:
                zone[1] -= 5 
            elif event.key == pg.K_s:
                zone[1] += 5
        
    #if (zone[0] < player[0] + player[2] < zone[0+2] and zone[1] < player[1] + player[3] < zone[1+3]):
    #if (player[0] < zone[0] + zone[2] and player[0] + player[2] > zone[0] and 
    #   player[1] < zone[1] + zone[3] and player[1] + player[3] > zone[1]):
        #print("collision detected")
        


    screen.fill((0,0,0))

    if rect_collision(player[0],player[1],player[2],player[3],zone[0],zone[1],zone[2],zone[3]):
        zone_colors = [0,200,0]
        print("PREPARE FOR IMAPCT!")
#            if rect_collision() want to do purple if the whole player is inside zone)
    else:
        zone_colors = [200,200,200]


    # Draw zones
    pg.draw.rect(screen, zone_colors, zone)

    # Draw player
    pg.draw.rect(screen, (200,20,20), player)

    # Update the screen window with any new drawings
    pg.display.flip()


    # Wait before next frame 
    time.sleep(0.2)
    tick = tick + 1
    print("tick", tick)

pg.display.quit()
pg.quit()

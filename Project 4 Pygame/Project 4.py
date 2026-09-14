import pygame as pg
import random
import os
import time
import util #expects util.py in same folder as game
import math

#set 1 player
x=500
y=500
w1=1
h1=1
r_p = 20

#variables
angle = 0
tick = 0

#objects
zones = []
zones.append([700,300,100,100])
zones.append([500,300,100,100])
zones.append([900,300,100,100])
zones.append([1100,300,100,100])

c_zones = []
c_zones.append([350,150,50])
c_zones.append([550,150,50])
c_zones.append([750,150,50])
c_zones.append([950,150,50])
zone_circle = [350,350,50]

#player
player = [x,y,w1,h1]

#colors_objects
zones_colors = []
zone_colors = [0,200,0]
zones_colors.append([0,200,0])
zones_colors.append([200,0,200])
zone_c_colors =[0,200,0]
player_c_colors = [200,0,0]

#length between the to circles centers
d = r_p + zone_circle[2]

screen = pg.display.set_mode((1440,760))
pg.display.set_caption("Spaceship miner")

br1 = pg.image.load("blackrock.png")
br2 = pg.image.load("blackrock2.png")
gr2 = pg.image.load("greenrock2.png")
pr2 = pg.image.load("purplerock2.png")
r1 = pg.image.load("rock.png")
ss1 = pg.image.load("spaceship1.png")
wr2 = pg.image.load("whiterock2.png")
yr2 = pg.image.load("yellowrock2.png")

# Load images
spaceship_animation = []
for i in range(4):
    img_file = os.path.join("Elementer", f"spaceship3a{i}.png")
    img = pg.image.load(img_file)
    spaceship_animation.append(img)

r_spaceship = [pg.transform.rotate(img, angle) for img in spaceship_animation]

pg.init()
pg.display.set_icon(r_spaceship[3])

#Collision detection
rect_collision = util.rect_collision
circle_collision = util.circle_collision

running = True

move_left = False
move_right = False
move_up = False
move_down = False


while running:
    
    current_frame = pg.time.get_ticks()
    events = pg.event.get()
    for event in events:
        print("event:",event)
        if event.type == pg.QUIT:
            running = False
            print("No")
#Movement
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            if event.key == pg.K_LEFT:
                move_left = True
                angle = 90
            if event.key == pg.K_RIGHT:
                move_right = True
                angle = 270
            if event.key == pg.K_UP:
                move_up = True
                angle = 0
            if event.key == pg.K_DOWN:
                move_down = True
                angle = 180
            if event.key == pg.K_SPACE:
                if move_down == True:
                    player[1]=player[1]+100
                if move_right == True:
                    player[0]=player[0]+100
                if move_left == True:
                    player[0]=player[0]-100
                if move_up == True:
                    player[1]=player[1]-100
                if event.key == pg.K_SPACE:
                    if not move_down and not move_left and not move_right and not move_up:
                        if angle == 90:
                            player[0]=player[0]-100
                        if angle == 0:
                            player[1]=player[1]-100
                        if angle == 270:
                            player[0]=player[0]+100
                        if angle == 180:
                            player[1]=player[1]+100

                    
        elif event.type == pg.KEYUP:
            if event.key == pg.K_LEFT:
                move_left = False
            if event.key == pg.K_RIGHT:
                move_right = False
            if event.key == pg.K_UP:
                move_up = False
            if event.key == pg.K_DOWN:
                move_down = False
            
    if move_left:
        player[0]=player[0]-2
    if move_right:
       player[0]=player[0]+2
    if move_up:
        player[1]=player[1]-2
    if move_down:
        player[1]=player[1]+2
    


#Draw background

    screen.fill((0,0,0))
    #Rect Collision + drawing and player hitbox
    Rect_Detect_Collision = False
    for zone in zones:
        if rect_collision(player[0],player[1],r_p,zone[0],zone[1],zone[2],zone[3]):
            Rect_Detect_Collision = True
            zone_colors = [200,0,200]
            break
        
        if not Rect_Detect_Collision:
            zone_colors = [0,200,0]

#Circle collision
    Circle_Detect_Collision = False
    for c_zone in c_zones:
        if circle_collision(player[0],player[1],r_p,c_zone[0],c_zone[1],c_zone[2]):
            Circle_Detect_Collision = True
            zone_c_colors = [200,0,200]
            break
    
        if not Circle_Detect_Collision:
            zone_c_colors = [0,200,0]


#Drawing zones and players hitbox
    for c_zone in c_zones:
            pg.draw.circle(screen,zone_c_colors,(c_zone[0],c_zone[1]),c_zone[2])

    for zone in zones:
            pg.draw.rect(screen,zone_colors,zone)

    pg.draw.circle(screen,player_c_colors,(player[0],player[1]),r_p)

    #screen.blit(br2,(200,200,50,50))

#Animation of player

    # Rotate the image based on the angle
    r = tick//8 % len(r_spaceship)
    rotated_image = pg.transform.rotate(r_spaceship[r], angle)

    # Get the rect of the rotated image and adjust its position to (x, y)
    rotated_rect = rotated_image.get_rect(center=(player[0], player[1]))

    # Blit the rotated image onto the screen at the correct position
    screen.blit(rotated_image, rotated_rect.topleft)

    # Update the screen window with any new drawings
    pg.display.flip()
    tick = tick + 1
    #print(f"i={i}  {i}%5={i%5}")
    #print(i, (i//2)%5)
    print(f"║ Ship: tick = {tick} ║ Ship: Animation frame = {r}  ║ Impact C: = {circle_collision(player[0],player[1],r_p,c_zone[0],c_zone[1],c_zone[2]) is True} ║  Impact R: = {rect_collision(player[0],player[1],r_p,zone[0],zone[1],zone[2],zone[3]) is True}")
    
    # Update the frame    
    pg.display.update()
    
    

pg.quit()
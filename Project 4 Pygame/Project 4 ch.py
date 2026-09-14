import pygame as pg
import random
import os
import time
import util  # expects util.py in the same folder as the game
import math

# set 1 player
x = 500
y = 500
w1 = 1
h1 = 1
r_p = 20

# variables
angle = 0
tick = 0

# objects
zones = []
zones.append([700, 300, 100, 100])
zones.append([500, 300, 100, 100])
zones.append([900, 300, 100, 100])
zones.append([1100, 300, 100, 100])

c_zones = []
c_zones.append([350, 150, 50])
c_zones.append([550, 150, 50])
c_zones.append([750, 150, 50])
c_zones.append([950, 150, 50])

zone_circle = [350, 350, 50]

# player
player = [x, y, w1, h1]

# colors for individual objects
zones_colors = [[0, 200, 0] for _ in zones]  # Initialize each rect with green
c_zones_colors = [[0, 200, 0] for _ in c_zones]  # Initialize each circle with green
player_c_colors = [200, 0, 0]  # Player color

screen = pg.display.set_mode((1440, 760))
pg.display.set_caption("Spaceship miner")

# Load images
spaceship_animation = []
for i in range(4):
    img_file = os.path.join("Elementer", f"spaceship3a{i}.png")
    img = pg.image.load(img_file)
    spaceship_animation.append(img)

r_spaceship = [pg.transform.rotate(img, angle) for img in spaceship_animation]

pg.init()
pg.display.set_icon(r_spaceship[3])

# Collision detection functions
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
        if event.type == pg.QUIT:
            running = False

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

        elif event.type == pg.KEYUP:
            if event.key == pg.K_LEFT:
                move_left = False
            if event.key == pg.K_RIGHT:
                move_right = False
            if event.key == pg.K_UP:
                move_up = False
            if event.key == pg.K_DOWN:
                move_down = False
            if event.key == pg.K_SPACE:
                if move_down == True:
                    player[1] += 100
                if move_right == True:
                    player[0] += 100
                if move_left == True:
                    player[0] -= 100
                if move_up == True:
                    player[1] -=100
                if event.key == pg.K_SPACE:
                    if not move_down and not move_left and not move_right and not move_up:
                        if angle == 90:
                            player[0] -= 100
                        if angle == 0:
                            player[1] -=100
                        if angle == 270:
                            player[0] += 100
                        if angle == 180:
                            player[1] += 100

    # Update player movement
    if move_left:
        player[0] -= 2
    if move_right:
        player[0] += 2
    if move_up:
        player[1] -= 2
    if move_down:
        player[1] += 2

    # Draw background
    screen.fill((0, 0, 0))

    # Rect Collision + drawing and player hitbox
    for i, zone in enumerate(zones):
        if rect_collision(player[0], player[1], r_p, zone[0], zone[1], zone[2], zone[3]):
            zones_colors[i] = [200, 0, 200]  # Change color on collision
        else:
            zones_colors[i] = [0, 200, 0]  # Reset to green if no collision

    # Circle collision + color update
    for i, c_zone in enumerate(c_zones):
        if circle_collision(player[0], player[1], r_p, c_zone[0], c_zone[1], c_zone[2]):
            c_zones_colors[i] = [200, 0, 200]  # Change color on collision
        else:
            c_zones_colors[i] = [0, 200, 0]  # Reset to green if no collision

    # Drawing zones and player hitbox
    for i, c_zone in enumerate(c_zones):
        pg.draw.circle(screen, c_zones_colors[i], (c_zone[0], c_zone[1]), c_zone[2])

    for i, zone in enumerate(zones):
        pg.draw.rect(screen, zones_colors[i], zone)

    pg.draw.circle(screen, player_c_colors, (player[0], player[1]), r_p)

    # Animation of player
    r = tick // 8 % len(r_spaceship)
    rotated_image = pg.transform.rotate(r_spaceship[r], angle)
    rotated_rect = rotated_image.get_rect(center=(player[0], player[1]))
    screen.blit(rotated_image, rotated_rect.topleft)

    # Update the screen window with any new drawings
    pg.display.flip()
    tick +=1

pg.quit()

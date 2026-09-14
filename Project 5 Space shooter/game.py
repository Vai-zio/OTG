# Arcade-style space shooter inspired by Galaga and Spacer Invaders.
# Made for the purpose of teaching git version control to beginners.

import pygame as pg
import os
import time
from PIL import Image
import math
import functions # as in functions.py in same folder

### Setup ###pg.init()
clock = pg.time.Clock()

sw, sh = 600, 800
screen = pg.display.set_mode((sw, sh))
pg.display.set_caption("Space Defender")


# Background GIF loading
space_world = pg.image.load("images/PLAY_BG_WORLD.jpg")
space = pg.image.load("images/PLAY_BG_SPACE.jpg")
flipped_space = pg.transform.flip(space, True, False)  # Flip horizontally
flipped_world = pg.transform.flip(space_world, True, False)  # Flip Vertically

gif_file = os.path.join("images/giphy.gif")
gif = Image.open(gif_file)
frames = []
try:
    while True:
        frames.append(gif.copy())
        gif.seek(gif.tell() + 1)
except EOFError:
    pass


# Initialize frame tracking and frame rate for GIF
frame_idx = 0
gif_frame_rate = 10  # GIF updates per second
gif_last_update = pg.time.get_ticks()

colors = [(220, 20, 60), (255, 165, 0), (255, 223, 0)]  # Deep Red, Bright Orange, Golden Yellow
transition_time = 2  # Transition time in seconds

# Function to interpolate between two colors
def lerp_color(start, end, t):
    return (
        int(start[0] + (end[0] - start[0]) * t),
        int(start[1] + (end[1] - start[1]) * t),
        int(start[2] + (end[2] - start[2]) * t),
    )

# Dictionary to store transition states for each text element
text_transitions = {
    "score": {
        "color_index": 0,
        "start_color": colors[0],
        "end_color": colors[1],
        "transition_start_time": pg.time.get_ticks(),
        "position": (10, 770),
        "text": "Score: 0",
    },
    "lives": {
        "color_index": 1,
        "start_color": colors[1],
        "end_color": colors[2],
        "transition_start_time": pg.time.get_ticks(),
        "position": (10, 720),
        "text": "Lives: 3",
    },
}

# Function to update color for each text
def update_text_color(transition_data):
    # Calculate the transition ratio (t)
    elapsed_time = (pg.time.get_ticks() - transition_data["transition_start_time"]) / 1000
    t = elapsed_time / transition_time  # Normalized time (0.0 to 1.0)

    # Update color and reset if transition completes
    if t >= 1.0:
        transition_data["color_index"] = (transition_data["color_index"] + 1) % len(colors)
        transition_data["start_color"] = colors[transition_data["color_index"]]
        transition_data["end_color"] = colors[(transition_data["color_index"] + 1) % len(colors)]
        transition_data["transition_start_time"] = pg.time.get_ticks()
        t = 0  # Reset t for the next transition

    # Interpolate current color
    return lerp_color(transition_data["start_color"], transition_data["end_color"], t)

# Spaceship character
ship_images = []
for i in range(4):
    img_file = os.path.join("Elementer", f"spaceship3a{i}.png")
    img = pg.image.load(img_file)
    ship_images.append(img)
ship_x = 250 
ship_y = 700
ship_w = ship_images[0].get_rect().size[0]
ship_h = ship_images[0].get_rect().size[1]

# Alien character
alien_images = []
for i in range(2):
    img = pg.image.load(f"images/alien_w{i}.png")
    alien_images.append(img)

#Alien hit color 
alien_colors = {
    6: (0, 255, 0),      # Green
    5: (102, 255, 0),    # Light green
    4: (204, 255, 0),    # Yellow-green
    3: (255, 204, 0),    # Orange-yellow
    2: (255, 101, 0),    # Orange
    1: (255, 0, 0)       # Red
}

def change_color(image, color):
    colouredImage = pg.Surface(image.get_size())
    colouredImage.fill(color)
    
    finalImage = image.copy()
    finalImage.blit(colouredImage, (0, 0), special_flags = pg.BLEND_MULT)
    return finalImage

# Initialize game variables
def initialize_game():
    global ship_x, ship_y, aliens, projectiles, cannons, score, current_alien_speed, alien_move_right, left_pressed, right_pressed, projectile_fired, cannon_fired
    ship_x, ship_y = 250, 700
    aliens = []
    for i in range(8):
        alien1 = {'x': 50 + 50 * i, 'y': 0, 'hp': 6, 'color': alien_colors[6]}
        alien2 = {'x': 50 + 50 * i, 'y': 50, 'hp': 6, 'color': alien_colors[6]}
        alien3 = {'x': 50 + 50 * i, 'y': 100, 'hp': 6, 'color': alien_colors[6]}
        aliens.extend([alien1, alien2, alien3])
    projectiles, cannons = [], []
    score = 0
    current_alien_speed = ALIEN_DESCENT_SPEED
    alien_move_right = True
    left_pressed, right_pressed = False, False
    projectile_fired, cannon_fired = False, False

#High score tracking
HIGH_SCORE_FILE = "high_score.txt"

def load_high_score():
    try:
        with open(HIGH_SCORE_FILE, "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0
    
def save_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as file:
        file.write(str(score))

high_score = load_high_score()

alien_w = alien_images[0].get_rect().size[0]
alien_h = alien_images[0].get_rect().size[1]

# Bullet settings
projectile_speed = 10
projectile_w, projectile_h = 4, 8

# List to store active bullets
projectiles = []

# Function to fire bullets with spread
def fire_projectiles_spread(x, y):
    """Fire three bullets from the given x, y position with spread angles."""
    spread_angle = 10  # Angle in degrees for left and right bullets

    # Central bullet (angle = 0 degrees)
    projectiles.append({'x': x, 'y': y, 'angle': 0})

    # Left bullet (-spread_angle degrees)
    projectiles.append({'x': x, 'y': y, 'angle': -spread_angle})

    # Right bullet (+spread_angle degrees)
    projectiles.append({'x': x, 'y': y, 'angle': spread_angle})

#Cannon
cannons = []
cannon_r = 20

# Alien movement settings
ALIEN_DESCENT_SPEED = 0.2  # Initial descent speed per frame
ALIEN_HORIZONTAL_SPEED = 1  # Speed of horizontal dodging movement
SPEEDUP_INTERVAL = 8000   # 80 seconds in milliseconds
ALIEN_SPEEDUP_INCREMENT = 0.1  # Increase in descent speed every 10 seconds

# Timer to track speedup intervals
last_speedup_time = pg.time.get_ticks()
current_alien_speed = ALIEN_DESCENT_SPEED

# Direction for dodging
alien_move_right = True

# Keypress status
left_pressed = False
right_pressed = False

# Sound: weapon / laser 
# https://sfxr.me/#34T6Pm25W5VunHtL14gUxhLx6MqNduzaeRPcUbqtT4RN55w6nP9NipaUrx5ZBBvohWwXgMrd5BS2e7HwRwEVyzmKM3FV8LiU7Gh5ob2VvvMi6ftqdhbVB54ZM 
pg.mixer.init()
sound_laser = pg.mixer.Sound("sounds/laser.wav")
sound_cannon = pg.mixer.Sound("sounds/cannon.mp3")
sound_ult = pg.mixer.Sound("sounds/ult.mp3")
sound_alien_death = pg.mixer.Sound("sounds/alien_death.mp3")

# Fonts
# https://fonts.google.com/specimen/Press+Start+2P/about
pg.font.init()
font_title = pg.font.Font("fonts/PressStart2P-Regular.ttf", 32)

font_body = pg.font.Font("fonts/PressStart2P-Regular.ttf", 18)

font_small = pg.font.Font("fonts/PressStart2P-Regular.ttf", 14)

### Game loop ###
running = True
tick = 0
score = 0

# Position tracking for the panning background
space_y1 = 0
space_y2 = -sh+space_world.get_height()  # Second position starts just above the screen
world_x1 = 0
world_x2 = -sw-space_world.get_width()
space_speed = 5  # Speed of the panning background
shift_pressed = False

state = "START"

initialize_game()  # Initialize variables
while running:

    if state == "START":
            current_time = pg.time.get_ticks()
            if current_time - gif_last_update > 1000 // gif_frame_rate:
                frame_idx = (frame_idx + 1) % len(frames)
                gif_last_update = current_time
            
            # Draw GIF frame to the screen
            #Gif background settings:
            frame = frames[frame_idx]
            mode = frame.mode
            size = frame.size
            data = frame.tobytes()
            gif_blit = pg.image.fromstring(data, size, mode)
            screen.blit(gif_blit, ((screen.get_width()//2 - gif_blit.get_width()//2), (screen.get_height()//2 - gif_blit.get_height()//2)))

            events = pg.event.get()
            for event in events:

                # Close window (pressing [x], Alt+F4 etc.)
                if event.type == pg.QUIT:
                    running = False

                # Keypresses
                elif event.type == pg.KEYDOWN:

                    if event.key == pg.K_ESCAPE:
                        running = False
                    
                    elif event.key == pg.K_SPACE:
                        initialize_game()
                        state = "PLAY"
                    elif event.key == pg.K_TAB:
                        state = "SECRET"
                #Not made yet

            # Update each text element's color independently
            for key, data in text_transitions.items():
                current_color = update_text_color(data)

            text = font_title.render(f"SPACE DEFENDER", True, (current_color))
            text_width = text.get_rect().width 
            screen.blit(text, ((screen.get_width()-text_width)/2, 120))

            text1 = font_title.render(f"Press", True, (255,255,255))
            text_width1 = text1.get_rect().width 
            text2 = font_title.render(f"[SPACE]", True, (current_color))
            text_width2 = text2.get_rect().width 
            screen.blit(text1, ((screen.get_width()//2 - text_width2//2 - text_width1//2), 630))
            screen.blit(text2, ((screen.get_width()//2 - text_width1//2 + text_width2//3), 630))

            text = font_title.render(f"to play!", True, (255,255,255))
            text_width = text.get_rect().width 
            screen.blit(text, ((sw-text_width)/2, 680))

    elif state == "PLAY":
        ## Event loop  (handle keypresses etc.) ##
        events = pg.event.get()
        for event in events:

            # Close window (pressing [x], Alt+F4 etc.)
            if event.type == pg.QUIT:
                running = False

            # Keypresses
            elif event.type == pg.KEYDOWN:

                if event.key == pg.K_ESCAPE:
                    running = False
                if event.key == pg.K_SPACE:
                    projectile_fired = True
                if event.key == pg.K_c:
                    cannon_fired = True
                if event.key == pg.K_r:
                    state = "GAME_OVER"
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
            ship_x -= movement_speed
        if right_pressed:
            ship_x += movement_speed

        # Alien movement with speed-up every 10 seconds
        current_time = pg.time.get_ticks()
        if current_time - last_speedup_time >= SPEEDUP_INTERVAL:
            current_alien_speed += ALIEN_SPEEDUP_INCREMENT
            last_speedup_time = current_time

        for alien in aliens:
            alien['y'] += current_alien_speed  # Move each alien down
            if alien_move_right:
                alien['x'] += ALIEN_HORIZONTAL_SPEED
            else:
                alien['x'] -= ALIEN_HORIZONTAL_SPEED

            # Reverse direction if an alien hits the screen boundaries
            if alien['x'] + alien_w >= screen.get_width()-50:
                alien_move_right = False
            if alien['x'] <= 50:
                alien_move_right = True
            if alien['x'] + alien_w >= screen.get_width()+100:
                aliens.remove(alien)
            if alien['x'] <= -100:
                aliens.remove(alien)

        # Projectile movement
        for projectile in projectiles[:]:  # Copy the list to avoid modification issues
            # Convert angle to radians for trigonometric calculations
            rad = math.radians(projectile['angle'])
            projectile['x'] += projectile_speed * math.sin(rad)
            projectile['y'] -= projectile_speed * math.cos(rad)

            # Remove projectiles leaving the top of the screen
            if projectile['y'] < 0 or projectile['x'] < 0 or projectile['x'] > sw:
                projectiles.remove(projectile)

        # Cannon movement
        # Reverse iteration needed to handle each projectile correctly
        # in cases where a projectile is removed.
        for cannon in reversed(cannons):
            cannon['y'] -= 6

            # Remove projectiles leaving the top of the screen
            if cannon['y'] < 0:
                cannons.remove(cannon)

        #To evade crashing because of color correction 
        aliens_to_remove = []

        # Alien / projectile collision 
        # Test each projectile against each alien
        for projectile in reversed(projectiles):
            for alien in aliens:

                # Horizontal (x) overlap
                if (alien['x'] < projectile['x'] + projectile_w and 
                    projectile['x'] < alien['x']+alien_w):

                    # Vertical (y) overlap 
                    if (projectile['y'] < alien['y'] + alien_h and 
                        alien['y'] < projectile['y'] + projectile_h):

                        # Alien is hit
                        projectiles.remove(projectile)
                        alien['hp'] -= 1
                        if alien['hp'] in alien_colors:
                            alien['color'] = alien_colors[alien['hp']]
                        if alien['hp'] == 0:
                            aliens.remove(alien)
                            score += 10
                            sound_alien_death.play()

                        # No further aliens can be hit by this projectile 
                        # so skip to the next projectile 
                        break

        # Alien / Cannon collision 
        # Test each cannon against each alien
        for cannon in reversed(cannons):
            for alien in aliens:

                # Horizontal (x) overlap
                if (alien['x'] < cannon['x'] + cannon_r and 
                    cannon['x'] < alien['x']+alien_w):

                    # Vertical (y) overlap 
                    if (cannon['y'] < alien['y'] + alien_h and 
                        alien['y'] < cannon['y'] + cannon_r):

                        # Alien is hit
                        sound_alien_death.play()
                        aliens.remove(alien)
                        score +=10

                        # No further aliens can be hit by this projectile 
                        # so skip to the next projectile 
                        break
    
        # Alien spawn
        if len(aliens) == 0:
            for i in range(8):
                alien1 = {'x': 50 + 50 * i, 'y': -130, 'hp': 6, 'color': alien_colors[6]}
                alien2 = {'x': 50 + 50 * i, 'y': -80, 'hp': 6, 'color': alien_colors[6]}
                alien3 = {'x': 50 + 50 * i, 'y': -30, 'hp': 6, 'color': alien_colors[6]}
                aliens.extend([alien1, alien2, alien3])
            ALIEN_DESCENT_SPEED = 0.2
        

        # Firing (spawning new projectiles)
        # Update this part of your game loop to handle projectile firing and movement
        if projectile_fired:
            sound_laser.play()
            fire_projectiles_spread(ship_x + ship_w / 2 - projectile_w / 2, ship_y)
            fire_projectiles_spread(ship_x + ship_w / 2 - projectile_w / 2, ship_y-18)
            projectile_fired = False
    

        # Firing (spawning new projectiles) CANNON!
        if cannon_fired:
            sound_ult.play()
            if sound_ult.play():
                sound_cannon.play()

            cannon = {'x': ship_x + ship_w/2,'y': ship_y}
            cannons.append(cannon)
            cannon_fired = False


        # Game Over condition: Alien reaches bottom and crosses borders
        if alien['y'] >= screen.get_height():
            state = "GAME_OVER"  # Switch to Game Over state
        if alien['x'] >= screen.get_width():
            alien_move_right = False
        if alien['x'] <= 0:
            alien_move_right = True
        if alien['x'] <= -10 or alien['x'] >= screen.get_width()+10:
            aliens.remove(alien)
            score += 10
        

        ## Drawing ## Play state
        screen.fill((0,0,0)) 
        
        # Move the panning background down
        space_y1 += space_speed
        space_y2 += space_speed

        # Reset positions when they go off-screen
        if space_y1 >= sh-space_world.get_height():
            space_y1 = -sh+space_world.get_height()
        if space_y2 >= sh-space_world.get_height():
            space_y2 = -sh+space_world.get_height()

        # Draw the two instances of the panning background
        screen.blit(space, (0, space_y1))
        screen.blit(flipped_space, (0, space_y2))
        screen.blit(space_world,(0,screen.get_height()-space_world.get_height()))


        # 3 images --> tick % 3
        # 100% animation speed: tick % 3
        # 25% animation speed: int(tick/4) % 3
        r = int(tick/4) % 3 
        screen.blit(ship_images[r], (ship_x, ship_y))

        # Alien
        r = int(tick/8) % 2
        for alien in aliens:
            colored_alien_image = change_color(alien_images[r], alien['color'])
            screen.blit(colored_alien_image, (alien['x'], alien['y']))

        # Projectiles
        for projectile in projectiles:
            rect = (projectile['x'], projectile['y'], projectile_w, projectile_h)
            pg.draw.rect(screen, (current_color), rect) 
        
        # Cannon ball
        for cannon in cannons:
            circle = (cannon['x'], cannon['y'])
            pg.draw.circle(screen, (current_color), circle, cannon_r) 


        # Update each text element's color independently
        for key, data in text_transitions.items():
            current_color = update_text_color(data)

        # Display score
        text = font_body.render(f"Score: {score}", True, (current_color))
        screen.blit(text, (10, 770))

        #Display restart function
        text = font_small.render("Press R to Restart", True, (255,0,0))
        screen.blit(text, (screen.get_width()- text.get_width()-10, screen.get_height()-text.get_height()-text.get_height()-20))
        text = font_small.render("Hold [LSHIFT] for double speed", True, (255,0,0))
        screen.blit(text, (screen.get_width()- text.get_width()-10, screen.get_height()-text.get_height()-10))

    elif state == "GAME_OVER":
        # Game Over screen

        if score > high_score:
            high_score = score
            save_high_score(high_score)

        events = pg.event.get()
        for event in events:
       
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    initialize_game()  # Reset all game variables
                    state = "PLAY"  # Restart the game
                if event.key == pg.K_SPACE:
                    state = "START"  # Restart the game

        # Update each text element's color independently
        for key, data in text_transitions.items():
            current_color = update_text_color(data)

        screen.fill((0, 0, 0))
        text = font_title.render("GAME OVER", True, (255, 0, 0))
        screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 150))
        
        if score == high_score:
            text = font_small.render("you suck less than expected", True, (current_color))
            screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 200))
        else:
            text = font_small.render("you suck", True, (255, 0, 0))
            screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 200))
    
        text1 = font_body.render("Press", True, (255, 255, 255))
        text2 = font_body.render("[R]", True, (current_color))
        text3 = font_body.render("to Restart", True, (255, 255, 255))
        total_text_width = text1.get_width() + text2.get_width() +  text3.get_width()
        screen.blit(text1, (screen.get_width() // 2 - total_text_width//2, 300))
        screen.blit(text2, (screen.get_width() // 2 - total_text_width//2 + text1.get_width() + 8, 300))
        screen.blit(text3, (screen.get_width() // 2 - total_text_width//2 + text1.get_width() + text2.get_width() + 16, 300))

        text1 = font_small.render("Press", True, (255, 255, 255))
        text2 = font_small.render("[SPACE]", True, (current_color))
        text3 = font_small.render("to get to the start screen", True, (255, 255, 255))
        total_text_width = text1.get_width() + text2.get_width() +  text3.get_width()
        screen.blit(text1, (screen.get_width() // 2 - total_text_width//2, 600))
        screen.blit(text2, (screen.get_width() // 2 - total_text_width//2 + text1.get_width() + 8, 600))
        screen.blit(text3, (screen.get_width() // 2 - total_text_width//2 + text1.get_width() + text2.get_width() + 16, 600))

        text = font_body.render(f"High score: {high_score}", True, (255, 255, 255))
        screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 450))

        text = font_body.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 350))


    # Update window with newly drawn pixels
    pg.display.flip()

    # Limit/fix frame rate (fps)
    clock.tick(50)
    tick += 1

pg.quit()
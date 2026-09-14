import pygame as pg
import os

# Setup
pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode((600, 800))
pg.display.set_caption("Space Shooter")

# Load Fonts and Sounds
font_scoreboard = pg.font.Font("fonts/PressStart2P-Regular.ttf", 20)
font_gameover = pg.font.Font("fonts/PressStart2P-Regular.ttf", 30)
sound_laser = pg.mixer.Sound("sounds/laser.wav")

# Initialize game variables
def initialize_game():
    global ship_x, ship_y, aliens, projectiles, cannons, score, current_alien_speed, alien_move_right, left_pressed, right_pressed, projectile_fired, cannon_fired
    ship_x, ship_y = 200, 500
    aliens = []
    for i in range(8):
        alien1 = {'x': 50 + 50 * i, 'y': 0}
        alien2 = {'x': 50 + 50 * i, 'y': 50}
        alien3 = {'x': 50 + 50 * i, 'y': 100}
        aliens.extend([alien1, alien2, alien3])
    projectiles, cannons = [], []
    score = 0
    current_alien_speed = ALIEN_DESCENT_SPEED
    alien_move_right = True
    left_pressed, right_pressed = False, False
    projectile_fired, cannon_fired = False, False

# Spaceship settings
ship_images = [pg.image.load(os.path.join("Elementer", f"spaceship3a{i}.png")) for i in range(4)]
ship_w, ship_h = ship_images[0].get_rect().size

# Alien settings
alien_images = [pg.image.load(f"images/alien_{i}.png") for i in range(2)]
alien_w, alien_h = alien_images[0].get_rect().size

# Projectile and cannon settings
projectile_w, projectile_h, cannon_r = 4, 8, 20

# Alien movement settings
ALIEN_DESCENT_SPEED = 0.2
ALIEN_HORIZONTAL_SPEED = 1
SPEEDUP_INTERVAL = 10000  # 10 seconds
ALIEN_SPEEDUP_INCREMENT = 0.1

# Initialize key variables and states
last_speedup_time = pg.time.get_ticks()
state = "START"  # Game states: "START", "PLAY", "GAME_OVER"
initialize_game()  # Set initial game variables

# Game loop
running, tick = True, 0
while running:
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False

            # Handle keypresses for each state
            if state == "START":
                if event.key == pg.K_SPACE:
                    state = "PLAY"
                    initialize_game()
            elif state == "PLAY":
                if event.key == pg.K_LEFT:
                    left_pressed = True
                elif event.key == pg.K_RIGHT:
                    right_pressed = True
                elif event.key == pg.K_SPACE:
                    projectile_fired = True
                elif event.key == pg.K_c:
                    cannon_fired = True
            elif state == "GAME_OVER" and event.key == pg.K_r:
                state = "PLAY"  # Restart the game
                initialize_game()  # Reset game variables

        elif event.type == pg.KEYUP and state == "PLAY":
            if event.key == pg.K_LEFT:
                left_pressed = False
            elif event.key == pg.K_RIGHT:
                right_pressed = False

    # Game logic based on state
    if state == "START":
        screen.fill((0, 0, 0))
        text = font_gameover.render("Space Shooter", True, (255, 255, 255))
        screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 100))
        text = font_gameover.render("Press SPACE to start", True, (255, 255, 255))
        screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 200))

    elif state == "PLAY":
        ## Updating (movement, collisions, etc.) ##
        # Spaceship movement
        if left_pressed:
            ship_x -= 8
        if right_pressed:
            ship_x += 8

        # Alien movement with speed-up and dodging
        current_time = pg.time.get_ticks()
        if current_time - last_speedup_time >= SPEEDUP_INTERVAL:
            current_alien_speed += ALIEN_SPEEDUP_INCREMENT
            last_speedup_time = current_time

        for alien in aliens:
            alien['y'] += current_alien_speed
            alien['x'] += ALIEN_HORIZONTAL_SPEED if alien_move_right else -ALIEN_HORIZONTAL_SPEED

            # Reverse direction if hitting the boundary
            if alien['x'] + alien_w >= screen.get_width() or alien['x'] <= 0:
                alien_move_right = not alien_move_right
                alien['y'] += 10  # Move down slightly when changing direction

            # Game Over condition: Alien reaches bottom
            if alien['y'] >= screen.get_height() - alien_h:
                state = "GAME_OVER"

        # Projectiles and Cannon movement
        for projectile in reversed(projectiles):
            projectile['y'] -= 8
            if projectile['y'] < 0:
                projectiles.remove(projectile)

        for cannon in reversed(cannons):
            cannon['y'] -= 4
            if cannon['y'] < 0:
                cannons.remove(cannon)

        # Alien / Projectile collision
        for projectile in reversed(projectiles):
            for alien in aliens:
                if (alien['x'] < projectile['x'] + projectile_w and 
                    projectile['x'] < alien['x'] + alien_w and 
                    projectile['y'] < alien['y'] + alien_h and 
                    alien['y'] < projectile['y'] + projectile_h):
                    projectiles.remove(projectile)
                    aliens.remove(alien)
                    score += 10
                    break

        # Alien / Cannon collision
        for cannon in reversed(cannons):
            for alien in aliens:
                if (alien['x'] < cannon['x'] + cannon_r and 
                    cannon['x'] < alien['x'] + alien_w and 
                    cannon['y'] < alien['y'] + alien_h and 
                    alien['y'] < cannon['y'] + cannon_r):
                    aliens.remove(alien)
                    score += 20
                    break

        # Firing projectiles and cannon balls
        if projectile_fired:
            sound_laser.play()
            projectiles.append({'x': ship_x + ship_w / 2 - projectile_w / 2, 'y': ship_y})
            projectile_fired = False

        if cannon_fired:
            sound_laser.play()
            cannons.append({'x': ship_x + ship_w / 2, 'y': ship_y})
            cannon_fired = False

        ## Drawing ##
        screen.fill((0, 0, 0))

        # Draw spaceship with animation
        r = int(tick / 4) % 3
        screen.blit(ship_images[r], (ship_x, ship_y))

        # Draw aliens with animation
        r = int(tick / 8) % 2
        for alien in aliens:
            screen.blit(alien_images[r], (alien['x'], alien['y']))

        # Draw projectiles and cannon balls
        for projectile in projectiles:
            pg.draw.rect(screen, (255, 0, 0), (projectile['x'], projectile['y'], projectile_w, projectile_h))
        for cannon in cannons:
            pg.draw.circle(screen, (255, 0, 0), (cannon['x'], cannon['y']), cannon_r)

        # Scoreboard
        text = font_scoreboard.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(text, (10, 760))

    elif state == "GAME_OVER":
        # Game Over screen
        screen.fill((0, 0, 0))
        text = font_gameover.render("Game Over", True, (255, 0, 0))
        screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 200))
        text = font_gameover.render("Press R to Restart", True, (255, 255, 255))
        screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 300))

    # Update display
    pg.display.flip()
    clock.tick(50)
    tick += 1

pg.quit()

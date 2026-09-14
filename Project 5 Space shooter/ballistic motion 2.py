import pygame as pg
import math
import random

pg.init()
clock = pg.time.Clock()

sw, sh = 1000, 800
screen = pg.display.set_mode((sw, sh))
pg.display.set_caption("Ball Launch and Bounce")

# Colors
bg_color = (0, 200, 100)
text_color = (255, 255, 255)
highlight_color = (255, 0, 0)
ball_color = (200, 20, 20)
trace_color = (200, 0, 20)
arrow_color = (0, 0, 0)

# Ball variables
x, y = 50, 700
vx, vy = 1, 1
bd = 20
trace = []
speed = 5
angle = math.radians(45)
shown_angle = 45
wall_bounces = 0
max_bounces = 3
speed_increment = 2  # Speed increase per reset

# Game state
game_state = "main"  # "main", "bounce", or "launch"
menu_options = ["BOUNCE", "LAUNCH"]
selected_option = 0

# Font setup
pg.font.init()
font_title = pg.font.Font(None, 64)
font_menu = pg.font.Font(None, 48)
font_small = pg.font.Font(None, 32)

running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if game_state == "main":
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pg.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pg.K_RETURN:  # Confirm selection
                    if menu_options[selected_option] == "BOUNCE":
                        game_state = "bounce"
                    elif menu_options[selected_option] == "LAUNCH":
                        game_state = "launch"
                        vx, vy = 0, 0  # Stop ball for launch mode
                        wall_bounces = 0  # Reset bounces
        elif game_state == "launch":
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:  # Launch the ball
                    vx = speed * math.cos(angle)
                    vy = speed * math.sin(angle)
                    game_state = "bounce"
                    trace = []  # Clear trace after launch
                elif event.key == pg.K_UP:  # Adjust angle upwards
                    angle += math.radians(5)
                    shown_angle = math.degrees(angle)
                elif event.key == pg.K_DOWN:  # Adjust angle downwards
                    angle -= math.radians(5)
                    shown_angle = math.degrees(angle)
                elif event.key == pg.K_w:  # Increase speed
                    speed += 1
                elif event.key == pg.K_s:  # Decrease speed
                    speed = max(1, speed - 1)
        elif game_state == "bounce":
            if event.type == pg.KEYDOWN and event.key == pg.K_r:  # Reset to main menu
                game_state = "main"

    if game_state == "main":
        # Draw main menu
        screen.fill(bg_color)
        title_text = font_title.render("Ball Game", True, text_color)
        screen.blit(title_text, ((sw - title_text.get_width()) // 2, 200))

        for i, option in enumerate(menu_options):
            color = highlight_color if i == selected_option else text_color
            menu_text = font_menu.render(option, True, color)
            screen.blit(menu_text, ((sw - menu_text.get_width()) // 2, 300 + i * 60))

    elif game_state == "launch":
        # Draw the ball at the initial position
        screen.fill(bg_color)
        pg.draw.circle(screen, ball_color, (int(x), int(y)), bd, 5)

        # Draw the aiming arrow
        arrow_length = 100
        arrow_x = x + arrow_length * math.cos(angle)
        arrow_y = y + arrow_length * math.sin(angle)
        pg.draw.line(screen, arrow_color, (x, y), (arrow_x, arrow_y), 3)

        # Draw angle and speed info
        angle_text = font_small.render(f"Angle: {int(shown_angle)}°", True, text_color)
        screen.blit(angle_text, (10, 10))

        speed_text = font_small.render(f"Speed: {int(speed)}", True, text_color)
        screen.blit(speed_text, (10, 40))

        bounce_text = font_small.render(f"Bounces: {wall_bounces}/{max_bounces}", True, text_color)
        screen.blit(bounce_text, (10, 70))

    elif game_state == "bounce":
        # Update position
        x += vx
        y += vy
        vy += 0.5  # Gravity effect

        # Bounce off walls
        if y >= sh - bd // 2 or y <= bd // 2:
            vy = -vy
            wall_bounces += 1
        if x >= sw - bd // 2 or x <= bd // 2:
            vx = -vx
            wall_bounces += 1

        # Check if max bounces are reached
        if wall_bounces >= max_bounces:
            # Reset to launch mode with increased speed
            game_state = "launch"
            x, y = 50, 700
            vx, vy = 0, 0
            speed += speed_increment
            wall_bounces = 0
            trace = []  # Clear trace after reset

        # Record trace
        trace.append((x, y))
        if len(trace) > 100:
            trace.pop(0)

        # Draw the trace
        screen.fill(bg_color)
        for xt, yt in trace:
            pg.draw.circle(screen, trace_color, (int(xt), int(yt)), 2)
        # Draw the ball
        pg.draw.circle(screen, ball_color, (int(x), int(y)), bd, 5)

    pg.display.update()
    clock.tick(50)

pg.quit()

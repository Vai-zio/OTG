import pygame as pg
import math
import random

pg.init()
clock = pg.time.Clock()

sw, sh = 1000, 800
screen = pg.display.set_mode((sw, sh))
pg.display.set_caption("Ballistic motion")

colors = [(220, 20, 60), (128, 0, 128), (0, 0, 200)]  # Deep Red, Purple, Blue
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

def initialize_game():
    global x, y, vx, vy, bd, trace, shown_angle, angle, speed
    x, y, vx, vy, bd = 50, 700, 1, 1, 20
    trace = []
    shown_angle = 1
    angle = 1
    speed = 5

#colors other than current_color
bg_color = (0, 200, 100)
text_color = (255, 255, 255)
highlight_color = (255, 0, 0)
ball_color = (200, 20, 20)
trace_color = (200, 0, 20)
arrow_color = (0, 0, 0)

# Game state
game_state = "main"  # "main", "bounce", or "launch"
menu_options = ["BOUNCE", "LAUNCH"]
selected_option = 0

# Fonts
pg.font.init()
font_title = pg.font.Font(None, 64)
font_small = pg.font.Font(None, 32)

initialize_game()
running = True

while running:
    # Process events once per frame
    events = pg.event.get()
    for event in events:
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

        elif game_state == "bounce":
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    initialize_game()
                    game_state == "launch"
                elif event.key == pg.K_SPACE:
                    vx *= 1.5
                    vy *= 1.5
                elif event.key == pg.K_LSHIFT:
                    vx /= 1.5
                    vy /= 1.5
                elif event.key == pg.K_m:
                    game_state = "main"
        
        elif game_state == "launch":
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:  # Launch the ball
                    vx = speed * math.cos(angle)
                    vy = speed * math.sin(angle)
                    game_state = "bounce"
                    trace = []  # Clear trace after launch
                elif event.key == pg.K_UP:  # Adjust angle upwards
                    angle -= math.radians(5)
                    shown_angle = math.degrees(angle)
                elif event.key == pg.K_DOWN:  # Adjust angle downwards
                    angle += math.radians(5)
                    shown_angle = math.degrees(angle)
                elif event.key == pg.K_w:  # Increase speed
                    vx *= 2
                    vy *= 2
                elif event.key == pg.K_s:  # Decrease speed
                    vx /= 2
                    vy /= 2
                elif event.key == pg.K_LEFT:
                    speed += 1
                elif event.key == pg.K_RIGHT:
                    speed -= 1

    # Game logic
    if game_state == "main":
        # Draw main menu
        screen.fill(bg_color)
        title_text = font_title.render("Ball Game", True, text_color)
        screen.blit(title_text, ((sw - title_text.get_width()) // 2, 200))
        
        for key, data in text_transitions.items():
            current_color = update_text_color(data)

        for i, option in enumerate(menu_options):
            color = current_color if i == selected_option else text_color
            menu_text = font_title.render(option, True, color)
            screen.blit(menu_text, ((sw - menu_text.get_width()) // 2, 300 + i * 60))

    elif game_state == "bounce":
        # Ball movement and bouncing logic
        x += vx
        y += vy
        vy += 0.5  # Gravity effect

        if y >= sh - bd // 2 or y <= bd // 2:
            vy = -vy
        if x >= sw - bd // 2 or x <= bd // 2:
            vx = -vx

        trace.append((x, y))
        if len(trace) > 100:
            trace.pop(0)

        # Drawing
        screen.fill(bg_color)
        for xt, yt in trace:
            pg.draw.circle(screen, (200, 0, 20), (int(xt), int(yt)), 2)
        pg.draw.circle(screen, (200, 20, 20), (int(x), int(y)), bd)

        # Draw angle and speed information
        speed = math.sqrt(vx**2 + vy**2) //1
        angle = math.atan2(vy, vx) 
        shown_angle = math.degrees(angle) //1

        arrow_length = 30
        arrow_x = x + arrow_length * math.cos(angle)
        arrow_y = y + arrow_length * math.sin(angle)
        pg.draw.line(screen, highlight_color, (x, y), (arrow_x, arrow_y), 3)

        for key, data in text_transitions.items():
            current_color = update_text_color(data)

        text = font_title.render(f"Angle: {shown_angle//1}", True, (current_color))
        text_width = text.get_rect().width 
        screen.blit(text, ((screen.get_width()-text_width)/2, 120))

        text = font_title.render(f"Speed {speed//1}", True, (current_color))
        text_width = text.get_rect().width 
        screen.blit(text, ((screen.get_width()-text_width)/2, (160)))
        
        text = font_title.render(f"Vx: {vx//1}", True, (current_color))
        text_width = text.get_rect().width 
        screen.blit(text, ((screen.get_width()-text_width)/2, (200)))

        text = font_title.render(f"Vy: {vy//1}", True, (current_color))
        text_width = text.get_rect().width 
        screen.blit(text, ((screen.get_width()-text_width)/2, (240)))

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
        text = font_title.render(f"Angle: {shown_angle//1}", True, (current_color))
        text_width = text.get_rect().width 
        screen.blit(text, ((screen.get_width()-text_width)/2, 120))

        text = font_title.render(f"Speed {speed//1}", True, (current_color))
        text_width = text.get_rect().width 
        screen.blit(text, ((screen.get_width()-text_width)/2, (160)))
        
        text = font_title.render(f"Vx: {vx//1}", True, (current_color))
        text_width = text.get_rect().width 
        screen.blit(text, ((screen.get_width()-text_width)/2, (200)))

        text = font_title.render(f"Vy: {vy//1}", True, (current_color))
        text_width = text.get_rect().width 
        screen.blit(text, ((screen.get_width()-text_width)/2, (240)))

    pg.display.update()
    clock.tick(50)

pg.quit()


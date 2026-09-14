import pygame as pg
import time
import random
import sqlite3
import time, datetime
from PIL import Image
import os

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

colors = [(88, 28, 135), (255, 45, 150), (153, 27, 27)]  # Colors
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

#Create SQL connection
con = sqlite3.connect("reaction-time-game.db") # connection
con.row_factory = sqlite3.Row

sql = """CREATE TABLE IF NOT EXISTS highscores(
        id INTEGER PRIMARY KEY,
        username TEXT,
        date TEXT,
        timems FLOAT
    )"""

con.execute(sql)
con.commit()

#Establish time for highscore
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

pg.init()

w = 800
h = 800
screen = pg.display.set_mode((w,h))

font_large = pg.font.Font(None, 80)
font = pg.font.Font(None, 40)

clock = pg.time.Clock()

timer_start = None
wait_start = None
wait_duration = None

name = ""

state = "ready"
running = True
while running:
    
    events = pg.event.get() 
    for event in events:
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            running = False


    if state == "ready":
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

        # Update each text element's color independently
        for key, data in text_transitions.items():
            current_color = update_text_color(data)

        text = font_large.render(f"REACTION TIME", True, (current_color))
        text_rect = text.get_rect(center=(w/2, 100))
        screen.blit(text, text_rect)

        msgs = ["Press any key as fast as you can",
                "when the screen turns green!",
                "Press [space] to start the game"]

        for i, msg in enumerate(msgs):
            text = font.render(msg, True, (current_color))
            text_rect = text.get_rect(center=(w/2, h/2+i*100))
            screen.blit(text, text_rect)

        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    state = "wait"
                    wait_start = time.time()
                    wait_duration = random.uniform(2,5)


    elif state == "wait":
        screen.fill((0,0,0))

        if time.time() - wait_start > wait_duration:
            start_time = time.time()
            state = "timer"

        for event in events:
            if event.type == pg.KEYDOWN:
                state = "gameover"

        
    elif state == "gameover":
        screen.fill((200,20,20))

        text = font_large.render("GAME OVER!", True, (255,255,255))
        text_rect = text.get_rect(center=(w/2, h/2))
        screen.blit(text, text_rect)
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    state = "ready"

        

    elif state == "timer":
        screen.fill((20,200,20))
        for event in events:
            if event.type == pg.KEYDOWN:
                state = "result"
                end_time = time.time()


    elif state == "result":
        reaction_time_ms = (end_time - start_time)*1000

        text = font.render(f"Your reaction time was: {reaction_time_ms:.2f} ms", True, (255,255,255))
        text_rect = text.get_rect(center=(w/2, 100))
        screen.blit(text, text_rect)
        reaction = f"{reaction_time_ms:.4f}"

        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    state = "highscores" 

                    con.execute("INSERT INTO highscores(username,timems,date) VALUES (?,?,?);",(name,reaction,now))
                    con.commit()
                else:
                    name += event.unicode
                
        text = font_large.render(f"Name: {name}", True, (255,255,255))
        screen.blit(text, (50,200))

        
        
    elif state == "highscores":
        for key, data in text_transitions.items():
            current_color = update_text_color(data)

        screen.fill((0,0,0))
        scores = [con.execute("""Select * from highscores ORDER BY timems DESC LIMIT 10;""")]
        for i, s in enumerate(scores, start=1):
            text = font.render(f"#{i}  {s}   {name}", True, (current_color))
            screen.blit(text, (100,i*100))
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    state = "wait"

        
        

    pg.display.update() 
    clock.tick(100)

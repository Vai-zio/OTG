import math

# Initialize game variables
ALIEN_DESCENT_SPEED = 0.2 
def initialize_game():
    global ship_x, ship_y, aliens, projectiles, cannons, score, current_alien_speed, alien_move_right, left_pressed, right_pressed, projectile_fired, cannon_fired
    ship_x, ship_y = 250, 700
    aliens = []
    for i in range(8):
        alien1 = {'x': 50 + 50 * i, 'y': 0, 'hp': 4}
        alien2 = {'x': 50 + 50 * i, 'y': 50,'hp': 4}
        alien3 = {'x': 50 + 50 * i, 'y': 100,'hp': 4}
        aliens.extend([alien1, alien2, alien3])
    projectiles, cannons = [], []
    score = 0
    current_alien_speed = ALIEN_DESCENT_SPEED
    alien_move_right = True
    left_pressed, right_pressed = False, False
    projectile_fired, cannon_fired = False, False

#High Score load functions
HIGH_SCORE_FILE = "high_score.txt"
def load_high_score():
    try:
        with open(HIGH_SCORE_FILE, "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0
# High score save function
def save_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as file:
        file.write(str(score))

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

# Define colors for gradient transition
def lerp_color(start, end, t):
#    """Linearly interpolate between two colors based on t (0.0 to 1.0)."""
    return (
        int(start[0] + (end[0] - start[0]) * t),
        int(start[1] + (end[1] - start[1]) * t),
        int(start[2] + (end[2] - start[2]) * t)
    )
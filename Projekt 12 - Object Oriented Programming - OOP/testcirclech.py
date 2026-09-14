# File: agario_expanding_map.py
"""
A compact Agar-like demo with:
 - triangle-style smooth player movement (WASD / arrows)
 - player faces mouse
 - pellets to eat (grow area)
 - hostile orbs that seek player, damage on hit
 - orbs damage one another on collision; if they die due to orb-orb collision you gain points
 - expanding world: world size and camera zoom change with player's growth
Controls:
 - Move: WASD or Arrow keys
 - Quit: ESC or window close
"""
from __future__ import annotations
import math, random, sys
import pygame as pg

# --- Config ---
SCREEN_W, SCREEN_H = 1000, 700
BASE_WORLD_W, BASE_WORLD_H = 1600, 1200
FPS = 60

NUM_PELLETS = 60
NUM_ORBS = 10
PELLET_MIN_R, PELLET_MAX_R = 4, 12
ORB_MIN_R, ORB_MAX_R = 14, 28

PLAYER_START_R = 18
PLAYER_START_POS = (BASE_WORLD_W / 2, BASE_WORLD_H / 2)

PLAYER_ACCEL = 1600.0
PLAYER_BASE_MAX_SPEED = 420.0
PLAYER_FRICTION = 1200.0

# Orb behavior
ORB_SEEK_FORCE = 110.0
ORB_MAX_SPEED = 160.0
ORB_HP = 3
ORB_HIT_TO_PLAYER_DAMAGE = 1
ORB_COLLISION_DAMAGE = 2

# Eat factor: player must be this many times bigger in radius to automatically eat pellet
EAT_FACTOR = 1.03

# Player death threshold
PLAYER_MAX_HITS = 5

# Scoring
POINTS_FOR_ORB_KILL_BY_ORBORB = 15

# Colors
BG_COLOR = (10, 14, 20)
PELLET_COLOR = (160, 220, 160)
ORB_COLOR = (220, 120, 120)
PLAYER_OUTLINE = (20, 20, 30)
HUD_COLOR = (220, 220, 220)

pg.init()
screen = pg.display.set_mode((SCREEN_W, SCREEN_H))
pg.display.set_caption("Agar-like: Expanding Map + Seeking Orbs")
clock = pg.time.Clock()
font = pg.font.SysFont(None, 20)

# --- Utility classes ---
class Circle:
    def __init__(self, x: float, y: float, r: float, color=(200,200,200)):
        self.x = float(x); self.y = float(y); self.r = float(r)
        self.color = color
        self.v = pg.math.Vector2(random.uniform(-40,40), random.uniform(-40,40))

    @property
    def pos(self):
        return pg.math.Vector2(self.x, self.y)

    @property
    def area(self):
        return math.pi * (self.r ** 2)

    def set_area(self, area):
        self.r = math.sqrt(max(area, 1e-6) / math.pi)

    def move(self, dt, world_w, world_h):
        self.x += self.v.x * dt
        self.y += self.v.y * dt
        # bounce on world edges
        if self.x - self.r < 0:
            self.x = self.r; self.v.x *= -1
        if self.x + self.r > world_w:
            self.x = world_w - self.r; self.v.x *= -1
        if self.y - self.r < 0:
            self.y = self.r; self.v.y *= -1
        if self.y + self.r > world_h:
            self.y = world_h - self.r; self.v.y *= -1
        # slight wander
        if random.random() < 0.01:
            self.v += pg.math.Vector2(random.uniform(-60,60), random.uniform(-60,60))
            if self.v.length() > 120:
                self.v.scale_to_length(120)

    def collide(self, other: "Circle") -> bool:
        dx = self.x - other.x; dy = self.y - other.y
        return dx*dx + dy*dy <= (self.r + other.r)**2

# --- Player using triangle movement (accelerate/friction) ---
class Player:
    def __init__(self, x, y, radius=PLAYER_START_R):
        self.pos = pg.math.Vector2(x, y)
        self.vel = pg.math.Vector2(0,0)
        self.accel = PLAYER_ACCEL
        self.friction = PLAYER_FRICTION
        self.base_max_speed = PLAYER_BASE_MAX_SPEED
        self.area = math.pi * (radius * radius)
        self.update_radius()
        self.angle = 0.0
        self.eaten = 0
        self.hits = 0
        self.score = 0

    def update_radius(self):
        self.r = math.sqrt(max(self.area,1e-6) / math.pi)

    def max_speed(self):
        # player becomes faster as they grow (but clamp)
        return self.base_max_speed + (self.area * 0.002)

    def handle_input_dir(self, keys):
        dx = 0; dy = 0
        if keys[pg.K_a] or keys[pg.K_LEFT]: dx -= 1
        if keys[pg.K_d] or keys[pg.K_RIGHT]: dx += 1
        if keys[pg.K_w] or keys[pg.K_UP]: dy -= 1
        if keys[pg.K_s] or keys[pg.K_DOWN]: dy += 1
        v = pg.math.Vector2(dx, dy)
        if v.length_squared() > 0:
            return v.normalize()
        return v

    def update(self, dt, keys, world_w, world_h):
        dirv = self.handle_input_dir(keys)
        if dirv.length_squared() > 0:
            self.vel += dirv * (self.accel * dt)
        else:
            # friction deceleration
            speed = self.vel.length()
            if speed > 0:
                decel = min(self.friction * dt, speed)
                self.vel.scale_to_length(max(speed - decel, 0))

        # clamp speed
        if self.vel.length() > self.max_speed():
            self.vel.scale_to_length(self.max_speed())

        # integrate
        self.pos += self.vel * dt

        # keep inside world
        self.pos.x = max(self.r, min(world_w - self.r, self.pos.x))
        self.pos.y = max(self.r, min(world_h - self.r, self.pos.y))

        # face mouse (world mouse pos will be set by camera)
        mx, my = pg.mouse.get_pos()
        # we expect update to receive camera transform externally; angle updated in main loop where we have world mouse
        # angle handled elsewhere

    def set_angle_towards(self, world_mouse_pos):
        rel = pg.math.Vector2(world_mouse_pos) - self.pos
        if rel.length_squared() > 0:
            self.angle = math.degrees(math.atan2(-rel.y, rel.x))

    def try_eat(self, pellet: Circle) -> bool:
        # can only eat if larger (radius) compared to pellet by EAT_FACTOR
        dx = self.pos.x - pellet.x; dy = self.pos.y - pellet.y
        if dx*dx + dy*dy <= (self.r + pellet.r)**2 and self.r >= pellet.r * EAT_FACTOR:
            self.area += pellet.area
            self.update_radius()
            self.eaten += 1
            return True
        return False

    def take_hit(self, amount=1):
        self.hits += amount

    def is_dead(self):
        return self.hits >= PLAYER_MAX_HITS

    def draw(self, surf, cam_offset, zoom):
        # draw rotated triangle; cam_offset and zoom applied to world coordinates
        # triangle defined pointing to +x
        r = self.r
        pts_local = [
            pg.math.Vector2(r, 0),
            pg.math.Vector2(-0.6*r, -r),
            pg.math.Vector2(-0.6*r, r),
        ]
        a = math.radians(self.angle)
        cos_a = math.cos(a); sin_a = math.sin(a)
        screen_pts = []
        for p in pts_local:
            rx = p.x * cos_a - p.y * sin_a
            ry = p.x * sin_a + p.y * cos_a
            wx = self.pos.x + rx
            wy = self.pos.y - ry
            sx = (wx - cam_offset.x) * zoom
            sy = (wy - cam_offset.y) * zoom
            screen_pts.append((int(sx), int(sy)))
        pg.draw.polygon(surf, (80,190,240), screen_pts)
        # outline
        pg.draw.polygon(surf, PLAYER_OUTLINE, screen_pts, 2)

# --- World helpers: camera, zoom, spawn ---
def world_to_screen(world_pos, cam_offset, zoom):
    return ((world_pos.x - cam_offset.x) * zoom, (world_pos.y - cam_offset.y) * zoom)

def spawn_pellet(world_w, world_h):
    r = random.uniform(PELLET_MIN_R, PELLET_MAX_R)
    x = random.uniform(r, world_w - r)
    y = random.uniform(r, world_h - r)
    return Circle(x, y, r, color=PELLET_COLOR)

def spawn_orb(world_w, world_h):
    r = random.uniform(ORB_MIN_R, ORB_MAX_R)
    orb = Circle(random.uniform(r, world_w - r), random.uniform(r, world_h - r), r, color=ORB_COLOR)
    orb.hp = ORB_HP
    return orb

# --- Game state ---
world_w = BASE_WORLD_W
world_h = BASE_WORLD_H
pellets = [spawn_pellet(world_w, world_h) for _ in range(NUM_PELLETS)]
orbs = [spawn_orb(world_w, world_h) for _ in range(NUM_ORBS)]
player = Player(*PLAYER_START_POS, radius=PLAYER_START_R)

# --- Main loop ---
def main():
    global world_w, world_h, pellets, orbs, player
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                running = False
            elif ev.type == pg.KEYDOWN and ev.key == pg.K_ESCAPE:
                running = False

        keys = pg.key.get_pressed()

        # Expand world slowly when player grows
        target_world_w = BASE_WORLD_W + player.area * 0.05
        target_world_h = BASE_WORLD_H + player.area * 0.04
        # smooth approach
        world_w += (target_world_w - world_w) * min(1.0, dt * 0.5)
        world_h += (target_world_h - world_h) * min(1.0, dt * 0.5)

        # Ensure pellets/orbs remain within world; random respawn if out of bounds by some margin
        def ensure_inside(entity):
            if entity.x - entity.r < 0 or entity.x + entity.r > world_w or entity.y - entity.r < 0 or entity.y + entity.r > world_h:
                entity.x = random.uniform(entity.r, world_w - entity.r)
                entity.y = random.uniform(entity.r, world_h - entity.r)
        for p in pellets: ensure_inside(p)
        for o in orbs: ensure_inside(o)

        # Update pellets
        for p in pellets:
            p.move(dt, world_w, world_h)

        # Update orbs: seek player slightly
        for o in orbs:
            # steering toward player
            to_player = pg.math.Vector2(player.pos) - pg.math.Vector2(o.x, o.y)
            if to_player.length_squared() > 0:
                steer = to_player.normalize() * ORB_SEEK_FORCE * dt
                o.v += steer
            # clamp speed
            if o.v.length() > ORB_MAX_SPEED:
                o.v.scale_to_length(ORB_MAX_SPEED)
            o.move(dt, world_w, world_h)

        # Update player (movement)
        player.update(dt, keys, world_w, world_h)

        # Camera: center on player, compute zoom based on radius (bigger => zoom out)
        # zoom range 0.5 .. 1.2
        zoom = max(0.45, min(1.25, 1.2 - (player.r - PLAYER_START_R) * 0.006))
        cam_w = SCREEN_W / zoom; cam_h = SCREEN_H / zoom
        cam_offset = pg.math.Vector2(player.pos.x - cam_w / 2, player.pos.y - cam_h / 2)
        # clamp camera inside world
        cam_offset.x = max(0, min(world_w - cam_w, cam_offset.x))
        cam_offset.y = max(0, min(world_h - cam_h, cam_offset.y))

        # Convert mouse to world coordinates for rotation & interactions
        mouse_sx, mouse_sy = pg.mouse.get_pos()
        world_mouse = pg.math.Vector2(mouse_sx / zoom + cam_offset.x, mouse_sy / zoom + cam_offset.y)
        player.set_angle_towards(world_mouse)

        # Collisions: player eats pellets
        for i in range(len(pellets)-1, -1, -1):
            pel = pellets[i]
            if player.try_eat(pel):
                # respawn pellet
                pellets.pop(i)
                pellets.append(spawn_pellet(world_w, world_h))

        # Collisions: orbs with player
        for orb in orbs:
            dx = orb.x - player.pos.x; dy = orb.y - player.pos.y
            if dx*dx + dy*dy <= (orb.r + player.r)**2:
                # contact: orb deals damage and also takes minor damage
                player.take_hit(ORB_HIT_TO_PLAYER_DAMAGE)
                orb.hp -= 1
                # bounce orb away
                # compute normal and push orb away
                n = pg.math.Vector2(orb.x - player.pos.x, orb.y - player.pos.y)
                if n.length_squared() == 0:
                    n = pg.math.Vector2(random.uniform(-1,1), random.uniform(-1,1))
                n = n.normalize()
                orb.v = n * max(80, orb.v.length())  # push away
                # if orb died from hitting player, treat as non-scoring death (no points)
        # Remove orbs that died (by any cause) but track cause: died_by_orborb = True -> award points
        # We'll process orb-orb collisions first to capture deaths by orb-orb then handle dead by player below.

        # Orb-orb collisions
        # naive O(n^2) acceptable for small NUM_ORBS
        orb_deaths_by_orborb = []  # list of orbs that died due to orb-orb collision
        for i in range(len(orbs)):
            for j in range(i+1, len(orbs)):
                a = orbs[i]; b = orbs[j]
                dx = a.x - b.x; dy = a.y - b.y
                if dx*dx + dy*dy <= (a.r + b.r)**2:
                    # collision: apply damage to both
                    a.hp -= ORB_COLLISION_DAMAGE
                    b.hp -= ORB_COLLISION_DAMAGE
                    # Simple elastic-like bounce: exchange some velocity
                    normal = pg.math.Vector2(dx, dy)
                    if normal.length_squared() == 0:
                        normal = pg.math.Vector2(random.uniform(-1,1), random.uniform(-1,1))
                    normal = normal.normalize()
                    # reflect velocities along normal to separate
                    a.v = a.v.reflect(normal) * 0.9
                    b.v = b.v.reflect(-normal) * 0.9
                    # If either died here, mark for scoring
                    if a.hp <= 0:
                        orb_deaths_by_orborb.append(a)
                    if b.hp <= 0:
                        orb_deaths_by_orborb.append(b)

        # Remove orbs that died: if died_by_orborb -> +points; else respawn silently
        surviving_orbs = []
        for o in orbs:
            if o.hp <= 0:
                # check if in deaths list (object identity)
                if o in orb_deaths_by_orborb:
                    player.score += POINTS_FOR_ORB_KILL_BY_ORBORB
                # respawn replacement
                # spawn new orb somewhere far from player
                new = spawn_orb(world_w, world_h)
                # ensure not spawning on top of player
                while (new.x - player.pos.x)**2 + (new.y - player.pos.y)**2 < (200 + player.r)**2:
                    new.x = random.uniform(new.r, world_w - new.r)
                    new.y = random.uniform(new.r, world_h - new.r)
                surviving_orbs.append(new)
            else:
                surviving_orbs.append(o)
        orbs = surviving_orbs

        # Also handle orbs that died from hitting player earlier (hp <= 0) -> respawn but no points
        # Already handled above since death cause may be mixed; we awarded points only if they died in orb_deaths_by_orborb.

        # Check player death
        if player.is_dead():
            # small death effect: lose some score and reset player
            player.score = max(0, player.score - 30)
            player.area = math.pi * (PLAYER_START_R**2)
            player.update_radius()
            player.pos = pg.math.Vector2(world_w/2, world_h/2)
            player.vel = pg.math.Vector2(0,0)
            player.hits = 0
            # optionally shrink world a bit
            world_w = max(BASE_WORLD_W, world_w * 0.9)
            world_h = max(BASE_WORLD_H, world_h * 0.9)
            # respawn orbs and pellets
            pellets = [spawn_pellet(world_w, world_h) for _ in range(NUM_PELLETS)]
            orbs = [spawn_orb(world_w, world_h) for _ in range(NUM_ORBS)]

        # --- Drawing ---
        screen.fill(BG_COLOR)
        # Draw world as simple rectangle (clipped to screen)
        # Draw pellets
        for p in pellets:
            sx, sy = world_to_screen(pg.math.Vector2(p.x, p.y), cam_offset, zoom)
            sr = max(1, int(p.r * zoom))
            pg.draw.circle(screen, p.color, (int(sx), int(sy)), sr)
            pg.draw.circle(screen, (10,10,10), (int(sx), int(sy)), sr, 1)

        # Draw orbs
        for o in orbs:
            sx, sy = world_to_screen(pg.math.Vector2(o.x, o.y), cam_offset, zoom)
            sr = max(2, int(o.r * zoom))
            pg.draw.circle(screen, o.color, (int(sx), int(sy)), sr)
            # health indicator (thin inner arc)
            if hasattr(o, 'hp'):
                # draw HP as small number
                hp_text = font.render(str(max(0, int(o.hp))), True, (240,240,240))
                screen.blit(hp_text, (int(sx - hp_text.get_width()/2), int(sy - hp_text.get_height()/2)))

        # Draw player
        player.draw(screen, cam_offset, zoom)

        # HUD
        hud_lines = [
            f"Score: {player.score}",
            f"Eaten: {player.eaten}",
            f"Hits: {player.hits}/{PLAYER_MAX_HITS}",
            f"Radius: {player.r:.1f}px",
            f"World: {int(world_w)}x{int(world_h)}",
        ]
        for i, ln in enumerate(hud_lines):
            surf = font.render(ln, True, HUD_COLOR)
            screen.blit(surf, (8, 8 + i*18))

        pg.display.flip()

    pg.quit()
    sys.exit()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import pygame
import random
import math
import sys
from collections import deque

# ----------------------------
# Config
# ----------------------------
TILE_SIZE = 32
GRID_W, GRID_H = 20, 15   # 640 x 480
SCREEN_W, SCREEN_H = GRID_W * TILE_SIZE, GRID_H * TILE_SIZE + 64  # extra HUD space
FPS = 60
TIME_LIMIT_SEC = 90
TREASURE_MIN_COUNT = 3

# Probabilities
WEIGHTS = {
    "nothing": 80,
    "treasure": 8,
    "water": 5,
    "break": 4,
    "rock": 3,
}

AXE_REPAIR_COST = 2  # how many points a new axe costs when it breaks
# how many additional blocks flood when water is uncovered
FLOOD_MIN, FLOOD_MAX = 3, 7

# Colors
COLORS = {
    "bg": (18, 18, 22),
    "hud": (30, 30, 36),
    "text": (235, 235, 235),
    "text_dim": (180, 180, 190),
    "dirt": (90, 70, 50),
    "dirt_edge": (60, 45, 35),
    "floor": (40, 35, 30),
    "rock": (110, 110, 115),
    "water": (40, 110, 205),
    "gold": (240, 190, 15),
    "break": (220, 80, 80),
    "player": (210, 210, 220),
    "helmet": (200, 180, 40),
    "axe": (180, 180, 180),
    "axe_head": (220, 220, 230),
    "blocked": (60, 60, 60),
}

# Directions
DIRS = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0),
}
DIR_ORDER = ["UP", "RIGHT", "DOWN", "LEFT"]


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


# ----------------------------
# Block Sprite
# ----------------------------
class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, content, font):
        super().__init__()
        self.gx, self.gy = x, y
        self.content = content   # hidden content: nothing | treasure | water | break | rock
        self.revealed = False
        self.font = font
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(
            topleft=(x * TILE_SIZE, y * TILE_SIZE + 64))  # + HUD

        # Pre-render appearances
        self._img_unknown = self._render_unknown()
        self._img_floor = self._render_floor()
        self._img_rock = self._render_rock()
        self._img_treasure = self._render_treasure()
        self._img_break = self._render_break()
        self._img_water = self._render_water()

        self._sync_image()

    def _render_unknown(self):
        s = pygame.Surface((TILE_SIZE, TILE_SIZE))
        s.fill(COLORS["dirt"])
        pygame.draw.rect(s, COLORS["dirt_edge"], s.get_rect(), 2)
        for _ in range(6):
            px = random.randint(3, TILE_SIZE-4)
            py = random.randint(3, TILE_SIZE-4)
            s.set_at((px, py), (70, 55, 40))
        return s

    def _render_floor(self):
        s = pygame.Surface((TILE_SIZE, TILE_SIZE))
        s.fill(COLORS["floor"])
        pygame.draw.rect(s, (55, 50, 45), s.get_rect(), 1)
        return s

    def _render_rock(self):
        s = pygame.Surface((TILE_SIZE, TILE_SIZE))
        s.fill(COLORS["rock"])
        for _ in range(3):
            x1, y1 = random.randint(
                4, TILE_SIZE-4), random.randint(4, TILE_SIZE-4)
            x2, y2 = clamp(x1 + random.randint(-8, 8), 0, TILE_SIZE -
                           1), clamp(y1 + random.randint(-8, 8), 0, TILE_SIZE-1)
            pygame.draw.line(s, (90, 90, 95), (x1, y1), (x2, y2), 2)
        pygame.draw.rect(s, (80, 80, 85), s.get_rect(), 2)
        return s

    def _render_treasure(self):
        s = self._render_floor().copy()
        for r in range(3, 7):
            cx = TILE_SIZE//2 + random.randint(-4, 4)
            cy = TILE_SIZE//2 + random.randint(-3, 3)
            pygame.draw.circle(s, COLORS["gold"], (cx, cy), r)
            pygame.draw.circle(s, (255, 235, 60), (cx-1, cy-1), max(1, r-2))
        return s

    def _render_break(self):
        s = self._render_floor().copy()
        pygame.draw.line(s, COLORS["break"],
                         (6, TILE_SIZE-6), (TILE_SIZE-8, 6), 5)
        pygame.draw.line(s, COLORS["break"],
                         (TILE_SIZE-10, 6), (TILE_SIZE-4, 12), 3)
        pygame.draw.line(s, COLORS["break"],
                         (TILE_SIZE-10, 6), (TILE_SIZE-4, 2), 3)
        return s

    def _render_water(self):
        s = pygame.Surface((TILE_SIZE, TILE_SIZE))
        s.fill(COLORS["water"])
        for r in range(4, TILE_SIZE//2, 4):
            pygame.draw.circle(s, (60, 140, 230),
                               (TILE_SIZE//2, TILE_SIZE//2), r, 1)
        return s

    def _sync_image(self):
        if not self.revealed:
            self.image = self._img_unknown
        else:
            if self.content == "nothing":
                self.image = self._img_floor
            elif self.content == "treasure":
                self.image = self._img_treasure
            elif self.content == "break":
                self.image = self._img_break
            elif self.content == "water":
                self.image = self._img_water
            elif self.content == "rock":
                self.image = self._img_rock
            else:
                self.image = self._img_floor

    def reveal(self):
        self.revealed = True
        self._sync_image()

    def is_passable(self):
        if not self.revealed:
            return False
        if self.content in ("water", "rock"):
            return False
        return True

    def is_impenetrable(self):
        return self.content == "rock"

    def set_as_water(self):
        self.content = "water"
        self.revealed = True
        self._sync_image()


# ----------------------------
# Player Sprite (with axe animation)
# ----------------------------
class Player(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y):
        super().__init__()
        self.gx, self.gy = start_x, start_y
        self.facing = "RIGHT"
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        self.rect = self.image.get_rect(
            topleft=(self.gx * TILE_SIZE, self.gy * TILE_SIZE + 64))
        self._base_player = self._render_base_player()
        self.swinging = False
        self.swing_timer = 0.0
        self.swing_duration = 0.20  # seconds per swing

    def _render_base_player(self):
        s = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        pygame.draw.rect(
            s, COLORS["player"], (8, 6, TILE_SIZE-16, TILE_SIZE-12), border_radius=6)
        pygame.draw.rect(s, COLORS["helmet"],
                         (8, 2, TILE_SIZE-16, 10), border_radius=4)
        return s

    def _render_axe(self, angle_deg):
        axe_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        cx, cy = TILE_SIZE//2 + 2, TILE_SIZE//2
        pygame.draw.line(
            axe_surface, COLORS["axe"], (cx-10, cy+10), (cx+8, cy-8), 4)
        pygame.draw.polygon(axe_surface, COLORS["axe_head"], [
                            (cx+6, cy-12), (cx+14, cy-4), (cx+2, cy-2)])
        rotated = pygame.transform.rotate(axe_surface, angle_deg)
        return rotated

    def start_swing(self):
        self.swinging = True
        self.swing_timer = 0.0

    def update(self, dt):
        self.image = self._base_player.copy()
        if self.swinging:
            self.swing_timer += dt
            t = clamp(self.swing_timer / self.swing_duration, 0.0, 1.0)
            base_angle = -60 + 90 * t
            facing_angle = {"UP": 0, "RIGHT": -90,
                            "DOWN": 180, "LEFT": 90}[self.facing]
            axe_img = self._render_axe(base_angle + facing_angle)
            r = axe_img.get_rect(center=(TILE_SIZE//2, TILE_SIZE//2))
            self.image.blit(axe_img, r)
            if self.swing_timer >= self.swing_duration:
                self.swinging = False

        self.rect.topleft = (self.gx * TILE_SIZE, self.gy * TILE_SIZE + 64)

    def try_move(self, dx, dy, board):
        nx, ny = self.gx + dx, self.gy + dy
        if 0 <= nx < GRID_W and 0 <= ny < GRID_H:
            target = board[ny][nx]
            if target.is_passable():
                self.gx, self.gy = nx, ny

    def set_facing_by_vec(self, dx, dy):
        if dx == 0 and dy == -1:
            self.facing = "UP"
        elif dx == 0 and dy == 1:
            self.facing = "DOWN"
        elif dx == -1 and dy == 0:
            self.facing = "LEFT"
        elif dx == 1 and dy == 0:
            self.facing = "RIGHT"


# ----------------------------
# HUD Sprites
# ----------------------------
class ScoreSprite(pygame.sprite.Sprite):
    def __init__(self, font):
        super().__init__()
        self.font = font
        self.score = 0
        self.image = pygame.Surface((SCREEN_W//2, 64))
        self.rect = self.image.get_rect(topleft=(0, 0))
        self._render()

    def set(self, score):
        self.score = score
        self._render()

    def _render(self):
        self.image.fill(COLORS["hud"])
        text = self.font.render(
            f"Treasure: {self.score}", True, COLORS["text"])
        self.image.blit(text, (12, 18))


class TimerSprite(pygame.sprite.Sprite):
    def __init__(self, font, duration_sec):
        super().__init__()
        self.font = font
        self.duration = duration_sec
        self.remaining = duration_sec
        self.image = pygame.Surface((SCREEN_W//2, 64))
        self.rect = self.image.get_rect(topleft=(SCREEN_W//2, 0))
        self._render()

    def update_time(self, dt):
        self.remaining = max(0.0, self.remaining - dt)
        self._render()

    def _render(self):
        self.image.fill(COLORS["hud"])
        t = int(math.ceil(self.remaining))
        text = self.font.render(
            f"Time: {t}s", True, COLORS["text"] if t > 10 else (255, 120, 120))
        self.image.blit(text, (SCREEN_W//2 - text.get_width() - 12, 18))

    @property
    def expired(self):
        return self.remaining <= 0.0


# ----------------------------
# Game Setup & Utilities
# ----------------------------
def build_weighted_bag(weights):
    bag = []
    for k, w in weights.items():
        bag.extend([k] * w)
    return bag


def generate_board(font):
    bag = build_weighted_bag(WEIGHTS)

    board = []
    positions = [(x, y) for y in range(GRID_H) for x in range(GRID_W)]

    for y in range(GRID_H):
        row = []
        for x in range(GRID_W):
            if x == 0 or y == 0 or x == GRID_W-1 or y == GRID_H-1:
                content = "rock"
            else:
                content = random.choice(bag)
            row.append(Block(x, y, content, font))
        board.append(row)

    inner_positions = [(x, y) for (x, y) in positions if 1 <=
                       x < GRID_W-1 and 1 <= y < GRID_H-1]
    treasure_spots = random.sample(inner_positions, k=TREASURE_MIN_COUNT)
    for (tx, ty) in treasure_spots:
        board[ty][tx].content = "treasure"
        board[ty][tx]._sync_image()

    return board


def reveal_start_area(board, start):
    sx, sy = start
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            x, y = sx + dx, sy + dy
            if 0 <= x < GRID_W and 0 <= y < GRID_H:
                b = board[y][x]
                if b.content != "rock":
                    b.reveal()
                    if b.content == "water":
                        b.content = "nothing"
                        b._sync_image()


def neighbors4(x, y):
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        yield x+dx, y+dy


def flood_water(board, srcx, srcy):
    target_n = random.randint(FLOOD_MIN, FLOOD_MAX)
    q = deque()
    q.append((srcx, srcy))
    visited = set([(srcx, srcy)])
    flooded = 0

    while q and flooded < target_n:
        x, y = q.popleft()
        for nx, ny in neighbors4(x, y):
            if 0 <= nx < GRID_W and 0 <= ny < GRID_H:
                b = board[ny][nx]
                if (nx, ny) not in visited and b.content != "rock" and b.content != "water":
                    b.set_as_water()
                    flooded += 1
                    visited.add((nx, ny))
                    q.append((nx, ny))
                    if flooded >= target_n:
                        break


def draw_grid_overlay(screen):
    overlay = pygame.Surface((SCREEN_W, SCREEN_H-64), pygame.SRCALPHA)
    for x in range(0, SCREEN_W, TILE_SIZE):
        pygame.draw.line(overlay, (0, 0, 0, 40), (x, 0), (x, SCREEN_H-64))
    for y in range(0, SCREEN_H-64, TILE_SIZE):
        pygame.draw.line(overlay, (0, 0, 0, 40), (0, y), (SCREEN_W, y))
    screen.blit(overlay, (0, 64))


def main():
    pygame.init()
    pygame.display.set_caption("Mine Digger: Treasure Rush")
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("consolas", 24)

    def new_game():
        board = generate_board(font)
        start = (1, 1)
        reveal_start_area(board, start)

        all_sprites = pygame.sprite.Group()
        blocks_group = pygame.sprite.Group()
        hud_group = pygame.sprite.Group()
        player_group = pygame.sprite.GroupSingle()

        for row in board:
            for b in row:
                blocks_group.add(b)
                all_sprites.add(b)

        player = Player(*start)
        player_group.add(player)
        all_sprites.add(player)

        score_sprite = ScoreSprite(font)
        timer_sprite = TimerSprite(font, TIME_LIMIT_SEC)
        hud_group.add(score_sprite, timer_sprite)
        all_sprites.add(score_sprite, timer_sprite)

        score = 0

        return {
            "board": board,
            "player": player,
            "all_sprites": all_sprites,
            "blocks_group": blocks_group,
            "hud_group": hud_group,
            "score_sprite": score_sprite,
            "timer_sprite": timer_sprite,
            "score": score,
            "game_over": False,
        }

    state = new_game()

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if state["game_over"]:
                    if event.key == pygame.K_r:
                        state = new_game()
                        continue
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                        continue

                if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                    dx, dy = 0, 0
                    if event.key == pygame.K_UP:
                        dy = -1
                    elif event.key == pygame.K_DOWN:
                        dy = 1
                    elif event.key == pygame.K_LEFT:
                        dx = -1
                    elif event.key == pygame.K_RIGHT:
                        dx = 1

                    state["player"].set_facing_by_vec(dx, dy)

                    oldx, oldy = state["player"].gx, state["player"].gy
                    state["player"].try_move(dx, dy, state["board"])

                    if (state["player"].gx, state["player"].gy) != (oldx, oldy):
                        cur = state["board"][state["player"].gy][state["player"].gx]
                        if cur.revealed and cur.content == "treasure":
                            state["score"] += 1
                            cur.content = "nothing"
                            cur._sync_image()

                elif event.key == pygame.K_SPACE and not state["game_over"]:
                    px, py = state["player"].gx, state["player"].gy
                    dx, dy = DIRS[state["player"].facing]
                    tx, ty = px + dx, py + dy
                    if 0 <= tx < GRID_W and 0 <= ty < GRID_H:
                        target = state["board"][ty][tx]
                        if not target.revealed:
                            target.reveal()
                            if target.content == "treasure":
                                pass  # now visible; collect on step
                            elif target.content == "break":
                                state["score"] -= AXE_REPAIR_COST
                                target.content = "nothing"
                                target._sync_image()
                            elif target.content == "water":
                                flood_water(state["board"], tx, ty)
                        state["player"].start_swing()

        if not state["game_over"]:
            state["player"].update(dt)
            state["timer_sprite"].update_time(dt)
            state["score_sprite"].set(state["score"])

            if state["timer_sprite"].expired:
                state["game_over"] = True

        screen.fill(COLORS["bg"])
        state["hud_group"].draw(screen)
        state["blocks_group"].draw(screen)
        draw_grid_overlay(screen)
        state["player"].draw(screen)

        if state["game_over"]:
            overlay = pygame.Surface((SCREEN_W, SCREEN_H-64), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 64))
            big = pygame.font.SysFont("consolas", 36)
            small = pygame.font.SysFont("consolas", 22)
            msg1 = big.render(
                f"Time's Up! Treasure: {state['score']}", True, (255, 230, 180))
            msg2 = small.render(
                "Press R to restart or ESC to quit", True, COLORS["text_dim"])
            screen.blit(
                msg1, (SCREEN_W//2 - msg1.get_width()//2, SCREEN_H//2 - 40))
            screen.blit(
                msg2, (SCREEN_W//2 - msg2.get_width()//2, SCREEN_H//2 + 6))

        pygame.display.flip()

    pygame.quit()


def _player_draw(self, screen):
    screen.blit(self.image, self.rect)


Player.draw = _player_draw


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Error:", e)
        pygame.quit()
        sys.exit(1)

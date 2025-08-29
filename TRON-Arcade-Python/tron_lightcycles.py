import pygame
import sys
import random
from dataclasses import dataclass, field
from config import *

# ---------------- Player ----------------
@dataclass
class Player:
    name: str
    color: tuple
    head_color: tuple
    start_pos: tuple
    start_dir: tuple
    controls: dict
    is_cpu: bool = False

    pos: tuple = field(init=False)
    direction: tuple = field(init=False)
    alive: bool = field(init=False, default=True)
    trail: set = field(init=False, default_factory=set)

    def reset(self):
        self.pos = self.start_pos
        self.direction = self.start_dir
        self.alive = True
        self.trail = set([self.start_pos])

    def handle_input(self, keys):
        if self.is_cpu or not self.alive:
            return
        if keys[self.controls['up']] and self.direction != DOWN:
            self.direction = UP
        elif keys[self.controls['down']] and self.direction != UP:
            self.direction = DOWN
        elif keys[self.controls['left']] and self.direction != RIGHT:
            self.direction = LEFT
        elif keys[self.controls['right']] and self.direction != LEFT:
            self.direction = RIGHT

    def cpu_turn(self, occupied):
        if not self.is_cpu or not self.alive:
            return
        options = [self.direction]
        idx = DIRS.index(self.direction)
        options.append(DIRS[(idx - 1) % 4])  # left
        options.append(DIRS[(idx + 1) % 4])  # right
        options.append(DIRS[(idx + 2) % 4])  # reverse
        for d in options:
            nx, ny = self.pos[0] + d[0], self.pos[1] + d[1]
            if 0 <= nx < GRID_W and 0 <= ny < GRID_H and (nx, ny) not in occupied:
                self.direction = d
                return

    def step(self, occupied):
        if not self.alive:
            return None
        new_pos = (self.pos[0] + self.direction[0], self.pos[1] + self.direction[1])
        x, y = new_pos
        if x < 0 or x >= GRID_W or y < 0 or y >= GRID_H or new_pos in occupied:
            self.alive = False
            return None
        self.pos = new_pos
        self.trail.add(self.pos)
        return new_pos

# ---------------- Game ----------------
class TronGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Tron Lightcycles — Pygame")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 20)
        self.bigfont = pygame.font.SysFont("consolas", 42, bold=True)

        self.grid_visible = True
        self.tps = TICKS_PER_SECOND
        self.tick_accum = 0.0
        self.paused = False
        self.round_over = False
        self.round_end_timer = 0.0

        mid_y = GRID_H // 2

        # Jogadores
        self.p1 = Player("P1", P1_COLOR, P1_HEAD, (GRID_W // 4, mid_y), RIGHT, P1_CONTROLS, is_cpu=True)
        self.p2 = Player("P2", P2_COLOR, P2_HEAD, (GRID_W - GRID_W // 4 - 1, mid_y), LEFT, P2_CONTROLS)

        self.score = {"P1": 0, "P2": 0}
        self.reset_round(hard=True)

    def reset_round(self, hard=False):
        self.occupied = set()
        self.p1.reset()
        self.p2.reset()
        self.occupied |= self.p1.trail
        self.occupied |= self.p2.trail
        self.round_over = False
        self.round_end_timer = 0.0
        if hard:
            self.score = {"P1": 0, "P2": 0}

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    self.reset_round(hard=True)
                if event.key == pygame.K_p:
                    self.paused = not self.paused
                if event.key == pygame.K_g:
                    self.grid_visible = not self.grid_visible
                if event.key in (pygame.K_PLUS, pygame.K_EQUALS):
                    self.tps = min(60, self.tps + 1)
                if event.key == pygame.K_MINUS:
                    self.tps = max(4, self.tps - 1)
                if event.key == pygame.K_b:
                    self.p2.is_cpu = not self.p2.is_cpu

        keys = pygame.key.get_pressed()
        self.p1.handle_input(keys)
        self.p2.handle_input(keys)

    def update(self, dt):
        if self.paused:
            return
        if self.round_over:
            self.round_end_timer += dt
            if self.round_end_timer >= 1.2:
                self.reset_round(hard=False)
            return

        self.p1.cpu_turn(self.occupied)
        self.p2.cpu_turn(self.occupied)

        self.tick_accum += dt
        step_time = 1.0 / float(self.tps)
        while self.tick_accum >= step_time and not self.round_over:
            self.tick_accum -= step_time
            new_positions = {}
            for pl in (self.p1, self.p2):
                np = pl.step(self.occupied)
                new_positions[pl.name] = np

            if self.p1.alive and self.p2.alive:
                if new_positions['P1'] == new_positions['P2'] and new_positions['P1'] is not None:
                    self.p1.alive = False
                    self.p2.alive = False

            for np in new_positions.values():
                if np is not None:
                    self.occupied.add(np)

            if not self.p1.alive and not self.p2.alive:
                self.round_over = True
            elif not self.p1.alive:
                self.score['P2'] += 1
                self.round_over = True
            elif not self.p2.alive:
                self.score['P1'] += 1
                self.round_over = True

    def draw_grid(self):
        if not self.grid_visible:
            return
        for x in range(GRID_W + 1):
            pygame.draw.line(self.screen, GRID_COLOR,
                             (MARGIN + x * CELL_SIZE, MARGIN),
                             (MARGIN + x * CELL_SIZE, MARGIN + GRID_H * CELL_SIZE), 1)
        for y in range(GRID_H + 1):
            pygame.draw.line(self.screen, GRID_COLOR,
                             (MARGIN, MARGIN + y * CELL_SIZE),
                             (MARGIN + GRID_W * CELL_SIZE, MARGIN + y * CELL_SIZE), 1)

    def draw_trails(self, player: Player):
        for (x, y) in player.trail:
            rect = pygame.Rect(MARGIN + x * CELL_SIZE, MARGIN + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.screen, player.color, rect)
        if player.alive:
            x, y = player.pos
            rect = pygame.Rect(MARGIN + x * CELL_SIZE, MARGIN + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.screen, player.head_color, rect)

    def draw_hud(self):
        tips = [
            f"P1 (CPU)  {self.score['P1']}",
            f"P2 (Arrows)  {self.score['P2']}",
            f"Speed: {self.tps} tps",
            "[P]ause  [R]eset  [G]rid  [B]ot  +/- speed  Esc=Quit",
        ]
        x = 10
        y = 8
        for t in tips:
            img = self.font.render(t, True, TEXT_COLOR)
            self.screen.blit(img, (x, y))
            y += img.get_height() + 2

        if self.paused:
            text = self.bigfont.render("PAUSED", True, TEXT_COLOR)
            self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 10))

        if self.round_over:
            msg = "DRAW" if self.p1.alive == self.p2.alive else ("P1 SCORES" if self.p1.alive else "P2 SCORES")
            text = self.bigfont.render(msg, True, TEXT_COLOR)
            self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

    def draw(self):
        self.screen.fill(BG_COLOR)
        self.draw_grid()
        self.draw_trails(self.p1)
        self.draw_trails(self.p2)
        self.draw_hud()
        pygame.display.flip()

    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000.0
            self.handle_events()
            self.update(dt)
            self.draw()


if __name__ == "__main__":
    TronGame().run()

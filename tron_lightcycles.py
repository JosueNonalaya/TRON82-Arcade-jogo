import pygame
import sys
import random
#from dataclasses import dataclass, field
from config import *

from entities.Player import Player
from entities.LightCycle import LightCycle
from game.board import Board


# ---------------- Game ----------------
class TronGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Tron Lightcycles — Pygame")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 20)
        self.bigfont = pygame.font.SysFont("consolas", 42, bold=True)

        #ADICIONANDO A CLASSE BOARD
        self.board = Board(GRID_W, GRID_H)

        self.grid_visible = True
        self.tps = TICKS_PER_SECOND
        self.tick_accum = 0.0
        self.paused = False
        self.round_over = False
        self.round_end_timer = 0.0

        mid_y = GRID_H // 2

        # CRIANDO AS MOTOS
        p1_lightcycle = LightCycle(P1_COLOR, P1_HEAD,(GRID_W // 4,mid_y), RIGHT)
        p2_lightcycle = LightCycle(P2_COLOR, P2_HEAD,(GRID_W - GRID_W // 4 - 1, mid_y), LEFT)

        # CRIANDO OS JOGADORES
        self.p1 = Player("P1", p1_lightcycle, None)
        self.p2 = Player("P2", p2_lightcycle, None)


        self.score = {"P1": 0, "P2": 0}
        self.reset_round(hard=True)

    def reset_round(self, hard=False):
        self.board.limpar()

        self.p1.lightcycle.reinicio()
        self.p2.lightcycle.reinicio()

        self.board.ocupar(self.p1.lightcycle.posicao)
        self.board.ocupar(self.p2.lightcycle.posicao)

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
        keys = pygame.key.get_pressed()

        if self.p2.lightcycle.vivo:
            if keys[P2_CONTROLS['up']] and self.p2.lightcycle.direcao != DOWN:
                self.p2.lightcycle.direcao = UP

            elif keys[P2_CONTROLS['down']] and self.p2.lightcycle.direcao != UP:
                self.p2.lightcycle.direcao = DOWN

            elif keys[P2_CONTROLS['left']] and self.p2.lightcycle.direcao != RIGHT:
                self.p2.lightcycle.direcao = LEFT

            elif keys[P2_CONTROLS['right']] and self.p2.lightcycle.direcao != LEFT:
                self.p2.lightcycle.direcao = RIGHT

    def update(self, dt):
        if self.paused:
            return

        if self.round_over:
            self.round_end_timer += dt
            if self.round_end_timer >= 1.2:
                self.reset_round(hard=False)
            return

        self.tick_accum += dt
        step_time = 1.0 / float(self.tps)
        while self.tick_accum >= step_time and not self.round_over:
            self.tick_accum -= step_time

            new_positions = {}

            for pl in (self.p1, self.p2):
                moveu = pl.lightcycle.mover(self.board)

                if moveu:
                    new_positions[pl.nome] = pl.lightcycle.posicao
                else:
                    new_positions[pl.nome] = None


            if self.p1.lightcycle.vivo and self.p2.lightcycle.vivo:
                if new_positions['P1'] == new_positions['P2'] and new_positions['P1'] is not None:
                    self.p1.lightcycle.vivo = False
                    self.p2.lightcycle.vivo = False

            if not self.p1.lightcycle.vivo and not self.p2.lightcycle.vivo:
                self.round_over = True
            elif not self.p1.lightcycle.vivo:
                self.score['P2'] += 1
                self.round_over = True
            elif not self.p2.lightcycle.vivo:
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

    def draw_trails(self, player):
        for (x, y) in player.lightcycle.rastro:
            rect = pygame.Rect(MARGIN + x * CELL_SIZE, MARGIN + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.screen, player.lightcycle.cor, rect)
        if player.lightcycle.vivo:
            x, y = player.lightcycle.posicao
            rect = pygame.Rect(MARGIN + x * CELL_SIZE, MARGIN + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.screen, player.lightcycle.cabeca_cor, rect)

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
            msg = "DRAW" if self.p1.lightcycle.vivo == self.p2.lightcycle.vivo else ("P1 SCORES" if self.p1.lightcycle.vivo else "P2 SCORES")
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

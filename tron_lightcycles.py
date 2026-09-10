import sys
from config.config import *

from infraestrutura.renderizado import Renderizado
from controllers.CPU import CPU
from controllers.Humano import Humano
from entities.Player import Player
from entities.LightCycle import LightCycle
from game.board import Board


# ---------------- Game ----------------
class TronGame:
    def __init__(self):
        #Inicializando PYGAME
        pygame.init()

        #Config janela jogo
        pygame.display.set_caption("Tron Lightcycles — Pygame")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.renderer = Renderizado(self.screen)
        self.clock = pygame.time.Clock()

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
        self.p1 = Player("P1", p1_lightcycle, CPU())
        self.p2 = Player("P2", p2_lightcycle, Humano(P2_CONTROLS))


        self.score = {"P1": 0, "P2": 0}
        self.reset_round(hard=True)

    #REINICIA PARTIDA
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

    # EVENTOS GERAIS CONTROLE: ESC, R, P, G, +/-, QUIT
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

        keys = pygame.key.get_pressed()
        self.p2.controller.controlar(self.p2.lightcycle, keys)

    # COORDENA O LOOP LOGICA PARTIDA
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

            self.p1.controller.controlar(
                self.p1.lightcycle,
                self.board
            )

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

    #DELEGA O RENDERIZADO
    def draw(self):
        self.renderer.renderizar(
            self.grid_visible,
            self.score,
            self.tps,
            self.paused,
            self.round_over,
            self.p1,
            self.p2
        )

    #LOOP PRINCIPAL
    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000.0
            self.handle_events()
            self.update(dt)
            self.draw()


if __name__ == "__main__":
    TronGame().run()

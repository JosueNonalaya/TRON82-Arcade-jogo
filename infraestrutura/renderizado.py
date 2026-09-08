from config.config import *

class Renderizado:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('consolas', 20)
        self.bigfont = pygame.font.SysFont('consolas', 42, bold=True)

    def draw_grid(self, grid_visible):
        if not grid_visible:
            return

        for x in range(GRID_W + 1):
            pygame.draw.line(
                self.screen,
                GRID_COLOR,
                (MARGIN + x * CELL_SIZE, MARGIN),
                (MARGIN + x * CELL_SIZE, MARGIN + GRID_H * CELL_SIZE),
                1
            )

        for y in range(GRID_H + 1):
            pygame.draw.line(
                self.screen,
                GRID_COLOR,
                (MARGIN, MARGIN + y * CELL_SIZE),
                (MARGIN + GRID_W * CELL_SIZE, MARGIN + y * CELL_SIZE),
                1
            )

    def draw_trails(self, player):
        for (x, y) in player.lightcycle.rastro:
            rect = pygame.Rect(
                MARGIN + x * CELL_SIZE,
                MARGIN + y * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
            pygame.draw.rect(
                self.screen,
                player.lightcycle.cor,
                rect
            )

        if player.lightcycle.vivo:
            x, y = player.lightcycle.posicao

            rect = pygame.Rect(
                MARGIN + x * CELL_SIZE,
                MARGIN + y * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )

            pygame.draw.rect(
                self.screen,
                player.lightcycle.cabeca_cor,
                rect
            )

    def draw_hud(self, score, tps, paused, round_over, p1, p2):
        tips = [
            f"P1 (CPU)  {score['P1']}",
            f"P2 (Arrows)  {score['P2']}",
            f"Speed: {tps} tps",
            "[P]ause  [R]eset  [G]rid  +/- speed  Esc=Quit",
        ]
        x = 10
        y = 8
        for t in tips:
            img = self.font.render(t, True, TEXT_COLOR)
            self.screen.blit(img, (x, y))
            y += img.get_height() + 2

        if paused:
            text = self.bigfont.render("PAUSED", True, TEXT_COLOR)
            self.screen.blit(
                text,
                (
                    WIDTH // 2 - text.get_width() // 2,
                    10
                )
            )

        if round_over:
            msg = (
                "DRAW"
                if p1.lightcycle.vivo == p2.lightcycle.vivo
                else (
                    "P1 SCORES"
                    if p1.lightcycle.vivo
                    else "P2 SCORES"
                )
            )

            text = self.bigfont.render(msg, True, TEXT_COLOR)

            self.screen.blit(
                text,
                (
                    WIDTH // 2 - text.get_width() // 2,
                    HEIGHT // 2 - text.get_height() // 2
                )
            )

    def renderizar(self, grid_visible, score, tps, paused, round_over, p1, p2):
        self.screen.fill(BG_COLOR)

        self.draw_grid(grid_visible)
        self.draw_trails(p1)
        self.draw_trails(p2)
        self.draw_hud(score, tps, paused, round_over, p1, p2)

        pygame.display.flip()
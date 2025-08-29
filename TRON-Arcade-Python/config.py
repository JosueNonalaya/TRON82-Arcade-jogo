import pygame

# ---------------- Config ----------------
CELL_SIZE = 10
GRID_W = 96
GRID_H = 64
MARGIN = 0
WIDTH = GRID_W * CELL_SIZE + MARGIN * 2
HEIGHT = GRID_H * CELL_SIZE + MARGIN * 2
FPS = 60
TICKS_PER_SECOND = 18

BG_COLOR = (8, 10, 18)
GRID_COLOR = (22, 26, 38)
TEXT_COLOR = (235, 240, 255)

# Cores dos jogadores
# Jogador da esquerda (CPU)
P1_COLOR = (255, 80, 70)      # vermelho
P1_HEAD = (255, 120, 100)

# Jogador da direita (setas)
P2_COLOR = (80, 200, 255)     # azul
P2_HEAD = (130, 240, 255)

# Direções
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
DIRS = [UP, RIGHT, DOWN, LEFT]

# Controles
P1_CONTROLS = {
    'up': None,    # CPU não precisa de teclas
    'down': None,
    'left': None,
    'right': None
}

P2_CONTROLS = {
    'up': pygame.K_UP,
    'down': pygame.K_DOWN,
    'left': pygame.K_LEFT,
    'right': pygame.K_RIGHT
}

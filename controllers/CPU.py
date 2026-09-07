from config import *
from controllers.Controller import Controller

class CPU (Controller):
    def controlar(self, lightcycle, board):
        if not lightcycle.vivo:
            return

        opcoes = [lightcycle.direcao]

        indice = DIRS.index(lightcycle.direcao)

        opcoes.append(DIRS[(indice - 1) % 4])
        opcoes.append(DIRS[(indice + 1) % 4])
        opcoes.append(DIRS[(indice + 2) % 4])

        for direcao in opcoes:
            nova_x = lightcycle.posicao[0] + direcao[0]
            nova_y = lightcycle.posicao[1] + direcao[1]

            nova_posicao = (nova_x, nova_y)

            if (
                board.esta_dentro(nova_posicao)
                and not board.esta_ocupada(nova_posicao)
            ):
                lightcycle.direcao = direcao
                return
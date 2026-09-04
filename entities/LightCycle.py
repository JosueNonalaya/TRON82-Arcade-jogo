
class LightCycle:
    def __init__(self, cor, cabeca_cor, posicao_start, direcao_start):
        self.cor = cor
        self.cabeca_cor = cabeca_cor
        self.posicao_start = posicao_start
        self.direcao_start = direcao_start

        self.reinicio()

    def reinicio(self):
        self.posicao = self.posicao_start
        self.direcao = self.direcao_start
        self.vivo = True
        self.rastro = {self.posicao_start}

    def mover(self, tabuleiro):
        if not self.vivo:
            return False

        nova_posicao = (
            self.posicao[0] + self.direcao[0],
            self.posicao[1] + self.direcao[1]
        )

        if not tabuleiro.esta_dentro(nova_posicao):
            self.vivo = False
            return False

        if tabuleiro.esta_ocupada(nova_posicao):
            self.vivo = False
            return False

        self.posicao = nova_posicao
        self.rastro.add(self.posicao)
        tabuleiro.ocupar(self.posicao)

        return True
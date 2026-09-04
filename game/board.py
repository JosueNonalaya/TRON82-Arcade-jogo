
class Board:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.posicoes_ocupadas = set()

    def esta_dentro(self, posicao):
        x, y = posicao

        return(
            0 <= x <= self.largura
            and
            0 <= y <= self.altura
        )

    def esta_ocupada(self, posicao):
        return posicao in self.posicoes_ocupadas

    def ocupar(self, posicao):
        self.posicoes_ocupadas.add(posicao)

    def limpar(self):
        self.posicoes_ocupadas.clear()
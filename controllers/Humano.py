from controllers.Controller import Controller
from config import *

class Humano(Controller):
    def __init__(self, controles):
        self.controles = controles

    #Faz o controle do lightcycle atravez das entradas teclado
    def controlar(self, lightcycle, keys):
        if not lightcycle.vivo:
            return

        if keys[self.controles['up']] and lightcycle.direcao != DOWN:
            lightcycle.direcao = UP

        elif keys[self.controles['down']] and lightcycle.direcao != UP:
            lightcycle.direcao = DOWN

        elif keys[self.controles['left']] and lightcycle.direcao != RIGHT:
            lightcycle.direcao = LEFT

        elif keys[self.controles['right']] and lightcycle.direcao != LEFT:
            lightcycle.direcao = RIGHT
from Confi import *
from Niveis import Nivel
import pygame
from sys import exit
from os.path import join
from pytmx.util_pygame import load_pygame


class Game:
    def __init__(self):
        pygame.init()

        # Configuração da escala
        self.largura_upscale = largura * escala
        self.altura_upscale = altura * escala

        # Criação da janela de jogo
        self.display_surface = pygame.display.set_mode((self.largura_upscale, self.altura_upscale))
        pygame.display.set_caption(titulo)  # Título do jogo
        self.clock = pygame.time.Clock()

        # Superfície do jogo
        self.game_surface = pygame.Surface((largura, altura))

        # Carregar mapas
        self.tmx_maps = {
            0: load_pygame(join("C:\\Users\\nathanbc\\PycharmProjects\\pythonProject1\\Sprite2\\sem_título.tmx"))}
        self.current_stage = Nivel(self.tmx_maps[0])

    def run(self):
        while True:
            dt = self.clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # Executar lógica do nível
            self.current_stage.run(dt, self.game_surface)

            # Ampliar a superfície do jogo
            scaled_surface = pygame.transform.scale(self.game_surface, (self.largura_upscale, self.altura_upscale))

            # Desenhar a superfície ampliada na tela
            self.display_surface.blit(scaled_surface, (0, 0))

            # Atualizar a tela
            pygame.display.update()


if __name__ == '__main__':
    jogo = Game()
    jogo.run()

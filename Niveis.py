from Confi import *
from Sprites import Sprite
from MC import player
from Inimigo import Enemy


class Nivel:
    def __init__(self, tmx_map):
        # Remover self.display_surface, já que vamos usar a game_surface da classe Game
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.enemy_collision_sprites = pygame.sprite.Group()
        self.setup(tmx_map)

    def setup(self, tmx_map):
        for x, y, surf in tmx_map.get_layer_by_name("Chao").tiles():
            Sprite((x * tamanho_tile, y * tamanho_tile), surf, (self.all_sprites, self.collision_sprites))
        for obj in tmx_map.get_layer_by_name("Player"):
            if obj.name == "Passaro":
                player((obj.x, obj.y), self.all_sprites, self.collision_sprites)
        #for obj in tmx_map.get_layer_by_name("Inimigos"):
        #    if obj.name == "Enemy":
        #        player((obj.x, obj.y), self.all_sprites, self.enemy_collision_sprites)

    def run(self, dt, surface):
        self.all_sprites.update(dt)
        surface.fill("black")  # Limpar a superfície do jogo
        self.all_sprites.draw(surface)

import pygame.sprite
from random import choice
from Confi import *
class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos,groups, collision_sprites):
        super().__init__(groups)
        self.image = pygame.Surface((64, 64))  # 16,16
        self.image.fill("blue")
        self.rect = self.image.get_frect(topleft = pos)

        self.direction = choice((-1, 1))

        self.collision_rects = [sprite.rect for sprite in collision_sprites]
        self.vel = 100

    def update(self, dt):
      #  self.rect.x += self.direction * self.vel * dt
        floor_rect_right = pygame.FRect(self.rect.bottomright, (1, 1))
        floor_rect_left = pygame.FRect(self.rect.bottomleft, (-1, 1))
        wall_rect = pygame.FRect(self.rect.topleft + vector(-1, 0), (self.rect.width + 2, 1))

       # if floor_rect_right.collidelist(self.collision_rects) < 0 and self.direction > 0 or \
           ##     floor_rect_left.collidelist(self.collision_rects) < 0 and self.direction < 0 or \
           #     wall_rect.collidelist(self.collision_rects) != -1:
          #  self.direction *= -1





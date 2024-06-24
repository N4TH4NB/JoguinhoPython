from Confi import *
from timer import Timer


class player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.image = pygame.Surface((8, 8))  #16,16
        self.image.fill("pink")
        self.rect = self.image.get_frect(topleft=pos)
        self.old_rect = self.rect.copy()
        self.direction = vector()
        self.speed = 150
        self.gravity = 20
        self.dash_size = 5
        self.doublejump_check = False
        self.doublejump = 1
        self.jump = False
        self.climb = False
        self.dash = False
        #self.on_ground = False
        self.void = False
        self.jump_height = -4.5  #-15
        self.collision_sprites = collision_sprites
        self.on_ground = {"chao": False, "left": False, "right": False}
        print(self.collision_sprites)
        self.timers = {"wall jump": Timer(15), "wall climb": Timer(100)}

    def input(self):
        keys = pygame.key.get_pressed()
        key = pygame.key.get_just_pressed()
        input_vector = vector(0, 0)
        if not self.timers["wall jump"].active:

            # Direita
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:  #keys[pygame.K_RIGHT] or
                input_vector.x += 1

            # Esquerda
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                input_vector.x -= 1

            self.direction.x = input_vector.normalize().x if input_vector else input_vector.x

        # Pular
        if key[pygame.K_UP] or key[pygame.K_w] or key[pygame.K_SPACE]:  #keys[pygame.K_UP] or keys[pygame.K_w] or
            self.jump = True

        # Escalar
        if keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE]:  #keys[pygame.K_UP] or keys[pygame.K_w] or
            self.climb = True

        #Dash
        if keys[pygame.K_LSHIFT] or keys[pygame.K_LSHIFT] or keys[pygame.K_x]:
            self.dash = True

            #  self.direction.y = -5
        #  print("cima")
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:  #keys[pygame.K_DOWN] or
            input_vector.y += 1
        # print("baixo")

    def move(self, dt):  #data time
        #   self.rect.topleft += self.direction * self.speed * dt
        self.rect.x += self.direction.x * self.speed * dt
        self.collision("horizontal")

        #   if self.dash:
        #    self.direction.x = -200 if self.on_ground["left"] or self.on_ground["chao"] else 200

        if not self.on_ground["chao"] and any((self.on_ground["left"], self.on_ground["right"])) and not self.timers[
            "wall climb"].active:
            if self.climb:
                self.rect.y -= 30 * dt
                self.climb = False

            else:
                self.direction.y = 0
                self.rect.y += self.gravity / 10 * dt

        else:
            self.direction.y += self.gravity / 2 * dt
            self.rect.y += self.direction.y
            self.direction.y += self.gravity / 2 * dt
        self.collision("vertical")

        # if self.doublejump > 4 and not any((self.on_ground["right"], self.on_ground["left"], self.on_ground["chao"])) and not self.jump:
        #  if self.jump:
        #     self.doublejump = 5
        #   if self.doublejump >= 1:
        #                  self.direction.y = self.jump_height
        #                  self.doublejump = 0

        if self.jump:

            if self.on_ground["chao"]:
                self.doublejump += 3
                self.direction.y = self.jump_height
                self.timers["wall climb"].activate()



            elif any((self.on_ground["right"], self.on_ground["left"])) and not self.timers["wall climb"].active:
                self.doublejump += 3
                self.timers["wall jump"].activate()
                self.direction.y = self.jump_height
                self.direction.x = 1 if self.on_ground["left"] else -1

            #self.direction.x = 1 if self.on_ground["left"] or self.on_ground["right"] else -1

            #    self.doublejump = 17
            self.jump = False
        if self.dash:
            if self.on_ground["left"]:
                self.rect.x += self.dash_size * 3
            elif self.on_ground["right"]:
                self.rect.x -= self.dash_size * 3.9


            elif self.on_ground["chao"]:
                if self.old_rect.left > self.rect.x:
                    self.rect.x -= self.dash_size
                if self.old_rect.left < self.rect.x:
                    self.rect.x += self.dash_size
            else:
                if self.old_rect.left > self.rect.x:
                    self.rect.x -= self.dash_size
                if self.old_rect.left < self.rect.x:
                    self.rect.x += self.dash_size

            self.dash = False
        # print(self.direction.y)

    def die(self):
        if self.rect.x > 1280 or self.rect.y > 720 or self.rect.x < -5:
            self.rect.x = 100 #445
            self.rect.y = 100 #350

    def check_contact(self):
        chao_rect = pygame.Rect(self.rect.bottomleft, (self.rect.width, 2))  #w,h
        left_rect = pygame.Rect((self.rect.topleft + vector(-2, self.rect.height / 4)), (1, self.rect.width / 2))
        right_rect = pygame.Rect((self.rect.topright + vector(0, self.rect.height / 4)), (1, self.rect.width / 2))
        collide_rects = [sprite.rect for sprite in self.collision_sprites]
        self.on_ground["chao"] = True if chao_rect.collidelist(collide_rects) >= 0 else False
        self.on_ground["left"] = True if left_rect.collidelist(collide_rects) >= 0 else False
        self.on_ground["right"] = True if right_rect.collidelist(collide_rects) >= 0 else False

    def collision(self, axis):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if axis == "horizontal":
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:  #1. conferir se o lado esquerdo do player ta colidindo com o lado direito de algum objeto; 2. Confere a última posição do player
                        self.rect.left = sprite.rect.right
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:  #conferir se o lado direito do player ta colidindo com o lado esquerdo de algum objeto
                        self.rect.right = sprite.rect.left
                else:  #if axis == "vertical":
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                    self.direction.y = 0
                #else:

                #   pass

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.update_timers()
        self.input()
        self.move(dt)
        self.check_contact()
        self.die()
    #   print(self.timers["wall climb"].active)

    #   print(self.doublejump)

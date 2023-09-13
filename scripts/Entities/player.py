import random

import pygame

from scripts.Entities.entity import Entity
from scripts.utils import load_images, Animation


class Player(Entity):
    def __init__(self, game, pos):
        self.game= game
        self.pos = pos
        self.assets = {
            'idle': Animation(load_images('entities/character1/idle', True), img_dur=5),
            'run': Animation(load_images('entities/character1/run', True), img_dur=7),
            'jump': Animation(load_images('entities/character1/j_down', True), img_dur=10, loop=True),
            'attack_1': Animation(load_images('entities/character1/1_atk', True), img_dur=5, loop=True),
            'attack_2': Animation(load_images('entities/character1/2_atk', True), img_dur=5, loop=True),
            'attack_3': Animation(load_images('entities/character1/3_atk', True), img_dur=5, loop=True),
            'defend': Animation(load_images('entities/character1/defend', True), img_dur=10, loop=False),
        }
        self.current_animation = 'idle'
        self.mask = pygame.mask.from_surface(self.assets[self.current_animation].img())
        self.size = (self.assets[self.current_animation].img().get_width(), self.assets[self.current_animation].img().get_height())
        super().__init__(self.game, self.pos, self.size, self.assets, self.current_animation)

        self.is_fighting = False

        self.is_attacking = False
        self.attack_number = 1
        self.attack_cooldown_counter = 0
        self.ATTACK_COOLDOWN_TIMER = self.assets["attack_"+str(self.attack_number)].duration()

    def passive(self):
        pass

    def attack(self):
        if not self.is_jumping and self.attack_cooldown_counter == 0:
            self.attack_number = random.randint(1, 3)
            self.ATTACK_COOLDOWN_TIMER = self.assets["attack_" + str(self.attack_number)].duration()
            self.attack_cooldown_counter = -self.ATTACK_COOLDOWN_TIMER
            self.is_attacking = True
            self.is_fighting = True

    def update_attack(self):
        if self.attack_cooldown_counter <= 0:
            self.attack_cooldown_counter = min(0, self.attack_cooldown_counter + 1)
            if self.attack_cooldown_counter == 0:
                self.is_attacking = False
                self.is_fighting = False
                self.assets["attack_"+str(self.attack_number)].reset()

    def defend(self):
        pass

    def ultimate(self):
        pass

    def handle_animations(self):
        if self.move[0] != 0:
            if self.move[0] < 0:
                self.facing_left = True
            else:
                self.facing_left = False
            self.current_animation = "run"
        else:
            self.current_animation = "idle"

        if self.is_jumping or abs(self.velocity[1]) > 1:
            self.current_animation = "jump"

        if self.is_fighting and self.is_attacking and not self.is_jumping:
            self.current_animation = "attack_"+str(self.attack_number)

    def update(self):
        #handle_animations get called here!
        self.update_attack()
        super().update()

    def render(self, surf, offset=(0, 0)):
        self.mask = pygame.mask.from_surface(self.assets[self.current_animation].img())
        if self.facing_left and "attack" in self.current_animation:
            self.assets[self.current_animation].update()
            surf.blit(pygame.transform.flip(self.assets[self.current_animation].img(), self.facing_left, False),
                      (self.pos[0] - offset[0] - self.assets[self.current_animation].img().get_width()//2, self.pos[1] - offset[1]))
        else:
            super().render(surf, offset)

        # surf.blit(pygame.transform.flip(self.mask.to_surface(), self.facing_left, False),
        #           (self.pos[0] - offset[0] ,
        #            self.pos[1] - offset[1]))




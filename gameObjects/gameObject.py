#
# gameObject.py
#
# Copyright (C)2011 Julian Ceipek and Patrick Varin
#
# Redistribution is permitted under the BSD license.  See LICENSE for details.
#

import pygame

class GameObject(pygame.sprite.Sprite):

    def __init__(self, image, parent, pos=(0,0), vel=(0,0)):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()
        self.rect.center = int(pos[0]), int(pos[1])
        self.position = pos
        self.velocity = vel
        self.parent = parent
        self.acceleration = (0,0)

    def move(self, delta):
        self.position = self.position[0]+delta[0], self.position[1]+delta[1]
        self.rect.center = int(self.position[0]), int(self.position[1])

    def moveTo(self, pos):
        self.position = pos
        self.rect.center = int(pos[0]), int(pos[1])

    def draw(self, surf):
        surf.blit(self.image, self.rect)

    def testMaskCollision(self, spriteGroup):
        if spriteGroup:
            return pygame.sprite.spritecollide(self, spriteGroup,
                                           0, pygame.sprite.collide_mask)
        else:
            return []

    def update(self, *args):
        gameTime, frameTime = args[:2]
        self.velocity = (frameTime*self.acceleration[0]+self.velocity[0],
                        frameTime*self.acceleration[1]+self.velocity[1])
        self.position = (frameTime*self.velocity[0]+self.position[0],
                        frameTime*self.velocity[1]+self.position[1])
        self.moveTo(self.position)



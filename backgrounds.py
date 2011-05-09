#
# backgrounds.py
#
# Copyright (C)2011 Julian Ceipek and Patrick Varin
#
# Redistribution is permitted under the BSD license.  See LICENSE for details.
#

import pygame
from engine.background import Background
from engine.functions import pathJoin
from gameObjects.gameObject import GameObject

class ScrollingCodeBackground(Background):
    def __init__(self):
        CodeObject.textCache = self.textCache
        CodeObject.resolution = self.resolution
        bg = pygame.sprite.Group()

        f = open("old/mindRush.py")
        CodeObject.specialText = f.readlines()
        CodeObject.maxCount = len(CodeObject.specialText)
        CodeObject.count = 0
        f.close()

        self.nextCodeTime = 0

        Background.__init__(self, bg)

    def update(self, *args):
        gameScreen, gameTime, frameTime = args[:3]
        if gameTime > self.nextCodeTime:
            self.bg.add(CodeObject((0,0)+self.resolution, vel=(0,0.5), pos=(self.resolution[0]//2,0)))
            self.nextCodeTime = gameTime + 30
        Background.update(self, *args)

class CodeObject(GameObject):
    def __init__(self, screenBoundaries, pos=(200,0), vel=(0,0), scaleSize=0.3):
        pygame.sprite.Sprite.__init__(self)
        self.boundaries = screenBoundaries

        if CodeObject.count+1 >= CodeObject.maxCount:
            CodeObject.count = 0

        self.text = CodeObject.specialText[CodeObject.count].strip()
        CodeObject.count += 1

        self.fontname = pathJoin(('fonts','orbitron',
            'orbitron-black.ttf'))
        self.size = int(self.resolution[1]*(1/15.0))
        if scaleSize != None:
            self.size *= scaleSize
            self.size = int(self.size)
        self.color = (255,140,0)

        self.antialias = True

        self.image = self.textCache.getText(self.text,
                        self.fontname, self.size, self.color,
                        antialias=self.antialias)
        self.rect = self.image.get_rect()

        self.rect.center = int(pos[0]), int(pos[1])
        self.position = pos
        self.velocity = vel

    def update(self, *args):
        gameScreen, gameTime, frameTime = args[:3]
        self.position = (frameTime*self.velocity[0]+self.position[0],
                        frameTime*self.velocity[1]+self.position[1])
        self.moveTo(self.position)

        #kill when off-screen:
        if ((self.rect.topleft[0] < self.boundaries[0]) or
           (self.rect.topleft[0] + self.rect.width > self.boundaries[2]) or
           (self.rect.topleft[1] + self.rect.height > self.boundaries[3])):
            self.kill()

    def kill(self):
        self.textCache.clearText(self.text,
                        self.fontname, self.size, self.color,
                        antialias=self.antialias)
        GameObject.kill(self)
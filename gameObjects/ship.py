#
# ship.py
#
# Copyright (C)2011 Julian Ceipek and Patrick Varin
#
# Redistribution is permitted under the BSD license.  See LICENSE for details.
#

from gameObject import GameObject
from engine.functions import pathJoin

class Ship(GameObject):

    def __init__(self, parent, pos=(0,0), vel=(0,0), screenBoundaries=None):

        shipPath = pathJoin(('images','ship.png'))
        shipImage = self.imageCache.getImage(shipPath, colorkey='alpha', mask=True)

        GameObject.__init__(self, shipImage, parent, pos, vel)
        self.targetPosition = pos
        self.mask = self.imageCache.getMask(shipPath)
        self.screenBoundaries = screenBoundaries
        self.health = 100
        self.score = 0
        if screenBoundaries != None:
            self.minXPos = screenBoundaries[0] + self.rect.width/2
            self.maxXPos = screenBoundaries[2] - self.rect.width/2

    def update(self, *args):
        gameTime, frameTime = args[:2]
        speed = .006
        error = self.targetPosition[0]-self.position[0], self.targetPosition[1]-self.position[1]
        self.velocity = error[0]*speed, error[1]*speed

        #don't allow the ship to jump over the target position (applicable only at high speeds)
        nextPos = [frameTime*self.velocity[0]+self.position[0],
                        frameTime*self.velocity[1]+self.position[1]]
        nextError = self.targetPosition[0]-nextPos[0], self.targetPosition[1]-nextPos[1]
        if error[0]*nextError[0] < 0:
            nextPos[0] = self.targetPosition[0]
        if error[1]*nextError[1] < 0:
            nextPos[1] = self.targetPosition[1]
        self.position = nextPos

        #don't allow the ship off of the sides of the screen
        if self.screenBoundaries != None:
            if self.position[0] > self.maxXPos:
                self.position = self.maxXPos, self.position[1]
            elif self.position[0] < self.minXPos:
                self.position = self.minXPos, self.position[1]
        self.moveTo(self.position)
        
class TestShip(Ship):
    def __init__(self, *args, **kwargs):
        Ship.__init__(self, *args,**kwargs)
        self.stage = 0
        self.finished = False
    def update(self, *args):
        GameObject.update(self, *args)
        if (self.stage == 0 or self.stage == 2) and self.position[0] < self.minXPos:
            self.velocity = (-self.velocity[0], self.velocity[1])
            self.stage += 1
        elif (self.stage == 1 or self.stage == 3) and self.position[0] > self.maxXPos:
            self.stage += 1
            self.velocity = (-self.velocity[0], self.velocity[1])
        elif self.stage == 4 and self.position[0] < (self.minXPos + self.maxXPos)/2:
            self.stage += 1
            self.velocity = (0,0)
            self.finished = True

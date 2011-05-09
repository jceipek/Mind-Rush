#
# boulder.py
#
# Copyright (C)2011 Julian Ceipek and Patrick Varin
#
# Redistribution is permitted under the BSD license.  See LICENSE for details.
#

from gameObject import GameObject
from engine.functions import pathJoin

class Boulder(GameObject):

    def __init__(self, parent, pos=(0,0), vel=(0,0), screenBoundaries = None):
        boulderPath = pathJoin(('images','boulder.png'))
        boulderImage = self.imageCache.getImage(boulderPath, colorkey='alpha', mask=True)

        GameObject.__init__(self, boulderImage, parent, pos, vel)
        self.mask = self.imageCache.getMask(boulderPath)
        if screenBoundaries == None:
            raise Exception('Boulders must have screen boundaries')
        self.boundaries = screenBoundaries
        self.acceleration = (0,.001)
        self.damage = 5 #Damage done to ship when it hits
        self.value = 5 #How many points the boulder is worth


    def kill(self):
        GameObject.kill(self)
        #from random import randint
        from math import sin,cos
        for i in xrange(8):
            self.parent.addBoulderFragment(pos=self.position,
            vel=(cos((2*3.14159)/8.0*i),sin((2*3.14159)/8.0*i)),id=i)

    def update(self, *args):
        GameObject.update(self, *args)

        #bounce off of the walls

        if self.rect.topleft[0] < self.boundaries[0] or \
            self.rect.topleft[0] + self.rect.width > self.boundaries[2]:

            self.velocity = -self.velocity[0], self.velocity[1]

        #hit the ground
        if self.rect.topleft[1] + self.rect.height > self.boundaries[3]:

            self.parent.killBoulder(self)

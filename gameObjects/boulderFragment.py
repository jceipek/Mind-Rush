#
# boulderFragment.py
#
# Copyright (C)2011 Julian Ceipek and Patrick Varin
#
# Redistribution is permitted under the BSD license.  See LICENSE for details.
#

from gameObject import GameObject
from engine.functions import pathJoin

class BoulderFragment(GameObject):
    def __init__(self, parent, pos=(0,0), vel=(0,0), id=0, screenBoundaries = None):
        fragmentPath = pathJoin(('images','fragments','fragment'+str(id)+'.png'))
        fragmentImage = self.imageCache.getImage(fragmentPath, colorkey='alpha', mask=False)

        rect = self.imageCache.getRect(fragmentPath)

        GameObject.__init__(self, fragmentImage, parent, pos, vel)

        if screenBoundaries == None:
            raise Exception('Boulders must have screen boundaries')
        self.boundaries = (screenBoundaries[0]-rect.width,
                           screenBoundaries[1]-rect.height,
                           screenBoundaries[2]+rect.width,
                           screenBoundaries[3]+rect.height)

        self.acceleration = (0,0.001)


    def kill(self):
        GameObject.kill(self)

    def update(self, *args):
        GameObject.update(self, *args)

        #kill when off-screen:
        if ((self.rect.topleft[0] < self.boundaries[0]) or
           (self.rect.topleft[0] + self.rect.width > self.boundaries[2]) or
           (self.rect.topleft[1] + self.rect.height > self.boundaries[3])):
            self.kill()

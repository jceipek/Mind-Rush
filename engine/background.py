#
# background.py
#
# Copyright (C)2011 Julian Ceipek
#
# Redistribution is permitted under the BSD license.  See LICENSE for details.
#

import

class Background:
    """
    A sprite group or solid color that is displayed on a screen.
    """
    def __init__(self, bg):
        self.bg = bg


    def draw(self, surf):
        if type(self.bg) == tuple:
            surf.fill(self.bg)
        else:
            self.bg.draw()

    def update(self):
        if not type(self.bg) == tuple:
            self.bg.update() #FIXME
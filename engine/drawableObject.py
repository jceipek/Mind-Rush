#
# drawableObject.py
#
# Copyright (C)2011 Julian Ceipek and Patrick Varin
#
# Redistribution is permitted under the BSD license.  See LICENSE for details.
#

class DrawableObject(pygame.sprite.Sprite)

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, imagePath, colorKey=None)

        self.image = image
        self.rect = image.get_rect()
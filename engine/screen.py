#
# screen.py
#
# Copyright (C)2011 Julian Ceipek
#
# Redistribution is permitted under the BSD license.  See LICENSE for details.
#

import pygame

class Screen(pygame.Surface):

    def __init__(self, background, size):
        pygame.Surface.__init__(self)
        self.background = background
        self.size = size #Should default to screen size if not specified

    def draw(self):
        pass
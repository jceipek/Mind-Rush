#
# textCache.py
#
# Copyright (C)2011 Julian Ceipek
#
# Redistribution is permitted under the BSD license.  See LICENSE for details.
#

import pygame
from weakref import WeakKeyDictionary
from potentialObject import PotentialObject

class TextCache:
    """
    A repository that stores text and fonts for reuse.
    It abstracts the process of handling font rendering so that
    the game logic does not have to decide whether fonts have been loaded
    or text has to be rendered to a surface.
    """
    def __init__(self):
        self.fonts = WeakKeyDictionary()
        self.text = WeakKeyDictionary()
        self.initialized = False
        
    def initialize(self):
        for key in self.fonts.keys():
            self.fonts[key].setObject(pygame.font.Font(key))
        for key in self.text.keys():
            font = self.getFont(key)
            self.text[key].setObject(font.render(key[0], key[4], key[3], key[5]))
            

    def getText(self, text, fontname, size,
                color, antialias=False, bgColor=None):
        antialias = int(antialias)
        if initialized:
            if not (text, fontname, size, color, antialias, bgColor) in self.text:
                font = self.getFont(fontname, size)
                self.text[(text, fontname, size, color, antialias,
                 bgColor)] = font.render(text, antialias, color, bgColor)
        else:
            if not (text, fontname, size, color, antialias, bgColor) in self.text:
                self.text[(text, fontname, size, color, antialias, bgColor)] = PotentialObject()
        return self.text[(text, fontname, size, color, antialias, bgColor)]

    def getTextHeight(self, text, fontname, size,
                color, antialias=False, bgColor=None):
        antialias = int(antialias)
        textObject = self.getText(text, fontname,
                                size, color, antialias, bgColor)
        return textObject.get_rect().height

    def getTextWidth(self, text, fontname, size,
                color, antialias=False, bgColor=None):
        antialias = int(antialias)
        textObject = self.getText(text, fontname,
                                size, color, antialias, bgColor)
        return textObject.get_rect().width

    def getFont(self, fontname, size):
        if initialized:
            if not (fontname, size) in self.fonts:
                self.fonts[(fontname, size)] = pygame.font.Font(fontname, size)
        else:
            if not (fontname, size) in self.fonts:
                self.fonts[(fontname, size)] = PotentialObject()

        return self.fonts[(fontname, size)]

    def clearText(self, text, fontname, size,
                color, antialias=False, bgColor=None):
        """
        Removes a text object from the cache to save memory.
        This should be called every time text on the screen changes
        for a while.

        Example: Call before a score counter gets updated.
        """
        if (text, fontname, size,
                color, antialias, bgColor) in self.text:
            del self.text[(text, fontname, size,
                color, antialias, bgColor)]

    def clearFont(self, fontname, size):
        """
        Removes a font object from the cache to save memory.
        Keep in mind that making new font objects requires disk access,
        which is relatively slow.

        Unless your game has many fonts, this needs to be called
        very infrequently.
        """
        if (fontname, size) in self.fonts:
            del self.fonts[(fontname, size)]

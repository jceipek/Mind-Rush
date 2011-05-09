#
# bar.py
#
# Copyright (C)2011 Julian Ceipek and Patrick Varin
#
# Redistribution is permitted under the BSD license.  See LICENSE for details.
#

import pygame

class Bar():
    """
    A bar useful for displaying information such as health and power. It is
    rectangular rather than image-based.

    Based on the Bar class in Complete-Galactic-Dominion's Overlay module, by
    Julian Ceipek and Patrick Varin, Jared Kirschner, Patrick Varin, and Berit Johnson
    """
    def __init__(self,maxValue,barWidth,barHeight,
                fullness=1.0,fullColor=(0,255,0),
                emptyColor=(255,0,0), borderSize=0, borderColor=(50,50,50)):
        from pygame import Surface
        self.maxValue = maxValue
        self.fullness = fullness
        self.fullColor = fullColor
        self.emptyColor = emptyColor
        self.barWidth = barWidth
        self.barHeight = barHeight
        self.borderSize = borderSize
        self.borderColor = borderColor

        self.surface = pygame.Surface((self.barWidth,self.barHeight))
        self.updateBarWithValue(maxValue)

    def updateBarWithValue(self,value):
        """
        Updates the self.surface to reflect the new value.
        """
        value = max(0,value)
        self.fullness = (float(value)/self.maxValue)

        valueRemaining = int(self.fullness*self.barWidth)
        valueRemainingRect = (0+self.borderSize,0+self.borderSize,
                            int(self.fullness*self.barWidth-self.borderSize*2),
                            self.barHeight-self.borderSize*2)

        if value > 0:
            valueLostRect = (valueRemaining-self.borderSize,0+self.borderSize,
                       self.barWidth-valueRemaining,self.barHeight-self.borderSize*2)
        else:
            valueLostRect = (0+self.borderSize,0+self.borderSize,
                            self.barWidth-self.borderSize*2,
                            self.barHeight-self.borderSize*2)

        if self.borderSize > 0:
            entireRect = (0,0,self.barWidth,self.barHeight)
            self.surface.fill(self.borderColor, entireRect)
        self.surface.fill(self.fullColor, valueRemainingRect)
        self.surface.fill(self.emptyColor, valueLostRect)

    def draw(self,surface,pos):
        surface.blit(self.surface,(pos,(self.barWidth,self.barHeight)))

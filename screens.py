#
# screens.py
#
# Copyright (C)2011 Julian Ceipek and Patrick Varin
#
# Redistribution is permitted under the BSD license.  See LICENSE for details.
#

import pygame
from engine.screen import Screen
from engine.functions import pathJoin
from engine.background import Background

class MenuScreen(Screen):

    def __init__(self, size, ui):
        background = Background((0,0,0))
        Screen.__init__(self, background, size, ui)
        MenuItem.textCache = Screen.textCache
        MenuItem.resolution = Screen.resolution

        self.menuItems = []
        self.addMenuItem(MenuItem('Play',(int(self.resolution[0]*(1/3.0)),self.resolution[1]//2,)))
        self.addMenuItem(MenuItem('Exit',(int(self.resolution[0]*(2/3.0)),self.resolution[1]//2)))

    def initializeCallbackDict(self):
        self.callbackDict = {}
        self.callbackDict['left_click'] = ('deviceString', self.leftClick)

    def addMenuItem(self,item):
        self.menuItems.append(item)

    def draw(self, surf):
        Screen.draw(self, surf)
        for menuItem in self.menuItems:
            menuItem.draw(surf)
            
    def leftClick(self):
        for item in self.menuItems:
            if item.rect.collidepoint(pygame.mouse.get_pos()):
                if item.text == 'Exit':
                    pygame.event.post(pygame.event.Event(pygame.QUIT,{}))
                elif item.text == 'Play':
                    print item.text

class MenuItem:

    def __init__(self, text, pos):
        self.text = text
        self.fontname = pathJoin(('fonts','orbitron',
            'orbitron-black.ttf'))
        self.size = int(self.resolution[1]*(1/15.0))
        self.color = (255,255,255)
        self.antialias = True
        self.textSurface = self.textCache.getText(text, self.fontname,
            self.size, self.color, antialias=self.antialias)
        self.rect = self.textSurface.get_rect()
        self.rect.center = pos

    def draw(self, surf):
        surf.blit(self.textSurface, self.rect)


class InputScreen(Screen):

    def __init__(self):
        pass


class GameScreen(Screen):

    def __init__(self, size, ui):
        background = Background((0,0,0))
        Screen.__init__(self, background, size, ui)


class ScoreScreen(Screen):

    def __init__(self):
        pass


class NotificationScreen(Screen):

    def __init__(self):
        pass

class LoadingScreen(Screen):

    def __init__(self):
        pass

if __name__ == '__main__':
    MenuItem('text')

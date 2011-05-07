#
# screens.py
#
# Copyright (C)2011 Julian Ceipek
#
# Redistribution is permitted under the BSD license.  See LICENSE for details.
#

from engine.screen import Screen
from engine.functions import pathJoin
from engine.background import Background

class MenuScreen(Screen):

    def __init__(self, size, ui):
        background = Background((0,0,0))
        Screen.__init__(self, background, size, ui)
        MenuItem.textCache = Screen.textCache
        
        self.menuItems = []
        self.addMenuItem(MenuItem('Play'))
        self.addMenuItem(MenuItem('Exit'))

    def addMenuItem(self,item):
        self.menuItems.append(item)
        
    def draw(self, surf):
        Screen.draw(self, surf)
        for menuItem in self.menuItems:
            menuItem.draw(surf)

class MenuItem:

    def __init__(self, text):
        self.text = text
        fontname = pathJoin(('fonts,orbitron,orbitron-black.ttf'))
        self.textSurface = self.textCache.getText(text, fontname, 20, (255,)*3, antialias=True)
        
    def draw(self, surf):
        surf.blit(self.textSurface,(0,0))


class InputScreen(Screen):

    def __init__(self):
        pass


class GameScreen(Screen):

    def __init__(self):
        pass


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

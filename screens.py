#
# screens.py
#
# Copyright (C)2011 Julian Ceipek and Patrick Varin
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
        MenuItem.resolution = Screen.resolution
        
        self.initializeCallbackDict()

        self.menuItems = []
        self.addMenuItem(MenuItem('Play',(self.resolution[0]//2,int(self.resolution[1]*(1/3.0)))))
        self.addMenuItem(MenuItem('Exit',(self.resolution[0]//2,self.resolution[1]//2)))

    def initializeCallbackDict(self):
        self.callbackDict = {}
        self.callbackDict['fire'] = ('deviceString', self.fire)
        self.callbackDict['joyFire'] = ('deviceString', self.joyFire)
        self.callbackDict['move'] = ('deviceString', self.move)

    def addMenuItem(self,item):
        self.menuItems.append(item)

    def draw(self, surf):
        Screen.draw(self, surf)
        for menuItem in self.menuItems:
            menuItem.draw(surf)
            
    def fire(self):
        print 'fire'

    def joyFire(self):
        print 'joystick Fire'
        
    def move(self,movement):
        if not movement.relative:
            print 'absolute position', movement.values
        else:
            print 'relative position', movement.values

class MenuItem:

    def __init__(self, text, pos):
        self.text = text
        self.position = list(pos)
        self.fontname = pathJoin(('fonts','orbitron','orbitron-black.ttf'))
        self.size = int(self.resolution[1]*(1/15.0))
        self.color = (255,255,255)
        self.antialias = True
        self.textSurface = self.textCache.getText(text, self.fontname, self.size, self.color, antialias=self.antialias)

    def draw(self, surf):
        topleft = self.position
        dy = -self.textCache.getTextHeight(self.text, self.fontname,
                self.size, self.color, antialias=self.antialias)//2
        dx = -self.textCache.getTextWidth(self.text, self.fontname,
                self.size, self.color, antialias=self.antialias)//2
        surf.blit(self.textSurface,
                (self.position[0] + dx, self.position[1] + dy))


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

#
# screens.py
#
# Copyright (C)2011 Julian Ceipek and Patrick Varin
#
# Redistribution is permitted under the BSD license.  See LICENSE for details.
#

import pygame
import random

from engine.screen import Screen
from engine.functions import pathJoin
from engine.background import Background

#For GameScreen:
from gameObjects.ship import Ship
from gameObjects.boulder import Boulder
from gameObjects.boulderFragment import BoulderFragment

class MenuScreen(Screen):

    def __init__(self, size, ui):
        background = Background((0,0,0))
        Screen.__init__(self, background, size, ui)
        MenuItem.textCache = Screen.textCache
        MenuItem.imageCache = Screen.imageCache
        MenuItem.resolution = Screen.resolution

        self.menuItems = []
        self.title = MenuItem('MindRush',(self.resolution[0]//2,int(self.resolution[1]/4)), scaleSize=1.5)
        self.addMenuItem(MenuItem('Play',(int(self.resolution[0]*(1/3.0)),self.resolution[1]//2,)))
        self.addMenuItem(MenuItem('Options',(int(self.resolution[0]*.5),self.resolution[1]//2)))
        self.addMenuItem(MenuItem('Exit',(int(self.resolution[0]*(2/3.0)),self.resolution[1]//2)))

        self.organizeMenuItems()

    def initializeCallbackDict(self):
        self.callbackDict = {}
        self.callbackDict['left_click'] = ('deviceString', self.leftClick)
        self.callbackDict['connectionQuality'] = ('deviceString', self.printConnectionQuality)

    def addMenuItem(self,item):
        self.menuItems.append(item)

    def draw(self, surf):
        Screen.draw(self, surf)
        self.title.draw(surf)
        for menuItem in self.menuItems:
            menuItem.draw(surf)

    def leftClick(self):
        for item in self.menuItems:
            if item.rect.collidepoint(pygame.mouse.get_pos()):
                if item.text == 'Exit':
                    pygame.event.post(pygame.event.Event(pygame.QUIT,{}))
                elif item.text == 'Play':
                    self.play()
                elif item.text == 'Options':
                    self.displayOptionsScreen()

    def organizeMenuItems(self):
        screenWidth = self.resolution[0]
        itemsLength = 0

        for item in self.menuItems:
            itemsLength += item.rect.width

        if itemsLength >= screenWidth:
            pass#FIXME, Handle this case
        else:
            itemSpace = (screenWidth-itemsLength)/(len(self.menuItems)+1)

        nextPosition = itemSpace
        for i in range(len(self.menuItems)):
            self.menuItems[i].rect.topleft = (nextPosition,self.menuItems[i].rect.topleft[1])
            nextPosition += itemSpace + self.menuItems[i].rect.width

    def play(self):
        gameScreen = GameScreen(self.resolution, self._ui)
        self._ui.clearActiveScreens()
        self._ui.addActiveScreens(gameScreen)

    def displayOptionsScreen(self):
        optionsScreen = OptionsScreen(self.resolution, self._ui)
        self._ui.addActiveScreens(optionsScreen)

    def printLook(self, event):
        print event.values

    def printConnectionQuality(self, event):
        print event.values

class MenuItem:

    def __init__(self, text, pos, scaleSize=None):
        self.text = text
        self.fontname = pathJoin(('fonts','orbitron',
            'orbitron-black.ttf'))
        self.size = int(self.resolution[1]*(1/15.0))
        if scaleSize != None:
            self.size *= scaleSize
            self.size = int(self.size)
        self.color = (255,255,255)
        self.antialias = True
        self.textSurface = self.textCache.getText(text, self.fontname,
            self.size, self.color, antialias=self.antialias)
        self.rect = self.textSurface.get_rect()
        self.rect.center = int(pos[0]), int(pos[1])

    def draw(self, surf):
        surf.blit(self.textSurface, self.rect)


class InputScreen(Screen):

    def __init__(self):
        pass


class GameScreen(Screen):

    def __init__(self, size, ui):
        Ship.imageCache = Screen.imageCache
        Boulder.imageCache = Screen.imageCache
        BoulderFragment.imageCache = Screen.imageCache

        background = Background((0,0,0))
        Screen.__init__(self, background, size, ui)

        self.ship = Ship(self, pos=(size[0]/2,size[1]), screenBoundaries=(0,0)+size)

        self.ship.move((0,-self.ship.rect.height/2))
        self.ship.targetPosition = self.ship.position

        self.boulders = pygame.sprite.Group()
        self.nextBoulderTime = 0

        self.boulderFragments = pygame.sprite.Group()


    def initializeCallbackDict(self):
        self.callbackDict = {}
        self.callbackDict['look'] = ('deviceString', self.steer)

    def steer(self, event):
        #move the spaceship in this method
        self.ship.targetPosition = (event.values[0], self.ship.targetPosition[1])
        pass#self.targetPosition = event.values[0]#the position of the event

    def addBoulderFragment(self, pos=(0,0), vel=(0,0)):
        newBoulderFragment = BoulderFragment(self,
                               pos=pos,
                               vel=vel,
                               screenBoundaries=(0,0)+self.resolution)
        self.boulderFragments.add(newBoulderFragment)

    def draw(self, surf):
        Screen.draw(self, surf)
        self.ship.draw(surf)
        self.boulders.draw(surf)
        self.boulderFragments.draw(surf)

    def update(self, *args):
        gameTime, frameTime = args[:2]
        self.ship.update(*args)
        self.boulders.update(*args)
        self.boulderFragments.update(*args)

        #For every boulder colliding with the ship,
        #kill the boulder & lose health
        for boulder in self.ship.testMaskCollision(self.boulders):
            boulder.kill()

        if gameTime >= self.nextBoulderTime:
            boulderPos = random.randint(0,self.resolution[0]), 0
            self.boulders.add(Boulder(self, pos=boulderPos, screenBoundaries=(0,0)+self.resolution))
            self.nextBoulderTime = gameTime + random.randint(10,1000)


class OptionsScreen(Screen):

    def __init__(self, size, ui):
        background = Background((0,0,0))
        Screen.__init__(self, background, size, ui)
        MenuItem.textCache = Screen.textCache
        MenuItem.resolution = Screen.resolution

        self.title = MenuItem('Options',(self.resolution[0]//2,int(self.resolution[1]/4)), scaleSize=1.5)
        self.menuItems = []
        self.addMenuItem(MenuItem('Calibrate',(int(self.resolution[0]*(1/3.0)),self.resolution[1]//2,)))
        self.addMenuItem(MenuItem('Input Settings',(int(self.resolution[0]*.5),self.resolution[1]//2)))
        self.addMenuItem(MenuItem('Back',(int(self.resolution[0]*(2/3.0)),self.resolution[1]//2)))

        self.organizeMenuItems()

    def initializeCallbackDict(self):
        self.callbackDict = {}
        self.callbackDict['left_click'] = ('deviceString', self.leftClick)

    def organizeMenuItems(self):
        screenWidth = self.resolution[0]
        itemsLength = 0

        for item in self.menuItems:
            itemsLength += item.rect.width

        if itemsLength >= screenWidth:
            pass#FIXME, Handle this case
        else:
            itemSpace = (screenWidth-itemsLength)/(len(self.menuItems)+1)

        nextPosition = itemSpace
        for i in range(len(self.menuItems)):
            self.menuItems[i].rect.topleft = (nextPosition,self.menuItems[i].rect.topleft[1])
            nextPosition += itemSpace + self.menuItems[i].rect.width

    def addMenuItem(self,item):
        self.menuItems.append(item)

    def draw(self, surf):
        Screen.draw(self, surf)
        self.title.draw(surf)
        for menuItem in self.menuItems:
            menuItem.draw(surf)

    def leftClick(self):
        for item in self.menuItems:
            if item.rect.collidepoint(pygame.mouse.get_pos()):
                if item.text == 'Back':
                    self._ui.clearTopScreen()
                elif item.text == 'Scores':
                    self.play()
                elif item.text == 'Calibrate':
                    self.displayOptionsScreen()

class ScoreScreen(Screen):

    def __init__(self):
        pass

class NotificationScreen(Screen):

    def __init__(self):
        pass

class LoadingScreen(Screen):

    def __init__(self):
        pass

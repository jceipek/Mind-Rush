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
        Fragment.imageCache = Screen.imageCache

        background = Background((0,0,0))
        Screen.__init__(self, background, size, ui)

        self.ship = Ship(self, pos=(size[0]/2,size[1]), screenBoundaries=(0,0)+size)

        self.ship.move((0,-self.ship.rect.height/2))
        self.ship.targetPosition = self.ship.position

        self.boulders = pygame.sprite.Group()
        self.nextBoulderTime = 0

        self.fragments = pygame.sprite.Group()


    def initializeCallbackDict(self):
        self.callbackDict = {}
        self.callbackDict['look'] = ('deviceString', self.steer)

    def steer(self, event):
        #move the spaceship in this method
        self.ship.targetPosition = (event.values[0], self.ship.targetPosition[1])
        pass#self.targetPosition = event.values[0]#the position of the event

    def addFragment(self, pos=(0,0), vel=(0,0)):
        newFragment = Fragment(self,
                               pos=pos,
                               vel=vel,
                               screenBoundaries=(0,0)+self.resolution)
        self.fragments.add(newFragment)

    def draw(self, surf):
        Screen.draw(self, surf)
        self.ship.draw(surf)
        self.boulders.draw(surf)
        self.fragments.draw(surf)

    def update(self, *args):
        gameTime, frameTime = args[:2]
        self.ship.update(*args)
        self.boulders.update(*args)
        self.fragments.update(*args)

        if gameTime >= self.nextBoulderTime:
            boulderPos = random.randint(0,self.resolution[0]), 0
            self.boulders.add(Boulder(self, pos=boulderPos, screenBoundaries=(0,0)+self.resolution))
            self.nextBoulderTime = gameTime + random.randint(10,1000)

class GameObject(pygame.sprite.Sprite):

    def __init__(self, image, parent, pos=(0,0), vel=(0,0)):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()
        self.rect.center = int(pos[0]), int(pos[1])
        self.position = pos
        self.velocity = vel
        self.parent = parent
        self.acceleration = (0,0)

    def move(self, delta):
        self.position = self.position[0]+delta[0], self.position[1]+delta[1]
        self.rect.center = int(self.position[0]), int(self.position[1])

    def moveTo(self, pos):
        self.position = pos
        self.rect.center = int(pos[0]), int(pos[1])

    def draw(self, surf):
        surf.blit(self.image, self.rect)

    def update(self, *args):
        gameTime, frameTime = args[:2]
        self.velocity = (frameTime*self.acceleration[0]+self.velocity[0],
                        frameTime*self.acceleration[1]+self.velocity[1])
        self.position = (frameTime*self.velocity[0]+self.position[0],
                        frameTime*self.velocity[1]+self.position[1])
        self.moveTo(self.position)

class Ship(GameObject):

    def __init__(self, parent, pos=(0,0), vel=(0,0), screenBoundaries=None):

        shipPath = pathJoin(('images','ship.png'))
        shipImage = self.imageCache.getImage(shipPath, colorkey='alpha', mask=True)

        GameObject.__init__(self, shipImage, parent, pos, vel)
        self.targetPosition = pos

        self.screenBoundaries = screenBoundaries
        if screenBoundaries != None:
            self.minXPos = screenBoundaries[0] + self.rect.width/2
            self.maxXPos = screenBoundaries[2] - self.rect.width/2

    def update(self, *args):
        gameTime, frameTime = args[:2]
        speed = .006
        error = self.targetPosition[0]-self.position[0], self.targetPosition[1]-self.position[1]
        self.velocity = error[0]*speed, error[1]*speed

        #don't allow the ship to jump over the target position (applicable only at high speeds)
        nextPos = [frameTime*self.velocity[0]+self.position[0],
                        frameTime*self.velocity[1]+self.position[1]]
        nextError = self.targetPosition[0]-nextPos[0], self.targetPosition[1]-nextPos[1]
        if error[0]*nextError[0] < 0:
            nextPos[0] = self.targetPosition[0]
        if error[1]*nextError[1] < 0:
            nextPos[1] = self.targetPosition[1]
        self.position = nextPos

        #don't allow the ship off of the sides of the screen
        if self.screenBoundaries != None:
            if self.position[0] > self.maxXPos:
                self.position = self.maxXPos, self.position[1]
            elif self.position[0] < self.minXPos:
                self.position = self.minXPos, self.position[1]
        self.moveTo(self.position)
        
class TestShip(Ship):
    def __init__(*args, **kwargs):
        Ship.__init__(*args,**kwargs)
        self.stage = 0
        self.finished = False
    def update(self, *args):
        GameObject.update(self, *args)
        if self.stage == 0 and self.position[0] < self.minXPos:
            self.velocity = (-self.velocity[0], self.velocity[1])
            self.stage = 1
        elif self.stage == 1 and self.position[0] > self.maxXPos:
            self.stage = 2
            self.velocity = (-self.velocity[0], self.velocity[1])
        elif self.stage == 2 and self.position[0] < (self.minXPos + self.maxXPos)/2:
            self.stage = 3


class Boulder(GameObject):

    def __init__(self, parent, pos=(0,0), vel=(0,0), screenBoundaries = None):
        boulderPath = pathJoin(('images','boulder.png'))
        boulderImage = self.imageCache.getImage(boulderPath, colorkey='alpha', mask=True)

        GameObject.__init__(self, boulderImage, parent, pos, vel)

        if screenBoundaries == None:
            raise Exception('Boulders must have screen boundaries')
        self.boundaries = screenBoundaries
        self.acceleration = (0,.001)


    def kill(self):
        GameObject.kill(self)
        #from random import randint
        from math import sin,cos
        for i in xrange(8):
            self.parent.addFragment(pos=self.position,
            vel=(cos((2*3.14159)/8.0*i),sin((2*3.14159)/8.0*i)))

    def update(self, *args):
        GameObject.update(self, *args)

        #bounce off of the walls

        if self.rect.topleft[0] < self.boundaries[0] or \
            self.rect.topleft[0] + self.rect.width > self.boundaries[2]:

            self.velocity = -self.velocity[0], self.velocity[1]

        #hit the ground
        if self.rect.topleft[1] + self.rect.height > self.boundaries[3]:

            self.kill()

class Fragment(GameObject):
    def __init__(self, parent, pos=(0,0), vel=(0,0), screenBoundaries = None):
        fragmentPath = pathJoin(('images','fragment.png'))
        fragmentImage = self.imageCache.getImage(fragmentPath, colorkey='alpha', mask=True)

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
                    self.play(self._ui.addActiveScreens(ScoreScreen()))
                elif item.text == 'Calibrate':
                    self._ui.addActiveScreens(CalibrationScreen(self.resolution, self._ui))

class CalibrationScreen(Screen):

    def __init__(self, size, ui):
        background = Background((0,0,0))
        Screen.__init__(self, background, size, ui)
        MenuItem.textCache = Screen.textCache
        Ship.imageCache = Screen.imageCache

        self.ship = TestShip(self, pos=(size[0]/2,size[1]), screenBoundaries=(0,0)+size)
        self.ship.move((0,-self.ship.rect.height/2))
        
        self.menuItems = []
        self.addMenuItem(MenuItem('You are about to calibrate your eye circuit',(self.resolution[0]//2,int(self.resolution[1]*.1)),scaleSize=.75))
        self.addMenuItem(MenuItem('Follow the ship with your eyes',(self.resolution[0]//2,int(self.resolution[1]*.17)),scaleSize=.75))
        self.addMenuItem(MenuItem('Press the spacebar to continue',(self.resolution[0]//2,int(self.resolution[1]*.24)),scaleSize=.75))
        
        self.running = False

    def initializeCallbackDict(self):
        self.callbackDict = {}
        self.callbackDict['startCalibration'] = ('deviceString', self.start)

    def addMenuItem(self,item):
        self.menuItems.append(item)

    def draw(self, surf):
        Screen.draw(self, surf)
        for menuItem in self.menuItems:
            menuItem.draw(surf)
        self.ship.draw(surf)
        
    def update(self, *args):
        self.ship.update(*args)
        pass

    def start(self):
        if not self.running:
            self.ship.velocity = (.01,0)
            self.running = True
            

class ScoreScreen(Screen):

    def __init__(self):
        pass


class NotificationScreen(Screen):

    def __init__(self):
        pass

class LoadingScreen(Screen):

    def __init__(self):
        pass

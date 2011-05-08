#
# window.py
#
# Copyright (C)2011 Julian Ceipek and Patrick Varin
#
# Redistribution is permitted under the BSD license.  See LICENSE for details.
#

import pygame

class Window:

    def __init__(self, resolution,
        windowTitle="Powered by engine"):
        """
        active
        manager
        resolution
        displaySurface

        gameClock
        maxFPS
        gameTime
        gameFrametime
        """
        self.active = True
        self.resolution = resolution
        self.openPygame(windowTitle)
        self.altInput = []

    def openPygame(self,windowTitle):
        pygame.init()
        pygame.display.set_caption(windowTitle)
        self.displaySurface = pygame.display.set_mode(self.resolution)
        self.gameClock = pygame.time.Clock()
        self.maxFPS = 60
        self.gameTime = 0
        self.gameFrametime = 0

    def registerManager(self, manager):
        self.manager = manager
        manager.registerEventWithCallback(pygame.QUIT, self.deactivate)
        self.manager.setupWithWindow(self)

    def addInputDevice(self, device):
        self.altInput.append(device)

    def run(self):

        while self.active:
            for device in self.altInput:
                if device.poll():
                    newEvent = device.getEvent()
                    pygame.event.post(newEvent)

            for event in pygame.event.get():
                self.manager.handle(event)

            self.displaySurface.fill((0,0,0)) #should go in manager

            self.manager.update(self.gameTime, self.gameFrametime)
            self.manager.draw(self.displaySurface)

            pygame.display.flip()

            self.gameFrametime = self.gameClock.tick(self.maxFPS)
            self.gameTime += self.gameFrametime

    def deactivate(self, event):
        self.active = False

    def cleanup(self):
        """Called when the program is closed"""
        for device in self.altInput:
            device.stop()
        print("Program Terminated Successfully.")

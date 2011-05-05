#
# window.py
#
# Copyright (C)2011 Julian Ceipek
#
# Redistribution is permitted under the BSD license.  See LICENSE for details.
#

import pygame

class Window:

    def __init__(self,manager,resolution=(640,480),
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
        self.registerWithManager(manager)
        self.resolution = resolution
        self.openPygame(windowTitle)
        self.run()
        self.cleanup()

    def openPygame(self,windowTitle):
        pygame.init()
        pygame.display.set_caption(windowTitle)
        self.displaySurface = pygame.display.set_mode(self.resolution)
        self.gameClock = pygame.time.Clock()
        self.maxFPS = 60
        self.gameTime = 0
        self.gameFrametime = 0
        self.manager.setupWithWindow(self)

    def registerWithManager(self,manager):
        self.manager = manager
        manager.registerEventWithCallback(pygame.QUIT,
            self.deactivate)

    def run(self):

        while self.active:
            for event in pygame.event.get():
                self.manager.handle(event)

            self.displaySurface.fill((0,0,0)) #should go in manager

            self.manager.update(self.gameTime, self.gameFrametime)
            self.manager.draw()

            pygame.display.flip()

            self.gameFrametime = self.gameClock.tick(self.maxFPS)
            self.gameTime += self.gameFrametime

    def deactivate(self):
        self.active = False

    def cleanup(self):
        """Called when the program is closed"""
        print("Program Terminated Successfully.")
#
# manager.py
#
# Copyright (C)2011 Julian Ceipek
#
# Redistribution is permitted under the BSD license.  See LICENSE for details.
#

import pygame

from textCache import TextCache

class Manager:

    def __init__(self):
        self.inputDict = {}
        self.initializeCaches()

    def initializeCaches(self):
        Manager.textCache = TextCache()
        
    def registerUI(self, ui):
        self._ui = ui
        self._ui.setCaches(textCache=self.textCache)

    def registerEventWithCallback(self, eventType, callback):
        """
        Will associate an event type with a callback.
        """
        self.inputDict[eventType] = callback

    def setupWithWindow(self, window):
        """
        Give the manager various window properties needed by game objects
        """
        pass

    def update(self, gameTime, gameFrametime):
        self.ui.update(gameTime, gameFrametime)

    def draw(self, surf):
        self.ui.draw(surf)

    def handle(self, event):
        """
        Will execute the function associated with the type of the pygame event passed in.
        """
        if event.type in self.inputDict:
            self.inputDict[event.type]()

    def post(self, event):
        pygame.event.post(Event)

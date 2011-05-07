#
# ui.py
#
# Copyright (C)2011 Julian Ceipek
#
# Redistribution is permitted under the BSD license.  See LICENSE for details.
#

from classMethod import ClassMethod

class UI:

    def __init__(self, manager):
        self._manager = manager
        self._manager.registerUI(self)
        self.activeScreens = []
        
    def addActiveScreens(self, screens):
        """
        Adds an ordered list of screens to the view
        Supports lists, tuples and singletons
        """
        if type(screens) != list:
            screens = list(screens)
            
        self.activeScreen.append(*screens)
        
    def clearActiveScreens(self, screens):
        """
        Removes all of the screens from view
        """
        self.activeScreens = []
        
    def clearTopScreen(self):
        """
        Removes the top screen from view and returns it
        """
        return self.activeScreens.pop()
        
    def draw(self, surf):
        
        for screen in self.activeScreens:
            screen.draw(surf)
            
    def update(self, *args):
        
        for screen in self.activeScreens:
            screen.update(*args)
            
    def setCaches(textCache=None):
        """
        Called by the manager to let the ui make images, text, etc.
        """
        if textCache != None:
            UI.textCache = textCache
            
    setCaches = ClassMethod(setCaches)

#
# ui.py
#
# Copyright (C)2011 Julian Ceipek
#
# Redistribution is permitted under the BSD license.  See LICENSE for details.
#

class UI:

    def __init__(self):
        self.activeScreen = None
        
    def setActiveScreen(self, screen):
        self.activeScreen = screen

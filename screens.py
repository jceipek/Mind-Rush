#
# screens.py
#
# Copyright (C)2011 Julian Ceipek
#
# Redistribution is permitted under the BSD license.  See LICENSE for details.
#

from engine.screen import Screen

class MenuScreen(Screen):

    def __init__(self, menuItems=None):
        if menuItems == None:
            self.menuItems = []
            self.addMenuItem(MenuItem('Play'))
        else:
            self.menuItems = menuItems

    def addMenuItem(self,item):
        self.menuItems.append(item)


class MenuItem:

    def __init__(self, text):
        self.text = text


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
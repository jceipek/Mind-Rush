#
# mindRush.py
#
# Copyright (C)2011 Julian Ceipek
#
# Redistribution is permitted under the BSD license.  See LICENSE for details.
#

from engine.ui import UI
from engine.manager import Manager
from engine.window import Window

from screens import MenuScreen

resolution = (640,480)

manager = Manager()
userInterface = UI(manager)
#screens must be initialized after the manager and the ui
mainScreen = MenuScreen(resolution, userInterface)
userInterface.addActiveScreens(mainScreen)
Window(manager,resolution,#(1440,900),
        windowTitle="Mind Rush")

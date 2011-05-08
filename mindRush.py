#
# mindRush.py
#
# Copyright (C)2011 Julian Ceipek and Patrick Varin
#
# Redistribution is permitted under the BSD license.  See LICENSE for details.
#

from engine.ui import UI
from engine.manager import Manager
from engine.window import Window

from biofeedback import Biofeedback
from screens import MenuScreen

resolution = (640,480)
#resolution = (1440,900)

altInput = Biofeedback('/dev/tty.usbmodem621')

window = Window(resolution,
        windowTitle="Mind Rush", altInput=altInput)

manager = Manager()
window.registerManager(manager)

userInterface = UI(manager)
#screens must be initialized after the manager and the ui
mainScreen = MenuScreen(resolution, userInterface)
userInterface.addActiveScreens(mainScreen)

window.run()
window.cleanup()
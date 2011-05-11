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

from screens import MenuScreen

#resolution = (640,480)
resolution = (1344,840)
#resolution = (1440,900)


window = Window(resolution,
        windowTitle="Mind Rush")

manager = Manager()
window.registerManager(manager)

#-------------------------------------------------------------------------
#         Uncomment the lines below to obtain bio-feedback control
#         You may need to modify '/dev/tty.usbmodem621' to match
#         the location of the Arduino communication port on your
#         machine. On Windows, this will be 'COM3' or higher,
#         and on Linux, it will be similar to '/dev/ttyAMC0'.
#         For instructions on obtaining this string, look through
#         http://arduino.cc/en/Guide/HomePage
#-------------------------------------------------------------------------
#from biofeedback import Biofeedback
#arduinoInput = Biofeedback('/dev/tty.usbmodem621',
#                            mindFlexActive=False, eyeCircuitActive=True)
#window.addInputDevice(arduinoInput)
#-------------------------------------------------------------------------

userInterface = UI(manager)
#screens must be initialized after the manager and the ui
mainScreen = MenuScreen(resolution, userInterface)
userInterface.addActiveScreens(mainScreen)

window.run()
window.cleanup()

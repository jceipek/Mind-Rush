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

userInterface = UI()
manager = Manager(userInterface)
Window(manager,resolution=(640,480),#(1440,900),
        windowTitle="Mind Rush")
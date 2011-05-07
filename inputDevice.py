#
# inputDevice.py:
#        A python module for handling arbitrary input devices in pygame.
#
# Copyright (C)2011 Julian Ceipek and Patrick Varin
#
# Redistribution is permitted under the BSD license.  See LICENSE for details.
#

from listener import Listener

class _InputDevice(Listener):
    """
    An abstract class that wraps a stateful system.
    It notifies its Manager when its state changes.

    """
    def __init__(self):
        pass


class PositionalDevice(_InputDevice):
    """
    An InputDevice that can have a value within a range

    """
    def __init__(self):
        InputDevice.__init__(self)


class StateDevice(_InputDevice):
    """
    An InputDevice that has an on or off state.

    """
    def __init__(self):
        InputDevice.__init__(self)

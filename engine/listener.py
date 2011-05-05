#
# listener.py
#
# Copyright (C)2011 Julian Ceipek
#
# Redistribution is permitted under the BSD license.  See LICENSE for details.
#

class Listener:
    """
    Liseners post events to the event Manager's event queue, which notifies
    other Listeners expecting those events.
    """

    def __init__(self, manager, eventTypes, runLevel=None):
        """
        manager: The Manager to which to post

        eventTypes: A list of classes of the Events to which the Listener should respond.

        runLevel: The way that the listener is run.
            - None: Can only fire events if queried
            - 'thread': Will automatically post to the manager as a daemon
            - 'process': Will post to the manager as a separate process
        """

        self.manager = manager
        self.eventTypes = eventTypes
        self.runLevel = runLevel

    def notify(self, event):
        """
        Called when the Manager needs to notify the Listener of an Event.
        Every class inheriting from Listener should override this.
        """
        pass
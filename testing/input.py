#
# screens.py
#
# Copyright (C)2011 Julian Ceipek and Patrick Varin
#
# Redistribution is permitted under the BSD license.  See LICENSE for details.
#

try:
    import multiprocessing
except:
    raise Exception("Unable to load multiprocessing Python module.")

try:
    import serial
except:
    raise Exception("""Unable to load serial Python module.
    Do you have pyserial installed?""")

import time

class TrueProcess(multiprocessing.Process):
    def __init__(self, target, *args):
        multiprocessing.Process.__init__(self, target=target, args=args)
        self.start()

class MindflexDevice:
    def __init__(self):
        self.active = multiprocessing.Value('i',1)
        self.eventReader = None
        self.proc = None

    def listen(self):
        eventReader,eventPipe = multiprocessing.Pipe()
        self.proc = TrueProcess(self.mindflexReader, eventPipe)
        return eventReader

    def mindflexReader(self, eventPipe):
        self.quality = -1
        self.attention = -1
        self.meditation = -1
        self.delta = -1
        self.theta = -1
        self.lowAlpha = -1
        self.highAlpha = -1
        self.lowBeta = -1
        self.highBeta = -1
        self.lowGamma = -1
        self.highGamma = -1

        try:
            ser = serial.Serial('/dev/tty.usbmodem411', 9600)
            time.sleep(1)
        except:
            raise Exception("Unable to communicate with Arduino")

        while self.active:
            try:
                line = ser.readline().strip()
            except Exception as e:
                line = ""
                print "Reading from Arduino Failed: ",e
            if not line == "":
                line = line.split(',')
                try:
                    if not len(line) == 11:
                        raise ValuError
                    newQuality = (200.0-int(line[0]))/200.0
                    newAttention = (200.0-int(line[1]))/200.0
                    newMeditation = (200.0-int(line[2]))/200.0
                    newDelta = int(line[3])
                    newTheta = int(line[4])
                    newLowAlpha = int(line[5])
                    newHighAlpha = int(line[6])
                    newLowBeta = int(line[7])
                    newHighBeta = int(line[8])
                    newLowGamma = int(line[9])
                    newHighGamma = int(line[10])

                    if self.quality != newQuality:
                        self.quality = newQuality
                        eventPipe.send(('quality',self.quality))
                    if self.attention != newAttention:
                        self.attention = newAttention
                        eventPipe.send(('attention',self.attention))
                    if self.meditation != newMeditation:
                        self.meditation = newMeditation
                        eventPipe.send(('meditation',self.meditation))
                    if self.delta != newDelta:
                        self.delta = newDelta
                        eventPipe.send(('delta',self.delta))
                    if self.theta != newTheta:
                        self.theta = newTheta
                        eventPipe.send(('theta',self.theta))
                    if self.lowAlpha != newLowAlpha:
                        self.lowAlpha = newLowAlpha
                        eventPipe.send(('lowAlpha',self.lowAlpha))
                    if self.highAlpha != newHighAlpha:
                        self.highAlpha = newHighAlpha
                        eventPipe.send(('highAlpha',self.highAlpha))
                    if self.lowBeta != newLowBeta:
                        self.lowBeta = newLowBeta
                        eventPipe.send(('lowBeta',self.lowBeta))
                    if self.highBeta != newHighBeta:
                        self.highBeta = newHighBeta
                        eventPipe.send(('highBeta',self.highBeta))
                    if self.lowGamma != newLowGamma:
                        self.lowGamma = newLowGamma
                        eventPipe.send(('lowGamma',self.lowGamma))
                    if self.highGamma != newHighGamma:
                        self.highGamma = newHighGamma
                        eventPipe.send(('highGamma',self.highGamma))
                except:
                    print "Caught Mindflex serial error!"

        ser.close()

    def deactivate(self):
        self.active.value = 0

if __name__ == "__main__":
    m = MindflexDevice()
    a = m.listen()
    while 1:
        if a.poll():
            print "MOO: ",a.recv()
    #ser = serial.Serial('/dev/tty.usbmodem621', 9600)
    print "HI"
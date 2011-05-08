#
# biofeedback.py
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

from engine.trueProcess import TrueProcess
from engine.altInput import AltInput

class Arduino:
    def __init__(self):
        self.active = multiprocessing.Value('i',1)
        self.eventReader = None
        self.proc = None

    def listen(self, deviceID, mindFlexActive=True, eyeCircuitActive=True):
        eventReader,eventPipe = multiprocessing.Pipe()
        self.proc = TrueProcess(self.mindflexReader, deviceID, eventPipe)
        return eventReader

    def mindflexReader(self, deviceID, eventPipe,
                        mindFlexActive=True, eyeCircuitActive=True):
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
        self.eyeSignal = -1

        try:
            ser = serial.Serial(deviceID, 9600)
            time.sleep(1)
        except:
            raise Exception("Unable to communicate with Arduino")

        while self.active and (mindFlexActive or eyeCircuitActive):
            try:
                line = ser.readline().strip()
            except Exception as e:
                line = ""
                print "Reading from Arduino Failed: ",e
            if mindFlexActive and ('EEG' in line):
                line = line.split(':')
                line = line[1].split(',')
                try:
                    if not len(line) == 11:
                        raise ValuError
                    newQuality = (200.0-int(line[0]))/200.0
                    newAttention = int(line[1])/100.0
                    newMeditation = int(line[2])/100.0
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
            elif eyeCircuitActive and ('EMG' in line):
                line = line.split(':')
                line = line[1].split(',')
                try:
                    if not len(line) == 1:
                        raise ValuError
                    newEyeSignal = int(line[0])

                    if self.eyeSignal != newEyeSignal:
                        self.eyeSignal = newEyeSignal
                        eventPipe.send(('eyeValue',self.eyeSignal))

                except:
                    print "Caught EMG circuit serial error!"

        try:
            ser.close()
        except:
            print "Unable to close connection to Arduino!"

    def deactivate(self):
        self.active.value = 0

class Biofeedback(AltInput):
    def __init__(self, deviceID):
        self.arduino = Arduino()
        self.listener = arduino.listen(deviceID)

    def poll(self):
        return self.listener.poll()

    def getEvent(self):
        reading = self.arduino.recv()
        identifier = reading[0]
        value = reading[1]
        discrete = False #All of the bio-feedback events we use are continuous values
        self.makeEvent(identifier, value, discrete)

    def stop(self):
        self.arduino.deactivate()

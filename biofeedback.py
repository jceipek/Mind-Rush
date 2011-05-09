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
        self.mindflexQueue = multiprocessing.Queue(11)
        self.eyeCircuitQueue = multiprocessing.Queue(5)
        self.proc = TrueProcess(self.mindflexReader, deviceID,
                                mindFlexActive, eyeCircuitActive)

    def mindflexReader(self, deviceID,
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

        connected = False
        count = 0
        while not connected and count <= 5:
            try:
                ser = serial.Serial(deviceID, 9600)
                connected = True
            except Exception as e:
                count += 1
                print e
                if count >= 5:
                    raise Exception("Unable to communicate with Arduino")

        while self.active.value == 1 and (mindFlexActive or eyeCircuitActive):
            try:
                line = ser.readline().strip()
            except Exception as e:
                line = ""
                print "Reading from Arduino Failed: ",e
            if mindFlexActive and ('EEG:' in line):
                line = line.split(':')
                line = line[1].split(',')
                try:
                    if not len(line) == 11:
                        raise ValueError
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
                        self.putMindflexMessage(('Arduino_quality',self.quality))
                    if self.attention != newAttention:
                        self.attention = newAttention
                        self.putMindflexMessage(('Arduino_attention',self.attention))
                    if self.meditation != newMeditation:
                        self.meditation = newMeditation
                        self.put(('Arduino_meditation',self.meditation))
                    if self.delta != newDelta:
                        self.delta = newDelta
                        self.putMindflexMessage(('Arduino_delta',self.delta))
                    if self.theta != newTheta:
                        self.theta = newTheta
                        self.putMindflexMessage(('Arduino_theta',self.theta))
                    if self.lowAlpha != newLowAlpha:
                        self.lowAlpha = newLowAlpha
                        self.putMindflexMessage(('Arduino_lowAlpha',self.lowAlpha))
                    if self.highAlpha != newHighAlpha:
                        self.highAlpha = newHighAlpha
                        self.putMindflexMessage(('Arduino_highAlpha',self.highAlpha))
                    if self.lowBeta != newLowBeta:
                        self.lowBeta = newLowBeta
                        self.putMindflexMessage(('Arduino_lowBeta',self.lowBeta))
                    if self.highBeta != newHighBeta:
                        self.highBeta = newHighBeta
                        self.putMindflexMessage(('Arduino_highBeta',self.highBeta))
                    if self.lowGamma != newLowGamma:
                        self.lowGamma = newLowGamma
                        self.putMindflexMessage(('Arduino_lowGamma',self.lowGamma))
                    if self.highGamma != newHighGamma:
                        self.highGamma = newHighGamma
                        self.putMindflexMessage(('Arduino_highGamma',self.highGamma))
                except:
                    print line
                    print "Caught Mindflex serial error!"
            elif eyeCircuitActive and ('EMG:' in line):
                line = line.split(':')
                line = line[1].split(',')
                try:
                    if not len(line) == 1:
                        raise ValueError
                    newEyeSignal = int(line[0])

                    if self.eyeSignal != newEyeSignal:
                        self.eyeSignal = newEyeSignal
                        self.putEyeCircuitMessage(('Arduino_eyeValue',
                                                    self.eyeSignal))

                except Exception as e:
                    print e
                    print "Caught EMG circuit serial error!",line


        try:
            ser.close()
            print "Arduino Serial Connection Closed"
        except:
            print "Unable to close serial connection to Arduino!"

    def putEyeCircuitMessage(self, message):
        while self.eyeCircuitQueue.full():
            self.eyeCircuitQueue.get()
        self.eyeCircuitQueue.put(message)

    def putMindflexMessage(self, message):
        while self.mindflexQueue.full():
            self.mindflexQueue.get()
        self.mindflexQueue.put(message)

    def deactivate(self):
        self.active.value = 0
        print("Closed Arduino Process")

class Biofeedback(AltInput):
    def __init__(self, deviceID, mindFlexActive=True, eyeCircuitActive=True):
        self.arduino = Arduino()
        self.arduino.listen(deviceID, mindFlexActive, eyeCircuitActive)

    def poll(self):
        return (not self.arduino.mindflexQueue.empty() or
                not self.arduino.eyeCircuitQueue.empty())

    def getEvents(self):
        events = []

        if not self.arduino.mindflexQueue.empty():
            reading = self.arduino.mindflexQueue.get()
            identifier = reading[0]
            value = reading[1]
            discrete = False #All of the bio-feedback events we use are continuous values
            mindflexReading = self.makeEvent(identifier, value, discrete)
            events.append(mindflexReading)

        if not self.arduino.eyeCircuitQueue.empty():
            reading = self.arduino.eyeCircuitQueue.get()
            identifier = reading[0]
            value = reading[1]
            discrete = False #All of the bio-feedback events we use are continuous values
            eyeCircuitReading = self.makeEvent(identifier, value, discrete)
            events.append(eyeCircuitReading)

        return events

    def stop(self):
        self.arduino.deactivate()

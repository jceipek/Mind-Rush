#
# Mind Rush!
# A bio-feedback defense game written in Python, Java, and MATLAB
#
# Copyright (C)2011 Julian Ceipek and Patrick Varin
#
# Redistribution is permitted under the BSD license.  See LICENSE for details.
#

import pygame, os, sys, multiprocessing

#Debugging Globals:
enableMindFlex = False #Change this to enable a hacked Mindflex headset connected to a Sun SPOT
enableEyeCircuit = False #Change this to enable an eye movement EMG circuit connected to a National Instruments NI USB-6009 data acquisition device and accessed via MATLAB
#------------------

#Identifiers:
SunID = "0000.0000" #Change this to match the ID of your Sun SPOT
#------------------

class TrueProcess(multiprocessing.Process):
    def __init__(self, target, *args):
        multiprocessing.Process.__init__(self, target=target, args=args)
        self.start()

class MindReader():
    def __init__(self):
        self.active = multiprocessing.Value('i',1)
        self.readyState = multiprocessing.Value('i',0)
        self.attention = multiprocessing.Value('i',200)
        self.meditation = multiprocessing.Value('i',200)
        self.quality = multiprocessing.Value('i',200)
        self.line = ""

        self.daemon = TrueProcess(self.readConstantly)

    def valueFromStr(self,line,astr,old,invertVal = None):
        if astr in line:
            val = int(line[line.find(astr)+len(astr):])
            #print line,astr,val
            if invertVal:
                return invertVal - val
            return val
        return old

    def isGoodSignal(self):
        return self.quality.value == 0

    def getSignalQuality(self):
        return (200.0-self.quality.value)/2.0

    def getAttentionValue(self):
        return (200.0-self.attention.value)/2.0

    def getMeditationValue(self):
        return (200.0-self.meditation.value)/2.0

    def readConstantly(self):
        import time
        if enableMindFlex:
            self.spotMonitor = os.popen("ant run 0014.4F01"+SunID)
            print("Attempting to Initialize SPOT...")
            from time import time,sleep
            elapsed = 0
            lastTime = time()
            while not "SPOT serial number" in self.line:
                if self.line != "":
                    elapsed = 0
                    lastTime = time()
                    print self.line
                else:
                    elapsed = time() - lastTime
                    if elapsed > 5:
                        self.deactivate()
                        print("Unable to connect to MindFlex via SPOT")
                        break
                self.line = self.spotMonitor.readline().strip()

        if self.activeState():
            self.readyState.value = 1
            print("Connection to hacked MindFlex established.")

        while self.activeState():
            if enableMindFlex:
                self.line = self.spotMonitor.readline().strip()
                if "[java] " in self.line:
                    self.line = self.line[self.line.find("[java]")+len("[java] "):]
                    print self.line
                    self.quality.value = self.valueFromStr(self.line,"QUALITY: ",self.quality.value)
                    self.attention.value = self.valueFromStr(self.line,"ATTENTION: ",self.attention.value)
                    self.meditation.value = self.valueFromStr(self.line,"MEDITATION: ",self.meditation.value)
                    sleep(0.01)
            else:
                self.quality.value = 0
                self.attention.value = 100
                self.meditation.value = 200
        print("Connection to hacked MindFlex closed.")

    def activate(self):
        self.active.value = 1

    def deactivate(self):
        self.active.value = 0

    def activeState(self):
        return self.active.value == 1

    def getReadyState(self):
        return self.readyState.value

class EyeReader():
    def __init__(self):
        self.active = multiprocessing.Value('i',1)
        self.readyState = multiprocessing.Value('i',0)
        self.direction = multiprocessing.Value('i',0)
        self.count = 0;
        self.daemon = TrueProcess(self.readConstantly)

    def deactivate(self):
        self.active.value = 0

    def activate(self):
        self.active.value = 1

    def activeState(self):
        return self.active.value == 1

    def getReadyState(self):
        return self.readyState.value

    def calibrate(self):
        self.session.run("[nMin,cLine,nMax] = calibrateNoiseCutoffs(Init_NI,Init_sampleRate);")
        print("Calibration complete!")
        self.readyState.value = 2

    def readConstantly(self):
        if enableEyeCircuit:
            from pymatlab.matlab import MatlabSession
        import time
        initialized = 0
        if enableEyeCircuit:
            import os
            print("Opening MATLAB session...")
            self.session = MatlabSession('matlab -nojvm -nodisplay')
            print("Attempting to connect to DAQ...")
            self.session.run("cd "+os.path.join(os.getcwd(),"daq"))
            self.session.run("Init") #Initializes DAQ and starts recording
            initialized = int(self.session.getvalue("Init_initialized"))
            if initialized == 0:
                print("DAQ Initialization failed. Ensure that the DAQ software is installed and try closing all open MATLAB Processes.")
                self.deactivate()
            else:
                print("Connected to DAQ")
                self.readyState.value = 1
                print("Calibrating Eye Circuit...")
                self.calibrate()
                self.session.run("oldVal = 0")

            while self.activeState():
                if enableEyeCircuit:
                    self.session.run("signal = monitor(Init_NI,Init_sampleRate,nMin,cLine,nMax,oldVal);")
                    self.session.run("oldVal = signal;")
                    self.direction.value = int(self.session.getvalue("signal"))
                    time.sleep(0.01)
                    self.count += 1
                    if self.count > 100:
                        self.session.run("refreshDevice(Init_NI);")
                        self.count = 0
        if enableEyeCircuit:
            print("Closing MATLAB Session...")
            if initialized == 1:
                self.session.run("Cleanup;")
            self.session.close()
            print("MATLAB Session Closed!")

    def getDirection(self):
        if self.direction == None:
            return 0
        else:
            return self.direction.value

class Window():
    def __init__(self,manager):
        self.active = True
        self.manager = manager
        self.resolution = (1440,800)
        self.displaySurface = None #Set in openPygame
        self.openPygame()
        self.run()

    def openPygame(self):
        pygame.init()
        pygame.key.set_repeat(1,10)
        pygame.display.set_caption('Boulder Defense!')
        self.displaySurface = pygame.display.set_mode(self.resolution,pygame.FULLSCREEN)
        #self.displaySurface = pygame.display.set_mode(self.resolution)
        self.manager.loaded()
        self.gameClock = pygame.time.Clock()
        self.maxFPS = 60
        self.gameTime = 0

    def run(self):
        newBoulderEvent = pygame.USEREVENT
        pygame.time.set_timer(newBoulderEvent, 700)

        newCodeFragmentEvent = pygame.USEREVENT+1
        pygame.time.set_timer(newCodeFragmentEvent, 100)

        from math import sin
        import time

        while self.active:
            self.gameFrametime = self.gameClock.tick(self.maxFPS)
            self.gameTime += self.gameFrametime

            for event in pygame.event.get():
                if self.manager.active == False:
                    self.active = False
                    print("Closing...")
                if event.type == pygame.QUIT:
                    self.active = False
                    self.manager.close()
                    print("Closing...")
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.manager.moveLeft(self.gameFrametime)
                    elif event.key == pygame.K_RIGHT:
                        self.manager.moveRight(self.gameFrametime)
                    elif event.key == pygame.K_SPACE:
                        self.manager.killBoulders()
                    elif event.key == pygame.K_ESCAPE:
                        self.active = False
                        self.manager.close()
                        print("Closing...")
                elif event.type == newBoulderEvent:
                    self.manager.addBoulder()
                elif event.type == newCodeFragmentEvent:
                    self.manager.addCodeFragment()

            self.displaySurface.fill((0,0,0))
            self.manager.update(self.gameFrametime,self.gameTime)
            self.manager.draw(self.displaySurface)
            pygame.display.flip()
        time.sleep(1)
        sys.exit()

class Bar():
    """
    Credits:
    ----------------------------------------------------------------
    From Complete-Galactic-Dominion's Overlay module, by
    Julian Ceipek and Patrick Varin, Jared Kirschner, Patrick Varin, and Berit Johnson
    """
    def __init__(self,maxValue,barWidth,barHeight,fullness=1.0,fullColor=(0,255,0),emptyColor=(255,0,0)):
        from pygame import Surface
        self.maxValue = maxValue
        self.fullness = fullness
        self.fullColor = fullColor
        self.emptyColor = emptyColor
        self.barWidth = barWidth
        self.barHeight = barHeight

        self.surface = pygame.Surface((self.barWidth,self.barHeight))

    def updateBarWithValue(self,value):
        """
        Updates the self.surface to reflect the new value.
        """
        value = max(0,value)
        self.fullness = (float(value)/self.maxValue)

        valueRemaining = int(self.fullness*self.barWidth)
        valueRemainingRect = (0,0,int(self.fullness*self.barWidth),self.barHeight)
        valueLost = (valueRemaining,0,self.barWidth-valueRemaining,self.barHeight)

        self.surface.fill(self.fullColor, valueRemainingRect)
        self.surface.fill(self.emptyColor, valueLost)

    def draw(self,surface,pos):
        surface.blit(self.surface,(pos,(self.barWidth,self.barHeight)))

class DrawableObject():
    def __init__(self,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.alive = True
    def draw(self,surface):
        if self.alive:
            surface.blit(self.image,self.rect)
    def updateImagePos(self):
        if self.alive:
            self.rect.center = tuple(self.pos)

class Boulder(DrawableObject):
    def __init__(self,image,mask,pos=None):
        if pos == None:
            self.pos = [1440/2,30]
        else:
            self.pos = pos
        DrawableObject.__init__(self,image)
        self.mask = mask
        self.updateImagePos()
        self.vel = 5
        self.setDifficulty()

    def setDifficulty(self):
        from random import randint
        self.difficulty = randint(0,5)

    def fall(self,frameTime,gameTime):
        from math import sin, cos
        if self.alive:
            if self.difficulty >= 0 and self.difficulty <= 2:
                self.pos[1] += self.vel*frameTime
            elif self.difficulty >= 3 and self.difficulty <= 4:
                self.pos[0] += (self.difficulty-4.0)*self.vel*frameTime
                self.pos[1] += self.vel*frameTime
            elif self.difficulty == 5:
                self.pos[1] += 3.0*frameTime
                self.pos[0] += 2.0*sin(self.pos[1])*frameTime
            if self.pos[1] > 800-128/2-20:
                self.alive = False
            else:
                self.updateImagePos()

class Fragment(DrawableObject):
    def __init__(self,image,pos):
        self.alive = True
        self.pos = pos
        DrawableObject.__init__(self,image)
        self.mask = pygame.mask.from_surface(self.image)
        self.updateImagePos()
        self.vel = [0,0]

    def move(self,frameTime):
        self.pos[0] += self.vel[0]*frameTime
        self.pos[1] += self.vel[1]*frameTime
        if self.pos[0] > 1540 or self.pos[0] < -100 or self.pos[1] > 1000 or self.pos[1] < -100:
            self.alive = False
        self.updateImagePos()

class Ship(DrawableObject):
    def __init__(self,image,pos=[1440/2,700]):
        self.pos = pos
        DrawableObject.__init__(self,image)
        self.mask = pygame.mask.from_surface(self.image)
        self.updateImagePos()
        self.health = 200
        self.laserCharge = 0

    def moveLeft(self,dist):
        if self.pos[0] - dist >= 78/2:
            self.pos[0] -= dist
        else:
            self.pos[0] = 78/2
        self.updateImagePos()

    def moveRight(self,dist):
        if self.pos[0] + dist <= 1440-78/2:
            self.pos[0] += dist
        else:
            self.pos[0] = 1440-78/2
        self.updateImagePos()

class CodeFragment(DrawableObject):
    specialText = None
    count = 0
    maxCount = 0
    def __init__(self,font,pos):
        self.font = font

        if CodeFragment.specialText == None:
            f = open("mindRush.py")
            CodeFragment.specialText = f.readlines()
            CodeFragment.maxCount = len(CodeFragment.specialText)
            f.close()

        if CodeFragment.count+1 >= CodeFragment.maxCount:
            CodeFragment.count = 0

        words = CodeFragment.specialText[CodeFragment.count].strip()
        CodeFragment.count += 1

        text = self.font.render(words,1,(255,140,0))
        self.pos = pos
        self.alive = True
        DrawableObject.__init__(self,text)

    def move(self,frameTime):
        self.pos[1] += frameTime/3
        if self.pos[0] > 1540 or self.pos[0] < -100 or self.pos[1] > 1000 or self.pos[1] < -100:
            self.alive = False
        self.updateImagePos()

class GameManager():
    def loaded(self):
        self.shipImage = pygame.image.load("ship.png").convert_alpha()
        self.ship = Ship(self.shipImage)
        self.boulders = []
        self.fragments = []
        self.codeFragments = []
        self.healthBar = Bar(200,1440,20,fullness=1.0,fullColor=(0,180,255),emptyColor=(100,100,100))
        self.laserBar = Bar(100,1440,20,fullness=1.0,fullColor=(0,255,180),emptyColor=(100,100,100))
        self.healthBar.updateBarWithValue(self.ship.health)
        self.qualityBar = Bar(100,800,20,fullness=1.0,fullColor=(180,180,180),emptyColor=(0,0,0))
        self.attentionBar = Bar(100,800,20,fullness=1.0,fullColor=(180,180,180),emptyColor=(0,0,0))
        self.laserBar.updateBarWithValue(0)
        self.mindReader = MindReader()
        self.eyeReader = EyeReader()
        if enableEyeCircuit == False and enableMindFlex == False:
            self.state = "Playing Game"
        else:
            if enableEyeCircuit == True:
                self.state = "Waiting for MATLAB"
            elif enableMindFlex == True:
                self.state = "Waiting for SunSPOT"
        self.font = pygame.font.Font(pygame.font.get_default_font(), 25)
        self.active = True
        self.text = None
        self.boulderImage = pygame.image.load("boulder.png").convert_alpha()
        self.fragmentImage = pygame.image.load("fragment.png").convert_alpha()
        self.boulderMask = self.mask = pygame.mask.from_surface(self.boulderImage)

        pygame.mixer.music.load("Music.ogg")
        pygame.mixer.music.play(-1, 0.0)

    def addBoulder(self):
        if self.state == "Playing Game":
            from random import randint
            newBoulder = Boulder(self.boulderImage,self.boulderMask,[randint(0,1440),-100])
            newBoulder.vel = randint(1,20)/10.0
            self.boulders.append(newBoulder)

    def addCodeFragment(self):
        if self.state == "Playing Game":
            from random import randint
            newCodeFragment = CodeFragment(self.font,[randint(0,1440),-100])
            self.codeFragments.append(newCodeFragment)

    def moveRight(self,frameTime):
        if self.state == "Playing Game":
            self.ship.moveRight(frameTime)

    def moveLeft(self,frameTime):
        if self.state == "Playing Game":
            self.ship.moveLeft(frameTime)

    def update(self,frameTime,gameTime):
        if self.state == "Playing Game":
            for b in self.boulders:
                b.fall(frameTime,gameTime)
                if not b.alive:
                    self.addExplosion(list(b.pos))
                    self.boulders.remove(b)
            for f in self.fragments:
                f.move(frameTime)
                if not f.alive:
                    self.fragments.remove(f)
            for c in self.codeFragments:
                c.move(frameTime)
                if not c.alive:
                    self.codeFragments.remove(c)
            self.testColl()
            direction = self.eyeReader.getDirection()
            #print("     DIR I SEE:"+str(direction))
            if direction == 1:
                self.moveLeft(frameTime)
            if direction == -1:
                self.moveRight(frameTime)

            if enableMindFlex:
                attention = self.mindReader.getAttentionValue()
                self.laserBar.updateBarWithValue(attention)
                pygame.mixer.music.set_volume(attention/100.0)
                if attention > 80:
                    self.killBoulders()
                if not self.mindReader.isGoodSignal():
                    self.state = "Waiting for MindFlex"
                    pygame.mixer.music.pause()
                    print(self.state)
        elif self.state == "Waiting for MindFlex":
            if self.mindReader.isGoodSignal():
                self.state = "Playing Game"
                print("Reconnected to MindFlex")
                pygame.mixer.music.unpause()
                self.text = None
                if self.ship.health <= 0:
                    self.state = "Game Over"
                    pygame.mixer.music.pause()
                    print("GAME OVER!")
        elif self.state == "Waiting for Eye Circuit":
            if self.eyeReader.getReadyState() == 2:
                if enableMindFlex == True:
                    self.state = "Waiting for SunSPOT"
                    self.text = None
                else:
                    self.state = "Playing Game"
                    self.text = None
        elif self.state == "Waiting for MATLAB":
            if self.eyeReader.getReadyState() > 0:
                self.state = "Waiting for Eye Circuit"
                self.text = None
        elif self.state == "Waiting for SunSPOT":
            if self.mindReader.getReadyState() == 1:
                self.state = "Waiting for MindFlex"
                self.text = None
        if self.state == "Waiting for MindFlex":
            self.qualityBar.updateBarWithValue(self.mindReader.getSignalQuality())

        if self.state == "Game Over":
            self.attentionBar.updateBarWithValue(self.mindReader.getAttentionValue()+(100-90))
            if self.mindReader.getAttentionValue() >= 90:
                self.state = "Playing Game"
                self.ship.health = 200
                self.healthBar.updateBarWithValue(200)
                pygame.mixer.music.unpause()
            if not self.mindReader.isGoodSignal():
                self.state = "Waiting for MindFlex"
                pygame.mixer.music.pause()
                self.text = None
                print(self.state)
        if self.mindReader.activeState() == False:
            self.close()

    def testColl(self):
        if self.state == "Playing Game":
            def distance(x1,x2):
                return (int(x1[0]-x2[0]),int(x1[1]-x2[1]))

            for b in self.boulders:
                if b.rect.colliderect(self.ship.rect):
                    shipCorner = list(self.ship.pos)
                    shipCorner[0] += 78/2
                    if not b.mask.overlap(self.ship.mask,tuple(distance(shipCorner,b.pos))) == None and b.alive:
                        self.ship.health -= 20
                        if self.ship.health <= 0:
                            self.state = "Game Over"
                            pygame.mixer.music.pause()
                            print("GAME OVER!")
                            self.text = None
                        self.healthBar.updateBarWithValue(self.ship.health)
                        b.alive = False
                        self.addExplosion(b.pos)

    def killBoulders(self):
        for b in self.boulders:
            b.alive = False
            self.addExplosion(list(b.pos))

    def addExplosion(self,pos):
        from random import randint
        from math import sin,cos
        for i in xrange(8):
            newFragment = Fragment(self.fragmentImage,list(pos))
            newFragment.vel = [cos((2*3.14159)/8.0*i),sin((2*3.14159)/8.0*i)]
            self.fragments.append(newFragment)

    def draw(self,surface):
        if self.state == "Playing Game":
            for c in self.codeFragments:
                c.draw(surface)
            for b in self.boulders:
                b.draw(surface)
            for f in self.fragments:
                f.draw(surface)
            self.ship.draw(surface)
            self.healthBar.draw(surface,(0,0))
            self.laserBar.draw(surface,(0,800-20))
        elif self.state == "Waiting for MATLAB":
            if not self.text:
                self.text = self.font.render("Setting up MATLAB. Get ready to relax and stare at the screen.",1,(255,255,255))
            pygame.draw.rect(surface,(255,255,0),(20,20,1440-40,800-40))
            surface.blit(self.text,(300,300))
        elif self.state == "Waiting for Eye Circuit":
            if not self.text:
                self.text = self.font.render("Calibrating to your eyes. Stare at these words...",1,(255,255,255))
            pygame.draw.rect(surface,(0,0,255),(20,20,1440-40,800-40))
            surface.blit(self.text,(300,300))
        elif self.state == "Waiting for MindFlex":
            if not self.text:
                self.text = self.font.render("Quality of connection to hacked MindFlex device has degraded:",1,(255,255,255))
            pygame.draw.rect(surface,(255,0,0),(20,20,1440-40,800-40))
            surface.blit(self.text,(300,300))
            self.qualityBar.draw(surface,(300,340))
        elif self.state == "Waiting for SunSPOT":
            if not self.text:
                self.text = self.font.render("Waiting for SunSPOT...",1,(255,255,255))
            pygame.draw.rect(surface,(255,140,0),(20,20,1440-40,800-40))
            surface.blit(self.text,(300,300))
            self.qualityBar.draw(surface,(300,340))
        elif self.state == "Game Over":
            if not self.text:
                self.text = self.font.render("Game Over! Concentrate in order to Restart!",1,(255,255,255))
            pygame.draw.rect(surface,(255,0,0),(20,20,1440-40,800-40))
            surface.blit(self.text,(300,300))
            self.attentionBar.draw(surface,(300,340))

    def close(self):
        self.state = "Closing"
        self.mindReader.deactivate()
        self.eyeReader.deactivate()
        self.active = False

if __name__ == "__main__":
    manager = GameManager()
    gameWindow = Window(manager)

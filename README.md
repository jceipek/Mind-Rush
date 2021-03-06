#Mind|Rush

![Mind|Rush Eyes](https://github.com/jceipek/Mind-Rush/blob/master/screenshots/eyes.png?raw=true "Controlled by your eyes!")
![Mind|Rush Action](https://github.com/jceipek/Mind-Rush/blob/master/screenshots/gameplay.png?raw=true "Mind Rush in action")

##About:

Mind|Rush is an obstacle avoidance game in the style of classic
"boulder dodge" style games.

What makes Mind|Rush unique is that it supports bio-feedback control in the 
form of eye-movement and concentration.

>I created the original program as part of my Real World Measurements course
as a Freshman at Franklin W. Olin College of Engineering. After the course 
was over, I teamed up with Patrick Varin to make an improved version that 
uses an Arduino and an EMG that can map your eye movement directly onto a
computer screen.

-Julian Ceipek


##Basic Dependencies (no biofeedback devices):

- Python 2.6 (other versions untested but should work)
- pygame


##Biofeedback Device Hardware Requirements/Dependencies
(The new version of Mind|Rush supports only eye control, but mind control
will be easy to add in the future)

- pyserial
- An Arduino (we used the Arduino UNO) with a USB cable connected to a 
  battery-powered laptop
- The Arduino Brain Library (https://github.com/kitschpatrol/Arduino-Brain-Library)
- The circuit detailed in `./eyeCircuit.png`. It can be built on a breadboard.


##Running:

The new version of Mind|Rush is extremely simple to set up in comparison
to the version in `./old`. It currently only supports eye control, but
EEG control via a Mattel Mindflex headset is planned in the near future.

To run it without any biofeedback devices, simply run `python mindrush.py`


##Running with eye control:

WARNING: If you choose to use the Mind|Rush project hardware, you do so 
ENTIRELY AT YOUR OWN RISK.

The hardware designs are distributed in the hope that they will be useful, 
but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE.

Note that CONNECTING A DEVICE VIA ELECTRODES TO HUMANS OR ANIMALS IS POTENTIALLY 
HAZARDOUS AND MAY RESULT IN ELECTRIC SHOCK AND/OR SEIZURE.

The authors do not guarantee that the information provided in the design files 
is complete or appropriate for any particular application.

adapted from the OpenEEG WARNING.txt file, which you should read in order to
  better understand the risks associated with using non-medically approved
  hardware (http://openeeg.sourceforge.net/doc/WARNING.html).

1. Build the circuit depicted in `./eyeCircuit.png`
2. Connect the left_eye input to an electrode on your left temple.
3. Connect the right_eye input to an electrode on your right temple. 
4. Connect the forehead input to an electrode on your forehead.
5. Uploa the code in `./hardware/arduinoEyeAndBrain/arduinoEyeAndBrain.pde` to the Arduino 
   (it depends on https://github.com/kitschpatrol/Arduino-Brain-Library for the unused 
    EEG component. Having this installed will cause no problems if you have no EEG, but
    you can easily modify the Arduino code not to rely on the brain library)
5. Connect the Arduino A0 pin to the output in the diagram.
6. Connect the Arduino's 5V power rail to the circuit. This requires basic
   circuitry experience because the circuit requires 2.5V power at several
   locations.
7. After checking the circuit thoroughly, connect the Arduino to a *battery*
   powered laptop. Connecting your head to a computer powered by a wall outlet
   could, in the unlikely event of a system failure or power surge, result
   in brain damage or death. Do NOT do this.
8. Modify the commented section of `./mindrush.py` as necessary.


##Running with Concentration Control from an EEG

See the README in `./old`


##Credits

###Game R&D:
- Patrick Varin
- Julian Ceipek

###Circuit:
- Patrick Varin
- Berit Johnson
- Brendan Quinlivan
- Chase Kernan
- Katherine Stegner

###Integration:
- Julian Ceipek


##Source Code

All of the code in the project is licensed under the open source BSD
license, which basically means that it can be reused and modified in free
and proprietary software as long as the original copyright notice is
preserved.


##Updates:

###5/10/11:
- Mind|Rush fully supports eye movement-driven operation
- Mindflex EEG devices are supported but not used
- Basic gameplay and scoring is implemented

###5/7/11:
- Patrick Varin and Julian Ceipek are on their way to making an extensible architecture
- On the hardware side, we are switching to using an Arduino for data acquisition
- We intend to use a more powerful EMG circuit that Patrick Varin helped design
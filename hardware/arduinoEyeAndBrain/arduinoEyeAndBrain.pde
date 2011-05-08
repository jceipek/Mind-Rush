//
// arduinoEyeAndBrain.pde - reads from the A0 analog pin and the RX digital pin
// to get values from the EEG and EMG
//
// Based on "brain example" by Eric Mika, 2010
//

#include <Brain.h>

// Set up the brain parser, pass it the hardware serial object you want to listen on.
Brain brain(Serial);

int eyeSensorPin = A0;    // select the input pin for the EMG
int eyeSensorValue = 0;

void setup() {	
	// Start the hardware serial.
	Serial.begin(9600);
}

void loop() {
	// Expect packets about once per second.
	if (brain.update()) {
		Serial.println("EEG:"+String(brain.readCSV())); //Reads from the Mindflex EEG
	}
	
        //Read from the EMG circuit:
        eyeSensorValue = analogRead(eyeSensorPin);
        Serial.println("EMG:"+String(eyeSensorValue));
	
}

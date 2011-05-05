/*
 * SensorSampler.java
 *
 * Copyright (c) 2008 Sun Microsystems, Inc.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to
 * deal in the Software without restriction, including without limitation the
 * rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
 * sell copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
 * DEALINGS IN THE SOFTWARE.
 */
package org.mindrush.eegreader;

import com.sun.spot.sensorboard.EDemoBoard;
//import com.sun.spot.io.j2me.radiogram.*;
import com.sun.spot.sensorboard.peripheral.ITriColorLED;
import com.sun.spot.peripheral.radio.RadioFactory;
import com.sun.spot.util.BootloaderListener;
import com.sun.spot.util.Utils;
//import javax.microedition.io.*;
import javax.microedition.midlet.MIDlet;
import javax.microedition.midlet.MIDletStateChangeException;


/**
 * This application is the 'on SPOT' portion of the SendDataDemo. It
 * periodically samples a sensor value on the SPOT and transmits it to
 * a desktop application (the 'on Desktop' portion of the SendDataDemo)
 * where the values are displayed.
 *
 * @author: Vipul Gupta
 * modified: Ron Goldman
 */
public class SensorSampler extends MIDlet {

    //private static final int HOST_PORT = 67;

    protected void startApp() throws MIDletStateChangeException {
        new BootloaderListener().start();
        //RadiogramConnection rCon = null;
        //Datagram dg = null;
        //String ourAddress = System.getProperty("IEEE_ADDRESS");
        long now = 0L;

        //EEG Setup
        byte recv;
        EDemoBoard board = EDemoBoard.getInstance();
        RadioFactory.getSleepManager().disableDeepSleep();
        board.initUART(9600, false); //Set the device to read as quickly as the Arduino

        ITriColorLED[] leds = EDemoBoard.getInstance().getLEDs();

        MindData mData = new MindData();
        //System.out.println("Starting sensor sampler application on " + ourAddress + " ...");
        //new com.sun.spot.util.BootloaderListener().start();       // Listen for downloads/commands over USB connection
        //try {
            // Open up a broadcast connection to the host port
            // where the 'on Desktop' portion of this demo is listening
        //    rCon = (RadiogramConnection) Connector.open("radiogram://broadcast:" + HOST_PORT);
        //    dg = rCon.newDatagram(50);  // only sending 12 bytes of data
        //} catch (Exception e) {
        //    System.err.println("Caught " + e + " in connection initialization.");
            //System.exit(1);
        //}

        boolean parsed = false;

        leds[7].setOn();

        while (true) {

            now = System.currentTimeMillis();

            try {
                recv = board.readUART();
                //System.out.println(""+byteToHex(recv));
                
                if (recv == (byte) (0xAA)) {
                    //System.out.println("1 Sync!");
                    leds[0].setRGB(0, 255, 0);
                    leds[0].setOn();

                    recv = board.readUART();
                    //System.out.println(""+byteToHex(recv));
                    leds[0].setOff();

                    if (recv == (byte) (0xAA)) //Sync again!
                    {
                        //System.out.println("2 Sync!");
                        leds[0].setRGB(255, 255, 0);
                        leds[0].setOn();

                        recv = board.readUART();
                        //System.out.println(""+byteToHex(recv));
                        leds[0].setOff();

                        while (recv == (byte) 0xAA) {
                            recv = board.readUART();
                            //System.out.println(""+byteToHex(recv));
                            //System.out.println("Still 170");
                        }

                        if (unsignedByteToInt(recv) < 170) {
                            leds[0].setRGB(0, 255, 255);
                            leds[0].setOn();
                            //System.out.println("Plength! : "+((int)recv));

                            int plength = unsignedByteToInt(recv);
                            int checksum = 0;
                            byte payload[] = new byte[plength];
                            for (int i = 0; i < plength; i++) {
                                recv = board.readUART();
                                //System.out.println(""+byteToHex(recv));
                                payload[i] = recv;
                                checksum += unsignedByteToInt(recv);
                                leds[0].setOff();
                            }
                            //System.out.println("Checksum: "+checksum);
                            checksum = (byte)(checksum & 0xFF);
                            checksum = (byte)((~checksum) & 0xFF);
                            //System.out.println("Inverted Checksum: "+checksum);
                            recv = board.readUART();
                            //System.out.println(""+byteToHex(recv));
                            //System.out.println("Real Checksum: "+recv);

                            parsed = true;
                            if (checksum == recv) {
                                System.out.println("Parsing!");
                                System.out.println("");
                                mData = parseData(payload, plength);
                                setIntensity(leds, 200-mData.attention);
                                if (mData.quality == 0){
                                    leds[7].setRGB(0, 255, 0);
                                } else {

                                    if (mData.quality > 0){
                                        leds[7].setRGB(50, 50, 0);
                                    }
                                    
                                    if (mData.quality > 100){
                                        leds[7].setRGB(255, 0, 0);
                                    }                 
                                }
                                System.out.println("");
                            } else {
                                System.err.println("CHKSUM FAILED");
                            }
                        }
                    }
                }


                if (parsed) {
                    parsed = false;
                    //Sleep to conserve battery.
                    Utils.sleep(500 - (System.currentTimeMillis() - now));
                }



                // Package the time and sensor reading into a radio datagram and send it.
                //dg.reset();
                //dg.writeLong(now);
                //dg.writeInt(reading);
                //rCon.send(dg);

                //System.out.println("Serial value = " + reading);


            } catch (Exception e) {
                //System.err.println("Caught " + e + ".");
            }
        }
    }


    public void setIntensity(ITriColorLED[] leds, int reading)
    {
                    if (reading>120)
                {
                    leds[1].setRGB(255, 255, 0);
                    leds[1].setOn();
                    leds[2].setOff();
                    leds[3].setOff();
                    leds[4].setOff();
                    leds[5].setOff();
                    leds[6].setOff();
                }
                if (reading>140)
                {
                    leds[2].setRGB(255, 255, 0);
                    leds[2].setOn();
                    leds[3].setOff();
                    leds[4].setOff();
                    leds[5].setOff();
                    leds[6].setOff();
                }
                if (reading>160)
                {
                    leds[3].setRGB(255, 255, 0);
                    leds[3].setOn();
                    leds[4].setOff();
                    leds[5].setOff();
                    leds[6].setOff();
                }
                if (reading>170)
                {
                    leds[4].setRGB(255, 255, 0);
                    leds[4].setOn();
                    leds[5].setOff();
                    leds[6].setOff();
                }
                if (reading>180)
                {
                    leds[5].setRGB(255, 255, 0);
                    leds[5].setOn();
                    leds[6].setOff();
                }
                if (reading>190)
                {
                    leds[6].setRGB(255, 255, 0);
                    leds[6].setOn();
                }
    }

    public MindData parseData(byte[] data, int plength) {

        MindData mData = new MindData();

        int bytesParsed = 0;
        int extendedCodeLevel;
        byte code;
        byte[] bigEndian = new byte[3];
        int length;
        while (bytesParsed < plength) {
            extendedCodeLevel = 0;
            while (data[bytesParsed] == ((byte) 0x55)) {
                extendedCodeLevel++;
                bytesParsed++;
            }
            code = data[bytesParsed++];
            if (unsignedByteToInt(code) >= unsignedByteToInt((byte) 0x80)) {
                length = unsignedByteToInt(data[bytesParsed++]);
            } else {
                length = 1;
            }
            //System.out.println("EXCODE lvl: "+extendedCodeLevel);
            //System.out.println("CODE: "+byteToHex(code));
            //System.out.println("VLENGTH: "+length);

            for (int i = 0; i < length; i++) {

                if (code == ((byte) 0x05)) {
                    System.out.println("MEDITATION: " + (unsignedByteToInt(data[bytesParsed + i])));
                    mData.meditation = unsignedByteToInt(data[bytesParsed + i]);
                } else if (code == ((byte) 0x04)) {
                    System.out.println("ATTENTION: " + (unsignedByteToInt(data[bytesParsed + i])));
                    mData.attention = unsignedByteToInt(data[bytesParsed + i]);
                } else if (code == ((byte) 0x02)) {
                    System.out.println("QUALITY: " + (unsignedByteToInt(data[bytesParsed + i])));
                    mData.quality = unsignedByteToInt(data[bytesParsed + i]);
                } else if (code == ((byte) 0x83)) {
                    if (i%3 == 0) {
                        System.out.println("");
                    }
                    bigEndian[i%3] = data[bytesParsed + i];
                    if (i%3 == 2) {
                        mData.eegPower[(i+1)/3 - 1] = unsignedByteArryToLong(bigEndian);

                        switch((i+1)/3 - 1)
                        {
                        case 0:
                          System.out.println("DELTA_POWER: " + mData.eegPower[(i+1)/3 - 1]);
                          break;
                        case 1:
                          System.out.println("THETA_POWER: " + mData.eegPower[(i+1)/3 - 1]);
                          break;
                        case 2:
                          System.out.println("LOW_ALPHA_POWER: " + mData.eegPower[(i+1)/3 - 1]);
                          break;
                        case 3:
                          System.out.println("HIGH_ALPHA_POWER: " + mData.eegPower[(i+1)/3 - 1]);
                          break;
                        case 4:
                          System.out.println("LOW_BETA_POWER: " + mData.eegPower[(i+1)/3 - 1]);
                          break;
                        case 5:
                          System.out.println("HIGH_BETA_POWER: " + mData.eegPower[(i+1)/3 - 1]);
                          break;
                        case 6:
                          System.out.println("LOW_GAMMA_POWER: " + mData.eegPower[(i+1)/3 - 1]);
                          break;
                        case 7:
                          System.out.println("MID_GAMMA_POWER: " + mData.eegPower[(i+1)/3 - 1]);
                          break;
                        default:
                          System.out.println("ASIC_EEG_POWER: " + mData.eegPower[(i+1)/3 - 1]);
                        }
                    }
                    

                } else if (code == ((byte) 0x80)) {
                    System.out.println("RAW_WAVE_VALUE: " + (unsignedByteToInt(data[bytesParsed + i])));
                }
                
                //System.out.println("Data: "+((int)data[bytesParsed+i]));
            }

            bytesParsed += length;
            
        }
        return mData;
    }

    public static int unsignedByteToInt(byte b) {
        return (int) b & 0xFF;
    }

    public static String byteToHex(byte b) {
        int i = b & 0xFF;
        return Integer.toHexString(i);
    }


    public static final long unsignedByteArryToLong(byte[] b)
    {
        long l = 0;
        l |= b[0] & 0xFF;
        l <<= 8;
        l |= b[1] & 0xFF;
        l <<= 8;
        l |= b[2] & 0xFF;
        return l;
    }

    protected void pauseApp() {
        // This will never be called by the Squawk VM
    }

    protected void destroyApp(boolean arg0) throws MIDletStateChangeException {
        // Only called if startApp throws any exception other than MIDletStateChangeException
    }
}

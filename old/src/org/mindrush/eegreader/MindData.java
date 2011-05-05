/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package org.mindrush.eegreader;

/**
 *
 * @author julian
 */
public class MindData {

    public int quality;
    public int attention;
    public int meditation;
    public int blinkStr;

    public long[] eegPower;
    public int delta;
    public int theta;
    public int lowAlpha;
    public int highAlpha;
    public int lowBeta;
    public int highBeta;
    public int lowGamma;
    public int midGamma;

    public MindData(){
        quality = 255;
        attention = 100;
        meditation = 100;
        blinkStr = 255;

        eegPower = new long[8];

        delta = 0;
        theta = 0;
        lowAlpha = 0;
        highAlpha = 0;
        lowBeta = 0;
        highBeta = 0;
        lowGamma = 0;
        midGamma = 0;
    }

}

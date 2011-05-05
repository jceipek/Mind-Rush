function [noiseMin,centerline,noiseMax] = calibrateNoiseCutoffs(NI,sampleRate)
    %Used to calibrate the acquisition for the specific
    %individual/setup/circuit
    
    %While this is running, the individual must relax their eyes
    pause(1);
    [~,data] = acquireData(NI,sampleRate,5);
    noiseMin = min(data);
    noiseMax = max(data);
    centerline = mean(data);
end

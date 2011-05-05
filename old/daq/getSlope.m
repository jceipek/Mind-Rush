function [slpe,avg] = getSlope(NI,sampleRate,noiseMin,centerline,noiseMax)
    [~,data] = acquireData(NI,sampleRate,1/200);
    %This will later be modified to do less, so that it can be used
    %to filter out blinking.
    %init = data(1);
    %fin = data(end);
    
    slpe = 0;
    
    if max(data)-centerline > (noiseMax-centerline)*2
       slpe = 1; 
    end
    
    if centerline-min(data) > (centerline-noiseMin)*2
       slpe = -1;
    end
     
    avg = mean(data);
end

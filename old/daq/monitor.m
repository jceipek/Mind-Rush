function signal = monitor(NI,sampleRate,noiseMin,centerline,noiseMax,oldVal)
    signal = getSlope(NI,sampleRate,noiseMin,centerline,noiseMax);
    if signal == 0
        signal = oldVal;
    end
end
function [time,data] = acquireData(NI,sampleRate,duration)
    %Gathers data for <duration> seconds.

    data = zeros(duration*sampleRate,1);
    time = zeros(duration*sampleRate,1);
    lastIndex = 1;
    flushdata(NI); %Clear current available samples
    availableSamples = 0;
    while lastIndex < duration*sampleRate
        while availableSamples == 0
            pause(duration); %wait for average time required to get 1 sample
            availableSamples = NI.SamplesAvailable;
        end
        [newData newTime] = getdata(NI,availableSamples); %get new data since last read

        %%% add new data: 
        data(lastIndex:availableSamples+lastIndex-1) = newData;
        time(lastIndex:availableSamples+lastIndex-1) = newTime;
        
        lastIndex = lastIndex + availableSamples;
        availableSamples = 0;
    end
    
end

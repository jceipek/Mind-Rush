%% DAQ Initialization Script
%  Run once at the beginning of the program to initialize acquisition from
%  the DAQ.

% All vars in this file will begin with Init_ to prevent conflicts with
% other scripts

%%Constants:
Init_sampleRate = 480;

try
    daqreset;
    %%Assign device ID programatically
        Init_NID = daqhwinfo('nidaq');
        Init_NID = Init_NID.InstalledBoardIds{1};
        Init_NI = analoginput('nidaq',Init_NID);
    %%---------------------------------
    addchannel(Init_NI,2);
    set(Init_NI,'SampleRate',Init_sampleRate);
    set(Init_NI,'SamplesPerTrigger',inf);
    set(Init_NI.Channel(1),'InputRange',[-2.5 2.5]);
    %%%------------------------------------------
    start(Init_NI);
    Init_initialized = 1;
catch err
    Init_initialized = 0;
end

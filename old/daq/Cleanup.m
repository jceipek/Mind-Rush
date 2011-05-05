%This script closes the device and clears all Init_ variables
stop(Init_NI);
delete(Init_NI);
daqreset;
clear Init_NI;
clear Init_sampleRate;
clear Init_NID;
clear Init_initialized;
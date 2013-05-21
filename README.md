#Listen to Bitcoin Mining#

A Python script that connects to cgminer's api, and generates a mining audio landscape that is synchronized to the current mining rate.  While mainly for entertainment purposes, this could be useful for passively monitoring a mining farm.


##Before Using##
Make sure to enable the API on cgminer. For example:

    cgminer --api-listen --api-allow W:127.0.0.1,192.168.1.0/24

Make sure your speakers are set at an appropriate volume.


##Usage##
    usage: listentobitcoinmining.py [-h] [--shares-per-sound SHARES_PER_SOUND]
                                    CGMINER [CGMINER ...]
    
    Bitcoin Mining Audio Landscape
    
    positional arguments:
      CGMINER               cgminer IP, e.g. 127.0.0.1:4028
    
    optional arguments:
      -h, --help            show this help message and exit
      --shares-per-sound SHARES_PER_SOUND
                            Play 1 sound for every X shares


##Details##
It will initially take about 30 seconds or so for your room to be filled with the blissful sound waves of Bitcoin mining.


##Accuracy##
While running, each "sound" played directly corresponds to a fixed number of shares, defined by the shares-per-sound option.  The rate at which the sounds are played, however, is only roughly correlated with the hashing rate.  Since information on the exact time the shares are found is not available, a truly direct correlation is not possible.  However, this does allow for more flexibility in how the audio landscape is constructed.  In other words, it sounds slightly less like a random mess.

##Video Demo##
http://www.youtube.com/watch?v=36zCtFHEOrg

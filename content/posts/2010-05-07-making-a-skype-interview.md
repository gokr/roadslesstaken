---
title: Making a Skype interview...
date: '2010-05-07 14:00:08'
slug: making-a-skype-interview
categories:
- Old blog
---
I got the opportunity to make a Skype interview with [Dan Ingalls](http://en.wikipedia.org/wiki/Daniel_Henry_Holmes_Ingalls,_Jr.), so I decided to try to record it. Had no idea it was not as easy as a "press record"-button. I am on Ubuntu, Karmic Koala. First of all I had serious trouble getting proper sound working with Skype, I ended up following the HOWTO in order to install Skype 2.1 beta - which uses PulseAudio ONLY. That took care of that issue, after a bit of fiddling in the "Preferences" dialog you get when right-clicking on your volume applet :)

So… I did roughly this:

Record both sides of the conversation using **parec**. This is a tool in PulseAudio, so the recording is done "outside" of Skype. In two different files! I used this shell script to record both sides at the same time (note that this produces RAW files):
` parec -r -d alsa_output.pci-0000_00_1b.0.analog-stereo.monitor \
-n "Mon Rec" > mon-rec & \
parec -r -d alsa_input.pci-0000_00_1b.0.analog-stereo \
-n "Mic Rec" > mic-rec &`
Note that I found the alsa-yaddayadda names in… eh, some dialog somewhere! Don’t recall. Anyway, read more on this part [here](http://www.outflux.net/blog/archives/2009/04/19/recording-from-pulseaudio/).

I then converted the resulting two RAW audio files into WAV using **sox**, some kind of audio swiss army knife. I don’t have the exact one-liner handy, but I used the options found in the link above.

Finally I mixed the two files together… eh, ah, problems… **They don’t synch!** Now… I have absolutely no idea how that can be, but the files end up drifting out of synch, and this seems to be a known Skype thing according to Mighty Google.

So in the end I had to manually cut/edit the two files in order to get a proper question+ answer sequence as an interview. I played with Audacity, ReZound etc but ended up doing it in Sweep, it felt simpler and didn’t cause me any other trouble.

NOTE: On "other less worthy platforms" than Linux there seems to be other options. I also found some stuff for recording on Ubuntu, but AFAICT these solutions would not work with Skype 2.1.

Well, perhaps it helps someone else out there intending to do the same journey!

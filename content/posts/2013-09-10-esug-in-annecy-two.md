---
title: ESUG in Annecy Day 2
date: '2013-09-10'
categories:
- Programming
- Languages
- Computing
- Smalltalk
- ESUG
---
Another day in [IAE Universite Savoie Mont-Blanc](http://www.iae.univ-savoie.fr) in Annecy. 

Only writing about stuff I attended :)

<!--more--> 

## GemStone/64 Update

A really good presentation from GemTalk! They are presenting a lot of customer cases in a way I have **never seen before**. Perhaps I just missed this earlier years on various conferences - but this was refreshing. This is what I want to hear. I can't help thinking this may be due to the fact that GemTalk now again stands on its own? Or perhaps not, but it was a very nice open presentation.

## NativeBoost tutorial

So Damien Pollet was running a tutorial on NativeBoost and it was good, but I personally ended up distracted since I got stuck on some odd error - apparently I was the only one (!) using Linux. Odd. I am a liiittle bit worried about all these Smalltalkers moving to the Mac. **Come on guys**! But NativeBoost rocks and is a true enabler for lots of interesting stuff. In fact, I was contemplating making a plugin for a specific task and now I am toying with the thought of perhaps using NativeBoost instead. I did try it earlier, so I know how it works, and these days it is probably better documented.

## Building a Pharo VM

After that it was lunch and the schedule didn't look that amazing so I ended up hanging around with Igor for a while, discussing this-and-that and finishing it off with a quick guide on how to check out and build the Pharo VM from github. It's nice and much easier than before - the only thing biting us was hunting down the correct libraries - and yeah, as **i386 and not the default x86_64** of course ;)

So reflecting a bit on that - building the VM has never been easier. In the end the steps were:
* Clone it from github.
* Run a shell script that automatically pulls down a VM binary and image that can generate sources.
* Fire up the generator image and run a single doit that is in front of you.
* Run the final build.sh script that basically run cmake and then make.
* ...and then spend a few minutes hunting down libraries missing (but I think cmake on the Mac does it for you)

Now, everyone who has built VMs before knows that the above procedure is a dream. And the best thing is that it is all properly versioned/contained inside that git repository. No hunting down version this of that and version that of this.


## Evening

So I spent most of the rest of the day talking to Igor and then we joined up with Igor's wife Lucy and Hilaire Fernandes and went to a very nice restaurant in old town, Alpine I think it was called. Thank you guys for a great evening!



---
title: Never an Intel SSD again
date: '2013-01-02'
categories:
- SSD
- Hardware
- Lenovo
- X220
- Linux
---
When I bought my Lenovo X220  - which I have been **extremely pleased with** to date - I chose an **Intel 320 160Gb SSD** disk with it, in retrospect a **BAD MISTAKE**. No idea why I didn't find the warnings plastered all over the net at the time, and the problem was even acknowledged by Intel [as early as july 2011](http://www.techpowerup.com/149064/Intel-Acknowledges-SSD-320-Series-8-MB-Bug-.html). The disk has been working fine since april when I got it, until the last day of 2012...
<!--more--> 

The laptop has experienced "freezes" from time to time - you know, when the only thing you can do is hold the ON button to shut it off hard. I have been suspecting bad memory, but every time I tested they seemed fine. Yesterday I ran memtest for 5 hours on them and no, no problem there. I would guess this has happened perhaps 15 times since I got the machine in april - so about 15 power cycles is all it took to make 2012 end with a BANG.

After this last freeze and power cycle the machine suddenly ended up at the grub prompt and couldn't boot. **Not a reassuring feeling**. Playing around at the grub prompt the partitions seemed to look fairly fine though, I could see "most" of my files.

After getting myself a bootable USB rescue disk I managed to access the disk and copy my home catalog to an external disk - phew! My backup was at least a week old so thank you, thank you disk Gods for allowing me to do this. ...then I did another reboot to try to figure things out **and suddenly not even a grub prompt**!

Ehrm, what? WHAT? I started scavenging the net and behold - this seems to be the well known so called "BAD_CONTEXT or BAD_CTX 8MB bug" that the Intel 320 based SSD drives are plagued with. So power cycling can apparently trigger this - and the disk for some odd reason (self protection?) decides to decapitate itself and set accessible cylinders down to 16 instead of 16384.

Funny thing here is that the last reboot was NOT a power cycle, but for some reason the **SSD decided that "enough is enough" and chopped off its head in desperation**.

<!--more-->

This is of course a legacy thing, SSDs don't have cylinders of course, but the net effect is that the disk appears to be only 8MB large. It seems (googling conclusion) this happens whenever the SSD experiences **ANY** disastrous error, so not only this particular "bug". 

And in fact, I am not even sure my disk got the same bug, because after the BAD_CTX there is a number, and mine says "15". The one people talk about, and that Intel claims to have fixed with a firmware update, is number "13". But fact remains, my disk is not accessible and it was apparently trigged by a power cycle.

Since the disk uses encryption internally (I *think* this is one of the reasons) there is **apparently no way for ordinary people to salvage any data**. And I can't even persuade the disk to even show me the rest of the disk. When the upper bound is set down like this the "hidden" area (most of the disk in this case) is called a [Host Protected Area](https://en.wikipedia.org/wiki/Host_protected_area). Using hdparm and other tools one is supposed to be able to set this "SET MAX ADDRESS" threshold back up and remove this "protected area", but all my fiddling with this has utterly failed. I tried [hdparm](http://www.thomas-krenn.com/de/wiki/SSD_Over-Provisioning_mit_hdparm) and [HDAT2 using ultimatebootcd](http://www.ultimatebootcd.com/) but no, no go. It just gives me some error when I try.

And the rest of the net also says that the **contents of the disk is lost** but that [you can reset the disk so that it at least "works" again](http://communities.intel.com/message/145676#145676), but empty. And another post describing [a different procedure](http://www.tested.com/forums/pc-and-mac/44240-huge-bug-in-intel-ssds-complete-recovery-information-here/).

Now... there is some data salvage firm claiming they can save data from this problem (sorry, no link from me, but if you are in this situation you will find them) - and I think they have cooperated with Intel to be able to do this. I would guess Intel has provided some "super keys" to the encryption in that case? Who knows. I haven't lost enough data to contact them though.

So... it seems the net is in fact quite enraged over Intel for all this - because this drive (and SSDs in general) is supposed to be very safe and actually has special features for preventing these exact things! How ironic.

Now, Intel is stone walling, they claim to have fixed the problem with the firmware update - but **lots of people are reporting the same issue happening again, over and over, even with updated firmware... And no answers from Intel**.

And you might ask, what about my firmware? Well, this is a Lenovo OEM (INTEL SSDSA2BW160G3L), so it has a Lenovo firmware number (4PC1LE04) but I did go through the Intel [firmware update dance](http://www.intel.com/support/go/ssdfirmware/index.htm) (unetbooting from Linux onto USB stick works fine) and it tells me that my firmware IS UP TO DATE. No, it doesn't tell me that I have some Lenovo firmware that it doesn't know about - it says **IT IS UP TO DATE**. So I trust Intel on that one. Ha, silly me. So yes, chalk me up as one of those that had new firmware and got hit by the truck anyway.

IMHO hardware that has faults is generally not a big problem, it doesn't generally cause lots of data loss if a graphics card or a motherboard burns up. But **disks** with bugs like this is more problematic. And we are not talking about "a few sectors lost" but **the whole 100% shebang lost**.

Backups? Sure. But you will generally still lose lots of valuable time when a thing like this happens, and I don't think it is enough to just point the finger back at the customer like that. Sure shit happens, but here we are talking about **known about and repeatedly happening after less than a year due to freaking bugs shit** and not just **weared down by 10 years of continuous spinning shit**.

What makes it more than "a problem" is that Intel doesn't respect its customers enough to:

* explain what is going on
* explain what these different error numbers mean
* explain why it truncates to 8MB
* explain why people still have problems after the firmware update
* explain what the firmware update claims to have fixed

...and **take responsibility** when their product is obviously badly broken and not trustworthy - that is much more than "a problem"!

Boycotting Intel is not an easy thing, but one thing is for sure, **I will NEVER buy an SSD from Intel again. NEVER. And if you google the net you will see lots of other people with the same conclusion.**

If Intel doesn't care about their customers and their own goodwill - so be it. And if someone from Intel wants to comment on this blog post - feel free - but I truly doubt it since they don't even comment **in their own damn forum** which is full of [posts like this one](http://communities.intel.com/message/153620#153620).

And if there are factual errors in this text and Intel somehow miraculously can explain all this crap - go ahead and contact me and I will HAPPILY edit the text and explain to the world what I completely misunderstood.

So... end of steam. Anyone that can recommend a good **trustworthy** SSD that fits in a Lenovo X220?

No idea what I will do with this old one, I sure don't trust it anymore and getting another one on warranty wouldn't make it different.

**UPDATE:** As I write in my comment below I revived the SSD but it's now just wasting space on my desk here. I instead bought a [Samsung 840 Pro, 512Gb](/2013/01/10/new-ssd-for-my-x220) (here is [one of all reviews](http://thessdreview.com/our-reviews/samsung-840-pro-512gb-ssd-review-killer-performance-and-untouchable-iops/)), yes, expensive but seems to be **extremely fast** (only 1-2 other SSDs are even close), uses **very little power** (no other SSD seems to be close) and above all - Samsung seems to have a better track record on robustness and how to deal with problems. Of course, I will know more in a year from now, and I am also investing some time into a full recovery solution like Mondo Rescue or similar. :)

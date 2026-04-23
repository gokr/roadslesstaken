---
title: New SSD for my Lenovo X220
date: '2013-01-10'
categories:
- SSD
- Hardware
- X220
- Lenovo
- Linux
---
After the [conundrum with my Intel 320 SSD](/2013/01/02/ssd-nightmare) I did some googling and decided to invest a fair chunk of money in a really good SSD - the [Samsung 840 Pro, 512GB](http://www.anandtech.com/show/6328/samsung-ssd-840-pro-512gb-review). The 840 Pro seems to be the king of the hill right now and it's only 7mm thick which is what I need for my X220 (although people have shoved 9mm drives into it with a bit of force).

<!--more--> 

![Not](/pics/pic3.jpg){ style="float:left; margin:0 1em 1em 0;"}

The actual replacement was trivial, one normal screw to remove the lid on the side, pull out the old disk, move the plastic rails over to the new disk (just pull off and slide onto the new drive), add a piece of tape as a pull handle (to make it easy to remove) and slide it in. If it doesn't want to go in you need to flip the rails.

Reboot, go into BIOS and make sure AHCI is selected for SATA and off to happy land. I installed Ubuntu 12.10 from a USB stick and just let it do the automatic thing. This creates a swap partition on the SSD, but that is fine with me - I adjust the swappiness instead to make sure it is only used when really needed.

<br clear="ALL">

You can test performance to make sure all looks ok:
``` bash
hdparm -tT /dev/sda

```
...or whatever /dev you have. I get around **7000MB/sec for cached reads and 515 MB/sec for buffered reads**.

In /etc/fstab I added the options "noatime,nodiratime,discard". The "nodiratime" is not really necessary since it is implied by noatime. This makes Linux not update access time on files which in turn reduces write operations a lot which prolongs the life of the SSD and increases performance.

The "discard" option is to make sure we enable [TRIM](https://en.wikipedia.org/wiki/TRIM) on the disk. I just followed [this article](http://techgage.com/article/enabling_and_testing_ssd_trim_support_under_linux) (and this [other](http://nedoboi.wordpress.com/2011/11/12/tiny-tips-ssd-linux-enable-trim-and-check-it-works)) describing it and how to test it works. Another good page on [AskUbuntu](http://askubuntu.com/questions/18903/how-to-enable-trim). Some [people say](http://serverfault.com/questions/307397/verify-trim-support-with-btrfs-on-ssd/401506#401506) that the test in that article is not reliable, but still, if you **do get zeroes** then you can rest assured it works. :)

Next up is setting down swappiness, changing to a disk scheduler more suitable for an SSD and setting /tmp up using tmpfs in RAM. I will not repeat all this - instead I offer some links to [good instructions at Tombuntu](http://tombuntu.com/index.php/2012/04/26/setting-up-ubuntu-on-an-ssd) or in the [ArchLinux wiki](https://wiki.archlinux.org/index.php/Solid_State_Drives) or [this one going even deeper](http://bernaerts.dyndns.org/linux/250-ubuntu-tweaks-ssd).

Rergarding partition alignment - I read that it should be automatic so I didn't bother looking into that.

---
title: Moving to SmalltalkHub
date: '2013-01-07'
categories:
- Smalltalk
- Pharo
- Squeak
---
As a long time Squeak/Pharo (Smalltalk) developer I have accumulated a set of packages that I have written or co-written and that have been published open source for others to use. Since quite a few years [SqueakSource](http://www.squeaksource.com) has been the natural hosting place, but it has reached the end of the road and it's [high time to move on](http://news.squeak.org/2012/11/18/move-your-squeaksource-files/).
<!--more--> 
Since then we have had [SqueakSource2](http://www.squeaksource.com/ss2.html) (an improved SqueakSource but not deployed I think) and now [SqueakSource3](http://ss3.gemstone.com) that runs in GemStone and hosted by GemStone. A lot of projects have migrated to SS3 and that is definitely **not a bad choice** and has been the suggested and only path forward for some time. Never mind it says *"public Alpha"* :)

Personally though I find [SmalltalkHub](http://www.smalltalkhub.com) more attractive - but this is perhaps because I am involved in some of the [technology](http://www.amber-lang.net) behind it and I know Nicolas quite well. Anyway, I am now moving (well, copying) all my projects there and the process to moving is simple and has been [described for SS3](https://marianopeck.wordpress.com/2011/11/08/migrating-projects-to-squeaksource3/) over a year ago:

* Create a project on SH. And if you don't have an account, create one.

* Run a few snippets using Gofer to copy over all the code. Here is an example copying over all snapshots for DeltaStreams, PlusTools and System in the DeltaStreams project on SS to my new project on SH:

``` smalltalk
Gofer it
	url: 'http://www.squeaksource.com/DeltaStreams' username: 'gokr' password: 'secretpasswordonSS';
	package: 'DeltaStreams';
	package: 'PlusTools';
	package: 'System';
	fetch

Gofer it
	url: 'http://smalltalkhub.com/mc/gokr/DeltaStreams/main' username: 'gokr' password: 'secretpasswordonSH';
	package: 'DeltaStreams';
	package: 'PlusTools';
	package: 'System';
	push
```
In the above code we need to list all packages that exists in this repository in order for Gofer to pick them all up. So you might want to look in the SS web UI (tab "Versions") to make sure you didn't miss any snapshots.

* Edit the package description on SS to reflect that SS is no longer the primary repository for this package:
```html
<b>NOTE: This project has been moved to <a href="http://smalltalkhub.com/#!/~gokr/DeltaStreams">http://smalltalkhub.com/#!/~gokr/DeltaStreams</a></b>!!!
```
To make it extra clear I also include a line like below on SH to make sure people understand this is the right place now:
	**NOTE: As of 2013-01-06 this is the primary repository of DeltaStreams, there is also an old repository on www.squeaksource.com.**

* Finally, if you have other people than yourself with write access on SS, make sure you check and add them as contributors in SH, if they have accounts on SH. And make sure to drop them an email! :)


And poh, a little bird just told me that **SH is being upgraded by the end of the week** with new functionality and bug fixes. Go Nicolas, go!

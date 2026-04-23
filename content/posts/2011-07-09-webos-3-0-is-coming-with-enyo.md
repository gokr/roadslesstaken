---
title: WebOS 3.0 is coming - with Enyo!
date: '2011-07-09 01:27:37'
slug: webos-3-0-is-coming-with-enyo
categories:
- Enyo
- Web tech
- WebOS
---
A few weeks ago I joined the Early Access program that HP/Palm has been offering for a while and I have been toying with the new [WebOS 3.0](http://developer.palm.com) (SDK with emulator) that appeared in public on the 1st of july when the [HP Touchpads](http://www.hpwebos.com/us/products/pads/touchpad/index.html) hit the stores in the US. Since a week I also have a [Palm Pre 2](http://www.hpwebos.com/us/products/phones/pre2/index.html) phone running WebOS 2.1, hopefully to be upgraded later to 3.0.

What can I say, **I am totally hooked!** The SDK for WebOS 3.0 looks really nice and the Palm Pre 2 is [the best phone](http://www.trustedreviews.com/Palm-Pre-2-Review_Mobile-Phone_review) I have ever used, if I disregard the poor battery life.

No, I have never owned an iPhone but my previous phone was the Samsung Galaxy, and that is a really good phone! :) Now, of course, getting the [Pre 3](http://www.hp.com/pre3) would be even better.


## Screenshots




## ## WebOS


Having used the phone for a week or two some things stand out:



	
  * The gesture and cards system for multitasking is a real joy to use. Hard to describe, should be experienced.

	
  * Notifications are [really nicely done](http://www.bgr.com/2011/06/08/apples-ios-5-notifications-are-great-but-webos-is-still-better/), non intrusive and slick.

	
  * The "just type" mechanism is awesome, typing in a name or a website or whatever - and WebOS will suggest and list "everything". And even better, WebOS discovers new "search engines" when I surf and offer to include them in quick list for searching! Simple and so smart.

	
  * Synergy - the system merging all contact information together is amazingly good, much better than on my Android phone. It merges and syncs info from my LinkedIn, Facebook and Google accounts (and many other sources) brilliantly.

	
  * Messaging is uniform, I can SMS or Gtalk or whatever in the same threaded view for a given contact. Yay!


And there is lots more of these little things, adding up to a very smooth user experience.


## Application frameworks


One of the primary new things in WebOS 3.0 (vs 2.x) is [Enyo](http://www.infoq.com/news/2011/07/webOS-3-Enyo) - the new application framework in Javascript that is replacing Mojo, the older framework. Enyo looks like a really well designed object oriented UI toolkit. It focuses on using code and not HTML to produce the user interface and the API looks nice, well documented with examples and quite complete!

Applications for WebOS 3.0 come basically in three flavors - Enyo/Javascript, OpenGL/SDL/C/C++, or hybrid.



	
  * An Enyo app is "just" Javascript running in V8 + Webkit and will be the framework that the majority of the applications will use. Given the push in Javascript land these days I would say it is a very interesting platform.

	
  * More demanding graphical apps, especially games, can be written in the C/C++ tool chain and use the OpenGL ES and [SDL](http://en.wikipedia.org/wiki/Simple_DirectMedia_Layer) APIs. This seems to be a very friendly platform for game development.

	
  * Hybrid apps are Enyo apps (or Mojo) that can embed native components written in the C/C++ tool chain and allow them to render parts of the screen and also communicate with them. This is clearly an interesting option for many demanding apps.




## An open eco system


Although WebOS is not open source it seems in many ways more "open" than the competition:



	
  * It is trivial to get "root" on the devices. Just type in "[upupdowndownleftrightleftrightbastart](http://en.wikipedia.org/wiki/Konami_Code)" and click the icon that appears!

	
  * HP/Palm seems to realize that the [homebrew community](http://www.webos-internals.org/wiki/Main_Page) is very important and this community is [exceptionally strong](http://www.preware.org).

	
  * Using the [Preware](http://www.preware.org) homebrew app catalog and installing themes, patches, applications and more is just as easy and smooth as the [regular app catalog](http://www.hpwebos.com/us/products/software/mobile-applications.html) (no, you can't browse it on the web, only on a device)!

	
  * The OS is a real Linux at the base! In fact, the ipk package format for apps is the deb format.

	
  * The base technologies used are major open source projects like Webkit, V8, SDL, GStreamer etc etc.

	
  * HP is offering a multitude of distribution channels including a "web distribution" channel where you can market your own app outside of the regular app catalog - but people can still just click on a URL and buy/install the application! That is very nice.


...and there are many more aspects to this "openness", but I think HP realize that they need to play this part of the game quite a bit better than the competition in order to be able to catch up.


## High hopes


I think HP has a diamond here in WebOS and if they play their cards right they should be able to find their piece of the market share. And that share just needs to be "descent" in order to be fruitful. But in order for that to happen I am hoping that:



	
  * The products (Touchpad, Pre 3, Veer) really hit the stores all over the world ASAP.

	
  * The 3G/4G versions of the Touchpad will show up soon. Just wifi is not enough.

	
  * The next generation of products keep up with the competition in hardware specs.

	
  * The major apps people want and need start appearing.


The first three are primarily up to HP. The fourth is hopefully not a problem since the eco system is so appealing to developers. And I think HP is trying to make sure some crucial apps are not missing - for example, I think HP made sure the Facebook app is there - and it is indeed a really good app!

Next up? Well of course, using Smalltalk to build Enyo applications... :)

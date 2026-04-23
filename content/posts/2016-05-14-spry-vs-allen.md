---
title: Spry vs Allen
date: '2016-05-14'
slug: spry-vs-allen
categories:
- Spry
- OOP
- Smalltalk
- Object orientation
- Languages
- Programming
---
Allen Wirfs-Brock [wrote down a bullet list](http://www.wirfs-brock.com/allen/posts/754) of what he thought actually made it possible for the Alan Kay team to [create Smalltalk](http://worrydream.com/EarlyHistoryOfSmalltalk/), and many other ground breaking things, at Xerox PARC in the 70s. Let's take a look at **his bullets one by one** and see how it applies to Spry and my puny little effort around it :)

![Assume](/spry/assume.jpg){ style="display:block; margin:0 auto;"}

<!--more-->

## Look 20 years into the future

That's obviously hard to do, but I am trying a little bit by **questioning every little thing** that many consider not being even relevant or possible to question. Some examples are:

 * Why we can't do OO in some new novel ways
 * Why we are so stuck in having source code in files
 * Why we still only share code instead of sharing live objects
 * Why our IDEs still can't do things like backwards debugging or modifying code while running
 
Everyone is so busy "doing stuff" that noone takes the time to actually reflect. Can we really not create a development system in which I can see exactly what is going on? Is there really no more powerful ways to do debugging?

So I may not look into the future, but most good ideas come from someone doing something unexpected, weird, impossible or downright stupid. In Spry I want us to try a few of those :)

## Extrapolate technologies

I don't really dare, but I think it's safe to say that Virtual Reality is probably going to be accessible everywhere. JavaScript has hopefully waned but leaving behind a new much **lower threshold to programming being the norm**, not the exception. Everyone wants to be able to program. **Hardware is basically free, very capable and everywhere**. People tend to think that the web is taking over everything, but I don't think its that simple - I think diversity is going to be much higher due to new companies creating new kinds of devices. Many more devices.

How does this affect choices in Spry? Well, I tend to not let performance considerations hinder various ideas. I also focus pretty hard on mobility of code and data, since I think we should be able to find a lot more models of computing in the area of distributed systems.

Finally I do think DSLs in different shapes or forms will play a big part in the future - so Spry should have excellent capabilities for that.

I also want Spry to be modular on most levels, while still being fairly simple.

## Focus on people

The Smalltalk team was focused on user interfaces, education and children. With Spry "people" means primarily "developers".

I don't think 20 years will remove the need for writing code, but the pressure for fast results will be immensely higher. I also think the boundaries of computing will be much fuzzier and that we will need to have more advanced tools to create and mold code into doing what we want. Things will run on many devices, distributed in novel ways reaching places in our lives we can not really imagine.

I want to create and modify systems live as they run, as they are being used. Not just run locally, or as prototypes, but as they run live in deployment. Continuous deployment will probably **evolve into 100% live online development**. How will that affect developers? What tools do we need? How can we evolve a live system with confidence?

This implies we will have to create much more powerful ways to create, debug and modify code. We need to raise the abstraction levels, but perhaps a key to that is to create a homoiconic language that lends itself to introspection and self reference. Smalltalk didn't do that (only to some extent), nor did JavaScript. The Lisp family of languages did to some extent, but for various reasons never really took off. Hard to say why.

## Create a vision

One vision is a **globally shared live system** of cooperating Spry objects. Like GemStone/S but on a global scale, and taken even further to the extreme. Today developers share code - dead code - via various package catalogs and copy/paste forums. The SaaS and PaaS etc are trying to create shared platforms, but it's still very much centered around the same coding model where we don't share actual functionality, but merely code and libraries to recreate the functionality on our own.

To be concrete - instead of downloading a library and create a small service that consumes a live feed of data and produces a stream of Spry objects, in Spry we would find not a library, but a live running existing service that we just hook into. The module is not dead code, but actually a live and running service.

This is homoiconicity driven all the way! During the years sharing of objects have been tried via various RPC-ish standards like CORBA or RMI, but those standards have always revolved around static early binding and separate specifications and have thus later been completely run over by late binding self describing technologies like REST-ful APIs using JSON and similar "soft" formats. Late binding and self description is key for how modern development is done to a large extent - experimentation.

Another vision is Spry being a language to serve as a new foundation for transferable portable active code. Kinda like a JavaScript that doesn't suck and that is homoiconic and thus easy to make tools for.

But in the end... I don't have any grand delusions about Spry - its all for fun and I just hope some of us will find it useful!


## A Team of Dreamers and Doers

Obviously I don't have this. Yet. I hope that if I can make enough progress on my own - then people will join. And I stand on firm shoulders in the form of Nim which makes Spry suffering less of NiH (no pun intended). I hope that some Smalltalkers will eventually join, but I need a good solid language manual and perhaps even a reasonably interesting IDE to get any real traction.

## Prototype the Vision

Spry has almost reached the point where we can start working on the fun stuff. The module system, serialization mechanisms and lossless AST improvements are all crucial steps towards this. Next step is getting the OO model working and do the Sophia integration to get a working image based system. After that I suspect its time to make a first IDE. I do have some plans and ideas for that too :)

## Live Within the Prototype

I think this is definitely important. The existing REPL is just a crude first trivial step. But it will get better!

## Make It Useful to You

I personally want to apply Spry in the domains of VR and IoT. Web systems is no longer that interesting to me, but if someone would like to evolve Spry compiled to js - I would be very grateful.

## Amaze the World

Hopefully, eventually! :)

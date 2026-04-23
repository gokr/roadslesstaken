---
title: ESUG in Annecy Day 4
date: '2013-09-12'
categories:
- Programming
- Languages
- Computing
- Smalltalk
- ESUG
---
It starts off with Cincom, Arden Thomas presenting their roadmap. He had a slide mentioning Jules Verne and I must ask him if he is aware of the influence from the books of Jules Verne - as Dan has explained, the ballon and the island in the [classic Smalltalk logo](http://st-www.cs.illinois.edu/Graphics/bytebloon.jpg) comes [from the Mysterious Island book](http://wiki.squeak.org/squeak/3459).

<!--more--> 

## Mist

Martin McClure enters the stage, this should be fun. Ah, now we are back to the metal! So Mist looks like a promising new really low level Smalltalkish language. So no VM, just Mist compiling to Fog compiling to machine code. A **non moving** memory scheme influenced by the memory allocator in the Linux kernel (I think he said), that simplifies TONS of things. No object header, things like identityHash or pointer to class is **just instance variables**. Slick. And the addition of tail call eliminiation, is that a first in a Smalltalk implementation? Probably not, but still a very nice thing.

Mist is of course a "low level hacking bliss" project, it can't really do anything yet :). But life is not always work, sometimes its just for fun. And yes, Martin had an episode of Forth earlier in his programming life, and the Forth community has a lot of track record in "going down to the metal".


## Mongodb and Voyage

Nico and Esteban did a tutorial on MongoDB and Voyage and I was there but not really following it. I am personally really interested in NoSQL databases but I have always hesitated about MongoDb so while I like to see how things work I will not use it myself. I am much more interested in other alternatives :)




...more to come...

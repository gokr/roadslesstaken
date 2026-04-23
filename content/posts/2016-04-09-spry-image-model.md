---
title: Spry image model
date: '2016-04-09'
slug: spry-image-model
categories:
- Spry
- Ni
- Smalltalk
- Rebol
- Homoiconic
- Languages
- Programming
---
In developing Spry - [renamed from Ni](/ni-is-now-spry) - I am getting closer to the **Really Fun Stuff**.

As a Smalltalker I dream "bigger" than just managing source code as text in files...

<a href="http://www.azquotes.com/quote/847274" title="Kent Beck quote"><img src="http://www.azquotes.com/picture-quotes/quote-i-mean-source-code-in-files-how-quaint-how-seventies-kent-beck-84-72-74.jpg" alt="I mean, source code in files; how quaint, how seventies! - Kent Beck"></a>

Smalltalk uses the "image model" in which the system is alive and running all the time, the full development environment is also live together with your application, and we are in fact modifying object structures when we develop Smalltalk programs. We can also snapshot that object memory onto disk and fire it up somewhere else. Several Lisp implementations have used a similar approach I think.

The image model has tons of really cool benefits, I don't have time repeating all of them, but a modern implementation of the idea should take a few things into account that was not considered in the 1970s:

* The "image" in Spry will be buildable from source
* You should be able to use Spry without the image mechanism (you can already)
* Spry code will have a readable text format and file structure
* The image model does not have to be all or nothing, it can be partial
* The image mechanism will be a module for the Spry VM, so you can skip it entirely

Some argue that the image model has downsides - like being an "ivory tower" incapable of interacting with the outside world. The Smalltalk environments have indeed historically suffered a bit in varying degree, but we can easily find ways around those issues while still **reaping the awesomeness of a fully live** programming environment, especially if we give the above items proper thought **from the start**.

With Spry I think I have a beginning to a novel approach... as well as taking the above into account.

<!--more-->

## The Smalltalk model

Most Smalltalks (not all) have been image based and the image has simply been a "memory snapshot" of the whole system down to a single disk file. Although quite novel both then and now - the concept of a single dump onto a file is rather primitive. Today we have TONS of different advanced database engines to choose from - why not use one of them instead?

Yes, [GemStone](https://gemtalksystems.com) is a remarkable exception to the traditional Smalltalk image model. Already in the late 1980s they realized that the object memory could be made transparently distributed, multiuser, transactional and persistent. GemStone is simply **DARN** cool and I haven't seen anything even close in other languages. But it's not open source, and it's expensive. And... can be a bit complex too.

Can we do something similar to GemStone but much simpler? Let's start in the single user perspective. Assume we have a transparently integrated advanced and super fast database engine. Sure, single user, but that will give us a strong platform to stand on for code management, IDE development and a lot more.

## Storage format
But hold on - first we need to decide on a suitable format to store in a database.

I thought briefly about the **binary path** where we simply store pages of RAM onto disk in order to avoid serialization/deserialization - but I opted out. It's complicated and it doesn't fit well into the idea of having future multiple implementations of the Spray VM catering to different eco systems. I also think CPUs are insanely fast these days so serialization/deserialization is not a bottleneck.

So let's presume we serialize, in what format? Definitely in a **readable** format I would say. What about JSON then? Mmm, JSON is simple and TONS of databases these days rely on it, and in fact Spry will have really nice abilities to manipulate and integrate JSON - but we have a more natural choice in Spry.

Spry is homoiconic and has a simple and easily parsed free form syntax of its own. In the name of unifying concepts and simplicity - we **obviously just use Spry!** This would be slightly in analogy with the `storeOn:` and `readFrom:` mechanisms that Smalltalk had from the start storing data "as code". But Spry is MUCH cleaner and consistent here, in the way Lisp is. The data model of Spry, including the model of **executable code**, is **the AST tree** and the syntax of Spry **mirrors** this tree.

## Serialization
After some optimizations in the current parser I made some tests on my laptop. I daftly generated some fake "data" in the Spry syntax and can happily note that Spry compiles (deserializes) about **10Mb source per second** into AST nodes. And it seems to scale pretty fine too. The serialization step is even faster.

## Compression
To put some icing on that cake I threw in LZ4 compression which is wickedly fast, so fast it isn't even noticed even when doing a full back to back cycle of a 430 Mb source file. And source is very amenable to compression, although my sample is repetitive so not a good reference.

Here is a trivial Spry script that reads a compressed file, uncompresses it, compiles it (deserialize) and then serializes it again and compresses it before writing it back on disk:

```
#!/usr/bin/env spry
writeFile "full3-lz42.sy" compress serialize deserialize uncompress readFile "full3-lz4.sy"
```
These commands I defined in prefix fashion which means the evaluation ends up as a chain from right to left. One could just as easily have defined them as infix to get a reverse evaluation, or one could use an Elixir style "pipe" function to get that effect. Spry is flexible here and obviously some kind of editor support or conventions may be needed to avoid confusion.

So where are we now? We can read and write files (trivial of course), compress/uncompress strings using `liblz4` and serialize/deserialize strings into and from Spry AST nodes. This means we can now store and load **code as well as data**, and we could trivially extend the REPL with a regular "image model".

## Sophia
But let's go all the way. Files are neat, but a really good database is better. I hunted high and low for something that seemed easy to use, with an interesting set of features and really, really good performance. I ended up choosing [Sophia](http://sphia.org) and I have a Nim wrapper of the C API of Sophia already cooking. I have a feeling this is going to be a blast, terabyte image size? No problem.

When the wrapper is working it's time to start thinking of how the memory model can be partitioned, manipulated through transaction boundaries, but that will be another article for another day!

If you want to chat about Spry, join up at [http://gitter.im/gokr/spry](http://gitter.im/gokr/spry)! Or at #spry on freenode.



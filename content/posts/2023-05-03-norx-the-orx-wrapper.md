---
title: Norx the ORX wrapper
date: '2023-05-03'
slug: norx-the-orx-wrapper
categories:
- Nim
- Norx
- Games
- ORX
- Programming
draft: true
---
A while back I wanted to explore game development, classic 2D games because I can't waste too much of my life in the rabbit hole of 3D. Me and a friend were avid C64 hackers back in the 80s and I haven't tried to make any games ever since. First I looked at available paths using Dart, like [Flame](https://flame-engine.org) for example. But I wanted to target low end very cheap hardware, be highly performant with good physics and be able to handle lots of players. Flame might have managed that, but it was too unproven.

So my search for a good 2D engine ended up me finding [ORX](https://orx-project.org/). This is a hidden **gem of an engine**, very good performance, highly portable written in C and with a very friendly and capable maintainer! But... C? Nope, that will not cut it for me. I do **love** that ORX itself is written in C because it means the performance and portability is good, but it also means we can fairly easily **wrap the engine** and use it from another language. In my case... Nim!

This resulted in creation of [Norx](https://github.com/gokr/norx), a Nim wrapper of ORX.

<!--more-->

...so ok, 

## ORX
This engine is a bit different than other engines since it is "data driven", this means a lot of behaviors and configuration that would be a bit complex to express in code can be handled purely through the use of "ini files", which simply are plain easy to read text files. This mechanism means you can get going quickly, and you can also solve some common patterns quite easily, like for example [animations](https://wiki.orx-project.org/en/guides/beginners/spritesheets_and_animation). Now, in combination with quite a fair bit of documentation and examples, this is powerful.

ORX is also hardware accelerated, is a complete single library handling audio, input, graphics and has a good integrated physics engine. It supports a lot of platforms and is under the zlib license. And above all - there are a [bunch of games already written with it](https://orx-project.org/showcase/).

## Creating Norx
Nim is a superb language that normally compiles via C, but its much more capable and more high level than C. And it is brilliant in wrapping and using C libraries. Norx was auto generated (using the tool `c2nim`) from ORX headers to begin with, then given various "post processing" (name manglings, moving comments to proper place etc) and finally also tweaked by hand a bit. Norx has a set of "low level" wrappers, one per C header basically. And then we also started making some high level modules, where we put Nim code abstractions making it all nicer from a Nim perspective.

The 
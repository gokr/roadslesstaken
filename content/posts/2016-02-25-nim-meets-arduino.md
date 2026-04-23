---
title: Nim meets Arduino
date: '2016-02-25'
slug: nim-meets-arduino
categories:
- Nim
- Languages
- Programming
- Arduino
- IoT
- c2nim
- Evothings
---
I now work as the Team Lead at [Evothings](http://evothings.com) and our **open source** product is a Workbench for creating **mobile HTML5 applications focused on IoT**, by editing and running them **live on the mobile device** inside our spiced up Cordova based "Evothings Viewer".

I am of course partial here - but the tool is really easy to use, doesn't force you into any specific framework or editor, enables a very quick development cycle and has tons of examples, tutorials, docs and some special IoT focused libraries like for example around BLE (Bluetooth Low Energy). You can have your code running on your phone literally within 1-2 minutes and you don't need to install XCode or the Android tools, you can even run it just fine from your trusty Linux laptop! Just [go for it](http://evothings.com/download). Ok, enough of the sales talk...

Since we are specializing in the IoT space we have our office filled to the brink with toys... eh, I mean **IoT devices** of all kinds from all different vendors. Two IoT communication standards are particularly important in this space, and that's **BLE and MQTT**. I have already written three [blog](http://goran.krampe.se/2015/12/14/evothings-meets-phoenix/) [posts](https://evothings.com/evothings-does-mqtt-with-bluemix/) [around](https://evothings.com/evothings-does-mqtt-with-vernemq-or-emqtt/) MQTT using Evothings. Now I am instead focusing on BLE and particularly the **embedded device side of the story**.

![LinkIt-ONE](/evothings/mediatek-linkit-one.png){ style="float:left; margin:0 1em 1em 0;"}


This led me to round up a bunch of devices at the office that are fairly technically capable and have BLE support. The one I selected was the [LinkIt ONE development board](http://www.seeedstudio.com/wiki/LinkIt_ONE) from [MediaTek](http://labs.mediatek.com) & [Seeed Studio](http://www.seeedstudio.com). It's an insanely feature packed little board (GSM/GPRS, GPS, Wifi, BLE, sound output, SD card) with decent computing power (ARM7 EJ-S, 16Mb flash, 4Mb RAM) while still remaining in the "medium" embedded space I would say, still ruling out plain Linux and regular tools. I consider the <a href="https://www.raspberrypi.org">Raspberri Pi</a> or <a href="http://getchip.com">C.H.I.P</a> and similar machines to be in the "large" embedded space, they are real computers and you can basically use whatever you like to develop on those.

The medium and small devices can be programmed using for example [Espruino](https://github.com/espruino) or [Micropython](http://micropython.org) (two very interesting projects) but in many cases, for more demanding applications, **C/C++ is still king** simply because of size and performance advantages. And also the fact that hardware vendor SDKs are typically in C/C++. But **could there be an alternative language out there?**

* A language that is just as fast and small that easily can use all these C/C++ SDKs?
* A language with a syntax similar to Python made to be easy to write and read?
* A language with soft realtime GC and a sane advanced type system with generics?
* A language with a good standard library and friendlier than C++?
* A language with compile time hygienic AST based macros written in the language itself?
* A language offering an imperative style and not forcing OO if you don't want to?

Yep! Read on to find out...

<!--more-->

![Nim](/nim/nim-logo2.png){ style="float:right; margin:0 0 1em 1em;"}

## Nim

I have written [extensively about Nim](http://goran.krampe.se/categories/nim) before, and there is even [a blog article](http://disconnected.systems/nim-on-arduino/) showing that Nim can even run on an Arduino UNO! To Nimmers this isn't surprising, Nim compiles to performant C and if you turn off the GC etc, Nim can fit wherever C can fit.

But that article used the low level mechanics of interfacing with C/C++ and did not use [c2nim](https://github.com/nim-lang/c2nim), the **excellent wrapper generation tool** written in Nim by Andreas Rumpf, the primary author of Nim.

What if we could use c2nim to wrap most of the Arduino and MediaTek C/C++ libraries used to access all the features of the LinkIt ONE?

## Ardunimo

Two weeks ago I pushed [Ardunimo](http://github.com/gokr/ardunimo) to github. Cheesy name, but I couldn't resist. Beware though, probably only me who have tried running this since you would need a LinkIt ONE!

The <a href="http://github.com/gokr/ardunimo">README at github</a> shows how to get going and all this is **ONLY tested on 64 bit Ubuntu 14.04**. But the top dir contains a VagrantFile that I also threw together that will fire up a Ubuntu 14.04 and install and build all the Nim parts (Nim, nimble, c2nim) you need.

The fun part is that **you don't need anything else!** The LinkIt ONE officially only supports development from Windows or OSX using <a href="https://www.arduino.cc/en/Main/Software">the Arduino IDE</a>, but I found some <a href="http://www.instructables.com/id/Using-LinkIt-One-with-Arduino-in-Linux/">instructables</a> <a href="http://www.instructables.com/id/Programming-LinkIt-One-in-Linux-no-WiNE/">showing</a> that **you can indeed use the Arduino IDE on Linux too**. I used that and looking at what the Arduino IDE does, to craft the Makefile to gain full control over the build process and get rid of the Arduino IDE.

So if you are like me, comfy from the command line, this setup should be perfect!

## The wrapper

Ardunimo consists of two Makefiles, one to create the wrapper and one to build the binary for the LinkIt ONE. A Nim wrapper consists of Nim modules, basically one .nim file for each header file of the C/C++ API we are wrapping. The top level Makefile will call the Makefile in the `wrapper` directory if needed, to generate the wrapper modules, but we can also do it manually in the wrapper directory using say `make clean && make`. Then we get all the nim wrapper modules recreated:

``` bash
gokr@yoda:~/ardunimo/wrapper$ ls *.nim
arduino.nim         lgps.nim           ringbuffer.nim  vmdcl.nim     vmuimisc.nim          wiring_shift.nim
ardunimo.nim        lstorage.nim       stream.nim      vmota.nim     winterrupts.nim       wstring.nim
binary.nim          ltask.nim          uartclass.nim   vmpromng.nim  wiring_analog.nim
hardwareserial.nim  message.nim        variant.nim     vmpwr.nim     wiring_constants.nim
itoa.nim            panicoverride.nim  vmappmgr.nim    vmsys.nim     wiring_digital.nim
lflash.nim          print.nim          vmdatetime.nim  vmthread.nim  wiring.nim
gokr@yoda:~/ardunimo/wrapper$
```
The Makefile uses the c2nim tool to generate these wrappers by parsing the header files from the SDK. These headers are in the `src` directory, and there are some local small modifications to them. Some details were harder to fix in the header files, so those files I ended up hand editing after the c2nim generation, and placing them into the `fixed` directory, so they are just copied from there. A bit more work to maintain of course.

The c2nim tool can generate wrappers following Nim naming conventions (CamelCase etc) but it caused some issues for me so I skipped that part.

## The Makefile

The top level Makefile builds our binary that we can copy onto the LinkIt ONE. It does this by first compiling the Nim source code, for example `blink.nim`, into .cpp source code, which then is compiled using the same commands that the Arduino IDE uses to compile. Normally the Nim compiler calls GCC (or whichever C compiler) by itself, but here I perform the C++ compilation and linking as usual in the Makefile in order to gain a bit easier control over the compilation and link commands.

Btw, this Makefile will also download the SDK and the ARM GCC to local directories, if they are missing.

The Arduino style is to have an include at the top, and then to define the `setup()` and the `loop()` functions that the Arduino framework then will call. This is how `blink.nim` looks like:

```nimrod
# In nim we normally use import but wrapper/ardunimo.nim
# needs to be included via include at the top.
include ardunimo

# ardunimo.nim defines two trivial templates, setup and loop
# making it clean and convenient. This is not the normal
# function syntax in Nim.
setup:
  # Nim is indentation based just like Python
  pinMode(13, OUTPUT)

loop:
  digitalWrite(13, LOW)
  delay(300)
  digitalWrite(13, HIGH)
  delay(300)

```
Before you build and run the above - you need to <a href="https://github.com/gokr/ardunimo#patch-nim">patch Nim</a>. Then you can continue to build and run, see <a href="https://github.com/gokr/ardunimo#building-blinknim">instructions in README</a>.

If we take a closer look at the `ardunimo.nim` file from the wrapper, it looks like this:

``` nimrod
# Some reasonable set of imports for a sketch
import arduino, wiring, wiring_digital, wiring_constants

# I couldn't figure out how to get this include into the
# sketch, it is needed in order to get setup/loop resolved
# from Arduino's main.cpp.
{.emit: """
#include "Arduino.h"
""".}

proc NimMain() {.importc.}

# Convenience templates, nifty
template setup(code: untyped): untyped =
  proc setup*() {.exportc.} =
    NimMain() # Initialize Nim since Arduino will not do it
    code

template loop(code: untyped): untyped =
  proc loop*() {.exportc.} =
    code

```

* The first thing this file does is to import a reasonable base set of wrapper modules. Nim can do deadcode elimination (see `nim.cfg` for the compiler directives) so there is no harm in importing stuff.
* We also use a hack, an emit, to make sure the Arduino.h file is included, I couldn't figure out how to get it otherwise.
* We import the `NimMain()` C-function that Nim has generated so we can call it. This is for Nim's runtime support to get a chance to initialize itself. The entry point of the binary is not controlled by Nim so we need to do this call manually.
* Then we define two convenience Nim templates for `setup()` and `loop()` so that it looks cleaner and to include the call to `NimMain()`. Nim templates are AST based macros and very powerful.

## Making your own
Just write your own **blabla.nim** and then build it using `make clean && make PROJECT=blabla`, it should hopefully work, although remember that the wrapper is by no means complete nor at all tested. :)

`blink2.nim` is similar to `blink.nim` but creates at compile time, a Nim sequence with different pauses in it. `nimicro.nim` is a first step at getting <a href="http://github.com/gokr/ni">the Ni VM</a> running, it fails still, but it can at least run the trivial program consisting of a single integer literal "1000" :)

## Next steps
For the moment this experiment is paused, I am now more focusing on <a href="https://www.mbed.com/en/development/software/mbed-os/">ARM mbed OS</a> based development, so I might end up redoing something similar, but with mbed OS instead of Arduino.

Anyway, hope someone found this interesting and fun!

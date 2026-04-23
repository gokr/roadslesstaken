---
title: Spry Performance
date: '2016-05-24'
slug: spry-performance
categories:
- Spry
- Nim
- Pharo
- JavaScript
- Python
- Smalltalk
- Languages
- Programming
---
When writing Spry I am so far mainly ignoring performance. The general execution of Spry code will be a regular interpreter (although stackless I hope) and not a JIT. But that doesn't prevent us from playing around and learning something!

In this article I do some silly experiments around interpreter startup time and fooling around with 40 million element arrays. As usual, I am fully aware that the languages (Pharo Smalltalk, NodeJS, Python) I compare with a) have lots of other ways to do things b) may not have been used exactly as someone else would have done it. A truck load of salt required. Now... let's go!

![The](/spry/thetruth.jpg){ style="display:block; margin:0 auto;"}

<!--more-->

## Startup time
Spry is pretty fast starting up which obviously has to do with Spry not doing much at all when starting :)

So a trivial hello world being run using hashbang, executed 1000 times from another bash script, takes substantially less time than the same in Python. Useful benchmark? Not really, but obviously we can do scripting with Spry and at least not paying much for startup times! Here are the two trivial scripts and the bash script running them 1000 times:

``` bash
#!/usr/bin/env spry
echo "Hello world"
```

``` bash
#!/usr/bin/env python
print "Hello World"
```

``` sh
#!/bin/bash
# Run a trivial hashbang Spry script 1000 times
for run in {1..1000}
do
  ./hello.sy
done
```

If we run the above, first for `hello.sy` and then `hello.py`, as reported by `time`:
``` bash
# Spry
real	0m4.071s
user	0m0.740s
sys	0m0.428s

# Python
real	0m13.812s
user	0m8.904s
sys	0m2.324s

# Empty shell script for comparison
real	0m2.505s
user	0m0.024s
sys	0m0.176s
```

Hum! So a trivial Spry script is **3-10x quicker** depending on what you count (real clock vs cpu time etc), and... no, it's not output to stdout that is the issue, even a "silent" program that just concatenates "hello" with "world" suffers similarly in Python.

We can of course also compile this into a binary by **embedding the Spry source code in a Nim program** - it's actually trival to do. The 5th line below could of course be a full script. Since the Spry interpreter is modular we can pick some base modules to include, in this case the IO module is needed for `echo` to work so we add it to the interpreter on line 3:

```nimrod
import spryvm, modules/spryio
let spry = newInterpreter()
spry.addIO()
discard spry.eval """[
  echo "Hello World"
]"""
```
..and then we build a binary using `nim c -d:release hello.nim` and if we run that instead from the same bash loop we get:
```
real	0m0.840s
user	0m0.028s
sys	0m0.096s
```

![Neat](/spry/neat.jpg){ style="display:block; margin:0 auto;"}

Of course Python can do lots of similar tricks, so I am not making any claims! But still very neat. And oh, we didn't even try comparing to Pharo here :) Startup times is definitely not a strength of Smalltalk systems in general, typically due to lack of minimal images etc.

## 40 million ints

I wanted to create some fat collection and do some loops over it. Spry has a universal ordered collection called a `Block`. Smalltalk has it's workhorse `OrderedCollection`. Nodejs has an `Array`. Let's stuff one with 40 million integers and then sum them up!

**NOTE: The first numbers published were a bit off and I also realized an issue with Cog and LargeIntegers so this article is adjusted.**

Pharo 4 with the Cog VM:

* Populating the collection: 3 seconds
* Sum the collection using iteration: 15 seconds
* Populating the collection with 1s only: 2 seconds
* Sum the collection of 1s (staying within SmallInteger) using iteration: **0.6 seconds!**

NodeJS 4.4.1:

* Populating the collection: **0.6 seconds!** (weird! sometimes much slower)
* Sum the collection using iteration: 3 seconds
* Sum the collection using reduce: 1.2 seconds

Python 2.7.10:

* Populating the collection: 7 seconds
* Sum the collection using iteration: 4 seconds
* Sum the collection using interation with lambda: **4 seconds!**
* Using sum function: **0.3 seconds!**

Spry:

* Populating the collection: 72 seconds (cough)
* Sum the collection using iteration: 101 seconds (cough, cough)

Spry with activation record reuse:

* Populating the collection: 32 seconds (better)
* Sum the collection using iteration: 60 seconds (better)


Ehum...

![Can](/spry/win.jpg){ style="display:block; margin:0 auto;"}

**NOTES**

* So **Cog kicks proverbial ass** when not spilling into LargeIntegers! Impressed.
* NodeJS is fast, we know that, but Cog beats it on the iteration which was interesting. But NodejS populating in 0.6 seconds? Weird! Sometimes it took 10 seconds, it was almost like NodeJS had some odd "warm caching" going on.
* Spry... is slow :) But a bit of activation record reuse definitely improved it by 2x.
* Python is definitely surprising me! Wow, especially **populating in 7 seconds and summing with lambda in 4? Impressive.**

![Python](/spry/python.jpg){ style="display:block; margin:0 auto;"}


If we spend some time profiling Spry we can quickly conclude that the main bottleneck is the lack of a binding phase in Spry - or in other words - **every time we run a block, we lookup all words**! Unless I am reading the profile wrong I think the endless **lookups make up almost half the execution time**. So that needs fixing. And I also will move to a stackless interpreter down the line, and that should give us a bit more.

And what about Python's `sum` function that did it in **whopping 0.3 seconds**? Yep, definitely the way to go with an optimized primitive function for this, which brings me to...

## Spry Secret Weapon

The secret weapon of Spry!

One core idea of Spry is to make a Smalltalk-ish language with its inner machinery **implemented in Nim using Nim data types**. So the collection work horse in Spry, the `block` is just a Nim `seq` under the hood. This is very important.

Combined with a very simple way of making Nim primitives we can quickly cobble up a **6 line primitive word** called `sum` that will sum up the ints in a block. We simply use the fact that we know the block consists only of integers. I am guessing the `sum` function of Python does something similar.

Here is the code heavily commented:

```
# nimPrim is a Nim macro to make Spry primitives
# First argument is the word to bind, second is if
# this is an infix word (first argument on the left)
# and finally how many arguments the primitive expects.
nimPrim("sum", true, 1):
  # The local variable spry refers to the Interpreter
  # evalArgInfix(spry) is a function call that returns
  # the infix argument evaluated at the call site.
  # We then cast this to a SeqComposite which is the
  # abstract super type of Blocks.
  let blk = SeqComposite(evalArgInfix(spry))
  var sum = 0
  # This is Nim iteration over the nodes member
  # of the SeqComposite, a seq of Nodes.
  for each in blk.nodes:
    # We cast the node to IntVal since we know
    # it's an int, and then we can get the value member
    # which is a regular Nim int.
    sum = sum + IntVal(each).value
  # All Spry functions returns Nodes so we wrap the int
  # as a Node using newValue() which will wrap it as an
  # IntVal.
  return newValue(sum)
```
It's worth noting that almost all primitive words in Spry are written using this same pattern - so there are lots of examples to look at! Of course this is a bit of "cheating" but it's also interesting to see how easy it is for us to drop down to Nim in Spry. We create a new word bound to a primitive function in **exactly 6 lines of code**.

![Spry](/spry/spry-speed.jpg){ style="display:block; margin:0 auto;"}

So how fast is Spry using this primitive word? It sums up in **blazing 0.15 seconds, about 100x faster than Cog and 10x faster than NodeJS** for summing up. And yeah, even 2x faster than Python!

And yes, we can easily make this primitive smarter to handle blocks with a mix of ints and floats and a proper exception if there is something else in there - then it ends up being 17 lines of code, and still almost as fast, 0.17-0.18 seconds! I love you Nim.

In summary, Cog - which is what I am most interested in comparing with - is fast but my personal goal **is to get Spry within 5x slower in general speed** - and that will be a good number for a pure interpreter vs an advanced JIT. And if we throw in primitive words - which is not hard - Spry can be very fast!


---
title: Here Comes Nim!
date: '2014-10-13'
slug: here-comes-nim
categories:
- Smalltalk
- Nim
- Nimrod
- LuaJIT
---
I just posted an article comparing some silly benchmarks between Cog Smalltalk and LuaJIT2. Now... let's take a look at one of the latest "Cool Kids" on the language front, Nimrod - or as it has been renamed - [Nim](http://nim-lang.org).

<!--more--> 

So I love programming languages. But generally I have preferred **dynamically typed** languages because I have felt that the static type systems that we have suffered with for the last ... 25 years or so has basically been completely awful. Perhaps not in implementation performance, but definitely in developer productivity and enabling good quality code.

Working in say Smalltalk has been like roaring free in the skies instead of crawling in the mud with C++, well, you get my point. I still recall one of the first 30 line "programs" I wrote in Smalltalk, just quickly jotted it down - and it ran perfectly at the first try. I attributed that to the concise language and "noise free" code (no static type noise!). My first stumblings in C++? Ha! Its not even funny.

But I have never been against static type information **per se** - I mean, its just a question of what we need to tell the compiler... so if we can have a type system that can reason around my code at compile time **without** bogging me down in endless typing and convoluted code that is hard to change and refactor and hard to read and hard to write... argh! Then yes, by all means.

Many new statically typed languages have started incorporating type inference. I haven't really worked with them, Haskell is perhaps one of the best known. Dart is a dynamically typed language but instead opted to adding mechanisms for static type **annotation** in order to help on the tooling front, a clever idea IMHO.

## Rust, Go and... Nim!

In another article I wrote about [Rust and Go (and more)](http://goran.krampe.se/2013/09/07/new-languages-this-century/) - two new, popular and very interesting statically typed languages. But I admit that I **totally missed Nim!** Previously known as Nimrod, ehrm. And yes, Nim does have type inference, although to a balanced extent.

Just like LuaJIT2 has been a "Tour de Force" of a single author, so has Nim - and that is interesting in itself. I would say it has been a pattern over the years with most successful open source languages.

Ok... so enough chit chatting, let's look at that silly benchmark I played with earlier - in Gang Nim Style:

```nimrod
# Import times for time measurements and future for some upcoming features (naked lambdas)
import times, future

# Just a recursive function, the astute reader notes that we declare a return type of int64
proc benchFib(fib) :int64 =
  if fib < 2:
    return 1
  else:
    return 1 + benchFib(fib-1) + benchFib(fib-2)

# Trivial helper to measure time, discard is used to show we ignore the return value
proc timeToRun(bench) :float =
  var start = epochTime()
  discard bench()
  epochTime() - start


# And this is the bytecode benchmark translated from Squeak
proc benchmark(n) :int =
  const size = 8190
  var flags: array[1..size, bool]
  for j in 1..n:
    result = 0
    # Clear all to true
    for q in 1..size:
      flags[q] = true
    for i in 1..size:
      if flags[i]:
        let prime = i + 1
        var k = i + prime
        while k <= size:
          flags[k] = false
          inc(k, prime)
        inc(result)

# And echo the time to run these two, note the naked lambda syntax "() => code"
# The "&" is string concatenation. The $ before timeToRun is "toString"
echo($timeToRun(() => benchmark(100000)) & " bytecode secs")
echo($timeToRun(() => benchFib(47)) & " sends secs")
```

Whoa! Look at that code! I mean... it looks like Python-something! And not much static type noise going on, in fact there are **only 4 places where I specify types** - the three return types of the three procs, and I also specify that the array has bools in it. That's it.

If you recall the numbers from LuaJIT2:

	10.248302 bytecode secs
	26.765077 send secs

...and Cog:

	49.606 bytecode secs
	58.224 send secs

...then **Nim mops the floor** with them:

	2.6 bytecode secs
	7.6 sends secs

**So Nim is about 4x faster on bytecode speed and 3x faster on recursive calls compared to LuaJIT2. And about 20x faster on bytecode speed and 8x faster on recursive calls compared to Cog.**

A few things of note:

* The Nim code is just as small and readable as the Lua and Smalltalk code.
* The brute speed comes from shoulders of giants, GCC. But it also means that the generated code is fairly C-friendly, which is fascinating given the depth of this language.
* I used a few extra features; const for the size, let for prime (non assignable var), inc() for incrementing variables - but all these didn't affect the numbers much, it was just fun to try to make it more Nimiomatic.
* The above little snippet compiles in 0.2 seconds to a 67kb executable on Linux using the short command "nimrod c -d:release test.nim". Nice!

## Conclusion

I wrote this as a teaser - Nim is actually a **brutally darn cool language**. Lots of people seem to prefer it over Rust - and it has a "pragmatic" soul - Rust on the other hand is very focused on safety, safety, safety. Nimrod is more focused on developer productivity. And it has a lot of nice stuff:

* Written all in itself, clean and nice bootstrap.
* Compiles via C (or C++/ObjC) which gives it very good performance, platform independence and integration with C/C++/ObjC etc.
* Has a very neat modules system
* Has lots of really, really interesting language features. Sure, a bit featuritis perhaps - but I am not judging just yet.
* ...and well, I just can't go through it all here! Its too much!

I would say that if you are thinking of perhaps taking a peek at the "Dark Side" (static typing) - then this is it. I think Nim will make you smile in more ways than one.

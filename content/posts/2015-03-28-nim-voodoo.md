---
title: Nim
date: '2015-03-26'
slug: nim-voodoo
categories:
- Nim
- Nimrod
- Languages
- Programming
---
Having been a die hard Smalltalker since 1994 I have finally found a new language and community that I am investing myself in. All the Ruby, Python, various JVM languages, C# and Mono etc - none has managed to capture my interest. Ruby and Python always felt like pale shadows of Smalltalk and I really don't want to be tied to the Java eco system, no matter what. And so on and on, lots of languages looking interesting but not being able to withstand my deeper look. As a Smalltalker I probably have acquired a particular taste.

Since a few months I am however deeply into Nim. I have written a slew of articles about Nim, and at our company we have decided to bet hard on it. So far I have written a little utility called blimp in Nim, and I have helped creating Urhonimo - the Nim wrapper of the Urho3D game engine.

With a deeper understanding of Nim, although I am far from good at it, what is it that makes me recommend you to try it?
<!--more--> 

## Fundamentals

For me to **really** bet on a language, I mean, really **investing** myself in it, not just dabbling - some things have to be there (in order of importance):

* Cross platform and open source
* Solid story for doing object oriented programming
* Easy to read and write
* Powerful abstraction capabilities
* Turtles
* Large and small enough community
* Decent performance

Cross platform and open source goes without saying. Nim is MIT licensed and truly grass root open source.

I want to be able to do OO when it fits, its my preferred way to deal with complex domain models. I am however fairly open to different kinds of OO and my style stems from Smalltalk and not... factory-abstraction-over-complication-madness like Java people often seem to love. What I have seen so far Nim supports OO quite well.

Easy to read and write is important, but I am not stuck up on specifics when it comes to syntax, as long as its simple enough. This may also be due to Smalltalk which has a rather unique syntax so I am not afraid to learn something different. Nim's syntax is Pythonical in some aspects and clearly designed to be easy to read and write.

With "abstraction capabilities" I basically mean that the language needs to be sophisticated enough in whichever ways it does that. I want higher level programming, collections, closures, various kinds of polymorphism and so on. The particular style achieving it is secondary, but being able to abstract is paramount. Smalltalk is very capable of abstraction through its pervasive use of closures, objects and dynamic typing. Nim is also very capable but uses closures, objects, methods, generics and compile time macros. A very different mix of mechanisms that in the end reaches the same level of abstraction power.

So... what about "Turtles"? Some of you probably recognize this and what I refer to is that I want the language to be growable and malleable, thus a big part of the language and of course its libraries, should be implemented in itself. Turtles all the way down. I find this essential, otherwise I will not be able to help evolving the language and its libraries nor will I be able to tailor it to my own needs. A growable language is also important for it to be able to evolve as open source.

Ideally there should not be a difference between the constructs I create as a developer versus the constructs available to me in the language and base libraries. In other words they should as far as possible be "first class". The Nim compiler is written in Nim. The base libraries are written in Nim. Heck, even the garbage collector is written in Nim! Extending the language is easy and there are very few non malleable things.

I want the community to be **large enough** to produce an eco system that is useful, but at the same time **small enough** so that I can actually be an active part of it and make a difference, and be heard! :) This last bit is something most people miss - they just think "the bigger the better". Nim is a perfect size for me, the base libraries are ok, the package manager has around 140 packages registered and the community is fairly large with around 130 people on IRC and a lively web forum.

Performance is not a crucial factor for me, as long as it beats Ruby/Python I am fine, Smalltalk is normally JITed and typically beats them but doesn't reach C/C++ levels. Nim is on the same level of performance as C/C++.

There are probably other languages that satisfies the above fundamentals. :)

## Killer features

Nim has a few features that together truly makes it shine. Individually they are not unique, there is always some language out there, but the magic arises when they play together:

* Meta programming
* Deep extensibility
* Focus on helping the developer

The meta programming part is probably the strongest single selling point of Nim. Its Nim's "main weapon" which it uses for many things.

....examples of macros and templates.... iterators?

The deep extensibility comes in a few mechanisms working together:

* Behaviors are in the form of free procedures
* The unified calling syntax makes them "message like"
* Operators are also procedures
* There are hooks for []-access, dot-access etc

The fact that the behaviors are "free procedures" (not bound to a class concept) means we can extend types not defined in our own modules, including base types like `seq` which is the dynamic array workhorse in Nim. For example, in Smalltalk we have *collect:* which is called `map` in Nim. In Nim `map` is actually defined in the system module so its always available.

But in Smalltalk we also have *collect:with:* that does the same but operates on two collections at the same time and expects a closure that instead **takes two arguments**. Adding it is trivial, 3 lines of code actually, if we skip the comments:

``` nimrod
import future

proc mapWith*[T, W, S](data1: openArray[T], data2: openArray[W], op: proc (x: T, y: W): S {.closure.}): seq[S] =
  ## Returns a new sequence with the results of `op` applied to every item in
  ## `data1` and `data2` until either of them runs out.
  ##
  ## Since the input is not modified you can use this version of ``map`` to
  ## transform the type of the elements in the input sequence. Example:
  ##
  ## .. code-block:: nim
  ##   let
  ##     a = @[1, 2, 3, 4]
  ##     b = @["a", "b", "c", "d"]
  ##     c = map(a, b, proc(x: int, y: string): string = y & $x)
  ##   assert b == @["1a", "2b", "3c", "4d"]
  newSeq(result, min(data1.len, data2.len))
  for i in 0..result.len-1:
  	result[i] = op(data1[i], data2[i])

when isMainModule:
  var
    a = @[1, 2, 3, 4]
    b = @["a", "b", "c", "d"]
  var c: seq[string]
  
  # Using a regular proc
  c = mapWith(a, b, proc(x: int, y: string): string = y & $x)
  assert(c == @["a1", "b2", "c3", "d4"])
  
  # Shorter with lambda syntax, but needs types on params
  c = mapWith(a, b, (x: int, y: string) => y & $x)
  assert(c == @["a1", "b2", "c3", "d4"])

  # It should work if one of the seqs is larger
  a = @[1, 2, 3, 4, 5, 6]
  c = mapWith(a, b, (x: int, y: string) => y & $x)
  assert(c == @["a1", "b2", "c3", "d4"])
```

Above we see that we first import the future module giving us access to the lambda syntax for procs, which is quite elegant. Then we define the new `proc` called `mapWith` instead of the regular `map`. The signature may look a bit complicated, but:

* The `*` just marks this procedure to be exported (not needed in this example though)
* The `[T, W, S]` are type parameters that will be resolved during compile time at the call site. These type parameters can then be used in the rest of the signature and body of the procedure making this procedure generic for several combinations of types.
* Then we define three parameters, `data1`, `data2` being the two collections we want to iterate over. Using the special type `openarray` Nim will allow both arrays (fixed size) and seqs (dynamic size) being passed in. The type parameters `T` and `W` here indicate that these collections may have different types for their elements, and we do not specify them here, its for the caller to do so.
* The `op` argument is the closure with the signature `proc (x: T, y: W): S {.closure.}`. This can be read as *"a procedure taking two arguments x and y of type T and W respectively and returning a result of type S"*. Its also annotated with a pragma saying that we accept a closure here.
* Finally the type for the result will be `seq[S]` which means we will return a seq with elements of type `S` which thus obviously can be different from both T and W.

Then the implementation is very straight forward. We allocate the new seq of correct size (the smallest of the two collections passed in) and then we iterate and run `op` for each element from the two collections as a pair and collect the result.

This is a very nice characteristic when a language is being "grown" because it means anyone can easily participate in extending the base libraries. The extension can be added and used non intrusively, and then if it turns out to be useful we can share it as a library, and eventually one can also decide to simply merge it into the module that we are extending.

The code that comes later is only compiled and executed when we compile this module as a standalone executable. This makes it a nice place to put basic tests. Here we use the simplest possibly style for testing, just doing a series of asserts. 


The unified calling syntax may seem only like "makeup" but the fact is that it enables the programmer to more clearly show object oriented intent - that the first argument is responsible for the behavior.


Examples of the last part is:

* Keeping the standard library pragmatic
* Automating silly things
* Approachable base code



## How to start

If you do decide to give Nim a spin (and a lot of people do these days), then I can recommend [Nim by example](http://nim-by-example.github.io/getting_started/) and [How I start with Nim](http://howistart.org/posts/nim) as good ways to get going.

The more detailed path for enlightenment may look like this:

1. Browse [Nim-lang.org](http://nim-lang.org), and [get it](http://nim-lang.org/download.html). You may also want to get IDE support.
2. Take a look at the [Learn](http://nim-lang.org/learn.html) section, [all my Nim articles](http://goran.krampe.se/category/nim) can also be reached at the bottom list of article links.
3. Log into #nim channel on freenode, lots of people willing to help! Or use any [other means of communicating with the community](http://nim-lang.org/community.html).


## What I forgot to shown

Especially the presentation of Go by Marcus made me often think *"Oh, shit I forgot to show Y"*, the stuff I can think of right now are:

* Nimsuggest in Aporia
* Point out the IDE support
* Some details of the toolset
* Objects in Nim
* Size and nature of executables
* Standard libraries and nimble
* Noteworthy projects
* Multiple assignment
* Typeclasses
* Concurrency

So... let's go through the above list.

I missed showing the cross referencing capabilities of Aporia - using [nimsuggest](https://github.com/nim-lang/nimsuggest) (replacing the old nim IDE tools) which is **the compiler running in a server mode incrementally parsing Nim code** and being able to answer queries like "go to definition" or do proper completion. The nice part here is of course that its the actual compiler doing it - so it will be correct by definition - and all IDEs can use the same mechanism :)

I did show Aporia, but there are [lots of IDEs with Nim support](https://github.com/Araq/Nim/wiki/Editor-Support) in various degrees. Sublime, Emacs and Vim all have fairly good support I think. There is also [VisualNimrod for VS](https://github.com/barcharcraz/VisualNimrod), but uncertain about its current status.

Nim has a few tools that are important to mention. First of all the `nim` compiler handles dependencies etc, so no need for Makefiles or the likes. It can also generate documentation in HTML or JSON from the source files which uses the so called "doc comments" (starting with two ##) that are in reStructeredText format. All documentation is built this way, for example [the standard library](http://nim-lang.org/lib.html) which is actually not that shabby :). There is a `nimfix` tool that can help with porting Nim code to the latest compiler, although in beta. There is no formatter or linter yet AFAIK. There is a tool called `niminst` that produces installers for Nim programs and this is used for the Windows installer etc of Nim itself. The tool called [c2nim](https://github.com/nim-lang/c2nim) I did mention and its a very important tool for wrapping external libraries in C or C++.

Objects in Nim is something I didn't show at all, but I have **covered them extensively in my 4 articles on OO in Nim**, this is [the last one with links to the preceeding](http://goran.krampe.se/2014/11/30/nim-and-oo-part-iv/). IMHO the capabilities to do OO in Nim are quite nice. Its also worth mentioning that just like Go Nim has no special kind of constructors - and I agree this is a strength. A similar approach is used with exporting `newXXX` procedures that returns new objects of type XXX, thus encapsulating the implementation details.

Size and nature of executables? Nim compiles via C/C++ typically and produces small and fast statically linked binaries by default. You can build both static libraries and dynamically linked libraries too, but nim modules are normally handled as source. The examples I showed range from **around 60kb for Helloworld, 70kb for sumlines to 95kb for the slightly more complicated example** with lambdas etc. Note that by default nim compiles with debug info, so you need to add `-d:release` option to get these small binaries, otherwise they are slightly larger.

Standard libraries are included with the compiler download of course, and does cover a fair set of stuff and growing all the time. There is also a neat Nim package tool called [Nimble](https://github.com/nim-lang/nimble) (earlier called Babel) that currently has around 140 packages. No, not close to either Rust or Go, but ... again, not shabby.

Some noteworthy projects I should have mentioned are [Jester](https://github.com/dom96/jester), a sinatra like web framework using the new asynchronous networking code and the [Nim forum](https://github.com/nim-lang/nimforum) written in Jester using Sqlite. Here is the [web forum of Nim](http://forum.nim-lang.org/). 

Someone asked about multiple assignment (and I was at a loss of what it meant at the time) and yes, you use the tuple unpacking style as [described in the manual in the section on var parameters](http://nim-lang.org/manual.html#var-parameters). But recently Billingsly Wetherfordshire (aka fowl or fowlmouth) showed how you can use Nim macros to support [tuple unpacking of arrays too](http://forum.nim-lang.org/t/1044), its a pretty slick example of Nim's power when it comes to extensibility of the language.

One area I did mention very briefly but didn't elaborate on is [type classes](http://nim-lang.org/manual.html#type-classes) and especially [user defined such beasts](http://nim-lang.org/manual.html#user-defined-type-classes). There is a good [article describing the latter](http://vocalbit.com/posts/exploring-type-classes-in-nimrod.html) and its IMHO very fascinating stuff, haven't used it yet myself though.

Finally... concurrency. Nim has a default model of "share nothing" threads each with their own heap and GC. Communication is done via channels, but there is also a slew of low level support for shared memory concurrency so... there is [more than one way to do it here](http://nim-lang.org/manual.html#threads).

## Conclusion

Nim is lots of fun and it was a long time ago since I was this impressed by a language not being Smalltalk. :) So hop in and join the fun, I am **gokr** on #nim/freenode, feel free to ask away.

Happy hacking!

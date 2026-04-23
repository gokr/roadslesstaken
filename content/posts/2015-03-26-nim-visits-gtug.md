---
title: Nim visits GTUG Stockholm
date: '2015-03-26'
slug: nim-visits-gtug
categories:
- Nim
- Rust
- Go
- Nimrod
- Languages
- Programming
---
Yesterday I had the pleasure of presenting the programming language [Nim](http://nim-lang.org) at the [Stockholm GTUG](https://sites.google.com/site/stockholmgtug/).
This evening we were around 50 people, I would guess mainly developers, listening to three presentations:

* [Rust](http://rust-lang.org), by [Johan Burell, EVRY](https://www.linkedin.com/in/johanburell)
* [Nim](http://nim-lang.org), by Göran Krampe, 3DICC
* [Go](http://golang,org), by [Marcus Olsson, Citerus](https://www.linkedin.com/in/marcusolsson1)

Now, that's a pretty fitting trio of languages! :) This article is a little followup because I failed to mention so much stuff...

<!--more--> 

## Rust

So... Johan Burell started with presenting [Rust](http://www.rust-lang.org/). After his presentation I still have the same **personal** feeling about Rust. I do **love** the fact that Mozilla is pushing the envelope with a new language. And I can sense their reasoning - they want to crank out maximum performance for a new browser using the future multicore machines people will have, and it must be rock solid. But... there isn't room for **productivity or programming convenience** in that vision...

And that's my main conclusion, its not a language for me because I want a language that makes it fun and easy to program. I don't want to battle a compiler and I like a good garbage collecting system or similar means of freeing me as a developer of arduous tasks. I like exceptions for error handling, well, not as they work in Java, but hey, exceptions work just fine in many other languages.

Just as most developers I can appreciate the sense of accomplishment when you *"beat the compiler"* in these less forgiving languages (think C or C++), but I don't want to work full time in that kind of hurt ;)

But thanks Johan for giving a better taste of it, and thanks to the Rust community for pushing forward in the language development arena challenging the behemoths, which of course benefits all new languages and their acceptance - not just Rust.

## Go

After Johan I presented Nim, but before I get to that I would like to talk about the last presentation - Go by Marcus Olsson.

Marcus described quite well the reasons and history of Go, and also made his point that the **tooling around Go is the primary strength** - not the language itself. I haven't been following Go closely but it seems to be gaining lots of traction perhaps as a *"cleaner no-nonsense"* alternative to Ruby/Python/Java for writing network server code. At least that's the impression I have, and I wrote more about Go in [my article covering languages since 2000](http://goran.krampe.se/2013/09/07/new-languages-this-century/) and also in [my article about missing Nim](http://goran.krampe.se/2014/10/20/i-missed-nim/).

For some criticism [check](http://yager.io/programming/go.html) out [what](http://jozefg.bitbucket.org/posts/2013-08-23-leaving-go.html) what [others](http://www.quora.com/What-reasons-are-there-to-not-use-Go-programming-language) say. But hey, this is just my **personal** opinion (and no, I haven't actually used it - but I can already say it wouldn't make a difference) - Go isn't for me, I don't want to sacrifice that amount of capabilities just in order to reach simplicity - languages like Smalltalk (and Lisp etc) has already shown to me that **you can have both marvellous capabilities and simplicity**, and I would argue Nim is showing the same, albeit in a much different way.

I do however think there is **lots to learn from the community around Go and its toolset** and it was fun seeing several of these tools and how they are perceived by a Go developer.

## Nim

I presented Nim, and hopefully it was fun and made some people decide to give it a closer look, which was the idea. It is however very hard to make a language like Nim justice in such a short timeframe, you would typically need 3 hours or similar to be able to give a more complete picture.

But if you do decide to give it a spin (and a lot of people do these days), then I can recommend [Nim by example](http://nim-by-example.github.io/getting_started/) and [How I start with Nim](http://howistart.org/posts/nim) as good ways to get going.

The more detailed path for enlightenment looks like this:

1. Browse [Nim-lang.org](http://nim-lang.org), and [get it](http://nim-lang.org/download.html). You may also want to get IDE support.
2. Take a look at the [Learn](http://nim-lang.org/learn.html) section, [all my Nim articles](http://goran.krampe.se/category/nim) can also be reached at the bottom list of article links.
3. Log into #nim channel on freenode, lots of people willing to help! Or use any [other means of communicating with the community](http://nim-lang.org/community.html).


## What I forgot to show

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

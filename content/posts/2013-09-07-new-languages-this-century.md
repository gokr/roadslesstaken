---
title: New Languages After 2000
date: '2013-09-07'
categories:
- Programming
- Languages
- Computing
---
I am sitting in a gate on an airport waiting to go to [ESUG](http://www.esug.org/wiki/pier/Conferences/2013) so I felt I should finally get this article out the door. In a presentation earlier this year I asked what has happened in the programming language area since year 2000? *Not much* I felt and I couldn't really name any interesting new language when thinking about it. But then I decided to look more closely and I can conclude I was at least partly wrong :)

So prepare for a **long** (too long) article digging through a whole bunch of languages trying to come up with the answer - *Have any interesting programming languages appeared since year 2000?*

(And at the end, how is the Smalltalk community doing?)

<!--more--> 

Googling wikipedia and more gave me this list of languages (and yes, you may point out more in the comments I am sure) that seem to be "somewhat successful" and were born after 2000:

- 2000: D, C#
- 2002: Io
- 2003: Scala, Factor, Nemerle
- 2004: Boo, Groovy
- 2005: F#
- 2006: Cobra, Cyclone
- 2007: Vala, Fortress, Fantom, Clojure, Nu
- 2008: Pure
- 2009: Go
- 2010: Rust, Gosu
- 2011: Dart, TypeScript, Clay
- 2012: Julia, Ceylon

## Here comes the broom

I have excluded several already due to different factors that indicate to me that they will likely not reach any kind of critical mass of adoption. And let's get the broom out again and prune this list so that it includes the ones that **I** think may be worth keeping an eye on. Please remember this is **my personal take** on these languages driven by **my personal taste** and experience.

[C#](https://en.wikipedia.org/wiki/C_Sharp_(programming_language) is legacy by now and well, not really interesting to me. Yes, I have coded a fair bit in both C# and Java and both will be around for a long time - but I really do consider them boring and frustrating :)

[D](http://dlang.org) is impressive by all means, technically a contender with C++ - but I do not think it offers enough differences to dethrone C++ from its niche and it is (just like C++) a complex language and I think that a successful new language should not have to be that complex and it definitely needs to **bring something new** to the table and not just be a "cleaner C++".

[Io](http://iolanguage.org) is a small very nice language, but not going anywhere - just wanted to mention it :)

[Factor](http://factorcode.org) is another real LSD trip, immensively impressive but being a concatenative (thus fairly cryptic to most of us - although Forth is way cool) language I consider it doomed to be a niche player, nothing wrong with being that of course! Can be a source of inspiration.

[Nemerle](http://nemerle.org) as well as [Boo](boo.codehaus.org) and [Groovy](groovy.codehaus.org) suffer from the *"Why not just use Java/C# then?"* being languages focused on the CLR and JVM platforms respectively with seemingly too little momentum behind them compared to *other* languages on these two runtime platforms. I don't think they stand much of a chance in the longer run. And yes, they are different - Nemerle is functional and Groovy is dynamically typed for example - but still, my impression is that they are being dwarfed. [F#](http://fsharp.org) and [Clojure](http://www.clojure.org) share this problem - and being functional also narrows down the audience. Although I agree that Clojure has seen lots of hype.

[Cobra](http://cobra-language.com) seems to be a kitchen sink language built ontop of the CLR runtime, and while touting a fairly massive feature list it didn't tickle me. Languages that try to implement as many features as possible is not up my alley. [Cyclone](cyclone.thelanguage.org) seems to be a "safe C" and while possibly useful I don't think that punchline will attract enough people.

[Vala](http://live.gnome.org/Vala) is a niche Gnome language which is statically typed, depends on GObject and Glib, uses reference counting and compiles through C. An extremely pragmatic approach and clearly a step up for C developers working in Gnome, not interesting enough though.

[Fortress](http://en.wikipedia.org/wiki/Fortress_(programming_language) is officially dead, so not really more to say about it, it did have some cool stuff in it, but it was also aimed squarely at the mathematical community turning it into a niche language.

[Fantom](http://fantom.org) seems to be an attempt to harmonize Java and C# and cleaning up a lot of things, IMHO doomed also since it just isn't different enough to gain any reasonable following and I also think those two communities "don't mix" that much. On paper I can agree with lots of its design decisions, but where is the community? Where is the momentum? Can't see it.

The [Nu](http://programming.nu) language is a Ruby/Lisp language built ontop of Objective-C... not interesting to me, too much niche (says the Smalltalker).

[Pure](https://code.google.com/p/pure-lang/) is functional, and with a focus on LLVM as the backend it might get some followers in the functional crowd, but again, sorry, I think pure functional languages still fight an uphill battle - and personally I am not comfortable in them. ;)

[Gosu](http://gosu-lang.org) is a Scala competitor that is simpler in several ways (which is probably a plus for many), less mature and less intrusive in how it modifies Java. But still a **"cleaned up Java"**. [Ceylon](http://ceylon-lang.org/) is RedHat's answer to **"the next Java"** and also tries to be simpler than [Scala](http://www.scala-lang.org). All these three turn me off since they are JVM languages (ok, so Ceylon can also run on Javascript...). I am sorry, it's not rational - but there it is.

**But that doesn't mean you shouldn't keep an eye on them** - I think one of these may very well end up being the long term successor of Java that Java sorely needs, although it will take a few years (or decades). If these languages make the lives a tad better for the hoards of Java developers - then that is indeed a good thing :)

This boiled the list down to **Go, Rust, Clay, Dart, TypeScript and Julia**.

[TypeScript](http://www.typescriptlang.org/) is also a turnoff for me, simply because **it isn't ambitious enough - same goes for CoffeeScript which I didn't even bother to list, it's just syntactic sugar**. TypeScript is of course more than CoffeeScript, but being a pure superset of javascript is not making me smile. And oh, Microsoft? Ehrm. All respect to Anders Hejlsberg though, no shadow on him.

[Clay](http://claylabs.com/clay/) is an interesting language and plays in the same "systems programming" arena as C/C++/D/Rust do - if you let me generalize a bit. So Clay is basically a C++ competitor but cleaned up and adding type inference, multiple dispatch and lambdas etc. Unfortunately I don't think it has enough push behind it to compete with the others, the original author lost interest and well, things probably stalled. Unfortunately.

## So what is left?

It seems the **last 13 years** have produced the following short list of **REALLY** interesting new languages with a plausible chance of becoming more than curiosities (and of course, I **will** be wrong on this prediction):

- [Go](http://golang.org). The Erlang inspired semi low level language from Google. Has traction, quite a bit of libraries and seems like fun and with good performance, around 1/2 of C. Not LLVM based, compiles using own compiler or GCC toolchain.
- [Rust](http://www.rust-lang.org). The low level high performance system programming language from Mozilla with lots of new interesting concepts. Finally a C/C++ replacement? Compiles through LLVM. Beta but clearly has attention and promises of good performance, although I am not sure about the current state.
- [Dart](http://dartlang.org). The high level dynamically typed javascript killer from Google. In fact, Dart is IMHO a "Smalltalk in disguise" (not surprising given the background of several of the team members) and is the only language in this pack that is also targetting the client side of HTML5 _and_ the server side. And yes, at least two of the languages I discarded promise the same - Ceylon and Typescript. Dart has both its own V8-ish VM and can compile to javascript. Performance using its own VM is already a bit better than javascript on V8.
- [Julia](http://julialang.org). A high level dynamically typed multiple dispatch language with performance close to C? Extremely impressive from several points of view, also LLVM based.

All these four languages are fascinating and all have some characteristics I would consider *"new stuff"*. So I have to retract my view that there hasn't been any new interesting languages the last decade, that is simply not true. On the other hand, none of them has *yet* gained any substantial momentum.

It is also interesting to see that they cover different domains, with some overlap of course, but they do not really compete fully head to head. Rust wants to replace both C and C++ and can be used without a runtime just like C, it has GC but it is optional. Go has GC so for really low level things it is probably not suitable, it seems to be more of a *"service level"* language (kinda the same niche as NodeJS) - not what you use to build an OS or a VM with, but definitely what you can use above that level. Both Go and Rust are statically typed. Dart and Julia are dynamically typed high level languages.

All seem to have good performance in relation to their design choices. Three of them use LLVM as backend technology (well, ok, I did filter out all the JVM/CLR competition!) - which is a smart choice since primarily Apple has been pouring TONS of effort into that toolchain and I guess it is only **a matter of time before it replaces GCC**.

Go and Dart are from Google and Rust from Mozilla so all but Julia are backed by organisations. Julia on the other hand is coming from academia. Dart is fairly obviously aimed at the web. Julia is primarily aimed at math.

Now, let me give you my personally biased view on these four languages **without actually having coded in them - yeah, I know, silly me, so take it with a huge grain of salt!**

##Go

Go is interesting and a lot of people love parts of it and ... a lot don't. The language is statically typed with a clear C syntactic inheritage. Go is not object oriented in any traditional point of view - but it has mechanisms that seem to reach more or less similar capabilities. First of all, one can associate functions with structs to create "classes", seems fine but I do fail to see the advantage over calling them "classes" and keeping the methods declared inside? Perhaps this "structs + functions" has some subtle difference I am missing.

There is no inheritance but one can compose structs without naming the members, this will expose the members of that "anonymous" member on the outside of the parent struct, a sort of **transparent automatic delegation**. So this gives us inheritance by composition (an area I feel has been lacking in general in the OO world) - so this is **clearly an interesting approach**.

Another nice idea is how interfaces work in Go - the struct that "implements" an interface doesn't need to say so! This is also something I have been looking for in statically typed OO languages for a long time. Of course, in dynamically typed OO languages we have this "automatically" so to speak. This decouples interfaces from the implementation and turns it into a one sided dependency. One can add interfaces implemented by "old code" etc, **kind of the static equivalence of formalized duck typing**.

I do like minimalistic languages and Go is definitely trying to be small, but if we compare to other minimalisic languages like Smalltalk and Lisp - the thing that makes these languages "get away" with being small - is the fact that they have powerful meta capabilities in which to implement mechanisms in libraries instead of in the language. Smalltalk for example has an Exception model more powerful than the one in Java, and it is all created in Smalltalk without modifying the language or the VM.

So if you try to be minimal you need careful design - and one of the areas in Go that feels... too much 1970 is the error handling model. I can sympathize with trying to find something simpler than Exceptions, but this "mix" of error mechanisms in Go feels cobbled together without true thought, and I don't think it makes very readable code either. But don't take my word for it - **perhaps it is simply brilliant and I can't see it**.

Only one loop keyword and that is "for"? Ok, perhaps I can buy that. No generics in a manifest statically typed language? So they added special case generic array and hashmaps, but that only removes the casting pain for these builtin collections. Mmm, ok. All in all I hesitate regarding Go and I did find someone managing to put his finger on it:

> "So, where is Go supposed to fit? I'll gladly acknowledge Go is a far better C, with garbage collection. But the GC makes it unacceptable for the only types of problems I'd ever consider using C for. And if I'm willing to put up with a GC, I'd always prefer Java/Scala/Python/Lisp/Haskell over Go for any problem I can think of."

At the same time Go seems to be attracting developers from the Ruby/Python camp that are looking for higher performance and better support for concurrency - instead of people from the Java camp sick of complexity, as some might have predicted.

In summary, performance seems pretty good and I like the "inheritance by composition" and the "duck type interfaces" - clearly an **interesting** language, but for me Go doesn't find a proper niche.

28 committers on google code, most from Google. And a **really ugly homepage :)**

## Rust

Let's get our hands even dirtier with some rust. This is hard core stuff and reading the tutorial while putting on your "close to the metal" hat it starts out really good:

- Type inference! Yes. A must have in a modern statically typed language I think.
- Almost everything is an expression. Very nice! Just like in Smalltalk.
- There is a nil type with a single value - (). Nice. Syntax? Odd, but ok.
- There is a bool type with proper literals true and false. The way it should be of course.
- There is a char type which is a 4 byte unicode point. Nice! As a Smalltalker it is obvious, but still good.
- Casting is done using &lt;expression&gt; as &lt;type&gt;. Also fine, readable.
- Regular operators etc like in C, fine, can live with that - we are on the metal after all.
- Syntax extensions with a clear marker (!) and use proper/clean AST macros. Ok, this is... advanced stuff and **somewhere here the language starts slipping into the darker land of complexity.** But let's give them the benefit of the doubt.
- Only bool works in conditionals. Thank you, thank you. C and Javascript really botched booleans so I am glad Rust is sensible.
- Has a match statement which is a switch statement on steroids, seems very powerful bordering on over engineered. This is begging for abuse.
- And then we get to **the core of Rust, the three different kinds of memory and how to work with references to them**. In theory, cool. In practice? Not sure. Very quickly the code starts looking like ... **Perl. And that is NOT a good thing :)**.

Reading the mailing list a bit shows "where" the language is currently and yes, [it is early, but moving fast](http://cmr.github.io/blog/2013/07/05/the-state-of-rust/) and participation is heating up. If you try to follow the discussions on the mailinglist you quickly realize that Rust is not a simple language - there are a lot of nuances here in the joint complexity created by mutability, generics, three kinds of pointers and just to make it a true headshot - pointer lifetimes. One thing that I did notice is that it is [already quite performant at version 0.6](http://attractivechaos.wordpress.com/2013/04/06/performance-of-rust-and-dart-in-sudoku-solving/).

If all these features don't make your head spin, well, then perhaps you are a seasoned C++ programmer - nothing scares them. :) It scares me though. The problem is - each concept on its own may seem logical and reasonable. But its the mix that makes it go "ouch". But the authors of Rust are very aware of this "cognitive burden", the question is - can they do something about it? And do they want to? I am a reasonably experienced developer but I want to use my brain cells for the domain and not for fighting the compiler.

This interesting quote positions Rust vs Go etc:

> "Rust is basically ML + C's lovechild. Sophisticated type inference, mostly pure variables, pattern matching lambda functions, a few other FP goodies. But it's also a fairly clean imperative language if you care to use it like that. Generics, mutable variables, {}; syntax, pointers, etc. Also, more fundamentally, I see D, OCaml, and Rust as occupying a "let's be clean" kind of space.
> I see Go as occupying a "let's be scruffy" space; not really pushing the language state of the art, focused on industrial work; it's like a type-safer & compiled python, afaict. It doesn't really strive to push the state of the art, it seeks to solidify certain well-known taken ground in programming language design, and to be really focused on that."

And from Reddit, let me include a longer very good quote:
> The hardest part of memory management in C is working out when allocated memory should be freed again. As such, people come up with patterns to give rules for when they should free memory. Rust basically takes some of the most popular patterns, and bakes them into the language itself:
>
> Something very common in library functions is "I got this pointer from somewhere else; I'm not going to worry about how it's allocated and just use it". This is Rust's &T; you can do what you like with it apart from keeping copies of the pointer itself (because for all you know, it might be freed immediately after you return).
>
> Another common pattern is "ownership semantics", where the idea is that you designate a function/struct/whatever responsible for the lifetime of the pointer, and everything that no longer needs the pointer has to either pass it to something else (which takes ownership of it), or free it. This is Rust's ~T, for the owner. (And if the owner passes temporary copies of it to other functions to look at, they get an &T.)
>
> Finally, for pointers with complex usage, many projects will simply use garbage collection or reference counting. This is Rust's @T, which basically just tells the compiler to use a garbage collector on the pointer, and then you can pretty much do what you like with it (as in Java or another garbage-collected language).
> — ais523 http://www.reddit.com/r/programming/comments/10yb5q/rust_refining_traits_and_impls/c6hybv6

I do like these ideas and I think they would work wonders in communication between concurrent threads and more. But my head still easily has a hard time parsing the code. A final quote yet again warning about complexity:

> "The common liturgy of language design is that x feature makes development easier, less error prone, safer, etc. Nearly always, the precise way in which x feature does this is as clear as a bell. But somehow, as we multiply the number of features, something truly destructive starts to happen. It's not just diminishing returns . . .
> I think about a language like C++. I can see the reasons for every single thing in it. I can understand the arguments for why this or that is a good thing. But it is perilously easy to write very unmaintainable code in this language, and to understand why, I think we have to get beyond the usual debates (static vs. dynamic, functional vs. OO, compiled vs. interpreted, etc). Small vs. large might be one place to start."

Still, I think Rust is going places as "a new C++". Mozilla is pushing hard, the community is boiling, the developers seem sharp and although the language is quite immature - **I don't see any other modern strong competitor fighting for the same spot**. C++ is not modern and no, I don't think D will take off in any substantial way.

587 forks and 267 contributors on github.

## Dart

Ahhh. Dart annoys me. As a Smalltalker I *should* like it, but I have a hard time getting itchy to try it. Ok, so:

- Syntax: JavaScript and C#
- Object Model: Smalltalk
- Compilation Strategy: Self
- Optional Types: Strongtalk
- Isolates: Erlang

(picked from a slideshow)

If one just takes a cursory look it **looks** like Java. It has the boring C curly brace syntax. It has types. But wait, it actually is NOT statically typed, it is **dynamically** typed. It turns out the types are simply "annotations" used by tools and giving more information to the developer. They are fully optional. They have ZERO function during runtime. And since the object model is basically from Smalltalk the net result is that Dart actually is very close to Smalltalk. And at the same time... not.

Things I find annoying already on paper:

- The IDE is an Eclipse derivative, just as boring. It might be good compared to... emacs. But as a Smalltalker it doesn't excite me. Sure, I know the history of the Eclipse project, and I did really like VisualAge (even the Java variant was nice).
- The language, tools and libraries are very web centric. Sure, fine, but it doesn't feel "general purpose" yet. Smart focus? Perhaps.
- The code looks so... boring. I can't help it but it really, really turns me off.
- The javascript integration looks pretty... messy, on paper. Or did I miss something? Not sure. I think that part is heavily worked on though.

And at the same time they are pushing hard, performance on their own VM looks very good (2x better than javascript more or less) and they seem to still be serious about it.

So I think Dart has potential, but at the same time... it looks like Java, in order to attract Java people but... what if Java people then still prefer Java? Will it attract enough web developers to get serious against javascript? Doubtful.

15 committers on google code, almost all from google.

## Julia

Perhaps the most impressive of all these four languages is Julia. It's a **dynamically typed language that aims for C performance**. Ok, so you have heard that one before, right? But Julia seems to not only be "huff and puff" - on a series of micro benchmarks Julia is already **less than 2x slower than C on all of them**. This means it beats V8 (js) on all of them and beats FORTRAN in 5 out of 7. Given that the Julia developers have "just started" I think they have a fair chance of reaching their goal, especially since they already *match C* on 2 of these micro benchmarks.

So a dynamically typed language with screaming performance? Ok, so Strongtalk was fast. And there are Smalltalk implementations that are quite fast, and Lisp of course. But **matching C**? Oooh, don't know about you but I think that is a first.

Interesting. And when you start looking closer you realize that Julia is more than a lanugage for math, for example this little [blog post](http://julialang.org/blog/2013/03/efficient-aggregates/) shows they are clearly pushing a few boundaries on the language front.

Julia seems to be picking very good base C libraries for performance, same libuv that NodeJS uses, and of course many math libraries since after all - **math is the focus of Julia**.

And oh, guess who I noticed posting on the Julia mailinglist? Avi Bryant (hey Avi!). Since Avi clearly has a nose for "good stuff" I find that very interesting! :) So I need to look closer at Julia, for sure. It has an academic feel so far, not at all a bad thing, but I hope they also manage to build a community and broaden the effort - **not seldom has brilliant academic stuff failed to build a community and eventually withered away**. On the other hand github indicates it is doing well so far!

469 forks and 149 contributors on github.


## And Smalltalk?

Being a hard core Smalltalker I of course want to ask myself: **How is the Smalltalk community stacking up against these new four challengers?**

The top players in the open source (I only care about that) Smalltalk world today is [Pharo](http://www.pharo-project.org) and [Amber](http://amber-lang.net) IMHO. Pharo has its own JIT VM called [Cog](http://www.mirandabanda.org/cog/) (shared with the Squeak project which Pharo forked from) which is not as fast as V8, but still quite fast. Pharo has a strong community and is evolving in an increasing speed.

Traiditionally Smalltalk - given its design - has been less ideal when it comes to interfacing with external libraries. Sure, in Squeak/Pharo we have always had FFI, VM plugins etc, but no "automated wrapper thing" like Swig or such. And even if the FFI and plugin mechanism is there - the intricacies of interfacing with the C world and its notion of structs and pointers and basic C types have been fairly demanding. Smalltalk is a very pure OO language and just the issue of mapping and converting basic types can be hard.

Now things are looking brighter because [Igor Stasenko](http://www.smalltalkhub.com/#!/~sig) in the Pharo community has been pushing hard with the new low level infrastructure called [NativeBoost](https://code.google.com/p/nativeboost) (NB for short). NB is more or less a dynamic assembler implemented as a Smalltalk internal DSL. So yeah, you can write assembler - but in Smalltalk. And more importantly - you can do it dynamically during runtime. So in a more philosophical way *Smalltalk is breaking out of its VM*. 

Without going any deeper, this is opening up new ways of interacting with the outside world of C libraries and the metal in general.

The Smalltalk community is one of those communities that will never die, just like Lisp I imagine. I am right now sitting at [ESUG](http://www.esug.org/wiki/pier/Conferences/2013) (Camp Smalltalk) together with 24 other Smalltalkers just hacking. If you look at [SmalltalkHub.com](http://smalltalkhub.com) - our very own github clone (written in Smalltalk of course, even the HTML5 client!) you will see that we are a long way from dead - **755 users and almost 1000 projects**. Now... SmalltalkHub is new and many projects are still moving into it from other older Smalltalk repositories, so these users/projects have signed up within the last year or so.

Ok, so if Pharo is our "answer" to server side, what about the web? The Smalltalk world has had [Seaside](http://www.seaside.st), one of the best web frameworks ever. Period. But the world is moving fast and server side generation of HTML is not the future, HTML5 is. Or in other words, a javascript app manipulating the DOM. Dart is offering a "better path than javascript" but in Smalltalk we have something else, even better one might argue - [Amber](http://amber-lang.net).

There is much to say about Amber, but basically it is a true Smalltalk implemented in and "on top" of Javascript. It has an advanced compiler pipeline, an IDE that runs directly in the browser (!) a working debugger (!!) and yeah, of course it runs wherever javascript runs - nodejs is fine. What sets Amber apart from Dart is probably that it is "live", IDE runs in the browser and you can interactively develop your HTML5 app, and it interfaces beautifully with javascript, which I think is an issue with Dart (it might have improved).

In fact, SmalltalkHub.com is an Amber application. :)

I think we are in a good shape, but perhaps we should:

* Take a closer look at Julia since it is so close to Smalltalk and has several interesting aspects (performance and very good math)
* Keep an eye on Rust, Dart and Go, if only for inspiration. Some of the ideas there are pretty slick.
* Perhaps even consider Rust as an interesting new language for VM construction.

Phew.

Happy hacking!

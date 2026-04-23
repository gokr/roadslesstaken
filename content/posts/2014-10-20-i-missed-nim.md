---
title: I missed Nim
date: '2014-10-20'
slug: i-missed-nim
categories:
- Nim
- Nimrod
- Rust
- Go
- Languages
- Programming
---
A year ago I wrote an article trying to round up [new languages since year 2000](http://goran.krampe.se/2013/09/07/new-languages-this-century) and what I think of them by just... glancing at them, or otherwise playing with them. I ended up sifting out the 4 most interesting in my not so humble opinion - [Go](http://golang.org), [Rust](http://www.rust-lang.org), [Dart](http://dartlang.org) and [Julia](http://julialang.org). Now a year has passed and...

**I discover that I missed Nim(Nimrod)!**

[Nim](http://nim-lang.org) was born somewhere around 2006-ish and is clearly a very serious language to consider, but is going suspiciously under the radar. Having reviewed this language more closely (and still doing so) I can safely say that **for me** it actually easily **tops this list**.

I have already posted [a few articles about Nim](http://goran.krampe.se/categories/nim), but this one is meant as a _followup_ to [that article](http://goran.krampe.se/2013/09/07/new-languages-this-century) trying to make amends :).

_**NOTE:** Technically [Nim](http://nim-lang.org) is still called "Nimrod" up to and including the [0.9.6-release that was done yesterday](http://nim-lang.org/news.html#Z2014-10-19-version-0-9-6-released). But for the upcoming 0.10.0 and onward its **Nim**. Short and sweet._

<!--more--> 


## What kind of language is Nim?

Nim is a **statically typed** imperative language (not primarily functional, nor OO - but can do most of it) with a whole slew of **advanced compilation techniques**. At the same time it strives to be "programmable" with a very **clean and noiseless indentation based syntax**.

```nimrod
# Fizz Buzz program
const f = "Fizz"
const b = "Buzz"
for i in 1..100:
  if i mod 15 == 0:
    echo f, b
  elif i mod 5 == 0:
    echo b
  elif i mod 3 == 0:
    echo f
  else:
    echo i
```

Readable? Definitely.

I would say not many languages today manage to combine the above. Most advanced statically typed languages completely **SUCK** in the programmability department. Unless you are some genius of course. In the quest for speed and features most of these languages totally miss the boat on making a language that is actually **easy to use**.

Now... have no doubt, Nim is a [pretty darn advanced language](http://nim-lang.org/manual.html) - and personally I tend to shun those. I like minimal languages and I have dwelled in the realm of Smalltalk minimalism for a long time, and as a Smalltalker I am also accustomed to a very high level of productivity, interactivity and sophistication of development environment. Nim may be productive once you get going - in fact - many people say they indeed are. But when it comes to interactivity and development environment, its very ... early in the game.

But **still** this language is **getting to me**, against all odds. I can't even remember when I last felt this interested in a statically typed language.

Andreas Rumpf, the designer and main implementor of the language and compiler (written in Nim of course) has an interesting balance between enabling very advanced compiler techniques and still - at least as it seems - maintain a language that is actually usable by "normal people".

> "Nimrod is a statically typed programming language that tries to give the programmer ultimate power without compromises on runtime efficiency."
> — Andreas Rumpf

Andreas has borrowed heavily from a range of different languages: Modula 3, Delphi, Ada, C++, Python, Lisp, Oberon. Notably several from "Pascal descent" and dare I also say, Windows centered languages? Just a guess, Andreas works primarily on Windows I think.

This little list of examples of borrowing was mentioned in the forum by Andreas:

* Macro system inspired by Lisp.
* Export marker taken from Oberon.
* Argument passing semantics taken from Ada.
* distinct types inspired by Ada.
* Syntax also heavily influenced by Python.
* Generics inspired by C++.
* The 3 pointer like types ptr, ref, var taken from Modula 3.
* async / await stolen from C#.
* let taken from ML.

Let's now look at Nim vs those four I identified; **Go, Julia, Dart and Rust**. When contrasting with Nim, and also looking at where these languages have gone during the year since I wrote that article - things are a bit more clear.

Julia is very focused on math and is a dynamically typed language, still very interesting but **clearly targetting the scientific community** - its definitely not really competing with Nim - its too different. It is also LLVM-based and as such has different characteristics on platform availability. Julia does however have a sophisticated macro system, just like Nim.

**Dart is focusing on the web**, much more so than I had hoped. Perhaps it will turn "general purpose" eventually, but evidently Google is trying to push it hard as a web dev tool. Its also dynamically typed (yes it is) and also too different to really overlap with Nim.

This leaves us Go and Rust which we can look a bit closer at.

### Nim vs Go

Go seems to be a _"C made developer friendly"_ and that's not strange given its creators of course, [but as others point out](http://yager.io/programming/go.html), it doesn't really bring much new stuff and is not particularly well designed - so **people say** that have actually used it :)

It is [fairly popular](http://zef.me/6191/the-march-towards-go/) however, and that is probably due to its C-syntax, being fairly fast and compiling to native, sticking to relatively simple constructions, ease of use and being backed by Google. The net effect is that its **seductively easy to get going with**. It seems to be picking up users both from dynamically and statically typed camps. Go is relatively stable by now and that's also important to adoption.

Compared to Nim then... Go is in some ways attracting a similar crowd - people who want a language that is productive, but not sacrificing speed. One can see several similarities around ease of use, like fast and simple compilation, easy package management and so on. Obviously there is a common feeling that things can be done simpler these days - and both Nim and Go developers share that idea. But there are **BIG differences**, here just a few highlighted:

* Go has no macros, no generics, no overloading, no object variants and... let's just say a **much less sophisticated type system**. Its very much "less".
* Both Go and Nim has **similar concurrency models** centered around non shared memory and asynchronous communication between them. 
* Nim has **optional** GC, and its soft realtime, per thread. Go is GC only.
* Nim has **optional** pointers and low level mechanisms, if you want to. This way it matches areas where C would be applicable. Go doesn't go there.

It seems though that perhaps people are "waking up" disillusioned in Go land, just like many did after getting seduced by NodeJS. This article [pinpoints it quite well](http://jozefg.bitbucket.org/posts/2013-08-23-leaving-go.html). My conclusion is that while the tooling, standard libraries and community around Go is excellent - **the language itself is NOT**, like others might describe in [much harsher words](http://www.quora.com/Googles-programming-language-Go-seems-to-be-the-most-modern-and-well-featured-language-in-existence-today-Is-that-the-case-or-are-there-major-drawbacks-that-Im-not-seeing).


### Nim vs Rust

Ok, so this is where the real battle lies and the lines get blurred. It looks evident that **Rust is much more complicated** to program in. Rust is also **very much focused on safety, safety, safety**, while Nim is more focused on being practical and pragmatic.

The main popular selling point of Rust is its memory model with a combination of different kinds of pointers and scope based allocation/deallocation making it all automatic while not needing a GC. But just like Nim it also has a sophisticated type system and well, these languages seem quite similar in feature sets.

Here are some differences at least, but I know both languages too little to give more discriminating details:

* Rust is "C syntax" and Nim is Python-ish. Nim wins this one hands down for me.
* Nim has [Exceptions](http://nim-lang.org/manual.html#exception-handling) with [tracking (!)](http://nim-lang.org/manual.html#effect-system) and Rust has [explicit error handling via the return value](http://doc.rust-lang.org/nightly/std/result/). Personally... that feels like a **big step backwards**, much like error handling in Go. Again, for me, a clear win for Nim. I know others feel differently, but that is ok :)
* Rust is pushed by Mozilla, Nim is a grass root "true open source" language. Having a "backer" might be good, but I like grass root efforts since they tend to be more open and easier to participate in as a "full" member.

**UPDATE 2014-11-08:** I know both languages are open source and have communities. But it remains a fact that Rust is **lead by Mozilla** (I would be surprised if not) and Nim is **lead by its community**. That doesn't necessarily mean one way is better than the other though. Regarding the error handling in Rust - I have **edited the above text** to point to the relevant current section in the Rust documentation. I would however urge Rust people to add a section in their documentation called "Error handling" or similar so that one can find it without having to read the entire manual! **UPDATE 2016-01-26:** And today there is [such a section](https://doc.rust-lang.org/book/error-handling.html), I have also read from several sources that Mozilla is not leading the Rust development anymore, but I don't know the details.

I think the [discussion here](https://news.ycombinator.com/item?id=7388014) sums up what several people feel about Nimrod vs Rust.

I think Rust is going places, but I don't feel attracted to it. Every time I read about it - I get too overwhelmed by the complexity. It does feel like C++ all over again, although perhaps without the segfaults :)

## Conclusion

My only conclusion is that I am glad I have found Nim and although the feature set is a bit overwhelming (especially if you just read the language manual) I wouldn't say the code I have read so far is in any way hard to read, on the contrary. I conclude that it is possible to make an advanced language while still crafting it in such a way that its practical to use. But that takes considerable devoted effort - and Andreas Rumpf seems to be pulling this off.

I also highly appreciate the fact that I can "chip in" and actually make a difference in the development and future directions of Nim - given its highly open, friendly and communicative community. I am used to another very friendly community (Smalltalk) and so far I am equally impressed by the Nim community.

Go Nim!

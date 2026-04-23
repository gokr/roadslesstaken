---
title: Joe is wrong
date: '2009-06-26 17:12:06'
slug: joe-is-wrong
categories:
- Object orientation
- Old blog
---
I just read Joe Armstrong’s old "Why OO sucks" [article](http://www.sics.se/~joe/bluetail/vol1/v1_oo.html), Joe Armstrong being the inventor of [Erlang](http://erlang.org/). Granted, the article is from year 2000 I think, so perhaps I should cut him some slack… nah! :)

First of all - no, I haven’t programmed in Erlang (yet), but quite a lot of other programming languages. My favorite language is the grand father OO language - [Smalltalk](http://squeak.org/). So sure, I am biased in favor of OO.

I have read other criticisms of OO, and various discussions about good or bad characteristics of OO in general and in specific OO languages… Sorry, **this article is IMHO not among the good ones**, and my feeling is that Joe wrote it quite quickly and with no real experience in programming in OO.

But I don’t intend to say his article "sucks" without arguing for **why** I feel it sucks :). And also, I am in great awe of the [stuff](http://couchdb.org/) Erlang makes possible so I have great respect for Joe - but that doesn’t mean he can’t be dead wrong.

Let’s go through his article bit by bit:


### "Objection 1 - Data structure and functions should not be bound together"


I quote:


> "Since functions and data structures are completely different types of animal it is fundamentally incorrect to lock them up in the same cage."


Rereading that first objection I only see kinder garten explanations of what functions and data are. I don’t see any real serious explanation of why they couldn’t be combined into objects other than "because they are different". That is not an argument.

It is in fact quite logical to group functions and data together into objects based on their interaction patterns, if for no other reason.

Let’s say we have data structures A, B, C and D. And we have functions q, x, y, z. If you start looking at what data is read and written by these functions you may find that q and x operates only on A and B, reading one and writing the other etc. So the functions and data structures form "natural clusters", and usually these clusters are quite intuitively modelled as objects.

Putting them together creates a boundary around this group of data and functions - encapsulation. Sure, you may call that a "module" but an object is IMHO slightly different since objects have identity, a life cycle and we can hold them, send them around etc.

So in some sense objects can probably be viewed as modules but often more fine granular. And we can combine such "modules" into larger modules (since objects have identity and can be referenced etc) and we can create and kill them dynamically (life cycle).

If I were coming from a language with a well developed "module" concept I can definitely see this as just "another step" forward.

Another interesting fact with objects having a life cycle is that since an object contains data A, B, C and D we now easily can create a whole such data "group" by just instantiating this object. And we deallocate them together as a single entity too - manually or automatically. Again, quite natural.

So ok, I can go on and on about this but since Joe didn’t really give any arguments I will stop there.


### "Objection 2 - Everything has to be an object."


Now, being a Smalltalker I wouldn’t use the phrase **has to be** but I can clearly see all the benefits when the paradigm is really **followed through in a pure way**.

Ok, but let’s look at what Joe says. He points to an example - different datatypes for describing amount of time, or well, not "amount" but in fact partial pieces of points in time. Hour (of day), minute (of hour), year etc. Without knowing Erlang these data type definitions typically define ranges of integer values valid for these types. Anyway, then his main points are:



	
  * These data types can be used everywhere.

	
  * There are no associated methods.


The first argument is odd. Let’s look at Smalltalk (or any OO language), let’s say we have a class called TimeStamp. Or Date. We can instantiate these classes from anywhere in the system, there is no reason for classes to have any less (or more) scope than data types. So objects of classes can also be used "everywhere".

The second argument is plain dumb (sorry). No associated methods? **There are TONS of interesting behavior you can attach to these kinds of objects!** For a true tour de force, just look at [Chronos](http://chronos-st.org/) for example. The fact that Joe can make such a claim is IMHO clearly showing that he really haven’t seen how a good OO library can work. Or I suspect ever programmed in an OO language in fact.

But if we disregard this bad example, going back to the original objection, I agree - everything does not HAVE to be an object. But a LOT of the problems in many OO languages can be traced to the fact that they still retain lots of "fundamental data types" that are not objects. And most of the modern OO languages get closer and closer to Smalltalk where almost everything really is an object, just look at Python, Ruby, Scala etc.

The object concept is very powerful and its power gets even greater when applied generously. :)


### "Objection 3 - In an OOPL data type definitions are spread out all over the place."


Ehm, sorry Joe but this one really shows poor understanding of OO languages. First of all, I presume you mean "data type definition" as an enum or similar. Or a class definition. Ok, and then you seem to say it is a pity that you can’t just put them in one single place - **ehrm, but you can… but it would be rather horrendous design.**

It is simple normal modularisation, you don’t want ALL data types/classes defined in a big global scope, right? I would in fact argue in the exact OPPOSITE - in an OOPL data type definitions **are where they should be - close to the place of use. The modular way.**

Anyway, now we come to the last paragraph - and it is simply confused. Let me quote:


> "In an OOPL I have to choose some base object in which I will define the ubiquitous data structure, all other objects that want to use this data structure must inherit this object. Suppose now I want to create some "time" object, where does this belong and in which object..."


No, no, no - why would all other objects need to **inherit** that class? Inheritance is normally used for **specialization**, the mechanism you are totally missing is **composition**. If my Account object needs to have a TimeStamp in it - then I simply instantiate a TimeStamp and let my Account hold onto it in an instance variable. This is **basic OO, chapter 1.**

It is also amusing that the examples of "ubiquitous data types" mentioned are LinkedList, Array and Hashtable. All three being standard collection classes that almost all OO languages have, no problem there, sorry. Note that Erlang was created around 1990. Smalltalk was created in the late seventies and Simula in 1967. Smalltalk has worked very successfully with an "all objects" approach and having very rich and appreciated collection classes - including LinkedList, Array and Dictionary (Hashtable). It feels like Joe thinks OO came around in 1996 with Java - nope, it is in fact much older than Erlang.


### "Objection 4 - Objects have private state."


Again, confused arguments. Quote:


> "OOPLs say 'hide the state from the programmer' "


Well, yeah, in an encapsulation-and-modularity-is-good-kinda-way. Not in a programmers-should-not-care-or-know-kinda-way.

The argument about C/Pascal using scoping rules - ehm, well, OOPLs do too, hard to see the distinction there. Joe call’s the OO idea of encapsulation as the "worst possible choice". But again, no real argument for why encapsulation would be a bad thing. In fact it is one of the most important aspects of OO - the ability to expose a concept - an object - in a comprehensive high level way with a nicely designed API without forcing the user to look at all the details inside. Classical black box composition, an idea older than… old :)

And no, the blackness does not have to be strict - if the programmer wants to look I say go right ahead. I am **definitely not defending the pretentious protective ideas gone berzerk in languages like Java, C++ and C#** where keywords like "final", "sealed", "private", "protected" etc tend to simply make life miserable for the programmer who actually knows exactly what he or she is doing. But enough of that little rant, claiming that encapsulation is a BAD THING is … simply daft.

The final conclusion about why OO got popular does not hold any substance either - I am not even going into it. So all in all I think Joe is totally off in this article. :) Having said that I still look forward to learn Erlang, and since I am dabbling with CouchDB I might get my feet wet soon.

**NOTE in 2011: Now I have finally met Joe and almost feel embarrassed of the above "bashing". But only almost :)**

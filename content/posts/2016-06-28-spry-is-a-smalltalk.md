---
title: Is Spry a Smalltalk?
date: '2016-07-19'
slug: is-spry-a-smalltalk
categories:
- Spry
- Smalltalk
- Homoiconic
- Languages
- OO
- Programming
---
I love [Smalltalk](http://world.st) and I have been in love with it since approximately 1994. I have used VisualWorks, VisualAge (IBM Smalltalk), Dolphin Smalltalk, GemStone, [Squeak](http://squeak.org) and [Pharo](http://pharo.org) quite a lot, and I was very active in the Squeak community for a long period.

But the last few years, finally, I have started to feel the "burn"... as in ["Let's burn our disk packs!"](http://gagne.homedns.org/~tgagne/contrib/EarlyHistoryST.html#29). And last year I started doing something about it - and the result is [Spry](http://sprylang.org). Spry is only at version 0.break-your-hd and several key parts are still missing, but its getting interesting already.

**Now... is Spry a Smalltalk? And what would that even mean?**

I think the reason I am writing this article is because I am feeling a slight frustration that not more people in the Smalltalk community find Spry interesting. :)

And sure, who am I to think Spry is anything remotely interesting... but I would have loved more interest. It may of course change when Spry starts being useful... or perhaps the lack of interest is because it's not "a Smalltalk"?

## Smalltalk family
The Smalltalk family of languages has a fair bit of variation, for example [Self](http://www.selflanguage.org) is clearly in this family, although it doesn't even have classes, but it maintains a similar "feel" and shares several Smalltalk "values". There have been a lot of Smalltalks over the years, even at PARC they made different variants before releasing Smalltalk-80.

**So... if we look at Spry, can it be considered a member of the Smalltalk family?**

There is an [ANSI standard](http://wiki.squeak.org/squeak/172) of Smalltalk - but not many people care about it, except for some vendors perhaps. I should note however that [Seaside](http://www.seaside.st) apparently (I think) has brought around a certain focus on the ANSI standard since every Smalltalk implementation on earth wants to be able to run Seaside and Seaside tries to enforce relying on the ANSI standard (correct me if I am wrong).

Most Smalltalk implementations share a range of characteristics, and a lot of them also follow the ANSI standard, but they can still differ on pretty major points.

My **personal take** on things in Smalltalk that are pretty darn important and/or unique are:

1. Everything is an object including meta levels
2. A solid model for object oriented programming
3. The image model
4. 100% live system
5. The browser based IDE with advanced cross referencing, workspaces and debuggers
6. The keyword syntax and message cascades
7. Message based execution model
8. Dynamic typing and polymorphism
9. Closures everywhere with lightweight syntax and non local return
10. Very capable Collections and a good standard library

Not all Smalltalks cover all 10. For example, there are several Smalltalks without the image model and without a browser based IDE. Self and Slate and other prototypical derivatives don't have classes. Some Smalltalks have much less evolved class libraries for sure, and some are more shallow in the "turtle department".

In Spry we are deviating on a range of these points, but we are also definitely **matching some** of them!

<!--more-->

## How Spry stacks up

1. **Everything is an object including meta levels**. No, in Spry everything is an AST node, not an object. A similar feel of uniformity exists, but it's different.
2. **A solid model for object oriented programming**. Yes I think so, but Spry does not use the classic class model but is experimenting with a functional OO model.
3. **The image model**. No, not yet. But the idea is to have it, not on a binary "memory snapshot" level, but in a more fine granular way.
4. **100% live system**. Yes, Spry is definitely 100% live and new code is created by running code etc.
5. **The browser based IDE with advanced cross referencing, workspaces and debuggers**. No, but eventually I hope Spry gets something similar. First step is making a UI binding and evolving the meta programming mechanisms.
6. **The keyword syntax and message cascades**. Yes, Spry has keyword syntax, but also has prefix syntax and currently no cascades nor statement separators.
7. **Message based execution model**. No, Spry execution is not message based, but rather functional in nature. The practical difference should be slim to none I hope.
8. **Dynamic typing and polymorphism**. Yes, Spry is dynamically typed and offers polymorphism, but through a different technique.
9. **Closures everywhere with lightweight syntax and non local return**. Yes, closures with non local return, similar pervasiness, even more light weight syntax than Smalltalk!
10. **Very capable Collections and a good standard library**. No, not yet. But intend to have it and will in many ways try to pick the best from Smalltalk and Nim.

So **Spry scores 5/10. Not that shabby!** And I am aiming for 3 more (#3, #5, #10) getting us up to 8/10. The two bullets that I can't really promise are #1 and #7, but I hope the alternative approach in Spry for these two bullets still reaches similar effects.

Let's look at #1, #2 and #6 in more detail. The other bullets can also be discussed, but ... not in this article :)

## Everything is an object including meta levels
In Smalltalk everything is an object, there are no "fundamental datatypes". Every little thing is an instance of a class which makes the language clean and powerful. There are typically some things that the VM treats differently under the hood, like SmallInteger and BlockClosure etc, but the illusion is quite strong.

Spry on the other hand was born initially as a "Rebol incarnation" and evolved towards Smalltalk given my personal inclination. **Rebol as well as Spry is homoiconic** and when I started building Spry it felt very natural to simple let the AST be the fundamental **"data is code and code is data"** representation. This led to the atomic building block in Spry being the AST Node. So **everything is an AST node** (referred to as simply "node" hence on), but there are different **kinds** of nodes especially for various fundamental datatypes like **string, int and float** and they are explicitly implemented in the VM as "boxed" Nim types.

In Smalltalk objects imply that we can **refer to them** and **pass them around**, they have a **life cycle** and are **garbage collected**, they have an **identity** and they are **instanciated from classes** which describes what messages I can send to them.

In Spry the **same things apply for nodes**, except that they are not instanciated from classes. Instead nodes are either created by the parser **through explicit syntax** in the parse phase, or they are created during evaluation by **cloning already existing ones**.

An interesting aspect of Spry's approach is that we can easily create new kinds of nodes as extensions to the Spry VM. And these nodes can fall back on **types in the Nim language** that the VM is implemented in. This means we trivally can reuse the math libraries, string libraries and so on already available in Nim! In essence - the Spry VM and the Spry language is much more integrated with each other and since the VM is written in Nim, **Nim and Spry live in symbiosis**.

Using Spry it should be fully normal and easy to extend and compile your own Spry VM instead of having to use a downloaded binary VM or learning **Black Magic** in order to make a plugin to it, as it may feel in the Squeak/Pharo world.

Finally, just as with Smalltalk the meta level is represented and manipulated using the same abstractions as the language offers.

**Conlusion? Spry is different but reaches something very similar in practice.**

## A solid model for object oriented programming

But what kind of behaviors are associated with a particular node then? In Spry I am experimenting with a model where all nodes can be tagged and these tags are the basis for polymorphism and dynamic function lookup. You can also avoid tagging and simply write regular functions and call them purely by name, making sure you feed them with the right kind of nodes as arguments, then we have a pure functional model with no dynamic dispatch being performed.

In Spry we have specific node types for the fundamental datatypes int, float, string and a few other things. But for "normal" objects that have instance variables we "model objects as Maps". JavaScript is similar, it has two fundamental composition types - the "array" and the "object" which works like a Map. In Spry we also have these two basic structures but we call them **Block** and **Map**. This means we can model an object using a Map, we don't declare instance variables - we just add them dynamically by name to the map.

But just being a Map doesn't make an object - because it doesn't have any behaviors associated with it! In Smalltalk objects know their class which is the basis for behavior dispatch and in Spry I am experimenting with opening up that attribute for more direct manipulation, a concept I call **tags**:

1. Any node can be tagged with **one or more tags**.
2. Functions are also nodes and can thus also be tagged.
3. A polyfunc is a composite function with sub functions.
3. A polyfunc selects which sub function to evaluate based on comparing tags for the first argument, the "receiver" with the tags for the sub functions.

The net effect of this is that we end up with a very flexible model of dispatch. This style of overloading is a tad similar to structural pattern matching in Erlang/Elixir.

One can easily mimic a class by associating a bunch of functions with a specific tag. The tags on a node have an ordering, this means we also get the inheritance effect where we can inherit a bunch of functions (by adding a tag for them) and then override a subset using another tag - by putting that tag first in the tag collection of the node. Granted this is all experimental and we will see how it plays out. It does however have a few interesting advantages over class based models:

1. Tags are dynamic and can be added/removed/reordered during the life cycle of an object.
2. Tags have no intrinsic relations to each other, thus multiple inheritance in various ways works fine.
3. Polyfuncs are composed dynamically which makes it easy to extend existing modules with new behaviors (like class extensions in Smalltalk).

I am just starting to explore how this works, so the jury is still out.

## The keyword syntax and message cascades

Spry supports infix and prefix functions and additionally keyword syntax using a simple parsing transformation. The following variants are available:

```
# Function call with zero arguments.
# Well, we are in fact referring to whatever is bound to the name "root"
# and evaluating it - and if it is indeed a func then it will be called.
# This happens to be a Spry primitive func that returns the Map holding the
# root bindings, essentially the same as "Smalltalk" in Smalltalk.
root

# Prefix function call with one argument.
echo "Hey"

# Prefix function call with two arguments. I am experimenting with different
# styles of conditionals in Spry, Smalltalk style is also doable.
if (3 < 4) [echo "yes"]

# Infix function call with one argument.
[1 2 3] size

# Infix function call with two arguments. In Spry this is currently not limited
# to a specific subset of characters like binary messages in Smalltalk.
3 + 4

# Infix function call with three arguments, keyword style.
# Parser rewrites this as "[1] at:put: 0 2" and since ":" is a valid character
# in a Spry name, it will simply run that func.
[1] at: 0 put: 2

# Infix function calls with 3 or more arguments do not need to use keyword style though,
# foo here could be an infix function taking 4 arguments. Not good style though.
1 foo 3 4 5

# Keyword style can be used for prefix functions too so
# that there is no receiver on the left! Looks funky for a Smalltalker and I
# am not yet certain it is a good idea.
loadFile: "amodule.sy"
```

This means Spry supports the classic Smalltalk messge syntax (unary, binary, keyword) in addition to prefix syntax which sometimes is quite natural, like for `echo`. Currently there is no syntactic support for cascades, but I am not ruling out the ability to introduce something like it down the road.

## Conclusion

Spry is very different from Smalltalk and I wouldn't call it "a Smalltalk", but rather "Smalltalk-ish". I hope Spry can open up new exciting programming patterns and abilities we haven't seen yet in Smalltalk country.

Hope you like it!

---
title: Adding objects to Ni!
date: '2015-09-25'
slug: adding-objects-to-ni
categories:
- Spry
- OOP
- Smalltalk
- Rebol
- Object orientation
- Languages
- Programming
---
So... Ni has almost reached the point where I can see objects appearing. The following describes the design I **currently** have in mind, read it and tell me what you think so I can scrap it and start over ;)

{{< img src="/ni/ni.png" alt="Ni" style="float:right; margin:0 0 1em 1em;" >}}

<!--more-->


## Introducing Dictionary

Before we get to objects, we need something else - a **Dictionary**. A Dictionary is just a key/value collection - the name comes from Smalltalk, in many other languages they are called Map or HashTable and in Nim it's called a `Table`. Rebol uses the word "Context", and that is the word I have used so far in the Ni sources and articles. But nah, sorry Rebol, calling it a **Dictionary** makes it easier to understand IMHO.

**Dictionaries and Blocks** are the **two primary plain data structures** in Ni. Other more specialized collections would be constructed as objects (just like in Smalltalk) or added as a Ni extension. In this sense Ni is a bit like Javascript. It's not purely OO as Smalltalk is, where both these are represented as objects. But IMHO as long as that fact doesn't cause "gotchas" it's fine.

As many languages before Ni has shown - having language syntax support for Dictionaries can be very useful.

I earlier hinted on using curly braces `{ ... }` for this, and I still think that's more useful than using them as a second asymmetrical (thus nestable) string delimiter, as Rebol does. Also, we generally like to follow Nim when it comes to details like this.

I kept brooding over this, what would be the best way to make it very readable and still fit in with **The Way of the Ni Knights?** First I was trying to mimic Javascript but it felt clumsy, then one morning it dawned upon me that the cleanest solution is the most obvious solution. And what is that then?

Well, how about if we combine the characteristics of a Paren (has no Dictionary of bindings, and evaluates containing code, when evaluated, to a single result) and a Block (gets its own activation record when evaluated and thus has a Dictionary of bindings, but does not evaluate its code when evaluated, only when explicitly done so via do).

And yes... I should have read more Rebol - because **creating objects in Rebol works quite similarly :)**

A Dictionary could then be created like this:

``` nimrod
{ a = 2 b = 3 }
```

And it would evaluate immediately as a Paren does, but it would also (upon evaluation) create an activation record with a Dictionary, like a Block does. And when the evaluation is done, it would return that Dictionary as its value! It's darn beautiful if you ask me. There is no need for special syntax inside the Curly, it's just arbitrary Ni code like in a Block! Muuaahhahaa! Yeah, yeah, all you Rebolers think this is old stuff of course. ;)

So the above could also be done more explicitly using a block like this:

``` nimrod
do [ a = 2 b = 3 bindings ]
```
We need to use `do` to run the block since blocks do not evaluate by themselves, and the block ends with `bindings` which would return the local Dictionary of the activation record.

A larger example:

``` nimrod
myDict = {
	age = 46
	interests = [programming boats badminton]
	name = "Göran"
	echo ("Just created " & name)      # Remember, this is just code!
}
echo (myDict at: 'name)
echo (myDict at: 'interests)
```

Tada! So now we have Dictionaries.

## Punting on Modules

In Ni, lookups are done lexically "outwards" until we reach the root Context. The root Context is our global namespace. Modules is in many languages a hot topic. Ni tries to learn its ways before introducing a Module system, but it most likely will be something derived from Dictionary, or nothing at all :)

## Introducing Object

A Dictionary is just a "plain datatype" or in other words, we can't associate "methods" with it. We can define infix functions usable on Dictionaries of course, and `at:` is an example of that, but there is no polymorphic dispatch going on on the Ni level (but inside the interpreter we use Nim methods to gain polymorphism for builtin datatypes).

Let's first suppose that **an Object in Ni is in essence a Dictionary but a bit different**. It feels natural that an object can be modelled as a Dictionary to hold the "instance variables". Just like we create Funcs from Blocks we could then create Objects from Dictionaries using an `object` word:

``` nimrod
rectangle = object {
	x = 0
	y = 0
	width = 0
	height = 0
}
```
This is an object that is quite silly, because it has no behavior. The idea of objects holding their own **instance based** behavior may look neat in theory but is pretty useless in practice I think. Most prototype based languages seem to evolve some kind of class mechanism to have shared sets of behaviors that we can reason about. Ni thus punts on any "instance based" lookup for behaviors, instead I am focusing on a mixin-style ordered lookup by making the object have a block of **Traits**:

``` nimrod
rect = object {
	traits = [Positionable Rectangle]
	x = 0
	y = 0
	width = 0
	height = 0
}
```
So in summary, we introduce an **Object** that we create using the `object` word that takes a **Dictionary** as input. This is an instance, not a class. The Dictionary can hold a special key `traits` which has a block of **Traits** in order. A Trait is the closest we get to a class in Ni, but it defines no structure and it also doesn't inherit from other Traits, it's just a Dictionary of named Funcs really.

So a more complete example could look like:

``` nimrod
# A set of behaviors for a Point that has an x and y
# We use capital letter for Traits. The trait word takes
# a Context and creates a Trait for us.
Point = trait {
  x        = func [.x] # A getter, note the .-scoping
  y        = func [.y] 
  x:y:     = func [:.x :.y] # A setter, note the .-scoping
  moveX:y: = func [self moveX: :dx self moveY: :dy] # Self calls
  moveX:   = func [.x = .x + :dx]
  moveY:   = func [.y = .y + :dy]
}

# One more Trait, a set of behaviors for a Rectangle with width and height
Rectangle = trait {
  area     = func [.width * .height]
  extent:  = func [:extent .width = extent x .height = extent y]
}

# An object which uses a single Trait
origo = object { traits = [Point] x = 0 y = 0 }

# An object which uses two Traits, lookup is in order so conflicts are just shadowed
# If you wish to resolve conflicts you create yet another Trait and put it first patching it up
rect = object {
	traits = [Point Rectangle]
  x = 0
  y = 0
  width = 0
  height = 0
}

# Creating new objects is easily done copying an existing object
rect2 = copy rect

# And you can always make funcs taking arguments returning new objects
# just like you typically do in Nim instead of constructors.
newRectangle = func [ :x :y :w :h
	object {
		traits = [Point Rectangle]
 	 	x = ..x # This will refer to the x argument in the func
 	 	y = ..y
 	 	width = ..w
 	 	height = ..h
  }
]

# And then we can easily call it, this time using Rebol
# style argument passing instead of a Smalltalk style keyword
# message. As one sees fit.
rect3 = newRectangle 100 100 640 400

# Polymorphic dispatch, both objects respond to the getter x
[rect origo] do: [echo :each x]
```

There are many details here one can discuss, but some thoughts:

* I find the above object model to feel less "confusing" than a delegation model, still need to bang on it for real though.
* I avoid instance specific behaviors since I doubt they are useful.
* A Trait is also created from a Dictionary. Purely a set of behaviors, clean, simple.
* I reserve the key `traits` for the slot in the object holding the Block of Traits. Fine! :)
* Lookup is by order, thus conflicts are ok, the Trait coming first simply wins.
* Inheritance and composition can be done in many ways here using copying of prototypes and manipulating the `traits` block
* Not inheriting structure doesn't feel like a great loss, and actually, since an Object is basically a Context - inheritance of structure can also be done via a simple `initialize` pattern letting the Traits in order initialize their variables.
* Ability to call "super" etc, well, it can also be added, although I am curious if one can avoid classic OO design where it easily becomes something you want to do.

I am **really interested** what kind of feedback I can get on this, a lot of other developers/language designers out there are much more educated than I am!

## Object dispatch

But how is the dispatch done?

I think I will try making Object nodes affect the lookup of the word coming right after. This means methods are strictly called with the receiver object on the left.

1. When Ni first encounters `rect` it will notice it's an Object, remember that, and continue to the next node.
2. Before the regular lookup of the next word, we first need to let `rect` look it up among its `traits`. If we find a func we call it with `self` bound to `rect`, thus methods like this overrides any available infix func we could have found.
3. If we didn't find anything, we continue normal lookup of the word since it may be a regular non polymorphic infix function.

Now we have the first seed of an Object model! Will it work? Haven't got a clue. Time to hack it. But... it does look doable and I think I like it.



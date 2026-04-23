---
title: Spry Modules, part II
date: '2016-05-03'
slug: spry-modules-ii
categories:
- Spry
- Modules
- Homoiconic
- Languages
- Programming
---
In the [last article](http://goran.krampe.se/2016/04/16/spry-modules) I outlined a simple **model of modules** and that is kinda implemented but needs a few fixes. The next step is how to find and combine modules and this is an area where I want to push the envelope a bit. Most popular package/module systems today are quite trivial in nature. Often it's a command line tool that queries central catalog(s) and then proceeds by downloading code in the form of source files onto disk. Then the compiler or runtime environment finds and loads the code by simply looking for files on disk. There are several parts of this that are very primitive.

When I built [SqueakMap](http://map.squeak.org) waaay back I was already then tainted with the idea of [shared object models](https://gemtalksystems.com) and one of the primary ideas in SqueakMap was to make sure each local Smalltalk environment got a full live object model of the catalog which then could be queried, viewed and reasoned about inside the Smalltalk environment. Much more powerful than a bunch of JSON files on disk. This led to the approach of downloading the full catalog in a serialized form - and then loading it into [Squeak](http://www.squeak.org).

With [Spry](http://sprylang.org) I want us to create a simpler meta model - at least for starters - but with an even smarter infrastructure backing it...

<!--more-->

## What we have

A quick summary of where the Spry modules implementation is today:

* A Module is **just a Spry Map** - a key value structure obviously forming a namespace.
* Since a Module is a Map and Spry is homoiconic, **it can hold anything**, not only code but any kind of Spry node.
* When loaded into memory a Module is **held in a global name**.
* **We don't allow nested Modules** in a hierarchy, I think it invites convoluted solutions and doesn't fit the "catalog" model either which typically is flat.
* The Module has **meta information kept inside** in yet another Map under the key `meta` with members like `name` and `version`. First I was thinking of using `_meta` but I am opting instead for plain `meta`. Collisions? Deal with it.
* Nodes in the Module can be referenced from the outside using **module qualified** eval- or get words like `Foo::bar` or `^Foo::bar`.
* There is **no import mechanism** but there is a global word `modules` referencing the Modules that should be consulted **in order** for lookups of non qualified words.

Modules can be trivially serialized or deserialized **in source form**, just like any other Spry node. This is how we serialize any node in Spry, remember that **data and code is the same thing**, its all turtles... I mean nodes. Thus, the source code, or file format, of a Map (and thus also a Module) looks like this:

```
# A Map is just a bunch of assignments inside a Curly. A Curly in Spry is just a sequence of Nodes.
# After parsing we have a Curly which is still just "data". If we evaluate the Curly Spry will
# execute the code inside it and at the end return the Map of locals that was populated by the code.
{
  # First is a very minimal meta Map holding the name of the Module in
  # the form of a literal Word which is similar to a Symbol in Ruby/Smalltalk.
  # There is no mandatory information, nor is the meta Map itself mandatory.
  meta = { name = 'Foo }
  
  # This just assigns 13 to x in the local scope Map
  foo = 13
  
  # Same again, but we can of course have funcs or whatever in a Module
  adder = func [:x + :y]
}
```

If we store this as `Foo.sy` (`.sy` being the Spry file extension I use) we can trivially load it into Spry with `loadFile: "Foo.sy"`. This is an example of a prefix keyword func, it could just as well have been named `loadFile`, but I am experimenting with finding good Spry conventions around this, but that's the subject of another article :)

## Issues so far
I have realized two isses so far:

1. `Foo::bar` as implemented at the moment looks **directly in globals** for `Foo`.
2. The current "module is a Map" doesn't create a closure for the module itself where it could keep private code or state.

The first issue, on my fourth thought, I decided it's powerful to have `Foo::bar` be implemented as equivalent to `Foo at: 'bar`. So I will make sure to look for `Foo` first using normal scoping lookup. This enables shadowing of modules but it should be a **Big No No** because it turns into **a kind of import statement** and as a reader of code you wouldn't be sure what `Foo::bar` really resolves to. But Spry can easily detect if you introduce a Module shadow, and hit you hard on the head!

The second issue is more intricate and caused me to think quite hard on which route to take. If we wrap the Map inside a block, we get a closure, and then we could create private bindings in that closure. That resembles the techniques used in the JavaScript community, so definitely not an odd concept. But it also leads to the module not being **serializable as itself**. The Map is no longer the module itself, instead it only holds the "exports" of the Module.

I want to stick to a declarative Map style and introduce hooks like `Foo::init` that is called upon Module load and `Foo::release` perhaps on Module unload. But how should private state of the module be created? Let that simmer while we dive into another aspect...

## Source code formatting
It would be pretty nice if we could unify storage of Modules (Spry nodes in general) so that we could simply `store: Foo asFile: "Foo.sy"`. Today we can do that, but **all indentation and comments are lost in the round trip!** So... it would be super slick if we could once and for all **get rid of source code :)**. Smalltalk never went all the way on this - although Smalltalk came quite close. Various ideas around this:

* Introduce a pretty printer and simply force us to use it always making formatting "moot", but comments are still not handled.
* Somehow collect comments and formatting and keep it on the side associated with the AST.
* Extend the AST to also include comments and formatting somehow, so that they are not lost but kept in the AST.

I am leaning towards the latter, even though it's **obviously insane**.

![You](/spry/crazy.jpg){ style="display:block; margin:0 auto;"}

So... if I extend Node with an optional string containing the "all whitespace and comments" right before the Node itself - then we should be able to serialize/deserialize without losses, except for anything coming after the very last node :). Default whitespace is a single space, we represent that as `nil`. And sure, wasting a full reference in every Node? I agree, completely nuts, but perhaps we can somehow magically avoid that later on. It still is too tempting to try!

## Proposal
Fiddling with closures for modules, as is done in JavaScript, feels hacky. First of all, I don't like modules that are primarily constructed by running code. It's too brittle. I want to have a loading phase that is declarative-ish, and then an activation phase where the module can execute code in specific hooks. This means that Spry can analyze the module when its loaded to check for collisions or other things. The simplest way of loading modules is to simply eval the Curly, to get a Map - but we could trivially create a "safe Module loader" that doesn't use plain `eval` and thus we would plug that security hole. For now, `eval` is fine though!

This leaves us with the question on how to create private state in the Module.

In earlier articles I introduced the concept of scoped words, `.x` and `..x`, but haven't followed through on actually implementing them. The `.x` could mean **"start resolving in closest enclosing Module or Object"**. This would make it work like instance variable access - and a Module will most obviously turn into an Object when I get the OOP stuff in place. Now, to make `x` be private I am thinking of `_x`. I stared at the ASCII table and didn't think the alternatives were good. And most developers use `_` to denote privateness. This means I have decided to go with:

* `.x` means **in the closest enclosing Object**. To begin with the closest enclosing Map is good enough.
* `..x` means **somewhere outside of the closest enclosing Map**. The definition if that we can experiment with later.
* `_x` means **just like .x but private**

![Underscore](/spry/underscore.jpg){ style="display:block; margin:0 auto;"}

## Next step

1. Fix `Foo::bar` to resolve Foo normally first. This enables `::` to be used for "property access" in general.
2. Implement `.x` and `_x` to behave as described above.
3. Implement comments and formatting collection in the Node.
4. Make some module testing this out.

Happy Sprying!


---
title: Spry Here Goes Nothing!
date: '2023-05-03'
slug: spry-here-goes-nothing
categories:
- Spry
- Languages
- Programming
draft: true
---
[Spry](https://sprylang.se) is more and more resembling a sort of "Smalltalk cousin" and that's not strange since I like how Smalltalk feels - even if I want Spry to be **quite different** in some areas. One area of [a lot of discussion](https://www.lucidchart.com/techblog/2015/08/31/the-worst-mistake-of-computer-science/) in the programming world is around the notion of "nothing", or as we like to say `null` or `nil`.

In the beginning Spry had both `undef` and `nil`, similar to Javascript. That was an experiment, the idea was to having `undef` representing the notion of "the variable does not exist", and `nil` to represent "the variable exists but has the nothing-value". I guess the original intent in Javascript was the same, but...

<!--more-->

...I removed `undef`, it ended up being a bit goofy in evaluation to have a "value" that represented "not having a value" :)

Also, having **both** these notions was confusing. It seemed slick at first, for example, checking in a Map could return `undef` if the key was missing, and `nil` if the key actually had that value. And even assigning a key to `undef` would actually **remove the key** from the Map!

But no, I think in retrospect that while it almost always is a good idea to be specific and not use the same thing for multiple purposes (lots of software use `null` to represent both a nothing-value and the absence of a value) - having a value representing "absence of value"... is kinda weird. I mean, how do you even reference it? :)

So at the moment Spry has just `nil` just like any Smalltalk (or most languages). But discussing error handling the idea was brought up on Discord that... perhaps we could also remove `nil` from Spry? Do we really need `nil`?!

In Smalltalk you **declare** instance variables, local variables and a bunch of other variables. So... the variables exist before having been explicitly assigned a value. In such a language it's reasonable to auto initialize them to something like `nil`, or at least it was a reasonable approach at the time.

**But Spry doesn't declare variables at all!** Objects in Spry are Maps, so we don't declare slots, we just add members in the Map. And we don't declare locals in functions, we just add members in the Map representing the local variables. This means that essentially, we don't need `nil` for auto initialization, we can simply force the developer to actually assign the variable a proper value, when the assignment actually takes place.

Hmmm, what about other uses of `nil`?

Apart from being a default value for auto initialization `nil` is:

1. Used as a cheap **error return value**
2. Used to signify **absence**

Traditionally in Smalltalk lots of methods return `nil` as an indicator that the request couldn't be made, a "poor man" generic error indicator. I think this is a left over from other languages like C, where you really don't have much other choices than having errors embedded in the return value.

A typical such case would be to perform a lookup, and returning `nil` to indicate nothing was found. But in that case, the more proper API design would be to always use something like `at:ifAbsent:`. This is a nice error handling pattern, the passed code block as the second argument works as an error handler to perform an alternative action if the key is absent.

An alternative would be to signal failure using `throw` that can be caught and handled, however, such code would end up looking fairly complex in most other languages, typically something like:

    var val; // Need to declare outside of try
    try {
        val = myMap.find("key");
    } catch(e) {
        val = "default value";
    }
    print("Value: $val");

...but that seems more to be a problem with designing clean and neat ways to **catch and handle errors**. In Spry we could easily make this work as a one-liner:

    val = ([myMap at: "key"] || "default value")
    echo ("Value: ", val)

...so `||` would be a Spry **method** that runs the block and if the code block throws an error, it instead returns the given argument. We can implement it like:

    || = method [:x activation catcher: [^x] do self]

...and then that works! Of course, having explicit methods like `at:ifAbsent:` is cleaner in most cases.

Ok, so... if we **avoid nil as error indicator**, and as shown, that's easy in Spry still keeping code non verbose, what about **absence**?

If we still keep `nil` around developers will undoubtebdly use it as the "goto indicator" of an absent value. Developers are lazy and having `nil` will invite usage for sure.

But isn't it useful to have say `foo` have the value `nil`? Well, what does it mean? If it means "the variable foo has no value", then we can just not have the variable `foo` defined!

In Spry, values are held in two ways - either as the value part in Maps, or as elements in a Block. All variables are actually held as key-value pairs in Maps. When it comes to Maps, the obvious answer is to actually represent absence by simply not having the key-value pair. Of course, it would be nice to be able to check for absence of a variable, and Spry earlier had that with `?`, but then I removed it, and well, I will add it back ;)

    x ?

...will thus return `true` or `false`, to check if that word is defined in the **current scope**. For checks that look all the way out, you would use something more elaborate. Checking instance variables look the same:

    @x ?

This would not solve the case when you wish to store an "absence" in a block, but... that feels quite contrived anyway and surely it would be better to use something unique to represent that particular absence - like a literal word for example (since they are canonicalized).

So let's pretend `nil` was removed from Spry according to the above. Would it solve Tony Hoare`s "billion-dollar mistake"? Not really, since Spry is a dynamically typed language, we can still end up with `x` holding a Duck instead of a Car. But it's far less likely in my experience that developers end up doing such mistakes, and removing the "generic nothing" that is so tempting to use - perhaps that is indeed a step in the right direction!

# First assign and Reassign
To further restrict Spry in order to catch errors, assignments should be made more explicit. Normal assignment `x = 12` would only be allowed if `x ? == false` (would throw error otherwise) and reassignment `x := 12` would similarly only be allowed if `x ? == true`. This also makes it easy to distinguish between reassigning an existing word in a scope outside, or assigning in the local scope where it does not yet exist.

# Bomb or Exceptions
Rebol has 
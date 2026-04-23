---
title: Spry Error Handling
date: '2021-04-21'
slug: spry-error-handling
categories:
- Nim
- Spry
- Languages
- Programming
---
Work on [Spry](https://sprylang.se) continues... in small spurts. :) One thing that I have pushed ahead of me for far too long is **error handling**. People interested in Spry have been asking about it and yes, I decided to start getting a handle on it.

In fact, I wrote this article **last year** but forgot to get it done and published!

Error handling is an interesting topic, earlier it wasn't really much controversy around it but the advent of new techniques (Optionals etc) in combination with languages making... "interesting" choices (I am looking at you Go) has made this subject fairly hot. So what do we want in Spry??

<!--more-->

## Error handling

Exceptions, errors etc are simply "not so often expected paths of execution". Clarity of code can often be enhanced if the vanilla code path is clean of clutter for all these less expected paths. One common mechanism to achive this in some form is of course the try-catch style of Exeption handling.

I want most Spry code to be uncluttered. I also don't want too many concepts in the language since Spry is meant to be minimalistic in nature.

One thing has already been added, I call it the catch-throw mechanism. The idea is to have it as a base for most of the rest of the call stack based mechanisms. For even more advanced stack manipulations the stack is gradually being reified, but that will be explored more when making the first Spry debugger.

There are quite a few ideas in current languages on error handling:

- Return errors just like values from the called function.
- Throw errors and catch them at an appropriate level higher up the stack, thus avoiding boilerplate for just passing them along. Also avoids the issue with code expecting a proper result suddenly getting an error in their hands.
- Multiple return so that a function can return both a value and a potential error, often exclusive.
- Optionals, the idea of stuffing an error and a value into a "struct" so that we still return "just a single thing", but it can contain either a proper value, or an error.
- defer and errdefer, the idea of installing a handler that can do cleanups, either always before returning or only before returning with an error etc.
- Declarations showing the developer if a function can return errors, and potentially exactly what errors it can return.
- Rebol treats errors as a specific kind of fundamental value type, but several languages treat errors as values (Go etc).
- Rebol uses a "bomb" trick so that it can return either a proper value, or an error (that will blow up if evaluated).
- Smalltalk and Dylan (and perhaps CLOS) has a conditional throw-catch system which means the stack is not unwound when the search for a handler is performed. This means resume after the throw is possible.
- Erlang has the idea of simply not trying to recover from errors, just restart instead. It's a nice idea.
- Smalltalk uses blocks pervasively in control structures and also in exceptional handling like for example with `at:ifAbsent:` etc.

Also found a [nice article](https://www.jungledisk.com/blog/2018/04/16/language-features-error-handling/) discussing some of the above.

## Catch throw
In Spry we now have a basic catch-throw mechanism in place, and that is useful for making calls to handlers "up the stack", not just errors. I started with the [STTCPW](https://acronyms.thefreedictionary.com/STTCPW), so... added a slot in the Activation record called "catcher". Setting this slot to a code block/func installs a "guard" that will be invoked if a `throw` is performed inside **this** activation, or in an **activation below**. This was simple to implement and acts as a reasonable primitive for error handling.

So... this example works in `ispry`:

    foo = func [
      activation catcher: [echo ("Caught a ", :banana)]
      echo "Throwing a banana..."
      throw "banana"
    ]
    foo

...will print:

    Throwing a banana...
    Caught a banana

If an activation record does not have a handler, throw will keep searching upwards and if none is found it will currently do a hard process exit 1.

Typically though, the top activation record should have a **catch all handler** installed and do something reasonable.

As in Smalltalk (and some other languages) throwing an Exception **does not unwind the call stack**, so a handler doing a normal return will **return back to the throw**! Unless it calls `activation unwind` first, if so, the return will instead go to caller of the record where the handler is installed (NOT YET IMPLEMENTED). In fact, the principle of least surprise may mean we should swap these behaviors :)

With this in place we can implement `catch:` (resembling try/catch) like:

    catch: = method [activation catcher: :handler do self]

...so what does this do? It's a method, so it takes a receiver block on the left. When we run the method we are in a new Activation, and we set the catcher to the given handler block passed as the argument, and then we `do self` in order to execute the receiver block that may possibly throw.

This enables "scoped" use familiar from most languages. Below we see it in action:

    foo = func [
      # This is an activation level catcher, just to show we never reach it
      activation catcher: [echo "we never reach this"]

      # Here we call `catch:` on a block with a handler block as argument.
      # This is the classic try-catch style found in many languages.
      [
        echo "Throwing a banana..."
        throw "banana"
      ] catch: [
        echo ("Caught a ", :banana)
      ]
    ]
    foo

...and it should print the same as before and never reach the catcher in foo :)

Going back to the general problem of error handling, my feelings so far:

- Go style multiple return and tons of `if err != nil {...}` is **NOT** to my liking. I can understand the philosophy, but sorry, don't like it. Especially not in the minimalistic style that Spry tries to adhere to.
- Only a try-catch conditional system like Smalltalk has is kinda boring. It can also get fairly confusing to debug, for example try-catch with empty catch clauses that "swallows" errors in silence, nested calls get hairy. It can also blur the "vanilla case" quite a lot. Nevertheless, it may form a "base" in combination with other mechanisms.
- It would be fun with something simpler and different! Spry is an experiment! But not sure yet what this would be...
- Spry shares the evaluation model of Rebol (kinda-ish), so the idea Rebol has with a special "bomb" is tempting in its simplicity, especially when writing vanilla code to begin with!
- Spry has tagging, we should be able to use it somehow, for example to tag funcs and methods.
- I want to be able to write vanilla code as long as possible, then gradually hardening, for example as result of unit tests. But I don't want hardening to introduce clutter in the vanilla code! Thus, somehow, I would want to be able to add error handling as a "side track" and not inlined in the vanilla code.
- The idea of doing error handling "on the side" and not inlined in the vanilla code. Defer and errdefer are going in this direction, they are code blocks that are executed only if certain rules are met, but they are clearly separate.
- We can either throw, or return. But we could also "signal". A signal is a neutral way of signalling a condition, it does not imply what to do next, we could hard exit the process :), or we could always log it and then throw, or we could always return it as a bomb etc.
- Dylan has interesting features, perhaps worth reading closely: https://opendylan.org/documentation/intro-dylan/conditions.html and  https://opendylan.org/books/drm/Conditions_Background

So... where to go from here? Ideas?

regards, Göran
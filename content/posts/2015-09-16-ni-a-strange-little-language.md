---
title: Who says Ni?
date: '2015-09-16'
slug: who-says-ni
categories:
- Nim
- Spry
- Nimrod
- OOP
- Smalltalk
- Rebol
- Object orientation
- Languages
- Programming
---
Ni is my [own little language](/spry) heavily influenced by [Smalltalk](http://www.world.st) but also other sources like Rebol, Forth, Lisp, Self and Nim. Ni is a bit strange, but it's not academic and really meant to become something useful.

So put on your helmet and let me take you to the shrubbery...

<!--more-->

I love Smalltalk - the language that pioneered OO back in the 1980s and is still [very much alive](http://pharo.org). But what makes Smalltalk so great? Trying to put my finger on it, here is a list:

* Closures and non local return for control structures.
* Low level types don't get in my way (numbers for example)
* Easy and quick manipulation of collections.
* Easy readable keyword syntax, everything is an expression etc, gives great power in expressing code.
* The object model is easy to reason about and picture mentally, doesn't get in your way.
* Fully reflective with live coding, inspectors, debuggers, while-we-run etc
* Cross referencing. All senders, implementors. All accesses to ivar, all references to class etc

In making Ni I am **striving to cover these bases** and some of the fundamental pieces are there already, like closures and non local return.

Ni comes in two modules, the parser (500 loc) and the interpreter (750 loc). The parser produces an AST which is also the internal representation of data in Ni. The interpreter then interprets the AST. Ni is written in Nim and thus compiles and runs on basically any platform supported by C. There is a trivial REPL (70 loc).

## A taste of Ni
In Smalltalk 99% of our collections are OrderedCollection and Dictionary. It does make sense to give these two as good treatment as possible in a new language, I think Javascript and JSON etc have shown us the importance of this. Smalltalk, while having **very strong collections**, is actually kinda weak when it comes to literal syntax for these two fundamental data structures. Ni tries to remedy that.

For the ordered sequence, Ni is inspired by Rebol/Lisp and has the "Block" as the fundamental data structure. It's like an OrderedCollection, and uses square bracket `[1 2 3]` syntax. And yes, it's also the same syntax for **code blocks** because Ni is homoiconic. This means that **code and data share the same representation**, just like in Lisp/Rebol. So in Ni we can do:
``` nimrod Self modifying code
code = [3 + 1]      # This is a block with 3 elements
code at: 2 put: 4   # Stuff the number 4 as the last element, we use positioning from 0
echo do code        # Prints out 7
```
In the above code we can immediately note that yes, Ni is dynamically typed and assignment is done via `=`. Assignment is actually a function call, but let's ignore that detail for now. Second line shows that Ni supports keyword syntax for multiple argument functions (like Self and Smalltalk), but it's actually implemented as syntactic sugar in the parser. The second line can thus just as well be written like:
``` nimrod
code at:put: 2 4
```
Which in a C-ish language can be read as:
``` nimrod
code.at:put:(2, 4)
```
This works since ":" is allowed in function names but they are given special treatment by the parser when they appear as the last character in a token.

Another interesting detail is that lines have no statement separator, but Ni does NOT use line endings or indenting to infer semantic meaning, so the code can actually be written without line endings like this too:
``` nimrod Look ma, no LFs!
code = [3 + 1] code at: 2 put: 4 echo do code
```
And it would still work the same, funky indeed. And yes, the conclusion is that whitespace is both **insignificant** (new lines don't matter, all kinds of whitespace is just whitespace) and **very significant** (whitespace is used as token separator) in Ni, `3+4` is not the same as `3 + 4`.

But let's get back to Blocks. Not only are they both code and dynamic arrays, they also do double duty as streams since they have an embedded position "cursor", just like in Rebol. This means iteration and streaming over Blocks is trivial:
``` nimrod Blocks have a cursor
block = [1 2 3]
# Lets loop over it manually using the internal position
block reset           # Set position back to 0
[block end?]          # We call an infix function called "end?" with block as argument
  whileFalse:         # We call an infix function called "whileFalse:" taking two blocks
    [echo block next] # We call an infix function called "next" to get next element and echo it
```
## Implementing select:

The above looks silly for practical use, but we have what we need to easily implement Smalltalk `select:`. Let's first learn some other details.
When we run a Block - an activation record is created to hold the local environment of the block - in other words, a closure. <del>We can also permanently associate such a Context</del> ..no, that was wrong. A Func adds in particular a reference to the lexical parent activation, and a boolean flag showing if this is an infix function or not. A Func is created from a Block using the `func` function (tihi!):
``` nimrod Making a func
myfunc = func [:a + :b]  # "func" takes the block as an argument and returns a Func
echo (myfunc 3 4)        # Should print 7, parenthesis are used since echo is not eager.
```
Here we also introduce another oddity of Ni, so called "arg words". An arg word begins with a `:` and when evaluating `:a` Ni will pull in another argument from the call site and store it locally in `a` and that's also the value of `:a`. It's reminiscent of Smalltalk, but note that this is not a declaration, it's actually an operation that can appear anywhere in the block. This means we can write extremely short lambdas like the above and we can also handle variable number of arguments.

As was seen above we can also make infix functions in Ni, using `funci`. This means the first arg word will pull from the left side at the call site:
``` nimrod Infix func in action
plus = funci [:a + :b]
echo (3 plus 4)          # Should print 7 since a is "pulled in from the left"
```
Ok, let's finish this little article by implementing the venerable Smalltalk `select:` through adapting the above code into an abstraction:

``` nimrod Implementing select:
select: = funci [:blk :pred
  result = []
  blk reset
  [blk end?] whileFalse: [
    n = (blk next)
    if do pred n [result add: n]]
  return result
]
[1 2 3 4] select: [:each > 2] # This will happily evaluate to "[3 4]"
```

The above implementation of `select:` in Ni is simply an infix Func taking two Blocks as arguments, blk and pred. The first block (the "receiver") is the block we want to iterate over. The second block is a code block taking one argument that should evaluate to true for those elements we are meant to filter out.

The body of `select:` first assigns an empty new Block to a local word (like a variable) `result`. Then it uses the builtin positioning of blk to loop over it, pluck out the next element and call pred using `do` (like sending #value in Smalltalk) to decide if we should add it to result. `if` is yet again a primitive function taking two arguments, first a boolean and second a block to evaluate if true. `true`, `false` and `nil` are words bound to known singletons just like in Smalltalk. At this point the pattern is quite clear - **all control structures in Nim are functions**, either primitive ones implemented in Nim and bound to words, or functions written in Ni.

Finally we return the result, `return` is actually a primitive function, as almost everything is in Ni. The final line shows usage, and as you can see it looks very similar to Smalltalk or Self.

## Going forward

Ni is evolving and it doesn't do objects yet but I think Ni already shows (as Rebol already also has shown to some extent) that you can have a Smalltalk-ish language that is at the same time homoiconic and deeply functional. A bit of structure using blocks, a bit of syntactic sugar enabling keyword syntax, a bit of semantics to be able to do non local returns (yes! Ni has those too, so `detect:` is similarly easy to implement) and... well, we have something new and interesting!

And oh, it's of course not only homoiconic but as examples above show - **Ni is 100% live too, everything can change at runtime**. And given that it mixes nicely with Nim that in turn easily can wrap and use C/C++ libraries - we have **a new Smalltalkish language with an interesting twist**.

Being written and easily embeddable in Nim makes Ni a great citizen in the C/C++ language eco system. Making a binary executable is trivial. Making a dll is also trivial. And finally, Nim has very interesting capabilities when it comes to multiple native threads and parallell computation, an area where we as Smalltalkers haven't seen much action. Native GUIs? No problem, Nim can already do them.

Hope you liked this little peak into Ni!

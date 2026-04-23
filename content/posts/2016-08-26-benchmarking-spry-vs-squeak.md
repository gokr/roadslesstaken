---
title: Benchmarking Spry vs Squeak
date: '2016-08-26'
slug: benchmarking-spry-vs-squeak
categories:
- Spry
- Smalltalk
- Nim
- Languages
- Programming
---
[Spry](http://sprylang.org) is evolving quite nicely during my night hours. Focusing on performance is however still premature, but I do want to verify that I am not barking up the wrong tree, like ... in the wrong forest even. So I make trivial benchmarks from time to time, just to see and learn.

Some background on the Spry implementation may be interesting. Spry is implemented in Nim as a **direct AST interpreter**, it's not a JIT, in only about 2000 lines of code. It has a **recursive classic "naive" design** and uses a **spaghetti stack of activation records**, all allocated on the heap relying fully on Nim's GC to do it's work. It also relies on Nim's method **dynamic dispatch** in the interpreter loop for dispatching on the different AST nodes. Blocks are true closures and control structures like `timesRepeat:` are implemented as primitives, normally **not cheating**. Suffice to say, there are LOTS of things we can do to make Spry run faster!

The philosophy of implementation is to keep Spry very small and "shallow" which means we rely as much as possible on the shoulders of others. In this case, primarily Nim and it's superb features, performance and standard library.

Enough jibbering, let's do some silly damn lies - ehrm, I mean silly tests!

<!--more-->

```python
| b r |
b := OrderedCollection new.
r := Random new.
2000000 timesRepeat: [b add: (r nextInt: 10)].
[b select: [:x | x > 8]] timeToRun
```

The above snippet runs in around 40 ms in latest Squeak 5.1. Nippy indeed! Ok, so in Spry then with a recently added primitive for `select:`:

```python
b = []
2000000 timesRepeat: [b add: (10 random)]
[b select: [:x > 8]] timeToRun
```
First of all, if this is the first Spry code you have seen, I hope you can tell it's **Smalltalk-ish and it's even shorter**. :) A few notes to make it clearer:

* We don't declare local variable names in Spry.
* Assignment uses `=` and equality uses `==`, no big reason, just aligning slightly with other languages.
* `[]` is the syntax for creating a Block (at parse time), which is the workhorse dynamic array (and code block), like an OrderedCollection.
* Spry has **no statement separators (!)** so no `.` at the end, nor does it rely on line endings or indentation, same snippet can be written exactly the same on a single line.
* You need (currently) a tad more parentheses in Spry code, for example we need `(10 random)` because Spry evaluates strictly from left to right.
* Blocks don't declare variables either, they are "pulled in" using the syntax `:foo`. So blocks are often shorter than in Smalltalk like `[:x > 8]` or even `[:a < :b]`.

Spry runs this in 1000 ms, not that shabby, but of course about 25x slower than Squeak. However... I think I can double the Spry speed and if so, then we are in "can live with that-country".

Just to prove Spry is just as dynamic and cool as Smalltalk (even more so actually in many parts), we can also implement `select:` in Spry itself (and for the more savvy out there, yes, `detect:` can also be implenented using the same non local return trick as Smalltalk uses):

```python
spryselect: = method [:pred
  result = ([] clone)
  self reset
  [self end?] whileFalse: [
    n = (self next)
    do pred n then: [result add: n]]
  ^result]
```

Without explaining that code, how fast is the same test using this variant implemented in Spry itself? 8.8 seconds, not horrible, but... I think we prefer the primitive :)

Now... let's pretend this particular case is an important bottleneck in our 20 million dollar project. We just **need to be faster**! The Spry strategy is then to drop down to Nim and make a primitive that does everything in Nim. Such a **7-line primitive** could look like this:

```nimrod
nimMeth("selectLarger8"):
  # evalArgInfix(spry) pulls in the receiver on the left.
  # We convert it to the type we expect - SeqComposite is a super type
  # of Block, Paren, Curly.
  let self = SeqComposite(evalArgInfix(spry))
  # We create a new empty Block to put the selected nodes in.
  let returnBlok = newBlok()
  # We perform a regular Nim iteration. self.nodes is a Nim seq[Node].
  for each in self.nodes:
    # For each element we convert to IntVal, which is the node type for a Spry int.
    # This will cause a catchable exception if it's not an IntVal.
    if IntVal(each).value > 8:
      returnBlok.add(each)
  # A primitive always returns a Node or subclass thereof, like in this case a Blok.
  return returnBlok
```
Then it runs in **10 ms!**

Yup, it's cheating, but the 20 million dollar project wouldn't care... The thing to realize here is that its MUCH easier to cheat in Spry than it is in Squeak/Pharo. But... yes, you would need to **know how to make a primitive**, and as a primitive **it's compiled code** so you can't mess with it live, and it **also presumes that each node is an IntVal**. However, Spry (when I fix error handling) should gracefully handle if it isn't an IntVal, that will trigger a Nim exception that the Spry interpreter should catch.

If you have made primitives in Squeak/Pharo you know it's much more complicated. You need to take great care with allocation since the GC can move things under your feet. You must convert things to C and so on, and building the stuff is messy. Spry on the other hand shares the underlying data structures with Nim. In other words, Spry nodes are Nim objects. It's trivial to work with them, allocate new ones like `newBlok()` above creates a new block and so on. This is a huge deal! Recently when I started integrating [libui](https://github.com/andlabs/libui) [with Spry (a pretty slick movie)](http://krampe.se/spry-ide.mp4) I got callbacks from libui back into Spry working in like... 30 minutes of thinking. That's HUGE! Doing callbacks from C or C++ back into Squeak has been a really messy and complicated thing for YEARS. Not sure if it's any better.

Also, going pure Nim would be much faster still since it would use a `seq[int]` and not a `seq[Node]` (boxed ints) - a vast difference. So if we really wanted to work with large blocks of integers, a special such node type could easily be made that exposes primitives for it. Kinda like the FloatArray thing in Squeak, etc.

## String finding

Let's look at another example where Spry **actually beats Squeak**. And by beat I mean really beat, **by factor 4x!** The test is to use `findString:startingAt:` in a fairly large string, to find a match, 2 million times.

```python
| s time |
"A file with a mixed text 15712 bytes, hit is at 11499, 6 partial hits before that."
s := (StandardFileStream oldFileNamed: 'string.txt') contentsOfEntireFile.
time := [2000000 timesRepeat: [
  s findString: 'native threads and super high performance garbage' startingAt: 12
]] timeToRun
```

This snippet runs in **135 seconds** in Squeak 5.1. The corresponding Spry code is:

```python
# A file with a mixed text 15712 bytes, hit is at 11499, 6 partial hits before that.
s = readFile "string.txt"
time = ([2000000 timesRepeat: [
  s findString: "native threads and super high performance garbage" startingAt: 12
]] timeToRun)
```
Again, note how Smalltalkish the code looks - and ... you know, come on Smalltalk... reading a file? It shouldn't need to be `(StandardFileStream oldFileNamed: 'string.txt') contentsOfEntireFile` for such a common and mundane task!

You gotta admit, `readFile "string.txt"` is nicer. But hey, says the careful reader, what the heck is that? Yes, Spry supports "prefix functions" that take arguments from the right, Rebol style. It isn't used much in Spry code, but for some things it really reads better. For example, in Spry we do `echo "hey"` instead of `Transcript show: 'hey'`. That's another thing that is overly verbose in Smalltalk and should IMHO be fixed, at least just to save poor newbies their fingers. Anyway (end of rant).... 

...Spry runs that in **33 seconds!** And just to get a sense for how large the primitive is in Spry, it's **exactly 5 lines of code**:
```nimrod
nimMeth("findString:startingAt:"):
  let self = StringVal(evalArgInfix(spry)).value
  let sub = StringVal(evalArg(spry)).value
  let start = IntVal(evalArg(spry)).value
  newValue(find(self, sub, start))
```

It's quite easy to follow. We just pull in arguments and unbox them into Nim string, int, int - and then we call [Nim's find](http://nim-lang.org/docs/strutils.html#find,string,string,Natural) and we finish by using `newValue()` to box the answer as a Spry IntVal again. This shows how easily - no... **trivially** we can map Spry behaviors to Nim library code which runs at the speed of C/C++.

## Speeding up Spry
Given all this, it would still be nice to improve Spry to come say ... within 10x of Cog for general code, perhaps in this case shave it down from 1000 ms to around 300 ms. The things that I do know I should do to improve speed in general are the following:

* Formalize **binding phase** in Spry. This means caching the binding of words "in place", especially words resolving to funcs and methods. This would eliminate a HUGE amount of idiotic lookups that Spry currently performs **every time it runs a block or function** and profiles have already shown that this is priority UNO to fix since it alone usually eats 50% of runtime.
* Move to a **stackless design** of the interpreter. Exactly what performance improvement this would give, I am not sure. But it would remove the growing intertwined C stack and enable things like Spry stack manipulations, continuations, coroutines etc, so we really want it!
* Profile the interpreter to see what low hanging fruit exists after the above. :)


I hope this got you interested in Spry!

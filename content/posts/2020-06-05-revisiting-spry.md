---
title: Revisiting Spry
date: '2020-06-05'
slug: revisiting-spry
categories:
- Nim
- Spry
- Languages
- Programming
---
After a period of slower progress I got reignited regarding [Spry](https://sprylang.se). So far I have written [a lot of articles](http://goran.krampe.se/categories/spry/) about Spry, and during this time things have evolved and changed.

So I am now trying to "clean house" on where Spry stands today. This sweep through the old articles is a first step, then I will update the language manual to be 100% in sync with the implementation.

Let's go through the articles from the beginning!

<!--more-->

Things wrong in [article one](http://goran.krampe.se/2015/09/16/ni-a-strange-little-language/):

* `funci` is now called `method`, indicating it is a message to a receiver on the left
* `if` as been changed to the more Smalltalkish `then:else:` (but shorter than `ifTrue:ifFalse:` and reads nice)
* `return` is now `^` just like in Smalltalk

In [article two](http://goran.krampe.se/2015/09/22/guts-of-ni/):

* Context is now called **Map**. It's the same as a Smalltalk Dictionary, but "Map" is a more popular term these days, and shorter.
* Get words use `$`-prefix, not `^` (which is return). This actually looks kinda ok, it makes them resemble "variables" from other languages.
* The idea with a pluggable parser... I think I will skip that and replace with something else in pure Spry!
* The scoping prefixes `.` and `..` have been removed and replaced with another way to assign.
* I wrote "This means Ni maintains no call stack of its own." - no idea what I meant by that. Spry indeed has a stack of activation records.

In [article three](http://goran.krampe.se/2015/09/23/ni-design-decisions/):

* There is no `ifelse`, instead we have `then:else:`, `else:then:`, `else:`, `then:`.
* The argwords design mistake is still here, but... can be avoided by not using argwords nested, so use `[:x :y ^[x + y]]` instead of `[^[:x + :y]]`. So it will probably have to stay.
* Single `?` is not used anymore, we can use `set?` to check if an unevaluated word is bound, like `x set?`
* Meaning of scopes are now (I have removed `.` and `..`):
  * `x` - look in locals and then all the way out.
  * `@x` - look in closest surrounding Map (self).
* Optional arguments have not been added, I don't think I ever will add.
* `&` has been changed to Smalltalk style `,` for concatenation, but leaning towards `+`.
* `undef` vs `nil` is slightly different:
  * `nil` is a value that means "no value"
  * `undef` has been removed, it was a fun experiment
* `?`-marks are used for funcs/methods that return booleans, convention. `!`-mark is still unused.
* `self` is as the **receiver for methods**. It can be anything.
* `context` is `locals`, returns the Map of the local scope.
* `activation` returns the current activation, not yet explored much but it's there!

In [article four](http://goran.krampe.se/2015/09/25/adding-objects-to-ni/):

* I later opted to call a Dictionary a **Map**, so it's Map now :)
* The `bindings` word is now `locals`.
* The description of `object` is partly the way it works, yes, it takes a Map as argument and returns an "object". But... this is done using tags that's not described in this article.
* Also, the traits idea and thoughts around that is not what has been implemented later. The current Spry instead is exploring if methods can be defined for things with specific tags, and then if those methods can be automatically composed into "polymethods" so that two different modules can define methods with the same name - and they are "merged" into a polymethod that get's bound to that name. When invoked the polymethod should "internally" pick which method to execute.

In [article five](http://goran.krampe.se/2016/04/08/ni-is-now-spry/):

* Yes, renamed to Spry. But... it's **sprylang.se**, not .org

In [article six](http://goran.krampe.se/2016/04/09/spry-image-model/):

* Yes, base idea of using compressed "Spry code" and store in a fast embedded database still stands! But I now have Rocksdb instead of Sophia, and a pure Nim implementation of Snappy instead of lz4 (it was too hard to get on various platforms)

In [article seven](http://goran.krampe.se/2016/04/16/spry-modules/)

* Yes, the current modules is implemented as described. Not tested much, but yes. I still think the base ideas stand.

In [article eight](http://goran.krampe.se/2016/05/03/spry-modules-ii/)

* I did fix so that `Foo::bar` first finds Foo, and then looks in it. So it works for Maps in general, not just modules. And yes, you can then shadow a module with a global.
* To access "map members" I instead added `@x` syntax. Since `self` is now bound to the receiver of methods, this resolves members also. One issue though, if you use blocks (and not funcs) then nested blocks in a method sent as parameters to other methods will obviously not resolve to the lexical self, but to the receiving self. Changing the block to a func solves this.
* Lossless AST was something I did experiment with, but dropped it. A bit too crazy perhaps.
* So... otherwise it basically sounds like a good plan, but not used much (or implemented much) yet.

In [article nine](http://goran.krampe.se/2016/05/14/spry-vs-allen/)

* This article is mostly "fluff" but there is one important thing I need to improve - "Live within the prototype". In other words, Spry code should be edited, browsed and debugged in Spry tools. I need to try to get that going!

In [article ten](http://goran.krampe.se/2016/05/24/spry-performance/)

* Nothing to note, except that yeah, Nim is fast and Spry is slow :)

In [article eleven](http://goran.krampe.se/2016/07/19/spry-is-a-smalltalk/)

* Most of this article seems quite correct and according to plan.

And finally, in [article twelve](http://goran.krampe.se/2016/08/26/benchmarking-spry-vs-squeak/) 

* Most here seems fine too.


## Latest Changes

* I have added `:=` for **reassignment**. If no existing binding is found there will be an error (not fixed yet). So `=` will work fine for single assignment, and will assign in local scope. And `:=` signify reassignment and will lookup outwards before assigning.
* I have removed `undef`. It felt neat but get's confusing. Maps can still hold nil, it's a valid value - if you want to check for a missing binding you will have to use explicit calls to do it instead, just as in Smalltalk.
* I have removed `.` and `..` scoping words. They can instead be implemented as direct access to `locals` or `activation parent lookup:` etc.
* I have implemented a base `catch:`, `throw` and `try:catch:` mechanism but more to come.

More on error handling in the next article!

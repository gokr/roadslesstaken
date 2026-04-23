---
title: Ni design decisions!
date: '2015-09-23'
slug: ni-design-decisions
categories:
- Spry
- OOP
- Smalltalk
- Rebol
- Object orientation
- Languages
- Programming
---
So... my little Ni language got some attention since it was first [on Hackernews](https://news.ycombinator.com/item?id=10235688), then [TheRegister](http://www.theregister.co.uk/2015/09/18/we_are_the_knights_who_code_ni/), all over Twitter and also [Reddit](https://www.reddit.com/r/programming/comments/3lfpym/ni_a_language_influenced_by_smalltalk_written_in/).

But I think it managed to come relatively unscathed out of it, although it **REALLY is pre-alpha-not-even-complete-eats-your-harddrive early** and you know, I really have no idea if it ever will go the distance since it takes quite a bit of work to get a language to actually be used. But I am going to stick with it.

Anyway, I have been experimenting with "arg words" and "lookup scoping" while thinking about how to add objects, and a few other things. This article doesn't introduce how I want to do objects, but the next one does (I split it in two). This article however covers a bunch of loose ends and my ideas on how to tackle them in Ni. And I will try to make this understandable even if you don't know Ni. ;)

<!--more-->

## Argwords design mistake

Argwords (Ni's mechanism for accessing arguments inside a function) as they stand today are neat but suffer from an embarrassing "design mistake". Simple blocks work fine, for example like these, similar to Smalltalk:

* `[:a :b a + b]`
* `[:a > :b]`

The first one seems *"just like Smalltalk"*. It looks like the arguments are declared at the beginning, but note that there is no separator between those "declarations" and the rest of the code like Smalltalk has (the `|`). This is because an argword in Ni is an **operation, not a declaration**. So `:a` means *"pull in the next argument from the callsite (evaluating it first), store the value in local variable a"* and the value of `:a` is the argument pulled in.

This means the second example works fine, since the value of `:a` is whatever we pulled in, and since the argwords can come anywhere in the block, we can call the `<`-word immediately like that.

*So what is the mistake?*

Well, let's say we do something like `[ifelse (:a > 0) [a + :b] [0]]`. It says *"pull in a and if it's bigger than zero, pull in b and add them together and return that, otherwise don't pull in a second argument and just return 0"*. One can definitely question the usefulness of such dynamic arity :) but anyway, let's see what `nirepl` says:

```nimrod
gokr@yoda:~/nim/ni$ nirepl
We are the knights who say... Ni! Enter shrubbery... eh, code and
an empty line will evaluate previous lines, so hit enter twice.
do [ifelse (:a > 0) [a + :b] [0]] 1 2

Oops, sorry about that: Can not evaluate 1 + [0]
```

Hehe, what? Ahh... so `:b` tries to pull in the next argument at the call site, but this is a nested block so it doesn't try to pull in `2` but instead tries to pull in "whatever comes next in the block where this block is defined". And that happens to be the else-block of `ifelse`... ooops. And yeah, Ni doesn't have any proper error model yet, any ideas on that is appreciated.

So the current design issue means... **argwords in nested blocks will not work as expected - since we use blocks for control structures!** It means that you would need to rewrite this example as `[if (:a <= 0) [0] a + :b]` which would work fine, since now `:b` is not in a nested block.

I don't have a good idea on how to make this work when nested, perhaps I will let this one just be a "language-gotcha" for now. 

## Scoped lookup

One thing I am experimenting with in Ni, which doesn't exist in either Rebol (I think) or Smalltalk, is different variants of lookups for words.

Currently, regular word lookup starts by looking in the local scope, then in the outer lexical scope and outwards out to the root activation of the interpreter (global scope). This is the default lookup which means you have shadowing on all levels. But then one can already use two different prefixes to change that behavior:

* `..banana` - similar to filepaths this means *only look in nearest outer lexical scope*
* `.banana`  - similar to filepaths this means *only look in local scope*

The idea is to use this both for access and left side in an assignment. BUT... I am having regrets, I think I will change it to:

* `banana` - start in local and go all the way out for access. Assignment however is local only.
* `.banana` - only access and assign in "self" which typically will be bound to an object or module. This is instance variable access.
* `..banana` - start in the "outer" scope and go all the way out. Both for access and assignment.

So the default scoping, `x` without a prefix, will work fine for local variables, arguments and other things outside in the outer scopes. When assigning it will however always be in the local scope.

For instance variables in objects you will have to use `.x`, both for access and assignment. So those are explicitly different from all other variables, which I think is good in a language like Ni where we do not declare any variables. See upcoming article for more on Objects.

NOTE: Since do not declare the names of variables - typos can only be discovered via heuristics, like "never assigned to nor an argument in this function" or "assigned to but never used" etc.

Finally using `..x` we are basically depending on an external environment to define `x` for us. It's kinda like "I wish for an x" and we presume someone will make sure it's out there somewhere. Exactly what "outer" scope means may be different depending on context. In a Func, it's just in the defining outer scope.

## Introducing undef

One other thing. I am considering introducing `undef` in addition to `nil`. Smalltalk suffers from its fair share of DNUs (doesNotUnderstand exception) due to variables being nil, most often not having been initialized to a proper value. But quite often in Smalltalk `nil` is also used as a proper value meaning "no value", in that case it doesn't mean "not set". Thus separating `undef` from `nil` seems like a useful idea.

So if a word evaluates to `nil` there is at least a binding for it, but it has `nil` as its value. If a word evaluates to `undef` there was no binding found at all. I would like a short and punchy name though, `undef` is quite boring. Perhaps `eki`? :)

## Exclamation point and question mark

In Rebol question marks are used as the last character of words to functions that evaluate to a boolean. Ruby does something similar I think and it's a good thing, so Ni adopts that. There is however nothing special about the `?`-character, it's just a convention.

The exclamation point is used in Rebol as a marker of a datatype word. Rebol has lots of datatypes and likes to easily test values if they are of a certain datatype. One can also add type declarations of arguments to functions, although they are checked only at runtime. Ni is more Smalltalk-like and it seems to me that relying on polymorphism is more sound. Smalltalk code very seldom tests like that, and if it's done we typically frown upon it. This makes the `!` free for some other use or convention, ideas welcome.

The word consisting solely of `?` could be used to test if a word is defined, so `banana ?` would be the same as `banana != undef`.

## Indexing and refinements

Also, two other issues that I really haven't given proper thought:

* **Indexing**. In Nim you do `x[1]` and `x[1] = 2` but in Smalltalk you use messages instead like `x at: 1` or `x at: 1 put: 2`.
* **Rebol refinements**. In Rebol this can also double for indexing so the above would be  `x/1` and `x/1 = 2`. Otherwise Rebol uses words for indexing similar to Smalltalk.

For the moment I consider **going the Smalltalk route for indexing**, since that works already and even though it's "longer to type" it works fine in Smalltalk. It also honours encapsulation.

Refinements in Rebol are kinda slick. They are used in two different ways - either as "indexing" or "member access", or as a way to pass "flags" or optional arguments to functions. Smalltalk works without explicit member access from the outside, you need a setter or getter and that seems fine to me and ensures encapsulation. I also think `foo/bar` looks kinda odd to read for member access or indexing.

The **flags to functions and optional arguments** seems useful though and can be likened with the `--opt` that Unix uses. The obvious advantage is that they are boolean in nature, so shorter to write `/short` instead of `short: true` and they can also appear in any order and they are optional.

Smalltalk does not have anything resembling this, there you often end up with a fairly clumsy approach with many similar keyword messages with various subsets of keywords, each calling the complete one with all keywords, supplying default values for those missing.

I am more of a Linux than a Windows guy, and I don't really like the "path" usage of refinements in Rebol. One idea is then to introduce a new kind of word: an option word. They would start with `-` (and be more than 1 character long so we can still have `-` for "minus") and they would evaluate to themselves. The magic would however be in the mechanism of argwords, when an argword is evaluated, and it instead pulls in an option-word, it would:

1. Gobble it up and create a local binding for the option word to `true`
2. Continue pulling to get a "real" argument

This means option words must come before an argument, otherwise they will not be pulled in.

Example:

```nimrod
plus = funci [:a :b
  if hhgttg ? [return 42] # hhgttg is available as a local word
  if negated ? [return ((a + b) ..negated)] # Note how we need to use ..negated in order to avoid the local shadow
  return a + b]
1 plus -hhgttg 3 # When plus is pulling b it will also pull in -hhgttg
1 plus 3
1 plus -negated 3
```

One can also imagine optional arguments (where the value is something else than `true`) like Rebol has by simply using a `:`:

```nimrod
concat = funci [:a :b
  if separator ? [return a & separator & b]
  return a & b
]
"bar" concat "foo"
"bar" concat -separator: ", " "foo" 

```

Now we quickly realize that **infix functions taking only one regular argument** will have issues with passing optional arguments... Options work, but not optional arguments since they would be pulled in "backwards". And another thing, if you haven't yet pulled all arguments you are not sure if you have pulled all options... In other words, if your function offers options, it should probably start by pulling in all arg words like `concat` does above.

Ok, let's chalk these oddities up as "language warts" for now. :)

## Reflection

A number of words could be used to access and manipulate the internal machinery of Ni, like the activation stack and the current scope. Smalltalk has superb power by reifying the stack and making it available via the pseudo variable `thisContext` so doing something similar seems obvious.

* `self` - the nearest outer Object. This is mainly used for calling methods on self and passing self as argument, since state is accessed via `.`-scoping. There is no super concept.
* `context` - the nearest Context which can be the Context inside a function. It enables reflection on what locals are defined etc.
* `activation` - the current activation record. This would be the same as `thisContext` in Smalltalk (since Smalltalk calls them "contexts").

I will start with these I think.

Until next time, happy coding

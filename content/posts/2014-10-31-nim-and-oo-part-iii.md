---
title: Nim and OO, Part III
date: '2014-10-31'
slug: nim-and-oo-part-iii
categories:
- Nim
- Nimrod
- OOP
- Object orientation
- Languages
- Programming
- Generics
---
So previously in [Nim and OO Part II](/2014/10/31/nim-and-oo-part-ii) we saw how we could solve the "super call" issue using only procs and generics in [Nim](http://nim-lang.org). This means that all code is statically bound.

But if you have read all these article you know I also tried the more appropriate mechanism for OO - so called **methods**. In Nim a proc is a regular statically bound function, simple and fast. A **method** on the other hand uses dynamic multimethod dispatch on the **runtime types** of all object parameters. The easy way to do objects in Nim (with inheritance of behavior) is using methods - but of course, this means dynamic lookup that has a runtime cost, but quite small as we will see.

Time for benchmarking!

<!--more--> 

With methods the fruit code looks like this:

``` nimrod
import math

# Dollars and Kgs
type
  Dollar* = distinct float
  Kg* = distinct float

proc `$`*(x: Dollar) :string =
  $x.float

proc `==`*(x, y: Dollar) :bool {.borrow.}


# Fruit class
type
  Fruit* = ref object of RootObj
    origin*: string
    price*: Dollar

method reduction(self: Fruit) :Dollar =
  Dollar(0)

# Code broken out enabling super call of it
method basePrice(self: Fruit): Dollar =
  Dollar(round(self.price.float * 100)/100 - self.reduction().float)

method calcPrice*(self: Fruit): Dollar =
  self.basePrice()


# Banana class
type
  Banana* = ref object of Fruit
    size*: int

method reduction(self: Banana): Dollar =
  Dollar(9)

method calcPrice*(self: Banana): Dollar =
  self.basePrice()

# Pumpkin
type
  Pumpkin* = ref object of Fruit
    weight*: Kg

method reduction(self: Pumpkin): Dollar =
  Dollar(1)

method calcPrice*(self: Pumpkin) :Dollar =
  Dollar(self.basePrice().float * self.weight.float)


# BigPumpkin
type
  BigPumpkin* = ref object of Pumpkin

method calcPrice*(self: BigPumpkin) :Dollar =
  Dollar(1000)


# Construction procs
proc newPumpkin*(weight, origin, price): Pumpkin = Pumpkin(weight: weight, origin: origin, price: price)
proc newBanana*(size, origin, price): Banana = Banana(size: size, origin: origin, price: price)
proc newBigPumpkin*(weight, origin, price): BigPumpkin = BigPumpkin(weight: weight, origin: origin, price: price)
```

The same code below using only procs and generics. This time I have also used proper `fn[T](self: T)` instead of the `fn(self)` - Andreas felt it looked "sloppy" without the proper signatures :). So again:

``` nimrod
import math

# Dollars and Kgs
type
  Dollar* = distinct float
  Kg* = distinct float

proc `$`*(x: Dollar) :string =
  $x.float

proc `==`*(x, y: Dollar) :bool {.borrow.}


# Fruit class, procs are generic
type
  Fruit* = ref object of RootObj
    origin*: string
    price*: Dollar

# Default reduction is 0
proc reduction*[T](self: T) :Dollar =
  Dollar(0)

# This one factored out from calcPrice
# so that subclasses can "super" call it.
proc basePrice[T](self: T): Dollar =
  Dollar(round(self.price.float * 100)/100 - self.reduction().float)

# Default implementation, if you don't override.
proc calcPrice*[T](self: T) :Dollar =
  self.basePrice()


# Banana class, relies on inherited calcPrice()
type
  Banana* = ref object of Fruit
    size*: int

proc reduction*(self: Banana): Dollar =
  Dollar(9)


# Pumpkin, overrides calcPrice() and calls basePrice()
type
  Pumpkin* = ref object of Fruit
    weight*: Kg

proc reduction*(self: Pumpkin): Dollar =
  Dollar(1)

# Override to multiply super implementation by weight.
# Calling basePrice works because it will not lose type of self so
# when it calls self.reduction() it will resolve properly.
proc calcPrice*(self: Pumpkin) :Dollar =
  Dollar(self.basePrice().float * self.weight.float)


# BigPumpkin, overrides calcPrice() without super call
# No reduction.
type
  BigPumpkin* = ref object of Pumpkin

proc calcPrice*(self: BigPumpkin) :Dollar =
  Dollar(1000)


# Construction procs
proc newPumpkin*(weight, origin, price): Pumpkin = Pumpkin(weight: weight, origin: origin, price: price)
proc newBanana*(size, origin, price): Banana = Banana(size: size, origin: origin, price: price)
proc newBigPumpkin*(weight, origin, price): BigPumpkin = BigPumpkin(weight: weight, origin: origin, price: price)
```

Now... the same technique is used to solve the "super call" problem: **Just factor out the code under a different method/proc name that you can call from the subclasses**. If you are hell bent on using only procs - then the generics are important in that factored out method, otherwise subsequent calls to self will not resolve "properly".

Discussing this today with Andreas he made a good point - _you can use procs for private behaviors, and methods for public ones_.

Its easier to get procs to bind statically properly for private behaviors. Because then you know all the callsites, they are in this module. So in this example, you can easily make `basePrice()` a proc since its private. The public protocol is better to keep as methods, since we don't have control over those callsites and the types of the variables being passed. And as you will see later in this article, it will become apparent immediately.

## Andreas and static_call to the rescue
The technique with factoring out to enable "super calls" will **not be needed in the future**. Andreas aims to add the so called `static_call` mechanism that you can use to "select" which method you wish to call.

**UPDATE: See (part IV)[2014/11/30/nim-and-oo-part-iv] about this.**

Today you can select any proc by using type conversion, so if you want to call the `myProc` that takes an `A` when you have a `b: B`  in your hand, you just do `myProc(A(b))`. But methods don't rely on static typing - they resolve based on the **runtime type** of the objects, so this technique currently only works for selecting among overloaded **procs**, not methods.

The idea is that using `static_call myMethod(A(b))` in front of the method call will cause Nim to use the **static types of the callsite** to resolve the proper method instead of the runtime types. So the name `static` implies static resolution instead of dynamic which is how methods usually do it.

This `static_call` makes it very clear what method you are calling and IMHO this indeed sounds much more explicit than the "call the next method"-approach that many other languages (CLOS, Dylan, Julia) seem to use. I guess those other languages strive to not "hard wire" the selection to specific types, thus preserving the "super style" that adapts to inheritance refactorings, but... it still seems a bit too automagic-gotcha-there-buddy.

## Performance
I devised a silly benchmark creating 5 million of each Bananas, Pumpkins and BigPumpkins in a single `seq[Fruit]`, and also 5 million of each in separate `seq` typed for each kind. And then looping over these collections and calculating the total price, and doing it 10 times over just to get more proper numbers.

If you have a heterogenous collection with proc based objects - then you need to do "manual type testing" code using `of` in order to know what to call:

``` nimrod
# Loop over fruits, darnit! Need to do type check and conversion
for f in fruits:
  if f of Banana:
    total += Banana(f).calcPrice.float
  # Note that you need to check for BigPumpkin first! `of` is true for all subtypes.
  elif f of BigPumpkin:
    total += BigPumpkin(f).calcPrice.float
  elif f of Pumpkin:
    total += Pumpkin(f).calcPrice.float
```

...which you don't need to do if you have the methods based objects of course. Speed? It turns out the manual checking above is around 10% slower than the automatic resolution done by Nim when you use methods. Neat.

But the penalty for methods can be seen for the homogenous collections - those loops run **about 2x faster for procs with static binding**. A factor of two sounds big, but in fact - that's a **very impressively small number I think**! For pure static code the compiler can do lots of funky optimizations

Below is the code used for benching the methods based code, the code for procs/generis is just the same but with the above test-type-and-convert code added in the fruits loop: 

``` nimrod
import fruitmethod, math, future

# Create LOTS of fruit in a heterogenous seq, sum up their costs.
# Also create three separate seqs, and sum up, to be fair comparing with procs.

# Util to measure time
import times, os 
template time(s: stmt): expr =
  let t0 = cpuTime()
  s
  cpuTime() - t0


# A heterogenous seq collection typed as Fruit
var fruits = newSeq[Fruit]()

# And some homogenous
var bananas = newSeq[Banana]()
var pumpkins = newSeq[Pumpkin]()
var bigPumpkins = newSeq[BigPumpkin]()

# Fill em up
for i in 1..5000000:
  fruits.add(newBanana(size = 0, origin = "Liberia", price = 20.00222.Dollar))
  fruits.add(newPumpkin(weight = 5.2.Kg, origin = "Africa", price = 10.00111.Dollar))
  fruits.add(newBigPumpkin(weight = 15.Kg, origin = "Africa", price = 10.Dollar))
  bananas.add(newBanana(size = 0, origin = "Liberia", price = 20.00222.Dollar))
  pumpkins.add(newPumpkin(weight = 5.2.Kg, origin = "Africa", price = 10.00111.Dollar))
  bigPumpkins.add(newBigPumpkin(weight = 15.Kg, origin = "Africa", price = 10.Dollar))


var total: float = 0

proc calcTenTimes() =
  for i in 1..10:
    # Loop over fruits, our classes use methods so we do not need to cast
    # f from Fruit to specific types.
    for f in fruits:
      total += f.calcPrice.float

proc calcTenTimesSame() =
  for i in 1..10:
    total = 0
    for f in bananas:
      total += f.calcPrice.float
    for f in pumpkins:
      total += f.calcPrice.float
    for f in bigPumpkins:
      total += f.calcPrice.float


echo "Time for calc: " & $time(calcTenTimes())
echo "Time for calc same: " & $time(calcTenTimesSame())
```

Running it:

``` bash
time ./shopmethod 
Time for calc: 1.591322
Time for calc same: 3.068159000000001

real	0m8.342s
user	0m7.163s
sys	0m1.106s
```

## Conclusion

First of all, **damn Nim is fast**! Creating 30 million objects, in a few collections dynamically growing. Then looping 10 times over them calling `calcPrice()` about 300 million times? And it all takes about 8 seconds? I am impressed.

Secondly, the penalty for methods is in fact very small - but if you happen to have code that indeed does millions of calls in a tight loop - sure, procs will be faster of course. But my guess is that for the majority of real code - the difference will not even be noticed.

Andreas also told me that method lookup is indeed pretty optimized, and can be faster than in C++ even. So I will **use methods with my objects, especially for the public behaviors** - and just be happy.

Finally, why are methods not used in the stdlibs? Quoting Andreas: _"The major reason why we don't use methods in the stdlib is that they don't play well with the effect system and our dead code elimination optimization."_

Of course. Remember, Nim is meant to be usable for system level programming. So having the stdlibs be "fully static" in nature is important.

Go Nim!

---
title: Nim and super
date: '2015-05-06'
slug: nim-and-super
categories:
- Nim
- Nimrod
- OOP
- Object orientation
- Languages
- Programming
---
As I described in [the](/2014/10/29/nim-and-oo) [earlier](/2014/10/31/nim-and-oo-part-ii) [posts](/2014/10/31/nim-and-oo-part-iii) Nim didn't support "super calls" when using **methods** instead of statically bound **procs and generics**. My article caused a little bit of discussion around this on IRC and Andreas decided to implement the mechanism he already had planned - but had not fully decided a good name for.

The other day Nim 0.11.2 [was released](http://nim-lang.org/news.html#Z2015-05-04-version-0-11-2-released) and it includes this mechanism. Let's have a look how it works in my sample code...

<!--more--> 

Instead of calling it `static_call` - implying that the call resolution is made at compile time **statically**, the name ended up as `procCall` - implying the call resolution is simply done just like its done for procs. Same, same - different words. To put it another way, **even though we are calling a method, let the static types of the arguments decide which method to call, not the actual runtime types**.

A bit of repetition from the earlier articles - today you can select among overloaded procs to call by using type conversion, so if you want to call `myProc` that takes an argument of type `A` when you have an object of type `B` in your hand (`B` being a sub type of `A`), you just do `myProc(A(b))`.

This is called a [type conversion](http://nimrod-lang.org/manual.html#type-conversions) and can be viewed as a type safe cast, it only works if its safe to do it. Nim also has `cast` but generally its something you should only use if you know what the heck you are doing. :)

Now... methods don't rely on static typing - they resolve based on the **actual runtime type** of the objects - that's their whole reason for existing and this is essential in supporting more complex OO code. So the type conversion technique in itself only works for selecting among overloaded **procs**, not methods.

But now, with the addition of `procCall` we can call overloaded methods using the exact same technique. Our Fruit code from earlier articles can now be simplified - we no longer need to factor out the base implementation of `calcPrice` as a method under a different name `basePrice`. And it still works as intended, here is the updated code:

``` nimrod Fruit library using methods and procCall
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

method `$`*(self: Fruit): string =
  self.origin & " " & $self.price

method reduction(self: Fruit) :Dollar =
  Dollar(0)


method calcPrice*(self: Fruit): Dollar =
  Dollar(round(self.price.float * 100)/100 - self.reduction().float)


# Banana class
type
  Banana* = ref object of Fruit
    size*: int

method reduction(self: Banana): Dollar =
  Dollar(9)

method calcPrice*(self: Banana): Dollar =
  procCall Fruit(self).calcPrice()

# Pumpkin
type
  Pumpkin* = ref object of Fruit
    weight*: Kg

method reduction(self: Pumpkin): Dollar =
  Dollar(1)

method calcPrice*(self: Pumpkin) :Dollar =
  Dollar(procCall(Fruit(self).calcPrice()).float * self.weight.float)


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

As we can see the "syntactic style" can vary as usual, in **line 40** we can use procCall without parenthesis, but on **line 51** we need to use it in a "calling style" in order for precedence to work out.

So... one may wonder, why not just have something like `super` as in Smalltalk or Java etc? The reason is quite simple, Nim supports multiple dispatch - in other words in Nim we can dispatch based on the types of several of the arguments, as long as they are objects. There is no specific argument in the method call that is privileged as "self", we just tend to use the first argument by convention as "the receiver". This also means that "super" has no reasonable meaning in Nim, super of who?

The type conversions you would use together with `procCall` does spell out the "super type" explicitly (in our example above - "Fruit"), thus making it very clear which method you want to call. A puritan would possibly claim that it "couples" the class with its superclass too much (compared to the more abstract uncoupled "super"). But I think this explicit style fits the Nim mindset better - and even if this makes changing superclasses a bit more tedious (you need to hunt down procCalls and fix the type conversions) - its nothing that some future refactoring tools couldn't easily fix, and changing superclasses isn't what you do every minute anyway.

One could also argue that the **intention of the programmer** is slightly lost with this style. It doesn't obviously read as "call the super implementation", and I suspect we may find coders using this also throwing in a small comment stating that *hey, this is a super call*.

The mechanism also enables "super super" since you can explicitly skip over intermediate classes which of course is generally bad style, but at the same time, explicitness follows the principle of least surprise :)

## Calling overloads on self

Another scenario we easily could have is a class with several overloads of a method `foo` in which one or many of them wants to call the "primary" implementation of the behavior. This is in fact technically the same scenario as the "super call", and would be solved the same way - its just an example of multiple dispatch where we are dispatching on more than the first argument. Let's say we have a Foo class which holds a seq of fruit names, for some ... odd reason. And we want to be able to add fruit names to it by sending in various different objects, well, a Fruit obviously, but also collection of Fruits etc.

``` nimrod
import fruitmethod

# Foo class
type
  Foo* = ref object of RootObj
    fruits*: seq[string]

# The core method we want to call
method add(self: Foo, fruit: Fruit) =
  echo "   ...and here we actually add it"
  self.fruits.add($fruit)

method add(self: Foo, banana: Banana) =
  echo "Adding a Banana"
  procCall self.add(Fruit(banana))

method add(self: Foo, pumpkin: Pumpkin) =
  echo "Adding a Pumpkin"
  procCall self.add(Fruit(pumpkin))

method add(self: Foo, fruits: seq[Fruit]) =
  echo "Adding a bunch of Fruit"
  for f in fruits:
    self.add(f)

# This is a constructor proc that is normally used to initialize objects
proc newFoo(): Foo =
  result = Foo(fruits: newSeq[string]())

when isMainModule:
  # Get us a Foo
  var foo = newFoo()
  
  # Add a single Banana
  foo.add(newBanana(size = 0, origin = "Liberia", price = 20.Dollar))
  
  # Create a seq of Fruit
  var s = newSeq[Fruit]()
  var b = newBanana(size = 0, origin = "Liberia", price = 20.00222.Dollar)
  var p = newPumpkin(weight = 5.2.Kg, origin = "Africa", price = 10.00111.Dollar)
  s.add(b)
  s.add(p)
  
  # Add them all, this will first call the method for a seq of Fruit,
  # and that method will in turn call the one for Banana and the one for Pumpkin
  # and those in turn will use procCall to call the primary method for Fruit.
  foo.add(s)
```

As we can see above we need to use `procCall` on **line 15 and 19** in order to be able to call the `add` method that takes a Fruit from the other `add` methods. So yes, **this is not only useful for doing classic super calls**.

## Conclusion

The mechanism `procCall` solves the super call problem with methods, and it also solves similar use cases along the way. As far as I can tell this removes the last "hurdle" for being able to do serious OO coding in Nim.

Go Nim!

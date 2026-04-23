---
title: Nim and OO, Part II
date: '2014-10-31'
slug: nim-and-oo-part-ii
categories:
- Nim
- Nimrod
- OOP
- Object orientation
- Languages
- Programming
- Generics
---
In the [previous article](/2014/10/29/nim-and-oo) when I explored OO mechanisms in [Nim](http://nim-lang.org) I felt I dropped the ball a bit in my Fruit example. This is a followup.

In that article we first implemented some Fruit "classes" mixing methods and procs. Then I presented a cleaned up version using methods only, and a teeny template in order to reuse a base method. This template was needed since Nim currently doesn't have a "call-next-method-matching" for multimethods like Dylan or CLOS have. This is being discussed and I think all agree that there needs to be **some** mechanism so that you can call a "next lesser match" of all matching multimethods.

But I also wrote that the example **can be written perfectly well using generics and procs only**, thus ensuring static binding and maximum speed. But the "super call" problem also existed for procs, and the template hack was just a hack. After more experimentation I now **think I found the proper Nim way** to do this so let's take a look...

<!--more--> 

## Generics

In Nim we can use generics to "generate" multiple "instances" of procs, for all different combinations of static types being used to call this proc. To be precise, the compiler doesn't necessarily need to generate multiple copies, it can deal with it using a simple case switch on types, or whatever - but its a reasonable mental model of what happens. Another mental model is that a generic proc, **as long as your shit compiles**, will be run with the types of the arguments at the given callsite. :)

So if we have a proc declared as `proc calcPrice(self): Dollar` with **no type specified** for `self` then Nim will consider that to be the same as `proc calcPrice[T](self: T): Dollar` and collect all callsites and for each unique static type of `self` being passed in, it will generate a matching `calcPrice` proc. Presumably writing all these procs manually **would result in equivalent code**.

This is how my final fairly nice generic variant of the Fruit library looks like:

``` nimrod
import math

# Dollars and Kgs
type
  Dollar* = distinct float
  Kg* = distinct float

proc `$`*(x: Dollar) :string =
  $x.float

proc `==`*(x, y: Dollar) :bool {.borrow.}


# Fruit class, all procs for Fruit are generic
type
  Fruit* = ref object of RootObj
    origin*: string
    price*: Dollar

# Default reduction is 0
proc reduction*(self) :Dollar =
  Dollar(0)

# This one factored out from calcPrice below
# so that subclasses can "super" call it.
proc basePrice*(self): Dollar =
  Dollar(round(self.price.float * 100)/100 - self.reduction().float)

# Default implementation, if you don't override.
proc calcPrice*(self) :Dollar =
  self.basePrice()


# Banana class, relies on inherited calcPrice()
type
  Banana* = ref object of Fruit
    size*: int
    
# Overrides reduction though.
proc reduction*(self: Banana): Dollar =
  Dollar(9)


# Pumpkin, overrides calcPrice() and makes a "super call" by calling basePrice()
type
  Pumpkin* = ref object of Fruit
    weight*: Kg

# Also overrides reduction.
proc reduction*(self: Pumpkin): Dollar =
  Dollar(1)

# Override to multiply super implementation by weight.
# Calling basePrice works because it will not lose type of self so
# when basePrice() calls self.reduction() it will resolve properly.
proc calcPrice*(self: Pumpkin) :Dollar =
  Dollar(self.basePrice().float * self.weight.float)


# BigPumpkin, overrides calcPrice() without super call
# No override of reduction.
type
  BigPumpkin* = ref object of Pumpkin

method calcPrice*(self: BigPumpkin) :Dollar =
  Dollar(1000)


# Construction procs, this encapsulates our structure of the objects in this module.
proc newPumpkin*(weight, origin, price): Pumpkin = Pumpkin(weight: weight, origin: origin, price: price)
proc newBanana*(size, origin, price): Banana = Banana(size: size, origin: origin, price: price)
proc newBigPumpkin*(weight, origin, price): BigPumpkin = BigPumpkin(weight: weight, origin: origin, price: price)
```

Okidoki. Before I came up with the above code which looks quite simple - I experimented with a composition style using delegation instead of inheritance, and used generics too. It did work, but it got quite messy. The above solution on the other hand feels like a simple pattern one can use to solve this "super call" issue. Now... _what was the problem again? :)_

**Problem:** When you only use procs and overload them to give implementations of `calcPrice()` for Banana, Pumpkin and BigPumpkin - and also a base default implementation in the base class Fruit - then **you can't call the one in Fruit from any of the others**. In other words, you can't make a "super call", just try it and watch the infinite recursion!

We could in theory use the type Fruit for self in the base implementation (and not a generic `self`), and use a type conversion of self like `Fruit(self).calcPrice()` to be able to call it - but then you will be running the `calcPrice()` in Fruit with **self as being a Fruit!** And that's no good, because when it subsequently calls `self.reduction()` **it will not resolve to the proper proc**, it will only resolve to the base implementation in Fruit. So forget using abstract types as types for the self argument in base implementations of procs, it is a BAD idea.

**Solution:** We can factor out the base implementation of `calcPrice()` under another name, like `basePrice()`. Then we can easily call it from the subclasses. And the default implementation of `calcPrice()` in Fruit will just call `basePrice()`. And this is important: we use generic `self` for the proc arguments in the Fruit class, so that we don't lose type information when we call those procs.


And here is the test code to see it works as it should:

``` nimrod
import fruit

# Create some objects using proper encapsulated construction procs 
var p = newPumpkin(weight = 5.2.Kg, origin = "Africa", price = 10.00111.Dollar)
var b = newBanana(size = 0, origin = "Liberia", price = 20.00222.Dollar)
var bp = newBigPumpkin(weight = 15.Kg, origin = "Africa", price = 10.Dollar)

# Check correct pricing
assert(b.calcPrice() == 11.0.Dollar)
assert(p.calcPrice() == (9*5.2).Dollar)
assert(bp.calcPrice() == 1000.Dollar)

proc testing(x) :Dollar =
  result = x.calcPrice()
  echo($result)

# Check correct pricing when called via a proc with generic type
assert(testing(b) == 11.Dollar)
assert(testing(p) == (9*5.2).Dollar)
assert(testing(bp) == 1000.Dollar)

echo "All good."
```

## Conclusion

How to use generics in Nim for someone like me who haven't used generics in a loooong time, is a bit of a head twister. But after a few hours of messing, it starts to click.

The only "issue" above I guess - is the fact that the default `calcPrice()` makes an extra call to `basePrice()` (but only the default, so only for Bananas) so a few cycles lost there unless Nim optimizes it away. Something that a template probably could solve of course. :)

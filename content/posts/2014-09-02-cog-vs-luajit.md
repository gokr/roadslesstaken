---
title: Cog vs LuaJIT2
date: '2014-10-13'
slug: cog-vs-luajit
categories:
- Pharo
- Smalltalk
- Squeak
- Lua
- LuaJIT
---
In the open source Smalltalk community we have a **pretty fast** VM these days - its called [Cog](http://www.mirandabanda.org/cog/) and is written by the highly gifted and experienced [Eliot Miranda](http://www.mirandabanda.org/cogblog/microbio/) who also happens to be a really nice guy! Cog is fast and its also still improving with some more developers joining recently.

Another **very fast** VM is [LuaJIT2](http://luajit.org) for the [Lua](http://www.lua.org) language (version 5.1), also written by a single individual with extraordinary programming talent - Mike Pall. LuaJIT2 is often mentioned as the **fastest dynamically typed language** (or VM) and even though Lua is similar to Smalltalk (well, its actually very similar to Javascript) its also clearly a different beast with other characteristics. If you start looking at the world of game development - then Lua appears **everywhere**.

<!--more--> 

I am a language lover but I admit to having only glanced at Lua earlier and wrongfully dismissed it in the category of "less capable and quirky languages". Now that I have looked closer I realize its a similar "hidden gem" as Smalltalk is! And just as Smalltalk was given a boost of interest when Ruby hit the scene - I guess Lua gets an influx now with the Javascript craze. And the gaming world keeps infusing it with fresh code.

## Lies and, well basically just lies...

In Squeak Smalltalk we have this silly little benchmark called **tinyBenchmarks**. It's not for benchmarking. No, let me repeat that - **it really is not**.

But hey, **let's just ignore that** for a second. :) And oh, comparing Lua vs Smalltalk - speed is only a tiny piece of the picture - there are other much more interesting characteristics of these two eco systems that would affect any kind of "choice":

* Smalltalk implementations typically have live reflective rich IDEs, and excel at complex domain models and interactive explorative development. And very clean late bound OO. Not so good at "playing well with others" though.
* Lua, and especially LuaJIT, is extremely good at playing with others - and specifically the C/C++ eco system. As a more traditional scripting language you have more choices in IDEs and SCM tools etc, but it is not as interactive and exploring as Smalltalk and is not focused at OO specifically, although it can do it pretty good. It does however have several good IDEs, but hardly anything matching a Smalltalk IDE.

So Smalltalk excels in interactive development - but you are often limited in integration options... while Lua excels as a dynamic language thriving as a catalyst in the C and C++ eco system.

These languages and their tools were simply born from two very different sets of goals. And Lua is also different from say Python, since Lua in contrast was **designed as a minimal language** (in many ways like Smalltalk was) and a language **meant for embedding** in a C/C++ application (almost no batteries included). This carves out a fairly unique niche for Lua.

Ok, so back to tinyBenchmarks. It consists of two small snippets of code, one measures "bytecode speed" by counting primes in a few nested loops and another is a recursive function similar to Fibonacci that just counts the number of recursive calls. Ok, so... latest Cog (binary VM.r3000) vs latest LuaJIT2 (2.1.0-alpha), here follows the Lua code I whipped up. I tried basically three different variants on the Fibonacci recursion to see how much penalty an OO design would give.

```lua
local class = require("classy")

-- First here is how you would do it in proper Lua, just a recursive function
local function benchFib(fib)
  if fib < 2 then
    return 1
  end
  return 1 + benchFib(fib-1) + benchFib(fib-2)
end

-- Or using a metatable for a bit more manual OO style
local Bench = {}
Bench.__index = Bench

-- A constructor
function Bench.new()
  local bench = {}
  setmetatable(bench, Bench)
  return bench
end

-- And a method in it
function Bench:benchFib(fib)
  if fib < 2 then
    return 1
  end
  return self:benchFib(fib-1) + self:benchFib(fib-2) + 1
end

-- A variant using the "Classy" OO lib. Another popular is called "MiddleClass"
local Benchy = class("Benchy")

-- And a method in it
function Benchy:benchFib(fib)
  if fib < 2 then
    return 1
  end
  return self:benchFib(fib-1) + self:benchFib(fib-2) + 1
end


-- And this is the bytecode benchmark translated just as it says in Squeak
local function benchmark(n)
  local size = 8190
  local count = 0
  for j=1,n do
    count = 0
    local flags = {}
    for q=1,size do
      flags[q] = true
    end
    for i=1,size do
      if flags[i] then
        local prime = i+1
        local k = i + prime
        while k <= size do
          flags[k] = false
          k = k + prime
        end
        count = count + 1
      end
    end
  end
  return count
end

-- Return seconds to run fn
local function timeToRun(fn)
  local start = os.clock()
  fn()
  return os.clock() - start
end


t1 = timeToRun(function() benchmark(100000) end)
t2 = timeToRun(function() benchFib(47) end)
t3 = timeToRun(function() Bench.new():benchFib(47) end)
t4 = timeToRun(function() Benchy():benchFib(47) end)

print(t1 .. ' bytecode secs')
print(t2 .. ' benchFib send secs (normal Lua)')
print(t3 .. ' Bench send secs (OO Lua)')
print(t4 .. ' Benchy send secs (OO Lua Classy)')
```


And the Smalltalk code would be:

```smalltalk
Transcript show: ([100000 benchmark] timeToRun / 1000.0) asString, ' bytecode secs';cr.
Transcript show: ([47 benchFib] timeToRun / 1000.0) asString, ' send secs';cr@
```

I picked 100000 and 47 to get fairly long running times, so LuaJIT:

	10.248302 bytecode secs
	26.765077 benchFib send secs (normal Lua)
	70.418739 Bench send secs (OO Lua)
	71.003568 Benchy send secs (OO Lua Classy)

...and Cog:

	49.606 bytecode secs
	58.224 send secs

**So LuaJIT2 is about 4x faster on bytecode speed and 2x faster on recursive calls.**

But wait, lots of things to note here:

* These are two trivial benchmarks meant to detect really bad regressions in VM code, not benchmarking.
* The above. Read it again.
* A recursive function call in Lua is not the same thing as a message send with full OO lookup in Cog. If we look at Bench and Benchy we see that 2x factor vanish!
* Integer math is clearly different in Lua vs Smalltalk. Lua does doubles only, Smalltalk has a full math system falling back to "big ints" when needed!
* Using Classy was the same speed as manual metatable approach. So in Lua you would definitely use such a lib instead of manual OO, much easier and with nice features.
* And oh, both grabbed a single core by the throat doing this - Cog even managed to squeeze out 104%! :)


## Conclusion

There is no real conclusion from the silly benchmark - it was just a fun exercise! I already knew Cog is pretty darn fast and LuaJIT is the King of the Hill - it even beats V8 regularly. Cog on the other hand is executing a much more refined and advanced language and object system, you really do need to keep that in mind here.

But I hope that especially Smalltalkers might get intrigued by this article and find Lua interesting. To me its much nicer than Javascript. Its also the first time in many years that I have found a language that actually can **keep my interest for a longer period - despite me constantly comparing it with my beloved Smalltalk**.

Python could never keep me interested, although I did try - but it kept turning me off, so unclean, lots of different mechanisms, too complicated. Same story with Ruby, too messy, no elegance and a community drug crazed with nifty tricks... IMHO.

But Lua has that smallness that Smalltalk has, it feels "designed". It has strong abstractions that it carries through all the way. In short it doesn't turn me off. And then, a lot more in this eco system is pure candy. LuaJIT2 has awesome speed. Very powerful interoperability with C and C++, in fact, the LuaJIT FFI can call C libraries **as fast as C can**! Tons of good libraries and tools. Very strong on mobile development. Many interesting projects like TurboLua, Tarantool, OpenResty, Lapis, Metalua etc etc.

Always nice to realize that there still is stuff out there that can attract an old Smalltalk dog... :)

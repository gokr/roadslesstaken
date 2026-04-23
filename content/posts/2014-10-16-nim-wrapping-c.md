---
title: Nim wrapping C
date: '2014-10-16'
slug: nim-wrapping-c
categories:
- Nim
- C
- Nimrod
- Programming
- HyperDex
---
Nim has all the language mechanisms needed to smoothly interoperate with C and C++. The rather [large collection of wrapped C libraries](https://github.com/Araq/Nimrod/tree/devel/lib/wrappers) (and that's only those in the standard libs) is also a testament to this fact. In this article I explain my personal findings testing out the waters of wrapping a simple C library. 

The basic approach to wrapping a simple C library is:

0. Install Nim.
1. Install c2nim using Babel or manually clone c2nim from github and build it.
2. Use c2nim to translate the C header file(s) to a so called Nim wrapper.
3. Make a small test showing it works.
4. Write a so called _"impure"_ intermediary library that uses the wrapper (next article)
5. Make a test green and declare Victory (next article)

Okidoki... (roll up sleeves)

<!--more--> 

## Just do it

I have a thing for new cool NoSQL databases and one of the **coolest bad ass NoSQL databases** that isn't that well known is [HyperDex](http://www.hyperdex.org). HyperDex doesn't have a published "over the wire" protocol - the approach to interface with it is to use their C client library which is very simple in its design so that its easy to wrap in various client languages. They support the usual suspect languages - but of course not Nim. **Bastards! :)**

## 0. Get Nim

Not going into details here, this works for me on Ubuntu:

1. [Get Nim](http://nimrod-lang.org/download.html). I used the source bootstrap at the bottom there, and [wrote about it in excrutiating detail too](http://goran.krampe.se/2014/10/15/bootstrapping-nim).
2. Get Babel (package manager). At the moment Babel is in a bit of flux since Dominik is renaming it to Nimble. But I got a slightly older commit to work:
``` bash Installing Babel
git clone https://github.com/nimrod-code/nimble.git
cd nimble
git checkout 7d18e2be1cdd4043f61918eae4a9877a90a296a4
nimrod c -r src/babel install
```

## 1. Getting c2nim

The trivial way to get c2nim is to use Babel:

`babel install c2nim`

And that's that. :)

Another option is to get [c2nim manually from github](https://github.com/nimrod-code/c2nim), but building it (`nimrod c c2nim`) hit a little snag:

`c2nim.nim(11, 33) Error: cannot open 'llstream'`

...some file searching later I note this is a module that is part of the Nimrod compiler itself. How come its not found? I checked in Babel etc, but no dice. Then I ended up trying out `nimrod dump` (see `nimrod --advanced`) and aha, the paths at the end looks weird, it tries to find `compiler` in `/usr/local/compiler`. I suspect it tries to locate it relative to the nimrod binary as `../compiler` which would work if we hadn't installed nimrod into `/usr/local/bin` and instead would be running it directly from the github clone.

Ok, then - I give up and do as _"the Romans"_ - **don't install Nim but use it directly from the clone by linking it into your path**. So I ran deinstall.sh from the github clone I installed:

  `sudo sh deinstall.sh /usr/local/bin`

...and then linked the nimrod binary into my `PATH`. After this compiling worked just fine. I also learned however that I can add search paths manually, so this also worked:

`nimrod -p:../Nimrod.devel/compiler/ c c2nim`


## 2. Using c2nim

I am no super C guru. Things that are obvious to the other Nimmers may not be for me. So... first of all I had a rather dim view on what c2nim is meant to do - _convert a C file to Nim?_ How will that actually help me make a **wrapper for a C library**?

I looked at some example wrappers, you can find them in `lib/wrappers` like say `lib/wrappers/sqlite3.nim` and from my googling I suspected these have been created using c2nim. Things to note in the sqlite3 example:

* Most wrappers tend to use dead code elimination - deadCodeElim pragma, I guess it works fine for this kind of Nim module (it turns out c2nim adds this pragma on its own when we use the `dynlib` pragma)
* There is a little `when`-section in the beginning. This is compile time logic, which is neat. The pattern used in the string for the library .so name is [specific for the dynlib pragma](http://nimrod-lang.org/manual.html#dynlib-pragma-for-import).
* Each proc has some pragmas associated `{.cdecl, dynlib: Lib, importc: "sqlite3_last_insert_rowid".}` that makes it tick.

Ok, time to dance. First I copied the header file I wanted to use to my c2nim directory, since I probably will need to adjust/clean it. But when I first just naively ran `c2nim hyperclient.h` I didn't get that `when`-section nor any pragmas attached to the proc declarations. It did quite fine translating typedefs, structs, enums etc to the Nim equivalents though. 

What does the [c2nim manual say](http://nimrod-lang.org/c2nim.html)? Hmmm, still not obviously clear to me - especially how the pragmas are meant to be used. But my understanding so far is that:

* We need `cdecl` so that the proc uses C convention for calls.
* We need `dynlib: Lib` (where Lib is the string var for the library name from the `when`-section) so that this proc actually maps into that library.
* We need the `importc: "blablabla"` pragma to actually map the proc to the proper function in the library.

Since reading manuals sometimes is not my strongest side I started trying it out using the options to c2nim, and came up with this incantation that actually seemed to do the right things:

`./c2nim --prefix:hyperclient_ --dynlib:libname --cdecl hyperclient.h --out:hyperclient.nim`

Running `c2nim --help` got me guessing these and yes it works, but I still have to add the `when`-section manually, hrm. But reading some more [the manual reveals](http://nimrod-lang.org/c2nim.html#dynlib-directive) how this can be **added in the header file instead**, so I edited the hyperdexclient.h accordingly:

* Removed some includes, they aren't used by c2nim anyway.
* Added a when section using `#ifdef C2NIM` as described in the manual section linked above, see below how it looks.
* Added my pragma options to the same section (dynlib, cdecl, prefix)
* Copied the contents of hyperdex.h into hyperdexclient.h, it was included using `#include` and it only contains some simple stuff so simpler to have a single header file.

A clever reader realizes that the above steps could be automated of course, perhaps in Nim! :) The section at the top now looks like:

```c
#ifdef C2NIM
#  dynlib libname
#  cdecl
#  prefix hyperclient_
#  if defined(windows)
#    define libname "libhyperclient.dll"
#  elif defined(macosx)
#    define libname "libhyperclient.dylib"
#  else
#    define libname "libhyperclient.so"
#  endif
#endif
```

So now we can simply run `./c2nim hyperdexclient.h` and it will produce a `hyperdexclient.nim` with the proper Nim stuff:

``` nimrod hyperdexclient.nim
 {.deadCodeElim: on.}
when defined(windows):
  const 
    libname* = "libhyperclient.dll"
elif defined(macosx): 
  const 
    libname* = "libhyperclient.dylib"
else: 
  const 
    libname* = "libhyperclient.so"
```

...and here we note the sudden appearance of deadCodeElim. If we peek in c2nim we find that it adds it **if we use dynlib pragma**.
Looking further down we can see how the pragmas got inserted into the proc declarations:

``` nimrod hyperdexclient.nim
proc create*(coordinator: cstring; port: uint16_t): ptr hyperclient {.cdecl, 
    importc: "hyperclient_create", dynlib: libname.}
```

I defined the cdecl calling convention since its the standard on Linux and most C compilers, I guess its what 99% of all wrappers use? And the above proc gets mapped to the `hyperclient_create` function in the library (note how we have stripped the `hyperclient_` prefix, since all these functions use it) and we point to the dynamically loaded library **named by the libname variable**.

Its damn funky and perhaps confusing to newbies that Nim has **compile time execution (macros etc) in Nim** and not some other inferior stupid language like the C preprocessor. Of course, as a Smalltalker its the _Obvious Right Thing_.

But... actually **compiling** this file BARFS:

``` bash Error...
/home/gokr/nim/c2nim/hyper/hyperclient.nim(108, 41) Error: undeclared identifier: 'uint16_t'
```

Mmmm, right. So c2nim didn't convert those guys, they are in an include called `<stdint.h>`. Google to the rescue, oh, so in the [zmq4 wrapper](https://github.com/idlewan/nawak/blob/master/lib/zmq4.nim) it was fixed like this:

``` nimrod int types
type
    size_t* = uint
    uint16_t = uint16
    int32t = int32
    uint8_t = uint8
```
So I did the same:

``` nimrod int types
type
  uint16_t = uint16
  uint64_t = uint64
  int64_t = int64
```
And then **it builds fine** :). But this requires manual editing of the nim file after running c2nim. Perhaps we can do something in the header file? It turns out we can, Araq mentions on IRC that we can use `#mangle` as described in the manual page (duh...):

```c
#ifdef C2NIM
#  dynlib libname
#  cdecl
#  prefix hyperclient_
#  if defined(windows)
#    define libname "libhyperclient.dll"
#  elif defined(macosx)
#    define libname "libhyperclient.dylib"
#  else
#    define libname "libhyperclient.so"
#  endif
#mangle uint16_t uint16
#mangle uint64_t uint64
#mangle int64_t int64
#endif
```

This will lead to a **search-and-replace-all on these matching tokens**, but that seems fine for these types. And yup, that works and makes it all cleaner. Wrapper done (we think).

## Does the Damn Thing Work?

Yup, it sure seems so! I am on Ubuntu 14.04 and [installing HyperDex](http://hyperdex.org/download/) and firing it up (see [Quick start](http://hyperdex.org/doc/latest/QuickStart/), one coordinator and one daemon is fine) is fairly easy, follow directions on the homepage and you should be golden (although I had to hunt down a deb for libcityhash, weird).

Then... I took the [C example from HyperDex](http://hyperdex.org/doc/latest/CAPI/#sec:api:c:client:helloworld) and translated it into Nim, so it **sure looks like crap** (well, like C in Nim clothing) but I just wanted to see if the wrapper actually works:

``` nimrod test.nim
import hyperclient

# First trivial low level test of the hyperclient.nim wrapper
# This is basically Nim as C code.

var
  client: ptr hyperclient
  attr: attribute
  attrs: ptr attribute
  op_status, loop_status: returncode
  op_id, loop_id: int64 = 0
  attrs_sz, i: csize

# Get us a client
client = create("127.0.0.1", 1982)
echo("HyperDex client created.")

# A value to stuff in at key "some key"
attr.attr = "v"
attr.value = "Hello World!"
attr.value_sz = attr.value.len
attr.datatype = HYPERDATATYPE_STRING

# Perform the "put" stuffing "Hello World!" at "some key" in space "kv"
# Nim is friendly and can take string as cstring
op_id = put(client, "kv", "some key", 8, addr attr, 1, addr op_status)

# Wait for it to complete
loop_id = loop(client, -1, addr loop_status)
# Do at least a minimal error check, this will for example catch if you 
# missed adding the space in Hyperdex.
if op_status != HYPERCLIENT_SUCCESS:
  quit("Error: " & $op_status)

echo("Put \"some key\" = \"Hello World!\", done.")

# Perform the "get" populating attrs
op_id = get(client, "kv", "some key", 8, addr op_status, addr attrs, addr attrs_sz)

# Wait for it to complete
loop_id = loop(client, -1, addr loop_status)
if op_status != HYPERCLIENT_SUCCESS:
  quit("Error: " & $op_status)

# A little helper to do pointer arithmetics, borrowed from:
#   https://github.com/fowlmouth/nimlibs/blob/master/fowltek/pointer_arithm.nim
proc offset[A](some: ptr A; b: int): ptr A =
  result = cast[ptr A](cast[int](some) + (b * sizeof(A)))

# Another helper to make a string from a NON null terminated cstring with a length.
proc `$`(x: cstring, len: int): string =
  result = newString(len)
  copyMem(addr(result[0]), x, len)

# Loop over attrs we got back, print out
for i in 0.. <attrs_sz:
  var a = offset(attrs, i)
  echo("Get \"some key\" gave back \"" & (a.value $ a.value_sz) & "\", done.")

# Clean up
destroy_attrs(attrs, attrs_sz)
destroy(client)

# Declare success, get coffee.
echo("All done, Nim rocks.")
```

Some comments that might help:

* `addr` returns the address of an l-value, [see manual](http://nimrod-lang.org/manual.html#the-addr-operator). Useful with C libraries. Kinda the opposite of `ptr`.
* HyperDex has an **asynchronous** client library, that's why we need to call loop() for operations to actually be performed and we get an op_id returned to keep track of each operation. In this example its trivial.
* The `offset` proc allows us to do pointer arithmetics so we can loop over the attributes returned from the get operation. It can be [further refined of course](https://github.com/fowlmouth/nimlibs/blob/master/fowltek/pointer_arithm.nim).
* The `$` operator is the Nim polymorphic "turn this to a string"-operator. In this case it turned out there was no such proc for non null terminated C strings (where you instead have a length). But Araq trivially solved that and since it now takes two arguments it can be invoked in an infix fashion `(a.value $ a.value_sz)` (see line 58). This may look... foreign but its already used in someplace in the stdlib, forgot where. 

Let's try it. First we create a trivial space in HyperDex called "kv" with key "k" and attribute "v", paste and run in bash:

``` bash Create space in HyperDex
hyperdex add-space -h 127.0.0.1 -p 1982 << EOF
     space kv key k attribute v
EOF
```
Then build test.nim with `nimrod c test.nim`. On my laptop I get a **177kb executable built in 0.9 seconds**. Then we try to run it:

``` nimrod Nim calling HyperDex, come in HyperDex...
gokr@yoda:~/nim/c2nim$ time ./test
HyperDex client created.
Put "some key" = "Hello World!", done.
Get "some key" gave back "Hello World!", done.
All done, Nim rocks.

real	0m0.005s
user	0m0.002s
sys	0m0.002s
```

Phew.


## Conclusion

The wrapping process was quite simple, but a HOWTO like this article would have been great to have! Now perhaps others can go starting wrapping stuff, the C eco system out there is HUGE and IMHO this is one of Nim's big selling points, and one of the primary reasons I am investigating Nim.

There will be a followup article on how to make the intermediate layer applying _"Nimiomatics"_ or _"Nidiomatics"_ (=idiomatics in Nim), but it might take me a while to get there.

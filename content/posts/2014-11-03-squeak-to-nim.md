---
title: Squeak to Nim, come in Nim...
date: '2014-11-03'
slug: squeak-to-nim
categories:
- Nim
- Nimrod
- Squeak
- Pharo
- Smalltalk
- Languages
- Programming
---
In my exploration of [Nim](http://nim-lang.org) the turn has come to see how we can use Nim together with [Squeak](http://squeak.org).

Squeak (and Pharo) has two basic mechanisms of interfacing with the C world:

* [Squeak VM plugins](http://stephane.ducasse.free.fr/FreeBooks/CollectiveNBlueBook/greenberg.pdf). That pdf is old, but still fairly accurate I guess.
* [Squeak FFI](http://wiki.squeak.org/squeak/1414), Foreign Function Interface.

The VM plugins are basically a controlled way to introduce new "named" primitives in Smalltalk that can be invoked from Smalltalk. A plugin can be built either linked into the VM binary (statically) or as a dynamically loaded library (dll, so, dylib etc). When "all else fails" a plugin is the way to go, but they are a bit awkward to work with.

Then we have the FFI which is a generic way to dynamically call dynamically loaded libraries. In other words, no compilation step needed - just type the correct Smalltalk line and the library will load and the calls work. Now... sure, the FFI mechanism is a bit slower, since it needs to look at arguments and make the proper type conversions for the call. But the FFI is heavily used in the commercial Terf system, in fact, all the OpenGL calls are done through it. So its quite proven, and not that slow.

**NOTE:** There are in fact several FFIs today, the old one, the one called Alien and Pharo is brewing a new one called UFFI.

Let's see if we can use the good old FFI with Nim.

<!--more--> 

# Making a Nim library

It turns out that making a library isn't hard, but there are a few things of note. An oh, [all files here](http://files.krampe.se/testlib.zip) if you want to try it out. Ok, so here is our `testlib.nim` library:

``` nimrod
# We exercise some trivial types and how they map.
#
#   SqueakFFI      Nim
#   =========      ======
#   long       =>  int
#   char*      =>  cstring        

import math

# A single proc, returns an int. Since we are on 32 bits
# an int is 4 bytes (same size as pointer) and in Squeak FFI
# this is a long. The exportc pragma ensures that the exported
# name for this proc is exactly "hello" and not mangled.
proc hello*(): int {.exportc.} =
  42

# Trivial, a Nim string can be sent as a cstring because they are
# automatically 0-terminated.
proc foo*(): cstring {.exportc.} =
  "hey"

# Not a problem taking int arguments, they are "long" in Squeak FFI.
proc add*(x, y:int): int {.exportc.} =
  x + y

# Just return the length of a cstring
proc length*(x: cstring): int {.exportc.} =
  len(x)

# Here we convert cstrings to Nim strings, concatenate and return.
proc concat*(x, y: cstring): cstring {.exportc.} =
  $x & $y
```

The only thing above that wasn't obvious - ehrm, unless you [read the manual](http://nimrod-lang.org/manual.html#exportc-pragma) of course - is that you need to use the `exportc` pragma to make the symbols stay unmangled in the library.

To compile the above to a **32 bit .so library on Linux**, we create a corresponding config file called `testlib.nim.cfg`:

``` bash
--app:lib
--cpu:i386
--passC:"-m32"
--passL:"-m32"
```
The above are options to the `nim` compiler, so we could have just used them on the command line. Now we compile it with `nim c testlib` and it should produce a file called **libtestlib.so**.

The first options means _"compile a lib instead of a program"_, and the second means _"make it 32 bit"_. The last two were needed to make it boil down to the C compiler, might be a bug somewhere, but it works.

Now... the above library worked just fine to call from Squeak... at least all procs **except the concat proc**. Boom. And it almost **DROVE ME NUTS** trying to figure out why I was having issues sending `char*` arguments from Squeak. I thought the problem was on the Squeak side, and I must say that googling for info on stuff like this is a bit of a haystack operation.

**Sidenote:** Squeak does suffer quite hard from a lack of proper singular documentation. I mean, lots of docs, wiki etc, all over - but what is current? What works? Its a bit of a problem in the Squeak community I would say. And... well, is Pharo different? Not entirely sure. I really like Smalltalk, Squeak and Pharo, and I am used to this, but I must say its a mess.

It turns out that the concat proc is the only one that creates a Nim string, that code needs the GC, and the GC... is in the `nimrtl.nim` module. This is also documented, but its in the [Compiler manual](http://nimrod-lang.org/nimrodc.html#dll-generation). So it wasn't hard, we just need to make sure to build it too as 32 bits, and copy it to some reasonable place:

``` bash
nim c --cpu:i386 --passC:"-m32" --passL:"-m32" --app:lib --define:createNimRtl lib/nimrtl.nim
sudo cp lib/libnimrtl.so /lib/i386-linux-gnu/
```

Then... we also need to add an option to compiling our lib, `-d:useNimRtl`, so testlib.nim.cfg looks like this:

``` bash
--app:lib
--cpu:i386
--passC:"-m32"
--passL:"-m32"
-d:useNimRtl
```

The end result is that we now have a dynamically loadable runtime library **libnimrtl.so** that has the GC etc. The above option makes sure our **libtestlib.so** uses that runtime library which in turn makes Nim strings work fine and tada, `concat()` works.

## Smalltalk side

Okidoki, so... thanks Andreas for helping me to get it working. Now, time to play. I put the `libtestlib.so` in the directory where I run Squeak. Now... I am working with an old Squeak, but it also works just fine with [Pharo 3.0](http://pharo.org). So easiest way to see it in action is to download Pharo 3.0 and try it there:

1. Download [Pharo 3.0](http://files.pharo.org/platform/Pharo3.0-linux.zip), unzip somewhere.
2. Unzip [this file](http://files.krampe.se/testlib.zip) into the `pharo3.0` directory. It has the **libtestlib.so** and also the Smalltalk source.
3. Install FFI into Pharo: I did it by opening the Configuration browser, finding FFI configuration, then "Install stable version". The FFI plugin itself is included in the VM.
4. File in the Smalltalk source: Open a File browser, select the file **Nim-Test.st** and do "Install into new changeset".
5. Open a Test Runner, search for "Nim" using upper left field, then run the test FFINimTest. If its green - yiha!

You find the calls on the class side of `FFINimTestLibrary`. For example the one for `concat()`:

``` smalltalk
ffiConcat: a with: b
	"self ffiConcat: 'a' with: 'b' "
	
	<cdecl: char* 'concat' (char* char*) module: 'testlib'>
	^self externalCallFailed
```
You can select the code between "" and run it with "inspect it". Hopefully you get the Smalltalk String `'ab'`.

## Remark

First versions of this article mentioned segfaults, but after looking closer it seems those segfaults appeared due to me using `Smalltalk unloadModule: 'testlib'` and then trying again, thus causing a reload. Apparently there is a problem doing this in the VM. But the code seems solid, I have run it hours on end with no problems.

I also studied the Squeak FFI code a bit up close and yes, for `char*` arguments it will copy them out into temporary allocated memory, and then make the call. Afterwards it will deallocate them before returning back into Squeak. For a `char*` result it will instantiate a ByteString object from inside the plugin and copy the bytes over into it, so the actual pointer and memory returned from Nim, is not used. If we use `byte*` we can do the same operation from inside Squeak, as the Terf codebase does extensively. But both approaches seem to be solid.

As noted the pointer returned from Nim in `concat()` is **the pointer to the Nim string itself**. This works because Nim strings "double" as cstring, because they are null terminated. That string is however a GC tracked ref in Nim, so **Nim will eventually garbage collect it** - but the GC doesn't run in its own thread, so the data is safe for Squeak to copy - at least until we return back to Nim in the next call. But generally having Nim return pointers to GC tracked data, is of course **not safe unless Squeak immediately copies it**. Now... thankfully for `char*` Squeak FFI does it automatically, for other types we can do it manually in Smalltalk code.

## Conclusion

The old Squeak FFI is quite proven and works. As we saw Nim can produce libraries quite easily. And using Nim instead of C/C++ is a nobrainer to me. :)

Happy hacking!


---
title: Nim Socket Server
date: '2014-10-25'
slug: nim-socketserver
categories:
- Nim
- C
- Nimrod
- Programming
---
In learning [Nim](http://nim-lang.org) I decided to implement a trivial Socket server, very small, as an example. Its **not a useful HTTP server** (it just returns a hard coded HTTP response so we can benchmark it using HTTP tools), and its **not async** - there are other such examples in the Nim examples directory and in its stdlib. No, I wanted to write a more classical threaded socket server to see how easy that is - especially with the new APIs in Nim ["bigbreak"](https://github.com/Araq/Nimrod/tree/bigbreak) - and see how it performs.

The new "bigbreak" branch that will become Nim 0.10.0 soon-ish has a bunch of new stuff in the networking area. Its replacing the single `sockets` module with a low level `rawsockets` module, and a higher level `net` module. And there is a new `selectors` module that abstracts over different modern IO polling mechanisms. This means that a single API will use **epoll on Linux, kqueue on BSD/OSX, old select on the other Unices and IO Completion ports on Windows**. At the moment epoll, select on "other Unices" and IO Completion ports works. kqueue is on the todo.

So without further ado...
<!--more--> 

...here is the code with lots of comments sprinkled all over it - so that hopefully even a non Nim programmer can understand how it works:

```nimrod
# Imports are by source, so this will import threadpool.nim, net.nim etc
# from ../lib relative to the location of the nim compiler. Everything
# will be compiled together into a single statically linked executable.
import threadpool, net, os, selectors, strutils

## A trivial spawning socket server where each connecting socket is handed
## over to the threadpool for handling and response.
##
## * Uses the new "threadpool" module to spawn off the actual handling of each request
## * Uses the new high level socket module called "net" which is above "rawsockets"
## * Uses the new abstract selector from module "selectors" to do efficient polling (epoll etc)
##
## Compile using Nim "bigbreak" with:
##   nim c --threads:on --d:release spawningserver.nim
##
## Run it and throw ab on it, 100 concurrent clients:
##   ab -r -n 500000 -c 100 http://localhost:8099/
##
## On my laptop for "bytes = 100"  I get about:
##
## Requests per second:    17133.43 [#/sec] (mean)
## Time per request:       5.837 [ms] (mean)
## Time per request:       0.058 [ms] (mean, across all concurrent requests)


# Just a regular kind of "Nim class definition" - the type "Server" inheriting
# the default root object with a single instance variable "socket" of type
# Socket.
type
  Server = ref object of RootObj
    socket: Socket

# Amount of data to send
const bytes = 100
# The payload
const content = repeatStr(bytes, "x")
# And the response
const response = "HTTP/1.1 200 OK\r\LContent-Length: " & $content.len & "\r\L\r\L" & content

# This is where we perform the response on the socket.
# This proc is spawned off in its own thread on the threadpool.
proc handle(client: Socket) =
  # TaintedString is used for strings coming from the outside, security mechanism.
  # The below is equivalent to TaintedString(r"") and TaintedString is a distinct type
  # of the type string. The "r" means a raw string.
  var buf = TaintedString""
  # Using try:finally: to make sure we close the client Socket
  # even if some exception is raised
  try:
    # Just read one line... and then send our premade response 
    client.readLine(buf, timeout = 20000)
    client.send(response)
  finally:
    # We may end up here if readLine above times out for example,
    # we just ignore (no raise to propagate further) and close.
    client.close()

# Eternal loop where we use the new selectors API.
# If we get an event on the listening socket
# we create a new Socket and accept the connection
# into it. Then we spawn the handle proc.
proc loop(self: Server) =
  # Create a Selector - cross platform abstraction for polling events.
  var selector = newSelector()
  # Register our listener socket's file descriptor, the events we want to wait for
  # and an optional user object associated with this file descriptor - we just use nil
  # since we are only listening on one Socket.
  discard selector.register(self.socket.getFD, {EvRead}, nil)
  while true:
    # Ask selector to wait up to 1 second, did we actually get a connection?
    if selector.select(1000).len > 0:
      # Socket is a ref object, so "Socket()" will allocate it on the heap.
      # Perhaps a bit needless since we will deepCopy it two lines down in spawn.
      var client: Socket = Socket()
      # Or like this, its equivalent:
      #   var client: Socket
      #   new(client)
      accept(self.socket, client)
      # Spawn it off into the new threadpool - nifty stuff. It is a self adapting
      # thread pool that checks number of cores etc. The argument is deepCopied over
      # ensuring threads do not share data.
      spawn handle(client)
# We create a listening port and then call loop() which does not return
proc listen(self: Server, port: int) = 
  # First we create a Socket. newSocket is a convenient proc with good
  # default values.
  self.socket = newSocket()
  # Hmmm, where is InvalidSocket defined in bigbreak?
  #if self.socket == sockets.InvalidSocket: raiseOSError(osLastError())
  
  # Then we bind/listen and call the loop. Whichever way we exit the try:
  # block (exception raised or a normal return) Nim will call the finally:
  # block for cleanups where we make sure to close the socket.
  try:
    self.socket.bindAddr(port = Port(port))
    self.socket.listen()
    echo("Server listening on port " & $port)
    self.loop()
  finally:
    self.socket.close()


# Only compiled when this is not used as a module
when isMainModule:
  # Type inference makes port an int
  var port = 8099
  # Type inference makes server a Server, which is
  # a "ref" to an "object", see type definition at top.
  # If you call a ref object type like this - it acts
  # like a constructor and will use new to allocate the
  # type ref'ed on the heap.
  var server = Server()
  # The listen proc takes a Server as first param
  server.listen(port)
```

## Remarks on code

Here are some things to note:

* On **line 46** we see `TaintedString""`which may look odd. Its equivalent to `TaintedString(r"")` and that is actually a so called [type conversion](http://nim-lang.org/manual.html#type-conversions) of a [raw string](http://nim-lang.org/manual.html#generalized-raw-string-literals). A TaintedString is (with `--taintMode:on`) a distinct type of string. So it "works" the same as string, but is another type according to the type system and thus way we can track the use of this string more closely. More on [TaintedString](http://nim-lang.org/manual.html#taint-mode). **NOTE: Compilation fails with taintMode:on currently, something doesn't handle it properly in `net`**
* On **line 64-71** we see trivial use of the new `selectors` module. The user object we send in as `nil` would typically be some object with a reference to the Socket, so when we call select (line 71) and get a sequence back with those user objects that had the event (we listen for `EvRead` in this case) - we don't need to do some lookup based on the Socket itself. In this code however we only listen on a single listener Socket, so we just want to know if the sequence wasn't empty (len > 0), meaning that we **did** get an event for our listening socket.
* On **line 74-78** we create a new `Socket` (it was called PSocket earlier, in "bigbreak" its been renamed to Socket) and since Socket is a "ref object" type it will implicitly call the `new` proc which allocates it on the heap. Then later on line 78 we call `accept` and the accept will _"fill in the details"_ in this new Socket object. The client parameter is a "var parameter" so in theory the accept procedure could assign to it - but it turns out this is a leftover from earlier code - because it doesn't assign to it. Personally I am still [slightly uneasy](https://github.com/Araq/Nimrod/wiki/Common-Criticisms#nim-doesnt-require-call-site-annotation-for-var-parameters) with the fact that I can't really tell **from the call** here that the client var can be modified to reference another Socket. But I also understand that having some annotation on the call site would make the code less readable.
* On **line 82** we do `spawn` and that will cause the argument (the Socket) to be deepCopied and handed over to another thread, making sure the threads are isolated from each other.


## Performance

Some notes before discussing the numbers:

* This code **doesn't do any keep-alive**, its all just lots of _connect/recv-and-send/close_.
* I only ran ab against localhost from localhost, so may be less realistic.
* This code doesn't really **do** anything in the handler. We basically measure spawn and socket accept/close overhead per request. And shoveling data.

And the verdict:

* For a trivial payload of 100 bytes and 100 concurrent we get **17k req/sec each taking 5-12 ms**, note that we do 100 in parallell. If we increase concurrency to 1000 we still do about **15k req/sec each taking 20-28ms**. Personally I felt these are good numbers, but I admit I need to compare with say Nginx or Nodejs or something.
* A slighty bigger payload of 100000 bytes and 100 concurrent we get **11k req/sec each taking 9-17ms**, serving in total about **1Gb/sec**.
* For a fat payload of 2Mb and 100 concurrent we get around **8k req/sec** but a whopping **1.5Gb/sec**.

I also verified that Nim sets up a thread pool (about 40 threads it seemed to use on my machine) and **most** of the utilization is focused around 5 threads - presumingly matching my 4 cores. But it was quite satisfying to watch the system monitor and see that all 4 cores are happily working :)

If you remove the `spawn` word then this turns into a synchronous server handling just one request at a time sequentially. You can then test with ab using a single client. It actually does a bit more requests per second then, about 22k I think I got. This is most probably due to the fact that we get rid of the "spawn overhead" so the listener forking off sockets will loop a tad faster even though it does the read-send-close in the loop.


## Conclusion

The code is short and clean, perhaps its not fully Nimiomatic - I use "self" as the name for "this", not sure what OO Nimmers tend to use. It was fun to write and performance seems very good to me. It's also quite stable and I can't see any memory leaking. :)

The thread pool mechanism is very promising (great work there Andreas!) and its also very neat that we can have epoll based polling with just a few lines of code - and its meant to work cross platform. Way to go Dominik! :)

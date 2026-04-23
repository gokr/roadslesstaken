---
title: Current Smalltalk obsessions...
date: '2012-02-07 00:15:10'
slug: current-smalltalk-obsessions
categories:
- Amber
- DeltaStreams
- Pharo
- Smalltalk
- Squeak
tags:
- activemq
- amber
- riak
- smalltalk
- stomp
---
These days I am, as usual, torn between several interesting technical projects.

# Amber

The new [Smalltalk](http://www.world.st) called [Amber](http://www.amber-lang.net) (by Nicolas Petton) that compiles to javascript is pretty awesome and there are tons of interesting things one can do with it. My contributions so far include the beginning of a package model, a faster simpler chunk format exporter/importer, a command line compiler, a Makefile system so that Amber can be built fully from the command line and a bunch of [examples](https://github.com/NicolasPetton/amber/tree/master/examples) running on top of [Nodejs](http://nodejs.org) and [webOS](http://developer.palm.com), and a few other odds and ends.

<!--more--> 

I would like to port [Deltas](http://wiki.squeak.org/squeak/DeltaStreams) to Amber in order to create a powerful toolset for managing code changes. Using local storage it would among other things enable undo and change logging to prevent accidental code loss. It could also easily form the basis for a "commit tool", similar functionality that git stash offers etc.

Another thing I would like to build is a dead simple public shared package repository. And play with [Socket.IO](http://socket.io), or just fool around with the compiler trying to add optimizations like various type inferencing, optimizing self and super sends etc :). So much fun stuff to do!


# STOMP and Apollo


For a personal "secret project X" I need scalability so it is being designed with lots of daemons each taking care of a specific task. I want to be able to implement these daemons primarily in either Nodejs (in plain js or using Amber) or [Pharo Smalltalk](http://www.pharo-project.org), but also in any other language that fits.

This requires some kind of messaging infrastructure to tie them together. So... after looking hard and long and reading a lot about messaging, job scheduling, [AMQP](http://www.amqp.org), [0MQ](http://www.zeromq.org), [STOMP](http://stomp.github.com), [Beanstalkd](http://kr.github.com/beanstalkd/), [RabbitMQ](http://www.rabbitmq.com), [ActiveMQ Apollo](http://activemq.apache.org/apollo/) (and tons of other things) I decided to try to use the new ActiveMQ Apollo together with [STOMP 1.1](http://stomp.github.com/stomp-specification-1.1.html) (which should also be supported by the STOMP plugin for RabbitMQ etc).

The new Apollo implementation is written in Scala using [HawtDispatch]( http://hawtdispatch.fusesource.org/) so the architecture seems modern and the JVM of course has very good performance these days. So, while I generally am very tired of Java and its eco system, this actually seems like a solid product and has already shown [very impressive numbers in benchmarks](http://hiramchirino.com/blog/2011/12/stomp-messaging-benchmarks-activemq-vs-apollo-vs-hornetq-vs-rabbitmq/).

So a sound asynchronous architecture with good performance is nice but the other thing I like with ActiveMQ is their focus on STOMP. Since I intend to use Pharo as one major component I need to be able to hook it into the messaging backbone. And sure, Tony Garnock Jones - one of the main developer behind RabbitMQ - actually has an AMQP client library written for Squeak 3.9, so I could probably us AMQP, but I somehow foresee a "world of hurt" in the complexity given that AMQP is a magnitude more complex than STOMP.

I have already [implemented STOMP 1.0 for Pharo](http://www.squeaksource.com/StompProtocol.html), actually tried it with RabbitMQ at the time, so I am now upgrading that library to work with 1.1 of the specification.


# Riak


The other important piece of the puzzle for true "Internet scalability" is of course the choice of persistence. I am a long time fan of the new NoSQL databases and having played with a few of them, implemented a C# binding for CouchDB, hacked some bindings in Squeak for both CouchDB and Tokyo Tyrant... I now have decided to focus on [Riak](http://wiki.basho.com/Riak.html). Riak is IMHO the most interesting NoSQL database out there right now, at least for worry free ultra scaling. Sure, it may not be the fastest on a single box - but if you are really serious about scaling - one box is totally uninteresting. :)

Runar Jordahl had already started a Riak binding in Pharo, I took it and changed quite a lot of it - not really because it was "bad" or anything, I just have a different style of coding I guess. So I decided to fork because I didn't feel comfortable - thus [Phriak was born](http://www.squeaksource.com/Phriak.html). Now Nicolas Petton is getting hard into Riak too and has pushed Phriak forward **quite a LOT** in the last few days, much further than I had time to do. It now has a clean command style protocol implementation, an object model similar to the one in Ripple (Ruby Riak client) and initial working code for both secondary indexing, link walking and map/reduce! Quite impressive stuff.

Nicolas is also experimenting with writing an "OODB-ish" database using [Fuel](http://rmod.lille.inria.fr/web/pier/software/Fuel) called [Oak](http://www.squeaksource.com/Oak.html) and after I managed to get him hooked on Riak he has been moving that codebase over onto Phriak. The initial experience we have with Phriak and Oak is extremely promising and who knows where this will lead.

Happy coding, Göran

---
title: RethinkDB - Yet Another NoSQL?
date: '2013-07-16'
categories:
- NoSQL
- RethinkDB
- Riak
- Computing
---
15-18 years ago my passion was in OODBs. As a Smalltalker [GemStone](http://www.gemtalksystems.com) was one of the most fascinating to work with, but as we all know OODBs never got really popular, despite their fantastic qualities. But the new NoSQL databases in many respects offer OODB-ish characteristics, although they of course also bring a whole new menu to the table.

In my eternal quest for "database bliss" my next stop is [RethinkDB](http://rethinkdb.com), but let me tell you how I got here.

<!--more--> 

When it comes to NoSQL databases I have both worked and dabbled with a few:

0. [Tokyo Tyrant](http://fallabs.com/tokyotyrant). Yeah, it was extremely fast (still is) and I did implement a [Squeak binding](http://map.squeak.org/packagebyname/tokyotyrant) for its binary protocol, but nah, the use cases are very limited. But it was fun!

1. [CouchDB](http://couchdb.apache.org/). A lot of nice design decisions with a very friendly HTTP oriented API, all JSON and interesting map/reduce mechanisms. CouchDB was one of the primary NoSQL databases to start the whole "movement" but although it's brilliant in many ways it also wasn't built to scale and it quickly got side tracked by the competition. Most other NoSQL databases have picked up quite a few tricks from Couch though so it has been very influential.

2. [Riak](http://basho.com/riak/). Riak feels like "CouchDB done right", same HTTP friendliness but a very robust Dynamo-inspired fully distributed architecture. If one wants a system that doesn't trade availability for consistency - Riak is it. But there is a cost - you need to put a lot of effort into conflict resolution mechanisms (resolving siblings) - and that is not trivial to do. While Riak is very "seductive" in all its **100% Buzzword Compliance-ness**, you might come to the conclusion that your use case actually isn't the next Amazon or Facebook needing to serve millions of people at the same time with 99.99999 availability.

3. [HyperDex](http://hyperdex.org). This is a **really fast** database with several interesting mechanisms like hyper hashing. The only API is going through the C library, which can be a bit of a hard time from [Pharo](http://www.pharo-project.org)/Squeak. I started out with [NativeBoost](https://code.google.com/p/nativeboost/) FFI (cool stuff Igor) for this but got stuck. Still very interesting and did I mention super fast? A bit immature (docs lacking) and it also depends on fixed schemas, not sure how to deal with schema migration. So, fascinating and FAST, with lots of cool functionality but... doesn't feel practical - there must be alternatives not needing fixed schemas? Why isn't the "spaces" definition grammar documented? Who knows, **HyperDex may be the Next Big Thing**, but as of now I think I am moving on.

So where to go from here? Riak is great, but I want more consistency guarantees to eliminate all that conflict resolution work. This [blog post](http://www.jeremyong.com/blog/2013/05/11/on-choosing-dynamo/) nails it pretty good - it probably turns out I want something that is CP instead of AP like Riak is. 

And in case you wonder - MongoDB is not for me, I know... some people love it, but let me quote (and there are many other sources too) the internetz:

{% blockquote Lucian http://www.tbray.org/ongoing/When/201x/2013/05/06/Tab-Sweep-Tech#c1367917902.203869 %}
I would suggest you don't try to use MongoDB in a high-availability mode (or at all if you can help it). It's quite buggy, lacks useful features and isn't in fact Consistent (even though its design might suggest it is). It's just a bad database with too much marketing :( There are a few decent-looking Consistent databases out there (HBase, Couchbase, RethinkDB, Hyperdex) and several decent Eventually Consistent databases (Cassandra, Riak, Dynamo).
{% endblockquote %}

So Google to the rescue, there must be more consistent NoSQL dbs out there...

4. [FoundationDB](http://foundationdb.com/). Sounds and looks very impressive "on paper" but it is not yet available and AFAICT it is not going to be open source either, so... nope.

5. [Couchbase](http://couchbase.com). Looks fairly interesting, Membase married to CouchDB, but their description of the "community edition" doesn't feel that inspiring to me. They don't really seem committed to open source, this is more a straight up commercial offering with "Enterprise trash talk". So no, not me, and the muddled merge with CouchDB has at least left me utterly confused over this product and what it actually "is".

5. [RethinkDB](http://rethinkdb.com). Aha. I think this is my next NoSQL database to **look closer at**, I really like what I see, both technically and how they feel as a company - very open and they seem to really understand how open source works, culturally. And installing it and playing with the web console was trivial... fun stuff!

Now I just need to implement [protobuf](https://code.google.com/p/protobuf/) in Pharo... :)



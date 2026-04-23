---
title: Tirade, part 2
date: '2009-03-20 00:34:07'
slug: tirade-part-2
categories:
- Old blog
- Pharo
- Smalltalk
- Squeak
- Tirade
---
In an article recently I described [Tirade](http://goran.krampe.se/2009/03/16/tirade-a-file-format-for-smalltalkers/) - a new generic "file format" for Smalltalk/Squeak, or actually a sub language! Since that article I have refined Tirade a bit. Tirade consists today of 4 classes (parser, reader, writer, recorder) totalling **about 500 lines of code**, excluding tests. Tests are **green in 3.10.2, pharo-10231, 3.9, 3.8 and 3.7**. It does turn red in 3.6 due to old initialize behavior, some missing methods etc, probably easily fixed if anyone cares. There are no dependencies on other packages. Compared to using the old Compiler>>evaluate: it is about 5-7 times faster.

Tirade is a very small "language" similar to [JSON](http://www.json.org/) (see below) and probably fits similar use cases as JSON fits.


#### Numbers


In my first Tirade description I opted out and only supported plain integers, no frills at all. Then after subsequent discussion I came to the conclusion that syntactically there is no problem to let**TiradeParser>>parseInteger** become **TiradeParser>>parseNumber** and just let it handle **all kinds of Number literals** that Squeak supports by either using SqNumberParser if present (in Squeak 3.9+) or by falling back on regular old **Number class>>readFrom:** which Scanner still uses in 3.10.2.

So now Tirade deals perfectly fine with:



	
  * 23.45 (Floats)

	
  * 16rFE (radix)

	
  * 1.0034e-5 (scientific notation)

	
  * 243s2 (scaled decimals)

	
  * "NaN", "Infinity" and "-Infinity"


…and whatever else should be there.

The performance penalty if we use SqNumberParser (Squeak 3.9+) is not that bad, about 20% on my little trivial benchmark. Using **Number class>>readFrom:** hurts more, increasing time for benchmark around 50%.


#### Security…


First I played with having the builder object (that is typically fed the Tirade messages from the Tirade reader) implement isSelectorAllowed: etc. I finally ended up encoding a simple security scheme in the default TiradeReader that relies on finding the implementations of the Tirade messages in the builder in a method category beginning with "tirade". It seems simple enough for most uses.

I also added a global "whitelist" of Tirade messages that can be registered in the reader before starting to parse. If selectors are found in this whitelist they are considered "ok". This can be useful in some situations.

If the builder relies on catching Tirade messages using **doesNotUnderstand:** then it is on its own for security, but that seems fine.

Finally you can turn off all selector checks by using #unsafe:.


#### Receiver juggling


Tirade is meant to separate "concerns" between Tirade "code", parser, reader and the builder object supplied by you. The Tirade "code" has no control over the receiver of the messages, Tirade "code" is just a sequential flow of messages separated with periods. The TiradeParser also doesn’t care, it just parses and then does "self processMessage", if you are using TiradeParser directly it has a default implementation of #processMessage that prints them out in Transcript and collects them in an OrderedCollection.

So yes, you can use TiradeParser to just gobble up some Tirade input and then muck about with the OrderedCollection afterwards - similar to how you work with JSON or an XML DOM. But the better approach is of course to subclass TiradeParser and implement #processMessage to actually do something - in a streaming SAX-ish fashion.

Then we have the reader. There is a default TiradeReader that implements the security described above and also implements logic for deciding the "next receiver" of the Tirade messages. The logic goes like this:



	
  * If the builder supplied implements Tirade messages by always returning self, it will always be the receiver. Simple.

	
  * If the builder returns another object X, X will be used as the "next receiver".

	
  * As long as X returns self it stays as the "next receiver".

	
  * If object X returns another object Y, X will be put on a "stack of old receivers" and Y will be used as the "next receiver".

	
  * If Y returns nil, X will be popped and be used as the "next receiver".

	
  * If X returns nil we are back to the original builder, and if it returns nil nothing changes.


So if the above is "enough" for controlling the receivers, then the builder object handles it by simply returning the "right" objects. These objects can of course be "sub builders" or domain objects themselves or whatever.

If the above is not enough you can register "control messages" in TiradeReader. A control message can be any selector and will result in TiradeReader pushing the current receiver on the stack and setting the original builder object as the "next receiver". There is also a small twist, if the control message returns self the reader will consider that to be equivalent to "nil" and thus pop the previous receiver back. This is because the common use is to make sure all control messages are sent to the original builder without disrupting the current stack of receivers. But… why? This enables the builder to explicitly control the reader during the parse, perhaps manipulating the current stack, even though it is not the "next receiver" receiving the regular Tirade stream of messages.

One very good reason to use this is when the current receiver is a domain object that does not "know" when to return nil to pop itself.

I am not perfectly happy with the current mechanisms, but it will do for now and I will revisit this when I see how it works out in practice. The important bits are in place though - Tirade input has no control over receivers and the builder object can control it if needed.


#### Compared to JSON again


The differences compared to JSON that I see right now:



	
  * **Smalltalk syntax and parsing rules for Strings.** This means no escapes except for double-single quotes. JSON has 8 other escape codes. Immediate advantage for me is able to store readable code in Tirade, including newlines.

	
  * **Smalltalk syntax for Numbers.** This means more capabilities for parsing numbers than JSON has (radix, NaN, Infinity, scaled decimals).

	
  * **Symbols.** JSON only has Strings.

	
  * **Associations.** JSON has an "object" which is a Dictionary restricted to String keys. JSON does not have a free standing Association. In Tirade any of the allowed objects can of course be keys or values and Assocations can be "standalone". So there is a little bit of greater flexibility here.

	
  * **Comments.** Hmmm, JSON has no comments. Tirade allowed Smalltalk comments, but ONLY between messages.

	
  * **Messages.** This is the big difference, Tirade consists of a sequence of unary or keyword messages, with the "data" described above as arguments.


The addition of messages adds an important extra level of "classification", "control" or "typing" or call it what you want. It also lends Tirade to easy streaming and concatenation. JSON consist on its top level of either a Dictionary or an Array. A parser could of course parse that in a "streaming fashion" one element or pair at a time, but they normally don’t do that I think.

Having messages of course makes it much more natural to map these messages onto a builder or multiple builders and also to use messages to control the message flow. I think this makes Tirade much more expressive in itself.

In summary, Tirade is similar to JSON but extended with messages and comments, more advanced Numbers, deals with text more easily (no escaping of CRs etc), can have comments in it, has a little bit more flexibility in data model (Associations) and uses Smalltalk syntax for it all.


#### Potential uses for Tirade


I started out with a focus on replacing "chunk format" with something simpler and secure for Deltas (Deltastreams project), eliminating the use of Compiler to parse it. Afterwards one can find several interesting places where Tirade could be used for example:



	
  * DSLs

	
  * RPC-ish communication

	
  * Transaction logs


…and a few more things :)

But hey, one thing at a time.

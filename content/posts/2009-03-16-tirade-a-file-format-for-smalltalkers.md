---
title: Tirade, a file format for Smalltalkers
date: '2009-03-16 00:24:07'
slug: tirade-a-file-format-for-smalltalkers
categories:
- Old blog
- Pharo
- Smalltalk
- Squeak
- Tirade
---
In my revived work on [Deltastreams](http://wiki.squeak.org/squeak/6001) in Squeak I ended up facing the choice of native file format for Deltas. Matthew has made an advanced format called [InterleavedChangeset](http://www.squeaksource.com/InterleavedChangeSet.html) which manages to squeeze a binary representation of a Delta into a [Changeset](http://wiki.squeak.org/squeak/1105) file (which is in Smalltalk chunk format). An impressive feat, and it has the advantage of being backwards compatible in the sense that a Delta in this format can be filed in as a plain old Changeset into an old Squeak image.

But I must say I don’t think that benefit alone is enough to justify these tricks. Oh well, time will tell - and multiple formats for Deltas are fine to have.

Looking at another file format for Deltas I decided I want these properties:



	
  * **Readable**. Changesets are nice because they are indeed readable. You can look at them in emacs if you like.

	
  * **Editable**. Same here, if you really need to you can edit changesets manually. The syntax is not totally bad.

	
  * **Secure**. Ouch, changesets fail here because they rely on Compiler>>eval: which of course opens up tons of tricks you can do. I don’t want that with Deltas.

	
  * **Declarative**. This is a spectrum but I would like the "style" for the file format to be declarative.

	
  * **Streamable**. The parser should not have to read it all into a "DOM structure" before actually doing something with it.

	
  * **Extendable**. It should be easy to extend the format in the future and have older code "ignore" such extensions.

	
  * **Fast**. It should be fast to parse and fast to produce. As always. :-)

	
  * **Small**. I mean both conceptually (easy to understand), codewise (parser etc) and syntactically.




#### JSON or YAML


First I looked at [JSON](http://www.json.org/) which nails 5-6 out of these 8. It is indeed "Readable", "Editable", "Secure", "Fast" and "Small". And it is very "hip" in the web arena. It suffers from some problems though:



	
  * **Strings can not have CRs in them**, which will make "larger texts" such as source code a pure pain to read. This is a killer! Sorry.

	
  * It is actually **not so well suited for streaming**. A JSON document is a single "thing", either a Dictionary or an Array. Sure, we could use convention and parse one key-value-pair (or element if it is an Array) at a time, but then I would need to write a new parser anyway.

	
  * It is declarative since it is "just data" but on the other hand this means it also **lacks semantics**. We would need to use Strings and keys (in key-value pairs) to denote our own semantics. Works, but probably would make the structure less apparent.

	
  * Same goes for extendability. Sure, we can add new keys in our key-value pairs etc, but what we really want is to be able to add new semantic elements, and again, those would need to be "encoded as data" in JSON. I think it would get messy.


…so JSON is out. I do like JSON though, in its utter simplicity and above all - it is available everywhere.

What about [YAML](http://www.yaml.org/) then - JSON’s big brother? YAML is a superset of JSON, well, it aims to be a strict superset at least. I did find a very good blog article [comparing](http://blog.ingy.net/2007/05/yaml-and-json.html) them. Looking at YAML it seemed to have lots of better ways to represent source code with CRs etc, but hey… simple? Mmmm, not. Sure, it may be "simple" to look at but I sure didn’t think the specification was simple and in fact HUGE and I had a hard time reading it due to its style. Sorry, not "small" enough for me! ;-)

When discussing all this on squeak-dev the good ole "Hey, why not Smalltalk?"-mantra popped up. I have been there lots of times, using Smalltalk as "representation language" is very neat since it enables so called "internal DSLs" at such ease, but it does fail pretty hard on "Secure", "Declarative" (depends on how you view that one, I know), "Streamable" and in some ways "Small". Although it would be strange if we didn’t have Compiler available when dealing with Deltas :-).


#### Smalltalk… or Angry Smalltalk?


But bringing it up did get my mind working - how about a nice **subset** of Smalltalk? That does what JSON does but fixes the problems I identify above? Pretty quickly a subset of Smalltalk crystallized itself that I named "Tirade" as in:

**"a long angry speech or scolding. Synonyms: diatribe, harangue, rant"**

Tirade, as the name somewhat implies, is just a sequence of Smalltalk unary or keyword messages with optional Smalltalk comments inbetween.

The only thing making Tirade **NOT a strict syntactic subset of Smalltalk** is that there is **no receiver to the left**, this is up to the reader/parser to decide. One seemingly useful pattern for determining the receiver is to use the result of each message as the next receiver.

Here is a fantasy example of Tirade input:

    
            "We allow unary messages, the period after each message is mandatory.
            A unary message is probably used mainly for semantic structure."
            beginWumpus.
    
            "We allow Symbols."
            push: #superbat.
    
              "Whitespace is just fine, so indentation can be used, but has no meaning.
              In Strings we use double single quote for a single quote. No other escaping exists."
              name: 'Bat from hell'
              description:
    
            'Black as devil''s tar, evil. Appear in flocks
            and when they come you better duck.
            Duck fast.'.
    
              "Integers are fine, positive or negative. No scientific notation, no floats."
              power: 'Can screech' damage: 3.
              power: 'Can bite' damage: -6.
    
              attrib: #size->43.
              attrib: #color->nil.
              attrib: #dangerous->true.
    
              moreattribs: { #wings-> 2 . #ears -> nil. #teeth -> {'one'.'two'.'three'}}.
    
            pop: #superbat.
    
            endWumpus.


Well, you get the idea. So source code with CRs will work fine, just like in Changesets. We could even add support for indenting Strings with embedded CRs (as you can see above they otherwise break indentation), but I haven’t done that. So we have Strings, Integers, Associations, true/false/nil and brace Arrays. Nested in any combination and depth. In Smalltalk all these are "literals" except Associations which are actually created using the message #-> sent to the key object. In Tirade it is not implemented "as a message", but rather built into the parser. I also chose the "brace array" instead of a regular array because it has separating periods and it allows Associations inside it.

Ok, so Tirade is just a sequence of messages with "data" as arguments. And the "data" is expressed very similarly to JSON, but with Smalltalk syntax. Is this better than plain JSON? I think so:



	
  * We got rid of the "CR in Strings"-issue, Tirade Strings are just like Smalltalk Strings - the only escape character is doubling a single quote.

	
  * Tirade is streaming since we parse and process the messages "one by one" and we get IMHO better "semantics" in the form of having something more than "just data": keyword messages.

	
  * Extending is easily done with new messages that old code can happily ignore at will - or capture using #doesNotUnderstand: and log or whatever.


I just created the Squeaksource project [Tirade](http://www.squeaksource.com/Tirade.html) for this, the code there has both reader, writer and green tests. It also has nice class comments :-) and it is not rocket science to get going with. The parser is a simple "predictive recursive descent" parser which anyone should be able to step through and understand. It has no ambiguity and it only checks the next Character for choice of production, which made it very easy to create.


#### Are we there?


Did we meet our objectives we started out with? Do we have our "dream format" we want? Let’s look at it again:



	
  * **Readable**. Oh yes, and for a Smalltalker VERY readable. We have simplicity, comments, indentation, CRs inside Strings etc.

	
  * **Editable**. Definitely, for a Smalltalker VERY editable. It is Smalltalk after all.

	
  * **Secure**. Very secure. There are no expressions and no access to globals. You can only send messages with data as arguments. You do not decide the receiver, the reader does. The base reader also does a security check asking the builder if it allows the selector.

	
  * **Declarative**. Given only messages (which creates structure and semantics) with data and no full Compiler I think it is very declarative.

	
  * **Streamable**. Yep. We just keep going and going! Since the period is mandatory after a message this also means you can concatenate Tirade streams together without syntactic problems.

	
  * **Extendable**. Just add new kinds of messages, make sure the old code can ignore "new messages" either by having a tolerant #doesNotUnderstand: or by letting #isSelectorAllowed: not allow unknown messages, which then will not be sent at all.

	
  * **Fast**. My first benchmark shows TiradeParser is about **7 times faster than Compiler**. It is pretty nippy.

	
  * **Small**. It is definitely small in all aspects mentioned.




#### Just one gripe…


Why is it not a true subset of Smalltalk - in other words, why did I leave out the receiver to the left?!? Well, since we don’t have any kind of variables there is not much you can put there! Should we still write out "self"? If we did, then it would be confusing if the reader uses the "result of message is the next receiver"-logic.

We could encode that policy by enforcing the code to say "me := me <message>", but then we would need to introduce a special variable "me" and it would look hackish and odd and confusing as hell. And it would also force this logic. I think leaving receiver out is ok. :-)

So why do we so dearly want to make it BE Smalltalk? In theory it could enable us to select some Tirade code with the mouse and press "alt-d" on it, but it is still quite easy to debug Tirade code directly. If someone makes a compelling argument I am willing to listen, but for now - sorry, no, Tirade is not == Smalltalk and it does not have an explicit receiver on the left. As Jecel pointed out though, it may be legal Self code. :-)


#### Conclusion


I think Tirade has interesting potential, especially as a readable serialization or configuration (!) format for Smalltalk. For "data interchange" JSON is probably still KING because then you often need to send data across language barriers and there are JSON parsers everywhere. Tirade is a Squeak only thing, although should be trivially portable to other Smalltalks.

I now intend to go full steam ahead and use Tirade as a file format for Deltas in the DeltaStreams project. We will see how it turns out when put to some real world usage.

---
title: Literal arrays vs JSON vs STON vs Tirade
date: '2012-05-08 00:11:22'
slug: literal-arrays-vs-json-vs-ston-vs-tirade
categories:
- Amber
- Computing
- Pharo
- Squeak
- Tirade
tags:
- JSON
- smalltalk
- STON
- Tirade
---
Recently there were a range of threads on the pharo-dev mailinglist discussing the textual format to use for Smalltalk source code metadata. The discussion veered off from the specific use case but basically four different formats were discussed and compared, of which one I am the author. And oh, sorry for the formatting of this article - I need to change theme on this blog for better readability.

<!--more-->

# JSON


The first format is [JSON](http://json.org), Javascript Object Notation. JSON is a simple language neutral (despite its name) readable format that is very small to implement. It is a restricted variant of the native JavaScript literal syntax for objects (dictionaries) and arrays. Basically it excels in simplicity but lacks a bit in features, but people tend to ignore those shortcomings due to its widespread adoption. I will not go into describing it, [json.org](http://json.org) does a very good job and there are TONS of JSON implementations around.


# STON


Sven Van Caekenberghe recently created a variation on JSON he calls [STON](https://github.com/svenvc/ston/blob/master/ston-paper.md), Smalltalk Object Notation. STON is basically JSON plus the following:



	
  * **Object references**, the concept of being able to refer to other previously described arrays/objects in the STON file. This is done by number using the @-sign like "@2" refers to the second array/object in the file.

	
  * **Class prefixing**, the idea of annotating arrays and objects (JSON terminology) so that one can instantiate a reasonable class when reading.

	
  * **Symbols**, simply adding support for a primitive data type for Smalltalk symbols, although I do note - a limited form of Symbols not allowing the same range of characters in them as Squeak/Pharo does.


Then there are a few subtle differences from JSON, like using $' instead of $" as string delimiter and nil instead of null, but not much else that I can see. Numbers seem to be exactly the same as in JSON, and escape codes inside strings are also the same, obviously by design.

First I admit that I have not played with STON, my comparison is purely in theory. STON has the same basic positive notes that JSON has, it is small, simple and well defined. **But are the differences worth it?**

JSON is everywhere and there are already tons of parsers for it, probably in every Smalltalk on earth, and of course all other languages too. STON on the other hand is Smalltalk only, and as of this writing probably Pharo only, although I admit it must be simple to port.

It boils down to if the additions are worth it and I don't think they are. Embedding class names, if needed, could be done in JSON, although slightly inelegantly of course, but one approach would be to wrap each "typed" object/array in an object like this:

    
    ByteArray [1, 2, 3] ==> {"type": "ByteArray", "data": [1, 2, 3]}


I agree, clunky, but on the other hand I tend to think that the parsing end needs to know the semantics and construction of the JSON anyway - JSON is too "simplistic" to be used as a true generic serialization mechanism and trying to turn it into such a beast by adding types and references, like STON does, is IMHO not that useful.

STON looks neat, but in practice** I don't think the benefits outweigh the ubiquity and availability of JSON**. Had it been even **more** different it might have been another story. But if we don't think we will use type annotations and circular references - then why not simply use JSON?


## Literal Smalltalk arrays


The simplest notation of all in the lineup is the literal array syntax in Smalltalk. The example below covers all its capabilities AFAIK (in Pharo/Squeak), please tell me if I missed anything:

    
    #(4711 3.4 16r3F 'string' #symbol #'another-symbol' (nested array) #(one more) true false nil $x #[12 32])


So we have space separated elements and arrays that can nest, with or without #-prefix inside the array. Primitive literals are numbers (full numeric Smalltalk parser, not as limited as JSON/STON), strings (no escape codes, single quotes needs to be doubled), symbols (can handle more characters than STON symbols), character literals, byte array literals and true/false/nil.

Literal arrays are quite nice but they lack the concept of "associations" and thus no simple readable way to represent a Dictionary. **And that is a BIG negative**. Funny enough, if we added support for literal dictionaries to Smalltalk then literal arrays would match JSON, with a few extras on the side!

Amber has recently added support for dynamic literal HashedCollections using this syntax:

    
    #{'hey'->12 . aString->'123123'}


It is simply a dynamic {} array (was introduced originally in Squeak I believe) but with the assumption that the expressions all evaluate to Associations that are limited to a string as key. This is because it will be turned into a HashedCollection which is the Amber counter part of a JavaScript object, and JavaScript objects are limited to having strings as keys (Sidenote: Amber also has a generic Dictionary without that limitation).

Without a syntax for dictionaries, literal arrays, although nifty and syntactically quite compact, are still limited in expression. And of course, while Smalltalk literals are fairly simple to parse, other languages do not typically know how to do it - and when it comes to numbers, the Smalltalk full range of syntax is perhaps a bit of an overkill if we aim at cross language portability. Having literal syntax for Characters is also clearly of less value, ByteArrays on the other hand are obviously useful.


## Sidestory: Adding literal Dictionaries to Smalltalk?


Smalltalk only evolves in micro steps every other 10 years, but with the current onslaught of Pharo perhaps there is an opportunity to actually take a few more such steps.

We will see below that Tirade has added support for "->" as a literal syntax instead of being a message send and as I mentioned above Amber has added a special syntax for dynamic Dictionaries, and that was actually done in order to more easily match JavaScript object syntax when interacting with JavaScript.

So perhaps the Smalltalk/Pharo community could decide to add literal Dictionaries to Smalltalk using the Amber "#{" syntax? In such a syntax the separators between Associations can probably not be spaces, it gets confusing to read:

    
    #{ key -> value key2 -> value2 }


A separator is clearly needed and since we use periods generally for that in Smalltalk it's a good choice. Syntactically it could lead people to think it's a dynamic Dictionary, but let's continue the thought experiment. How would it look? As is customary for #() we can ommit the # inside the array:

    
    #(123 'hey' {key -> value. key2 -> value} 456)


It looks fairly nice. However I do admit that we probably should take a long hard look at all our syntaxes and try to bring some harmony to them. Currently, due to legacy, we have literal and dynamic Arrays using #() and {}. A bit unfortunate since we then use both $( and ${ as delimiters for Arrays and make it harder to find good characters for Dictionaries.

It would be nice to have a symmetric syntax. Ideally the leading # could indicate "literalness" - and perhaps we could use another character to indicate dynamic evaluation? Again, just a thought:



	
  * #() - literal Array

	
  * §() - dynamic Array, expressions separated by periods.

	
  * #{} - literal Dictionary, literals separated by periods, support for associations as literals.

	
  * §{} - dynamic Dictionary, expressions separated by periods, associations created as usual using sends.


Yeah, right, how would we ever be able to reach concensus on a leading dynamic character? :) Also, I do think it is wise to syntactically indicate literal vs dynamic, heuristics only lead to developer traps. Better to clearly indicate intention.


# Tirade


[Tirade](http://www.squeaksource.com/Tirade.html) is a format I created for Deltas (ChangeSets improved) and I have written [four](http://goran.krampe.se/2009/03/16/tirade-a-file-format-for-smalltalkers/) articles [about](http://goran.krampe.se/2009/03/20/tirade-part-2/) [it](http://goran.krampe.se/2009/04/20/tirade-first-trivial-use/) [earlier](http://goran.krampe.se/2011/04/15/tirade-supporting-embedded-text/). Now, if I would at this point subjectively rank the formats along a few axis it could look like this:



	
  * **Interoperability**


	
    * JSON: 100% (all languages has it)

	
    * STON: 70% (one could probably tweak a JSON parser in any language to work)

	
    * Litarrays: 30% (could get higher score if we limit them, a parser would still have to be written)

	
    * Tirade: 20% (same problem as with literal arrays, but even more advanced to parse)


	
  * **Capability**


	
    * Tirade: 100% (has the most features and options, by some margin)

	
    * STON: 60% (second best, still not much better than JSON)

	
    * JSON: 50%

	
    * Litarrays: 40% (severely limited by lack of assocations but has a some features to compensate)


	
  * **Grokkability**


	
    * JSON: 100% (well documented, we all know it and so does the rest of the world)

	
    * STON: 90% (rides on JSON)

	
    * Litarrays: 80% (not hard but has quite a few quirks)

	
    * Tirade: 70% (more or less as hard as literal arrays, but with a few more concepts added)



Conclusions from the above? Before looking at Tirade I think we can safely say that **JSON is a strong choice**. STON is IMHO in limbo, I can't see picking it instead of any of the others in a given situation, sorry. Literal arrays could easily become the obvious "JSON for Smalltalk" if it had associations/literal dictioneris, it sucks for interoperability though.

Tirade on the other hand **has associations** (on two levels one could even claim) so it can be viewed as "JSON++ for Smalltalk". But with more features comes a slightly higher learning curve and a penalty in interoperability. We now have set the scene for the last section about Tirade.


# Tirade


Obviously I am partial, since I created Tirade. But let me try to contrast Tirade to all the others. Note that Tirade was never meant to be interoperable with other languages, it was however designed to be interoperable between different Smalltalk implementations, or at least all Squeak derivatives.


## A stream of messages


First of all, Tirade is slightly different than the others. They describe a single structure. A valid Tirade "document" on the other hand, is a series of "records" terminated by periods. Each such "record" looks like a Smalltalk message (but without a receiver on the left side), either a unary or a keyword message, like this:

    
    unaryMessage.
    key: 'Hello' word: 'world' message: 4711.


This high level view as a "stream of messages" gives us several nice properties:



	
  * The selector of the Tirade message is a kind of record "type". It normally maps to a method on the receiving end that handles this record. That method then knows what to do with the arguments, and thus we don't need to hard code class names into Tirade, like STON does. **NOTE: This is not a security problem.** There is nothing forcing the parsing end to just blindly perform these messages. In fact, there is nothing forcing the parsing end to be specific at all, it could just be a generic Tirade parser.

	
  * If we look at a keyword message we realize that it is very similar to a JSON object, it is basically a "naked dictionary" where each key word is... right, a key! :) So for simple data we need perhaps not make it more complicated than this.

	
  * It makes it very easy to extend a Tirade format by simply adding new message selectors that the receiving end can ignore if it wants to.

	
  * Since Tirade is a flow of messages instead of a single, potentially quite large, structure like the other three formats, we can naturally stream it and handle each message one by one.

	
  * And since we have this flow we can also use "control messages" that can instruct the receiving end on how to receive the messages coming next in the flow. One could even use Tirade over a bidirectional link (a SocketStream for example) and do handshaking and client server communication with it.

	
  * Finally, in between Tirade messages one can add Smalltalk style comments which are simply skipped by the parser. JSON and STON has no concept of comments.




## Smalltalk literals


The next level of Tirade is what kind of arguments we are allowed to put in between the keywords. Basically its most kinds of Smalltalk literals with some additional constructs. I would also like to point out that this part is not encarved in stone, I am still contemplating the best mix of literal support here. But the main point is that **we only allow literals - no expressions**, so there is no generic "eval" going on here.

Notable differences again compared to JSON/STON on the atomic level are just like with literal arrays:



	
  * Strings are Smalltalk strings, no escape codes except for double single quote for single quote.

	
  * Numbers are Smalltalk literal numbers, in fact we rely on the number parser of Pharo/Squeak. This gives us a rich notation for numbers, at the expense of possible portability issues with other Smalltalks.


**NOTE:** Tirade doesn't currently implement Character literals nor ByteArrays, both can of course be added.

Let's continue with the added features for literals.


### Literal feature: Verbatim strings


A problem with JSON for dealing with readability is that JSON strings can't have newlines in them! So if you want to store source code in JSON it will end up as a single very long line.

Smalltalk strings like in Tirade can have newlines in them, but they suffer from double quoting of single quotes and the problem that the single quotes surrounding the string needs to be first on the first line and last on the last line, which makes it less readable.

This is why I came up with verbatim strings in Tirade, specifically for being able to contain unmodified source code in a readable way with no escapes whatsoever. I am not sure if this is the best approach, perhaps here-docs would be a simpler approach, but currently a verbatim string looks like this:

    
    some: 1 message: 'hey' withVerbatimStringForCode: [
     This is untouched, perfectly unescaped source code, ANY character combinations will work!
     Tirade will split the input on each CR (byte = 13) and then prepend each line with a TAB character.
     This means that the parser can detect the end by looking for the first line starting with "]",
     that must be the end of the verbatim string since all other lines start with TAB.
     Copy paste will work but you will need to care for the TAB indentation, but most editors
     can do that easily. Also, right before and after the string there is a newline added to improve readability.
    ].




### Literal feature: Associations


Since we really want to be able to do dictionaries I first added literal support for Associations. This means "->" is a literal syntax for creating an Association, it doesn't need to be in a Dictionary, you can use them wherever you like and the key and value can be ANY literal construct allowed by Tirade, even an Assocation!

Note though that we do not have parenthesis in Tirade (no expressions at all) and the current Tirade parser is a recursive descent bottom up parser so the code below will produce an Assocation with key #key and value an Association 123->'123'. In Smalltalk where #-> is a message this is instead executed from left to right creating a different result.

    
    cool: #key->123->'123'.


This also means that Tirade can have associations inside literal arrays, which is not syntactically possible in Squeak/Pharo:

    
    cool: #(12->'123').


Finally, since Amber lately added #{} syntax for Dictionaries I think it could be a worthwhile addition to Tirade also.


### Literal feature: Dynamic arrays as literal


Tirade supports {} style arrays, but doesn't allow expressions so they are very much like normal arrays except they do not remove #-prefixes from nested arrays/symbols and they look more natural to Squeakers since Squeak allows Association literals inside them:

    
    cool: {12->'123. 'banana'->true}.


Is it worth supporting both kinds of arrays? It depends, either Tirade defines a literal subset that is as small as possible, or Tirade tries to cover all literals of Pharo. I was leaning towards a subset but perhaps a super set is more attractive to people.


# Ending thoughts


I hope this article explained a few things and made at least Tirade a bit clearer. There are several things not fully settled in Tirade and if anyone wants to dig in and tweak it, feel free to email me.

regards, Göran

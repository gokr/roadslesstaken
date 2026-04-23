---
title: Tirade, first trivial use
date: '2009-04-20 00:43:55'
slug: tirade-first-trivial-use
categories:
- Old blog
- Pharo
- Smalltalk
- Squeak
- Tirade
---
Last night I started hooking [Tirade](http://goran.krampe.se/2009/03/16/tirade-a-file-format-for-smalltalkers/) into Deltas. Quick background: Deltas is "Changesets for the 21st century", or in other words an intelligent patch system under development for Squeak. Tirade is a Smalltalk/Squeak centric "JSON"-kinda-thingy. I made Tirade in order to get a nice file format for Deltas. Just wanted to share how the first trivial code looks, and thus illustrate simple use of Tirade.

I have a DSDelta (a Delta being almost like a ChangeSet). It consists of some metadata (a UUID, a Dictionary of properties and a TimeStamp) and a DSChangeSequence (which holds the actual DSChange instances). As a first shot I only implemented the metadata bit. So step by step:



	
  1. Write a unit test, first let’s set up our readers and writers on a common stream:

    
         setUp
             | stream |
             stream := RWBinaryOrTextStream on: String new.
             reader := DSTiradeReader on: stream.
             writer := DSTiradeWriter on: stream





…then a trivial write, read and compare test - note that they both look at the same stream:

    
            testEmptyDelta
    
                | delta same |
                delta := DSDelta new.
                writer nextPut: delta.
                reader reset.
                same := reader next.
                self assert: same = delta.
                self assert: delta timeStamp = same timeStamp.
                self assert: delta properties = same properties.
                self assert: delta uuid = same uuid





	
  1. Create DSTiradeWriter. It turns out that DSTiradeWriter at this point is just an empty subclass of TiradeRecorder! Eventually we might need to add behaviors but at this point there is no need. The TiradeRecorder uses DNU to intercept messages and encode them as Tirade.

	
  2. Implement #tiradeOn: in our domain object DSDelta. This will be used by the writer and looks like this:

    
         tiradeOn: recorder
    
             recorder
                 delta: uuid asString36
                 stamp: timeStamp printString
                 properties: properties





…here we convert the UUID to a String (base 36) and the timeStamp too. The properties Dictionary just holds "simple" data that Tirade can represent, so no need to convert it. The rule is that we make up a message (in this case #delta:stamp:properties:) which will be used in the Tirade stream, and we make sure our arguments are "Tirade proper" which basically means Booleans, Strings, Symbols, Arrays, Numbers, Associations and Dictionaries thereof. Note that the recorder being a DSTiradeWriter inherits the implementation of #doesNotUnderstand: from TiradeRecorder that will write this Tirade message onto the stream typically looking like this:

    
            delta: 'd71oknvt1bwswhno6iwgund07' stamp: '20 April 2009 11:20:50 am' properties: nil.


And then the final step, our reader:



	
  1. Creata a DSTiradeReader. We simply create an implementation of the above Tirade message #delta:stamp:properties: and put it in the method category "tirade" so that the default security mechanism is happy:

    
         delta: uuidString36 stamp: timeStampString properties: properties
    
             result := DSDelta new.
             result uuid: (UUID fromString36: uuidString36); properties: properties; timeStamp: (TimeStamp fromString: timeStampString)





…this class inherits an instvar called ‘result’, which is fine to reuse. As you see the properties needs no conversion, the others are converted from Strings.

And tada - the unit test is green! So we implemented reading and writing in more or less two lines of code. Kinda neat! :)

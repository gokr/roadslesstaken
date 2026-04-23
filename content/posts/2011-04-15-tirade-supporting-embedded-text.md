---
title: Tirade, supporting embedded text
date: '2011-04-15 01:22:58'
slug: tirade-supporting-embedded-text
categories:
- Pharo
- Smalltalk
- Squeak
- Tirade
---
Two years ago I ended up creating [Tirade](http://goran.krampe.se/2009/03/16/tirade-a-file-format-for-smalltalkers/) - a new "file format" for Smalltalkers. Or rather, a way to serialize stuff into a sequence of Smalltalk messages with literals as arguments. I have written a [few blog articles about Tirade](http://goran.krampe.se/category/tirade) so I will not go into details in this one.

One thing that has been disturbing with Tirade is that I wanted it to be the main format for serializing Deltas, the new implementation of "21st Century ChangeSets". This means I want Tirade to handle Smalltalk source code in the best possible way. Ideally I would want the Tirade file to be editable in a text editor if I wanted, and not being broken by that.

So, what properties do we want:

	
1. **No escaping of special characters.** In regular Tirade strings (just like in Smalltalk) need to escape the single quote as doubled single quote, and that would suck for Smalltalk code of course.
	
2. **No length encoding.** One way to avoid escaping is to store the length of the data before the actual data - like a [Netstring](http://cr.yp.to/proto/netstrings.txt) for example. This prohibits easy editing in a text editor though, since that would change the length.

3. **A reasonable syntax.** Tirade so far has been a subset of Smalltalk (disregarding lack of receiver to the left), but I think we might have to break that a bit here.


After pondering this for a while I have come up with this solution which feels kinda nice, but **if someone has an even better idea I am all ears**. This is how it could look embedding a method source in Tirade:
	class: #MyClass selector: #at:put: source: [
		at: pos put: arg
		"Put something here"

		^array at: pos put: arg
	].
So what gives here?  We are reusing the syntax for Smalltalk blocks without arguments. Simply [...content...]. The content will be delivered as a String and the guarantee is that it will be received exactly as sent. There is a trick here - this is what Tirade will do:



	
1. Write the starter $[ and then a CR
	
2. Before each line in the string (a line being all characters up to and including the next CR or up to end) we insert a TAB. This means that the String begins on the line after the opening $[ and all lines will be prefixed with a TAB.

3. Then, regardless if the last line ended with a CR or not - we add a CR before the closing $]. This makes sure the closing $] ends up on its own line.


The above trick gives us the ability to detect the end of the string because if a line starts with something else than a TAB then we have reached the end. Thus we do not have to escape the $] inside the string and we still don't need to do length encoding. **We DO however need to make sure all lines begin with a TAB, but if you are editing a Tirade file you should just learn that fact. :)**

I am not sure if the above is a good solution, but it is ONE solution and I can't come up with a better one, unless we would use a really "odd" marker at the end in order to not have to escape it, but that feels "dirty" to me.



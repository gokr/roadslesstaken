---
title: ESUG in Annecy Day 1
date: '2013-09-09'
categories:
- Programming
- Languages
- Computing
- Smalltalk
- ESUG
---
Here we go! Time for a week of Smalltalking fun in [IAE Universite Savoie Mont-Blanc](http://www.iae.univ-savoie.fr) in Annecy. 

While [ESUG](esug.org/wiki/pier/Conferences/2013) this year is not super big, I think **around 110 people** or so, there were still quite a few arms raised when checking how many were here for the first time. The organisation seems impeccable, as always - thank you Stéphane Ducasse, Herve Verjus, Laurent Laffont and of course all volunteers!

Enough chit-chat, let's get on with the talks...

<!--more--> 

## VA Smalltalk Product Update and Roadmap

We started off with news from [Instantiations](http://www.instantiations.com) with John O'Keefe. Instantiations is evidently growing and has been able to employ more engineers, nice! And tada, a new release, [v8.6](http://www.instantiations.com/products/vasmalltalk/whatsnew.html)! And the most notable change seems to be the new [Scintilla](http://www.instantiations.com/PDFs/presentations/STIC2013/Modernized%20Text%20Editor-STIC%202013.pdf) based text editor. Also a lot of small tweaks to the debugger and other tools.

[Seaside](www.seaside.st) and [GLORP]() are two very important open source tools for companies that want to build web apps in VAST. Seaside obviously, being the mature (IMHO outdated by now, but still important given its maturity) web framework of the Smalltalk world. And GLORP for any larger company where data of course lives in some RDB. Upcoming planned features include 64 bit support and improved GC, and a lot more.

Although I am not using VAST (though I did back in the 1990s for some projects) it is very nice to hear its still live and kicking. Note though that these tools are not cheap - they are very mature development tools aimed for large enterprise customers. On the other hand they have special offers for [open source developers](http://www.instantiations.com/company/open-source.html) and academia.

What I find interesting is how these companies handle the furious evolving industry, do they know how to play well with open source? Do they understand how to attract new customers? Instantiations seems to be doing well but I can't stop wondering if they are attracting new customers or living on their old base. In any case I **wish them all the best**.


## MVC Revival on the Web

Next up was Janko Mivsek going through MVC. The history is quite interesting, going all the way back to 1978/79 when Trygve Reenskaug created this pattern when he visited PARC. You can google all this and if you don't know the history I think it is worth reading about it because MVC is such an "abused" term these days.

Pretty soon Janko moved over to present day and the onslaught of javascript frameworks for "MVC". Backbone.js, AngularJS, KnockoutJS, Ember.js blablabla... :) Personally I haven't looked at these, but perhaps I should! And of course, how does [Amber](http://www.amber-lang.net) fit into these ideas...

## Beach Parasol

Web testing. So... how to use Selenium WebDriver (instead of the older Remote Control?). A quite interesting presentation on how to do web testing of Seaside (or other apps) using this from within Smalltalk. 

...and then my attention kind of drifted, sorry guys. The presentation **Towards a Smalltalk VM for the 21st Century** was interesting, Boris showed how to use a low level full system simulation like Simics to put a breakpoint into the VM machine code and then go in and inspect registers and memory when it is stopped. Another very interesting capability is to "record" execution and then go back and replay to find critical timing bugs for example - you know, those "Heisenbugs" that hide themselves when you step in the debugger.

The evening moved onto the **Innovation Technology Awards** where we had the chance to see 10 (or so?) projects being presented by the authors while the rest of us drank beer and wine. :) Really nice and IMHO the clear winner **should be** [Amber](http://www.amber-lang.net). Ok, so I may be a bit partial, but Amber is such a true **tour de force** in crafting a whole new Smalltalk including a really nice modern compiler toolchain, slick and fast IDE running inside your browser and now **even a stepping debugger** through the brilliant move to implement an Amber AST interpreter in Amber, thus enabling interactive stepping of Amber code.

## Evening

Bus downtown and long interesting talks into the warm night. :)

Over and out.

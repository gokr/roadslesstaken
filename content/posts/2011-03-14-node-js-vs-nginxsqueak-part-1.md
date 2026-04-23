---
title: Node.js vs Nginx/Squeak, part 1
date: '2011-03-14 16:55:58'
slug: node-js-vs-nginxsqueak-part-1
categories:
- Conferences
- Smalltalk
- Squeak
- Web tech
---
Hmmm, after seeing the [Node.js](http://nodejs.org) presentation at [Dyncon 2011](http://swdc-central.com/dyncon2011/index.html) I couldn't help installing Nginx and Blackfoot (SimpleCGI) in a Squeak 4.2 image running on the Cog VM to make some performance tests! In fact I started doing that during the presentation. :)

My first run on Nginx/Squeak looked quite unimpressive. Well, one client doing 1300 req/s to a small helloworld was decent although Node.js handled approximately 2x that. With Nginx we have a two tier solution so a factor of 2 is not really surprising in this trivial case. Top showed similar load, both solutions only seem to consume 8-9% of my CPU power on this box, but the Nginx/Squeak solution of course spreads load between them with approximately 1/3 or 1/4 on nginx.

But jacking up concurrent clients really destroys Nginx/Squeak! How come? I was surprised because my memory of this when I wrote Blackfoot was that it was handling that fairly ok. Trying 50 concurrent clients with Node.js pushes it up to almost **8000 req/s**! Quite impressive and it still only uses about 9% of my CPU power. Blackfoot ends up serving less than 1/10nth of that. Now, thinking and looking more closely it is quite obvious - SCGI opens **a new connection for each request... ouch**. Why on earth did they design SCGI like that? So basically Nginx will hammer Squeak just like we hammer Nginx I guess, and Squeak doesn't deal with that too nicely.

A small experiment with firing up 3-5 Squeak backends and letting Nginx load balance over them (really simple to do) shows that we can get around this somewhat and scare Blackfoot into serving over **3000 req/s** and still not going over 30% CPU. Not that shabby, but still not in the same league as Node.js, but now we know why - we need a solution that holds the connection open between Nginx and the backend.

At this point I wanted to try three things:



	
  1. What numbers can Nginx on its own produce, just returning a small HelloWorld file?

	
  2. What numbers can plain KomHttpServer running on Cog produce?

	
  3. And finally, how does Nginx/AJP/Squeak behave? AJP does keep the connection open I think.


Let's guess first - plain Nginx should beat Node.js, Kom with Cog is probably not much faster than regular Squeak VM since the issues I believe are in the Socket plugin (and we saw that it didn't like getting hammered by Nginx), and finally I am hoping AJP puts Squeak at say half Node.js even with 50 concurrent clients, that would be 4000 req/s and I would be darn happy. And of course, with a load balancer on top even more, but that can be done with Node.js also of course.
So more on that next time...

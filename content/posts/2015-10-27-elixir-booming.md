---
title: Elixir Booming
date: '2015-10-27'
slug: elixir-booming
categories:
- Elixir
- Functional
- Languages
- Programming
---
It seems like the *"damp cloth of Java"* that has been plastered all over the programming landscape the last 20 years is finally being lifted. I admit, I do **dislike Java ...immensely**. And not only on technical grounds, but even more based on what I perceive as it's community worshipping complexity for it's own sake. Of course IMHO.

These days new and **truly interesting languages** are all over the place. [Rust](http://rust-lang.org) and [Go](http://go-lang.org) are two examples with a lot of momentum, although I personally choose [Nim](http://nim-lang.org) over both.

And [Smalltalk](http://pharo.org) is still my "super productive dynamically typed" language of choice, but I just learned about a language that I **really** think is going places...

<!--more-->

[Erlang](http://www.erlang.org) has always been on my todo list, and I did try once or twice but frankly, the language seemed a bit primitive. But anyone with any clue about Erlang also knows it is extremely strong in the area of **robust, forever running and very scalable distributed systems**.

Erlang got a revival with the new focus on highly distributed systems, especially the emerging NoSQL database systems - it fit like a glove. [Riak](http://basho.com/products/#riak) from Basho is perhaps the most obvious example of these systems. And [WhatsApp](http://www.fastcompany.com/3026758/inside-erlang-the-rare-programming-language-behind-whatsapps-success) is the latest **$19 billion** poster child for the Erlang story.

## Enter Elixir

But now things are **heating up significantly**. In 2012 [José Valim created Elixir](http://www.infoq.com/interviews/valim-elixir), a new language targeting the Erlang VM. [Elixir](http://www.elixir-lang.org) manages to be true to the core Erlang ideas and is very compatible with the Erlang eco system - but at the same time it brings a whole lot more to the party. And it is [making a buzz](http://www.creativedeletion.com/2015/04/19/elixir_next_language.html) for sure, [even Joe Armstrong likes it](http://erlanginside.com/en/article/408/joe-armstrong-s-a-week-with-elixir) (one of the core Erlang creators).

José Valim comes from the RoR community, having been a core developer there, so a lot of the Ruby people, including [Dave Thomas](https://pragprog.com/book/elixir/programming-elixir), are [hopping aboard](https://medium.com/@kenmazaika/why-im-betting-on-elixir-7c8f847b58#.nqhssr9vk) the [Elixir express](https://www.youtube.com/watch?v=5kYmOyJjGDM).

And that inevitably brings us to the primary web framework of Elixir called [Phoenix](http://www.phoenixframework.org/) mainly developed by Chris McCord and [reaching 1.0 just two months ago](http://www.phoenixframework.org/blog/phoenix-10-the-framework-for-the-modern-web-just-landed). Phoenix is picking up the challenge to create a "Rails killer" in Elixir and [this presentation is one of the most informative on it](https://www.youtube.com/watch?v=STO-uN0xHDQ).

But not only is Elixir and Phoenix attracting the interest of web developers that want a fresh air of truly stellar performance (especially compared to RoR) - it is also [making a dent in the embedded world](http://nerves-project.org/) due to its extreme robustness and ability to do hot code deployment, see [this presentation](https://youtu.be/kpzQrFC55q4).

The more I read and browse the more I find. Real world success stories, books, blog articles - truly impressive given it's only been **approximately a year since the language hit 1.0**! The IRC channel has more than 450 people, almost twice as much as Rust has, still half of Python or Go but let's check again in a few months. ;)

Several Erlang people tend to describe [Elixir as a logical next step for Erlang](http://www.theerlangelist.com/article/why_elixir), which means it is blending in with the already well established Erlang community. This is a big plus. As an example Elixir's package manager is [Hex](http://hex.pm) but it can also do Erlang packages and may very well turn into the main package manager for the whole Erlang eco system.

## The Boom

Given how it looks I think Elixir is about to go big. It is a stellar language for scalable systems and [Phoenix brings it to the web](https://www.youtube.com/watch?v=STO-uN0xHDQ) arena leaving RoR completely in the dust performance wise. Elixir also utilizes all your cores (well, it's what Elixir gets for free from running on BEAM), without the significant burden of the asynchronous "code mess" that NodeJS and similar asynchronous solutions has forced us to endure. And that pain didn't give us multicore anyway!

This means Elixir has a great position to catch **both the Rails and the Node developers** with a superb offering. Javascript will still be king on the frontend (browser and hybrid mobile) for the foreseeable future, but on the server side I think all the dynamic web frameworks will get disrupted by Phoenix. This means typically all the frameworks for Node, Ruby and Python.

Phoenix is also [perfect for the new style of connected HTML5 apps](http://www.phoenixframework.org/blog/phoenix-10-the-framework-for-the-modern-web-just-landed#the-real-time-web) - the modern web. Yeah, it's funny, we are back to the client server architecture for sure. So does that scale? It [sure as hell seems to](https://twitter.com/chris_mccord/status/658767562231185408). See Chris talking about [what comes next in Phoenix](https://www.youtube.com/watch?v=-7Q3bD4qSVE).

Elixir has a lot of checkboxes checked:

* Very strong and vocal lead developers (José Valim, Chris McCord and more)
* Good tooling
* Growing list of packages
* Several evangelists
* It's own conference
* It's own web framework
* Several books published
* Natural path to both Rails and Erlang people

Here is a [nice terse introduction for the impatient](https://sendgrid.com/blog/intro-elixir-lang/). You can also read the official [Getting Started](http://elixir-lang.org/getting-started/introduction.html), but it has evolved into more of a language manual.

I am going to see if I can get my Raspberry Pi (that I got from my brother as a christmas gift) to run some Phoenix...

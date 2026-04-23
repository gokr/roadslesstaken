---
title: Elrond and NEAR
date: '2021-04-21'
slug: elrond-and-near
categories:
- Elrond
- NEAR
- EGLD
- Crypto
---
Back in 2018 I got into crypto currencies. I ended up focusing on [Nano](http://nano.org) and built [Canoe](https://getcanoe.io), a cross platform (mobile and desktop) wallet for Nano. Nano is **crazy fast** (one or a few seconds) and has **zero fees**. For payments it's superb and the architecture of Nano is clear and simple. I still have a lot of respect for Nano, but... 2020 taught me one thing - smart contracts are actually not just a gimmick.

So for me, sorry, Nano is not a project "of the future"!

I accidentally got involved in the DeFi world in the [CORE](https://cvault.finance) project, which runs on top of Ethereum. My contribution was just making a cross Discord/Telegram chatbot, [RoboCORE](https://github.com/gokr/robocore), and writing a bit about "floor price calculations" but the whole DeFi landscape convinced me that smart contracts are **an essential ingredient in a modern crypto currency platform**.

Real true scalability is also mandatory, which IMHO really has to boil down to sharding, even if novel faster consensus models are damn cool like Avalance has (the Snowflake consensus protocol).

So back to googling and reading ... and there are two projects that so far stand out in my book:

* [Elrond](https://elrond.com)
* [NEAR protocol](https://near.org)

<!--more-->

...ok, so there are tons of so called "eth killers" out there. I have looked at least a little bit on most of them by now.

## Elrond

I find Elrond to be one of the most promising. Strong solid development focus, just like Nano always had. But also **good marketing** which Nano sucked at, yup, it's the truth. Sub second transactions? No, but Elrond does them in 5-6 seconds which is just below the magical threshold in order to be useful for payments.

Zero fees? No, not zero, but very very low. And while Nano's idea of using a bit of PoW as payment is pretty neat, it still suffers from the "spam problem" (although recent developments may have solved it, unsure), so a low fee is probably a smarter more practical route to take. Elrond can also shift the fee to a third party so that end users can use a system feeless, that's clever and very useful.

The Elrond team is primarily in Romania but seems to be doing a great job in maintaining a good community. They also realize that the end users are key - so they also made [Maiar](https://maiar.com) which was relatively recently released. It's a very slick and smooth mobile wallet for EGLD (eGold) which also **maps phone numbers and so called "herotags"** to accounts. That last part is a brilliant move by the Elrond team.

When we made Canoe for Nano we also implemented a system for "aliases" (like herotags, we even used "@" as prefix) but... since it was not "on chain" it suffered from fragmentation with several different implementations and security risks in abundance. So putting this **on chain** is really the ONLY solution, and it is a true enabler.

Maiar takes your phone number, hashes it and then associates the hash with the Elrond account of your wallet, and stores it on chain. Net effect is that as Maiar (or other Elrond wallets) virally spreads to more people - you will be able to see which of your existing contacts in your phone **already has an Elrond account** and can be sent EGLD. Very nice indeed. At the same time, the phone number is not revealed, since it's a hash being stored.

Elrond seems to have a very good base with a properly sharded design up and running on mainnet and several pieces being put in place. It also made a true run in value early 2021, **from about $25 and quickly up over $210**. It's probably a good bet it will continue climbing, but hey, not financial advice of course ;)

## NEAR Protocol
Another contender in the ethereum killer space is the NEAR protocol. It's a technically **very** capable project that has a more "grassroot, down to earth" feeling. Not as much marketing as Elrond, which to be honest sometimes gets a bit over the top for my taste. I mean, how many meaningful "partnerships" can a project really have?

NEAR has that "community feeling" that I like a lot, even the website is a **.org and not a .com**. No nonsense, tech first, developers first. And technically it might be one of the strongest projects around, even Vitalik Buterin has acknowledged that NEAR may present itself as a worthy challenger to Ethereum 2. Very fast finality, a solid sharded design. And to be frank, I love the website style with documentation and developer focus!

I haven't dwelved that deeply into NEAR yet, but they also have a clever DNS based account naming model similar to EGLD. And no, there is no official mobile wallet (there are other multi currency wallets supporting NEAR), but... in some ways it may be a strategy more in line with the grassroot model of NEAR. NEAR focuses on the platform and might be better off leaving things like mobile wallets to external parties.

## Conclusion
There are lots and lots of new smart contract platforms out there vying for a bit of the "Ethereum cake". Will Ethereum 2 deliver and make all other obsolete? Will the future have room for 10 or 20 different platforms? Or will 2-3 of these new kids on the block (sorry for the pun) step up and take over?

I have no clue but it seems to me that:

* Ethereum is struggling now due to **insane** gas costs, projects are scrambling for alternatives.
* Ethereum 2 seems too far in the future before it starts being useful.
* Elrond and NEAR are two of the most interesting competitors, and they are **working right now**.

Elrond is at the time of writing at **$3,315,197,861** in market cap with 55% in circulation. NEAR is at **$1,770,738,752** with 36% in circulation. Elrond is 84x smaller market cap that current Ethereum.

Ok, so sorry, this article doesn't go into that much technical details. You will just have to learn yourself!

And no, nothing of the above is **financial advice**. ;)
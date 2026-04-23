---
title: CORE floor price musings
date: '2020-11-01'
slug: floor-price-musings
categories:
- CORE
- Ethereum
- Programming
---
I have already written [three different articles](http://goran.krampe.se/category/core) explaining how CORE floor price can be calculated. But just a day or two back the CORE team decided that using the floor price concept in communcation doesn't work out very well. Why? Because a LOT of people just can't seem to understand it properly and keep perpetuating wrong conclusions around it. In short - people can't understand math :)

A list of common misconceptions are:

* Floor price is the "correct value" of CORE and that the current price then must be too high
* Floor price is some kind of approximation and the price can actually go lower
* Floor price is a technical analysis support level
* Floor price can change if another market starts trading CORE lower
* Floor price can never ever go down in USD value
* Floor price can never ever go down in ETH value

And a whole bucket of other misconceptions - just pile it on! Let us start with an explanation of what floor price **ACTUALLY IS** and then go through the above list...
<!--more-->

The floor price is a **technical mathematical price that CORE can never ever go below** as long as:

* There are only 10000 CORE. And that's in the design of CORE, so can not change.
* Uniswap pricing mechanism isn't changed. That's in the Uniswap v2 contract so can also not change.
* The CORE contracts forbid liquidity tokens to be converted back to the underlying assets. In other words, you can not remove liquidity from a Uniswap CORE trading pair after you have added it.

These three pillars were listed in my first article, but I list them here again. These three facts **work together** to create the price floor.

Ok, so... first of all - if we could mint more CORE, then of course price would go lower. If you suddenly double the supply of COREs the price would promptly go to half. So a fixed supply is very important. Secondly, the insight that the price on Uniswap is not a price set by the "sellers", it's not governed by any human at all, it's just governed by math. There are tons of articles on how this works and my first article did explain it carefully.

How does the price go down in the first place? If people don't want to hold CORE and decide to sell it, then price goes down. Let's pretend the CORE holder world consists of Lisa, Peter and John. They all have 1000 CORE each. The rest is in the Uniswap trading pairs. If Lisa decides to sell all her CORE it will end up inside one of the pairs, and she will get ETH or CBTC in return. The price of CORE goes down (Uniswap math, pillar two), as well as the pile of ETH (or CBTC) in the pair she sold into (Uniswap math, pillar two), since she got ETH (or CBTC) in return.

If John and Peter also sells all their CORE then all CORE is suddenly in the trading pairs. No CORE is held by any other party. Since there is no more CORE, remember - we can't mint more CORE, then there is no more CORE to sell into the pairs. The maximum of CORE that can be in the pairs, is thus 10000. See pillar one above.

At this point, is there ETH and CBTC still left inside the pairs? **Yes there is!** The sum of all that ETH and CBTC is what we like to call **the TVPL - Total Value Permanently Locked**. The word "permanently" here implies that this big chunk of value can never ever be removed from the pairs, because the only way to "get" that ETH and CBTC is to sell CORE into the pair, but there is no more CORE to sell!

Ok, but what if ... the people who provided the liquidity into the pairs in the first place came and removed it? Ah. Right. They can't. That's the third pillar above. The contracts of CORE have that distinguishing feature - that once you added liquidity and got a Liquidity Pool token in return - then you can't reverse it.

I hope it's clear at this point that if all CORE is sold, we would end up at the lowest price. The fun part is that this price can be calculated, because Uniswap has such a clean mathematical pricing formula. It's not governed by supply and demand - it's governed by simple plain math.

Now... let's take a look at all misconceptions.

## Floor price is the "correct value" of CORE and the current price must be too high
There is no human involved in "deciding" or "setting" the floor price, it's just a mathematical boundary. But the **value of CORE is up to us to decide**, that depends on expectations going forward and so on, just like the value of a stock or some other valuable. The only reason CORE to actually ever get anywhere close to the floor price would be a **total freaking disaster** in the CORE eco system, making everyone feel that CORE is simply worthless! And everyone would decide to panic sell. I guess one could say that other clones of CORE have "tested the floor price concept", by failing miserably to deliver on promises and thus people have decided that hey, this is a worthless clone - and sold. But yes, even in such a disaster - the price simply can't go to zero.

An analogy would be if we could go to a vault, and put in 1 ETH, and get an IOU-note back. And at any point in time I can go back to the vault and exchange that IOU back to the 1 ETH. Now... I can sell that IOU to you, but I would be daft if I sold it for 0.5 ETH, because you can always go and exchange it for 1 ETH. So ... in a similar way CORE also has this base value locked away, the TVPL, so that you can always sell your CORE for **at least** the floor price - around $633 at the time of writing.

But CORE is a project, en endeavour, with plans going forward and a team and community delivering on the plans. Thus it has a promise of future earnings and that is what drives the current price. The floor is of course an interesting factor in all this, the fact that there even is a floor is a strength of CORE.

## Floor price is some kind of approximation and the price can actually go lower because anything can go to zero value
No. There is no human that has made any kind of estimation or valuation here. The floor price is just a mathematical truth. But sure, it does depend on certain factors - like we need the Internet to keep working and the Ethereum blockchain must still work, since the CORE ecosystem is built on Ethereum smart contracts.

The dependence on Uniswap is quite small and could relatively easily be replaced. But yes, if World War III kills the Internet - then CORE is quite worthless. But so would lots of other currencies be at that point.

## Floor price is a technical analysis support level
No, no, no. A support level is just an imaginary construct - it's a "level" we humans see when we study a chart. We notice perhaps that an asset tends to stay above a certain price over a period of time, and then one of us decides to call that a "support level". Technical analysis has nothing to do with the floor price.

I am trying to lose some weight, I have been hovering around 88 kg but I want to get down to 83. Evidently there is some kind of "support level" around 88 kg :) but... depending on choice of mathematical models I could argue with decent certainty that **floor mass for me is 12.5 kg**. I promise that it's impossible for me to have less mass than that, because that is the mass of my skeleton. Ok, so first draft of this article I claimed floor mass to be 0, but it felt a bit silly. The clever reader noticed me choosing the word "mass" instead of "weight" since I actually do weigh 0 kg in space, but my mass is for sure more than 12.5 kg. Perhaps not the best analogy to pick!

## Floor price can change if another market starts trading CORE lower
This is interesting though. There are already other markets for CORE than the two trading pairs on Uniswap. Hotbit and Gate are two CEXes evidently offering trading in CORE, but they all currently trade at a slightly higher price than on Uniswap. Those markets follow supply and demand, using an order book, so don't play by the same rules so to speak. But arbitrage ought to work in the direction of making the price similar. But remember - floor price is **the ultimate disaster scenario**. What would happen? Noone would want to buy CORE on those CEXes in such a panic sell off, so all sellers would flock back to the trusty Uniswap because Uniswap **always buys from you**! So all CORE would still flow right back into the AMM pairs, and we would still hit the same old floor. So other non AMM markets have no real impact on the floor price, at least to my current understanding.

But any new AMM pairs using Uniswap pricing model definitely impacts the floor price! When the next third pair is launched the floor price will take yet another jump upwards. And if any of the already existing CORE pairs on Uniswap suddenly starts getting liquidity - they would impact floor too.

## Floor price can never ever go down in USD value
Oh yes it can! When we had a single CORE-ETH pair then the floor was around 1.13 ETH. It could **never** go below 1.13 ETH. But the price of ETH in USD varies, so if we looked at the floor price in USD - then sure, it varied over time just as much as ETH varied!

But now we also have a second pair in CBTC. So the current floor price is actually **part ETH and part BTC**. This means the current floor price, which is around 1.66 ETH (it took a healthy jump from around 1.13 to 1.6 ETH when second pair was introduced) - should in theory actually be more stable, since one can argue that a portfolio consisting of part ETH and part BTC will have a more stable or balanced total value, than if it was only ETH or only BTC.

So it can go down in USD. But this movement is exactly the same as the movement of ETH and BTC.

## Floor price can never ever go down in ETH value
That was true, when we had just the CORE-ETH pair. Now it's not true anymore, because the floor value is part BTC also, so if BTC drops in value compared to ETH, then the total floor **valued in ETH** would go down. Similarly, if we valued it in BTC it could go down if ETH went down, in relation to BTC. Argh! :) But it's not a negative, on the contrary. The current mix of the floor value makes it more resistant to movements. And with the third DAI pair coming, it will be even more stable.

All of this is just per my own understanding of the concepts involved and should DEFINITELY NOT be taken as any kind of financial advice :) But if you ask me - the floor price is a great thing and it makes CORE quite unique. It's the solid bed rock underneath the house. We don't want to sleep directly on it, but we sure like it's there to keep the house steady.

Finally, here is a trivial [floor.ods](/files/floor.ods) spreadsheet where you can experiment with new pairs. By estimating amount of CORE in the existing and any new pairs the spreadsheet shows the new floor price.

Cheers, Göran
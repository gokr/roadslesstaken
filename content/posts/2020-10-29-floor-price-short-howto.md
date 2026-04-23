---
title: CORE floor price short howto
date: '2020-10-29'
slug: floor-price-short-howto
categories:
- CORE
- Ethereum
- Programming
---
In the previous [two](http://goran.krampe.se/2020/10/29/floor-price-revisited/) [articles](http://goran.krampe.se/2020/10/28/floor-price-in-core/) I explained the principles behind CORE's floor price, the lowest price that CORE can reach and ended it all by explaining the "q method" that works for any number of CORE pairs. For lots of people that was possibly an overdose of math, so ... here is the super short and **lacking any explanations on why** description on how to calculate floor price of CORE using the "q method".

<!--more-->

Find `q`. This is done by:
   
    q = (10000 - sum-of-all-CORE-in-all-pairs) / (sum-of-all-CORE-in-all-pairs)

Then take one pair, for example the CORE-ETH pair, and calculate floor as:
   
    floor = (poolCORE * poolETH) / ((poolCORE + 0.997 * (q * poolCORE)) * (poolCORE + q * poolCORE))

And that's it, so again, using the numbers at the time of writing (ask RoboCORE with command **!s** in Discord or **/s** in Telegram):

    q = (10000 - (3451 + 630)) / (3451 + 630) = 1.45037980887

And then:

    floor = (3451 * 33578) / ((3451 + 0.997 * (1.45037980887 * 3451)) * (3451 + 1.45037980887 * 3451)) = 1.62336028634

At this moment RoboCORE says floor is 1.6228 so yeah, **1.62336028634 is close enough!**

Cheers, Göran
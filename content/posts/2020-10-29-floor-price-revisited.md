---
title: CORE floor price over more pairs
date: '2020-10-29'
slug: floor-price-revisited
categories:
- CORE
- Ethereum
- Programming
---
In the previous article I explained the principles behind CORE's floor price, the lowest price that CORE can reach. It's a novel concept and a very interesting characteristic of CORE.

I showed the mechanisms involved and how to calculate the floor price, if we only have **a single** [trading pair](https://info.uniswap.org/pair/0x32ce7e48debdccbfe0cd037cc89526e4382cb81b) to worry about. I have also solved the equation for two trading pairs, that equation is currently used in RoboCORE with success.

But how to handle three pairs or more? Complexity seemed to spin out of control, but... it turns out **there is a simple solution!**

<!--more-->

...but before we get to the beautiful simple solution that works for `n` number of pairs, we need to really bask ourselves in the glory of complexity in solving it for two pairs using the obvious math used from the solution for one pair.

Without explaining the math too carefully (sorry), the equations from one pair suddenly got **a bit more complex**. Let's presume we are going to sell `X` COREs back into pair1, and the rest into pair2 - and afterwards the two pairs should have the same price, which will be the floor price.

For pair one we can formulate the new amount of ETH in the pool as `newPoolETH = k / (poolCORE + (X * 0.997))` taking the Uniswap fee into account. And using the fact that the rest needs to get sold into pair2, we then get `newPoolWBTC = k2 / (poolCORE2 + (10000 - poolCORE2 - poolCORE - X) * 0.997)`.

After these two trades are done the price of both pools should be equal to each other. The two price formulas are `price1 = newPoolETH / (poolCORE + X)` and `price2 = (newPoolWBTC / (10000 - poolCORE - X)) * priceBTCinETH`. So let's put them equal to each other:

    newPoolETH / (poolCORE + X) = (newPoolWBTC / (10000 - poolCORE - X)) * priceBTCinETH

...and we can expand `newPoolETH` and `newPoolWBTC` from the previous equations giving us this final big one:

    (k / (poolCORE + (X * 0.997))) / (poolCORE + X) = (k2 / (poolCORE2 + (10000 - poolCORE2 - poolCORE - X) * 0.997)) / (10000 - poolCORE - X) * priceBTCinETH

As a careful reader now notices we have **only one unknown** in the equation, and that is `X`! Yes! So we need to solve for `X`. And... that's where it get's really messy! I am not going further here, but let's just conclude that it can be done and that it turns into a second order equation with two potential solutions for `X`. Often we can ignore one of the solutions as impossible in practice. This math is currently used by RoboCORE and it calculates the floor price **exactly** for the two current CORE pairs we have.

## A Simple Beautiful Solution

Someone came up with the idea on Discord or Telegram (don't recall which one) that... perhaps all the pairs could be combined into a single pair, and thus the problem would be trivial even for many, many pairs? It sounded nice, but instinctively I felt that the "k constant" would sort of get lost in such a way of thinking.

But it was intriguing to find a solution for `n` number of pairs (since the third pair is probably juuuuust around the corner) so I started playing around in LibreOffice Calc. After an hour of juggling numbers and mainly goofing around it dawned upon me that... there is a solution that is so simple it's almost ... unbelievable!

## The Assumption
Let's pretend we have `n` pairs. The problem we need to solve is still how to distribute the remainder of CORE outside of the pairs into the `n` pairs so that they **all end up having the same price** (in ETH for example, or USD). There is an assumption we can make that can be used to make this much simpler and that is presuming that **the pairs have the same price already**. At least within say 1-2% or whatever small margin we allow. If they wouldn't, then someone would arbitrage and make them get close again. So the assumption seems fine!

Aha! So the problem suddenly is easier. We just need to distribute our CORE so that **we change the price with the same factor** for all the pairs. Because if they already are the same price, and we change the price with the same factor, then they damn well ought to still be the same after we have poured our last COREs into them!

Ok, how was the price formulated for a pair now again? The current price is just `poolCORE / poolZZZ` (where ZZZ is ETH or CBTC at the moment, depending on pair). Ok, that is not helpful because the **new price depends on the amount of CORE we sell into the pair**. So, we need to figure out how much CORE to sell into each pair, to make sure the price is changed **with the same factor**.

Let us recall the Uniswap math from above for price1. It's the left side of the long equation above:
    
    price = (k / (poolCORE + (X * 0.997))) / (poolCORE + X)
    
This is the price of a pair after we have added `X` amount of CORE to it. Note that it only depends on `k` and `poolCORE`! The different pairs will have different `k`. Hmmm, ok. For simplicity, let's rename `poolCORE` to just `C` for CORE.

Let us rewrite that expression to:
    price = k / ((C + 0.997 * X)(C + X))

And `X`... let's pretend `X = q * C`, or in other words, we will add a number of CORE that is **proportional to the number of CORE already in the pair** - the proportion we call `q`. So if pair has 100 CORE and `q` is 0.5, then we will add 50 CORE for that pair. Now we can rewrite the formula for price once more, replacing `X` with `q * C` so it now looks like: 

    price = k / ((C + qC * 0.997)(C + qC))

...and we can then extract `C` from the expression so that it now looks like:

    price = k / (C^2 * (1 + 0.997q)(1 + q))

At this point you are staring blankly at the screen thinking... he's gone mad! The mad hatter! :) Let's take a look and see what the heck we have arrived at.

The formula says that the new price for **any of the pairs** will be it's `k` divided by `C^2` (the amount of CORE in the pair) multiplied with "an expression of q". And `q` was a proportion of the existing CORE in the pair. Uhuh.

So... if we can use the same `q` for all our pairs, then ... the price of all our pairs will be divided by the same number, namely `(1 + 0.997q)(1 + q)`. And since their price were the same before, then dividing by **the same number** will make them all the same again!

Muuhhaaahahaa! ...insert Evil laughter and Mad Hatter eyes glistening here... we are close now! So we just need to find a `q` that makes sure we put all our "outside" CORE into the pairs.

Let's grab an example! Let's say we have 5 pairs and they have 200, 3000, 250, 600 and 850 COREs each. This makes a total of 4900 COREs and that means we have 5100 COREs free "outside" of the pairs. Now.. we just need a `q` to consume all 5100 COREs!

So `5100 = q*200 + q*3000 + q*250 + q*850` which is `5100 = q(200 + 3000 + 250 + 850)` and yes, `q = 5100 / (200 + 3000 + 250 + 850)`. Bam! We have `q` and thus we can trivially calculate the new price of ANY pair, and funny enough - we only need to calculate the new price for ONE pair, because all will have the same price!

## Yeah, right, he has lost his last marble
You are thinking... he is just blowing smoke up our... something. Let us apply the above to the current two pairs! I asked RoboCORE at the time of writing and he said the CORE-ETH pair has **3471 CORE & 33349 ETH**, and the CORE-CBTC pair has **638 CORE & 179 CBTC**.

This gives `price1 = 33349 / 3471 = 9.60789 ETH * 388.80 = $3735` and `price2 = 179 / 638 = 0.28056 BTC * 13761.76 = $3861`. Hmmm, oops, diff of almost 3% but yeah, let's pretend they are the same! :)

Now... Robo says **floor price is 1.6325 ETH**. Can we find the same number using the q approach?

So we find q using `q = (10000 - 3471 - 638 - 1280) / (3471 + 638 + 1280) = 1.43368216111`. We then take `q * 3471 = 4976.3` CORE and add it to pair1 and we add the rest (`5891 - 4976.3`) to pair2, which should also be same as `q * 638 = 914.7` (yup it is). Now, the new price of pair1 should be `(k / (poolCORE + (X * 0.997))) / (poolCORE + X)` so `price = (3471 * 33349) / (3471 + 0.997 * 4976.3)(3471 + 4976.3)`. And it yields **1.625 ETH**! Close enough!

Let's look at pair2, it should end up at the same price: `price = (638 * 179) / (638 + 0.997 * 914.7)(638 + 914.7)`. It's **0.04745334321**! Eh.. what the hell? Oh, in BTC :) So ... multiply by price of WBTC in ETH which is **34.22899** and we have **1.6243 ETH**!

And that's where I say ... Yippee ki-yay muth... I mean, Yippee ki-yay!

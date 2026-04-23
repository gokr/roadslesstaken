---
title: Everything you wanted to know about CORE floor price but was too afraid to
  ask
date: '2020-10-28'
slug: floor-price-in-core
categories:
- CORE
- Ethereum
- Programming
---
The last month I have gotten involved in a fairly new crypto currency project called [CORE](https://twitter.com/CORE_Vault), or [cvault.finance](https://cvault.finance). My main contribution is [RoboCORE](https://github.com/gokr/robocore) a chat bot operating on both Discord and Telegram serving the CORE community with various calculations and notifications.

A concept central to CORE is what is known as "the floor price" and in developing RoboCORE I had to learn how to calculate it properly. This concept is a bit hard to grasp, so this article tries to clear up the fog!

What is a floor price? It's simply the lowest price CORE can ever reach. It's not a floor in fiat, like the USD, but rather a floor **measured in ETH** (or BTC), the assets CORE is traded against. So if those drop to zero in worth, then there is nothing CORE can do about that!

<!--more-->

Earlier CORE was available **only in a single** trading pair [CORE-ETH on Uniswap](https://info.uniswap.org/pair/0x32ce7e48debdccbfe0cd037cc89526e4382cb81b). Let's pretend it still is, for the sake of most of this article, and we can expand to two trading pairs at the end.

There are three main mechanisms that together give CORE it's floor price:

1. The fact that there is a fixed supply of CORE. 10000. There will never be more CORE minted.
2. The fact that the CORE contracts prevent removing liquidity from the CORE-ETH pair.
3. The Uniswap rules governing the price of a Uniswap trading pair.

Ok, so there is only 10000 CORE, ever. Some of these CORE are in the trading pair, at the moment of writing there is 3333 CORE there, and 34667 ETH. So "outside" of the pair, in the hands of people, there must be `10000 - 3333 = 6667` COREs. Again, disregarding the [second trading pair](https://info.uniswap.org/pair/0x6fad7d44640c5cd0120deec0301e8cf850becb68) that just recently was started, let us just pretend that hasn't happened :)

**NOTE: I sometimes write pair and sometimes pool. It's the same thing.**

Some of you may even be unaware of how a Uniswap pair works. The simple mental image is that it is a trading pair of two coins. In this case CORE and ETH. It let's you buy or sell CORE against ETH. And it does so without an order book, this is the beauty of Uniswap and so called decentralized exchanges. The pair itself consists of two piles of money, one pile of CORE and one pile of ETH. These two piles together is often referred to as a "pool". The amount of money in the two piles, summed together, is called the liquidity of the pair. Trading is done by "swapping", you basically put in CORE and get ETH out, or vice versa.

Now... mechanism number 2 says we can not remove liquidity from the pair. This is essential and means that the ETH in the pair can only be "removed" from the pair by buying it, using CORE. There is no other way, noone can just remove both chunks of money. The fact that **liquidity is locked in** is a key novel feature of the CORE trading pairs. The CORE project invented this idea and it has profound effects, including creating the price floor.

Then we arrive at mechanism number 3. What is the price of a Uniswap trading pair? It's trivial, the price at all times is simply `<pooledETH> / <pooledCORE>`. Simple!

At the time of writing `price = 34667 / 3333 = 10.40 ETH/CORE`. Ok, given this insight, this should mean that the lowest price is reached by increasing number of CORE in the pair and decreasing number of ETH in the pair. And the only way we can do that, is by selling CORE into the pair so we can pull out ETH. Let this sink in since it's fundamental. We reach the lowest price when we have the highest amount of CORE and the lowest amount of ETH in the pair.

So when I sell 10 CORE into the pair, the price will go down. If I sell 10 more it will go down even more. If I sell **ALL CORE THERE IS** outside the pair, 6667 CORE, then the price should be down at the floor price, because there is no more CORE to put into the pool!

## Uniswap trading dialog
A lot of people start fiddling with the Unsiwap trading dialog at this point, entering "6667" and seeing the price Uniswap **would buy those COREs for**, and mistakenly conclude this price to be the floor price. **It is NOT**. That's the price you would get for selling 6667 CORE into the pair, but it is NOT the price CORE will have after you sold! So just drop that notion.

The math that comes below will also show how that particular price is calculated by Uniswap, but it's still an uninteresting price - unless you really do have 6667 CORE to sell. The interesting price is what CORE will cost AFTER all CORE has been dumped into the pool, because if that would indeed occur - it would be lots and lots of little dumps, until the very last CORE was dumped. It would never be a single Megalodon dumping 6667 CORE.

## Time for math
So at this point I hope I have convinced you the reader that CORE will have it's lowest price when ALL CORE is in the trading pair. All 10000 of them. The problem is, we don't know how much ETH is left in the pair at that time. If we knew, then the price would simply be that amount of ETH divided by 10000, right?

Going back to Uniswap rules, there is a really slick rule that we must understand and that is the rule of "keeping k constant". All Uniswap pairs abide by this rule, and it's also the rule that figures out the price when you enter an amount to sell or buy in the Uniswap trading dialog.

Now what is `k`? `k` is the name they have given to the mathematical product of the pooled assets. So `k = <pooledETH> * <pooledCORE>`. So right now `k = 3333 * 34667 = 115545111`. It's just a number, not really something that can be interpreted to mean anything all by itself. But Uniswap will make sure it **stays constant** after each trade. This is what makes Uniswap tick. If k is 115545111 now, it should be so even after the next trade.

This means, that after you sell say... 100 CORE into the pool, k should still be 115545111. But wait a minute, if you sell 100 CORE, then CORE in the pool will go from 3333 to 3433 so... in order for k to stay constant the amount of ETH in the pool must be lowered. Well, duh, of course, because if you sell 100 CORE you want some ETH in return! So this determines the amount of ETH you will get for your 100 CORE, by determining how much ETH should be left in the pool.

Let's do the numbers. `k = 3333 * 34667`. You sell 100 CORE. So now `k = 3433 * x` where x is the amount of ETH that should still be in the pool. But k needs to stay constant so we can replace k in the equation with the value k had BEFORE the trade, so this gives us `115545111 = 3433 * x`. And ok, we can now solve for `x` so `x = 115545111 / 3433`. What was `x` now again? It was the amount of ETH left in the pool after the trade. It turns out to be `33657.2`. Since we had `34667` before, that must mean you got `34667 - 33657.2 = 1009.8` ETH for your 100 CORE. And the price ended thus up being `1009.8 / 100` which is 10.098 ETH/CORE. But the price now, after you sold, is actually `33657.2 / 3433 = 9.804 ETH/CORE`! Aha! That's interesting in itself, the price **you** get is not the same as the **new price** right after your transaction.

So this is how Uniswap figures out how much ETH you will get when you sell CORE! And of course the other way around too. And this obviously then also gives us amount of ETH still left in the pool.

Finally we have reached the thought experiment - what happens if we sell ALL available CORE outside the pool into the pool? And... is the end result the same if we sell it all in one big swoop, or if 1000s of people do it with 1000s of small paper cuts? The answer is, it does not matter how many trades we do it in, which is kinda logical. The k must remain at `115545111` at all times, it does not matter how many trades we use.

So yes, let's see what happens if we sell ALL of CORE into the pair. It's just the same as above, but this time we sell 6667 CORE instead of 100. Again, we want to know x - the amount of ETH left in the pool. Given k, this must be `x = 115545111 / 10000`. So we would have 11554.5111 ETH left in the pool. And then the new price is simply `price = 11554.5111 / 10000 = 1.15545111 ETH/CORE`.

This is our floor price. But do note it is a floor price **in ETH**. So if ETH goes down in fiat value, that means CORE's floor in fiat also goes down, obviously. But it will NEVER EVER go down in ETH value below 1.15545111 ETH.

## What about... fees
Ok, so indeed, we cheated with that part too. Uniswap takes a fee and that part goes back into the pool as added liquidity. This actually means that the amount of ETH slowly grows a little bit in the pair, slowly growing the floor price. This means that instead of doing `x = oldk / (pooledCORE + addedCORE)` we need to do `x = oldk / (pooledCORE + (addedCORE * 0.997))` instead. So when calculating x, which is the amount of ETH left in the pool, we divide with a number slightly lower, which will make the amount of ETH left in the pool slightly higher (and thus the amount of ETH you receive for your CORE, a bit less). This means the ETH pool grows a little teeny bit, and k actually grows a little teeny bit, and thus floor price also grows a little teeny bit, with every trade. RoboCORE takes this into account, but for simple calculations it does not change the outcome much at all.

## What about... the second pair?
Ah, yes. This makes it all much more complex! In the next article I will explain how to deal with two pairs, but it basically goes like this - instead of pouring all 10000 CORE into a single pair, we now need to do a balancing act. We need to pour some CORE into the CORE-ETH pair, and some into the new CORE-CBTC pair until there is no more CORE to pour.

So at that point, all 10000 CORE should be distributed in some way, between the two pairs. But how do we know how much we should put into each pair? Well, given that arbitrage would occur any stable floor price would have to be a price that is the same for both pairs. So the math problem boils down to finding the distribution of all 10000 CORE between the two pairs - that make them have **the same price**.

Without explaining in this article how we calculate that, I can show the current numbers. As we saw above we have 3333 CORE in the CORE-ETH pool. And there is now 615 CORE in the CORE-CBTC pool. Calculations say we would find the common price if we put 5048 COREs into the CORE-ETH pair and the rest, 1004 into the second pool. So 8381 and 1619 CORE respectively.

This makes a floor substantially higher, at around **1.63 ETH** right now. One last final observation - with two pools the floor value can actually go down when valuated in ETH. Before it could not do that, but now with the second pair we need to take the CBTC-ETH rate into account also. So current floor does not only rely on ETH but also on CBTC, and that means the relationship between BTC and ETH will affect the floor, and subsequently the floor price **valuated in ETH only** can actually go down.

That's all for today, keep HODLING :)

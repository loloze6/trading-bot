---
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
source-idea: 021-01_above-rising-cloud-continues-up.d1_above-thick-cloud-continues
line: 7.g patterns
backtest: 021-01_above-rising-cloud-continues-up.d1_above-thick-cloud-continues_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The more a coin's daily return falls below zero, measured against its recent 20-day volatility, the more the coin rises over the next day above its normal drift.
Consequence: A trader would lean long a coin for a day after an unusually sharp down day, and refuse to short into that fall.
Why:
- F1: Across all 6 coins, a coin's daily return scaled by its 20-day volatility predicts the next day's excess return with the opposite sign: the pooled slope is +0.16 % of next-day return per unit of fall, t 4.03 on 14,356 days. The effect holds in both halves of the windows (w1–w12 t 3.63, w13–w24 t 2.23), is positive on all 6 coins, and is strongest on XMR (t 4.46) and ETH (t 2.22).
- F2: That next-day reversal is mostly a rebound after falls. After a day down more than 1 volatility unit, the next day's excess return is +0.50 % (1,804 days), against −0.05 % after a day up more than 1 unit (1,983 days). After a fall of 1–2 units the t is 3.57 (1,444 days); after a fall of more than 2 units it is +0.61 % with t 2.00 (400 days). These one-day moves are 2.6 to 3.2 times the backtest's 0.19 % round trip.

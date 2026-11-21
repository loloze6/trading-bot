---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-04_support-breakdown-continues-down.d2_deep-support-break-rebounds
line: 7.d not profitable
backtest: 020-04_support-breakdown-continues-down.d2_deep-support-break-rebounds_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes far below a price where it turned up several times in the past 90 days, it tends to rise over the next 5 days, and the deeper its close under that level and the more times the level held, the larger the rise, a rise that grows steeply only among the very deepest breaks of the most-touched levels, except when its 5-day return into the break is among its sharpest falls.
Consequence: Buy a support break only when it is extreme in absolute depth × touches and the slide into it was not a crash; otherwise stay out instead of carrying a long through ordinary breaks.
Why:
- F2: The rebound exists only at the most extreme breaks. Sorting the raw depth × touches into deciles, deciles 0 to 8 all have negative unusual 5-day moves (-0.10 % to -1.18 %; decile 3 has t -2.01 on 237 cases). Only the top decile rises: +2.03 % unusual (t 2.40, 237 cases, strength 0.18) and +2.63 % total, about 13 times the 0.19 % cost of a trade.
- F3: The forecast's dead zone does not isolate that extreme. The top fifth by forecast earns only +0.43 % unusual (t 0.75, 469 cases), against +0.99 % for the top fifth by raw value, and the second forecast quintile loses -1.13 % (t -2.50). Standardising against the coin's own past 90 values blurs how deep the break is in absolute terms.
- F5: Inside the top-fifth raw breaks, the rebound fails after the sharpest 5-day falls. The lowest tercile of the 5-day return has an unusual move of -0.20 % (t -0.20, 151 cases), against +1.74 % (t 2.03, 150 cases) and +1.20 % (t 1.18, 151 cases) for the middle and highest terciles.
- F6: The deep-break rebound is broad. Unusual moves are positive in all 6 coins (+0.07 % to +2.14 %) and in 71 % of the 21 windows that have such cases.
- F1: The book loses where it spends most of its time: it is long on 74 % of bars, and on the 2366 grid cases where the close sits under a past swing low at all, the following 5-day unusual move is -0.32 % (t -1.51; total +0.27 %, barely above the 0.19 % cost). On the 1053 cases with no support broken it is +0.71 % (t 1.83; total +1.30 %). Yet the book holds a mean allocation of 0.48 in the first state and 0.05 in the second, so it is long when the coin does worse than usual and flat when it does better. This is why it trails holding: 0.038 % against 0.119 % per day, and a Sharpe 0.15 below holding's.

---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-01_downtrend-bounce-given-back.d1_bounce-fades-near-lows
line: 7.d not profitable
backtest: 025-01_downtrend-bounce-given-back.d1_bounce-fades-near-lows_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 90-day return is negative, a one-day rise that is large relative to its usual daily move (its 20-day standard deviation of daily returns) is followed by a fall over the next 5 days, the larger the rise counted in usual daily moves the larger the fall, and the farther the coin's close above its lowest close of the past 90 days and the shallower its 90-day loss, the larger the fall.
Consequence: A trader would short only outsized bounces in coins that are falling mildly and sit well off their lows, and would refuse to short ordinary up days or bounces in coins that have already fallen deeply and sit near their lows.
Why:
- F1: The book loses because it is short a coin that drifts up. Its 1987 trades are all shorts, with a mean gross result of -3.83 % (-3.93 % after fees) and 33 % winners. Per held bar it loses 0.036 %, of which 0.041 % is the market's own rise working against the short, while timing adds only +0.005 %. The coins' normal 5-day drift is +0.30 % to +0.91 %.
- F2: The signal fires mostly on ordinary days, not on large bounces. Standardising over its past 90 values saturates the forecast: 240 of 311 short entries sit at a forecast between -15 and -20. 67 % of entries come on days whose rise is under one usual daily move, and those entries are followed by a 5-day move of only -0.72 % (t -1.27).
- F3: In falling coins, only the largest bounces are given back. On the 5-day grid in the falling regime, moves over the next 5 days are:
- F4: Nearness to the 90-day low works against the fall, not for it. Among falling-regime bounces of more than two usual moves (all bars), those closer to the low than the median rise +1.52 % over 5 days (n 111, t 1.62), while those farther above it move -0.35 % (n 110).
- F5: The depth of the coin's fall also works against the short. On the falling-regime grid:

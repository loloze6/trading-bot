---
brief: 023_range-reversion-when-no-trend
source-idea: 023-03_flatter-range-stronger-reversion
line: 7.g patterns
backtest: 023-03_flatter-range-stronger-reversion_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The farther a coin's close sits from the middle of its 30-day closing range, the more it moves further toward that edge over the next 5 days, down from near the bottom and up from near the top.
Consequence: A close near the bottom of its monthly range is a reason to refuse a long, and one near the top a reason to refuse a short.
Why:
- F1: The tested reversion runs the other way: on the 5-day grid (2555 cases), where the close sits in its 30-day range predicts the coin's next 5-day return in the same direction (corr +0.054, t +2.75), and the strongest long-forecast quintile (close far below the middle) is followed by -1.33 % relative to drift (t -3.08, n 511), consistent with step 5's negative main mean (t -3.39, unusual move -0.40 % per case, about 2 times the 0.19 % cost of a trade in absolute size).
- F3: Flatness does not strengthen the effect in either direction: the range-position slope is t +1.10 in the trendiest tercile, +2.20 in the middle and +1.52 in the flattest (about 850 cases each), and the flat-half extreme bottom quintile alone shows -2.28 % (t -2.94, n 158), the opposite of the brief's reversion.
- F4: The continuation is not stable over time, which weakens its weight after this many angles: by year its 5-day slope is t +3.29 in 2020 and +2.47 in 2021 but -2.34 in 2022 and -0.71 in 2018, the w1-6 block is t -2.21 against +3.37 and +3.26 in w7-12 and w13-18, and leaving out 2020 drops the pooled t to +1.30 (2021: +1.67).

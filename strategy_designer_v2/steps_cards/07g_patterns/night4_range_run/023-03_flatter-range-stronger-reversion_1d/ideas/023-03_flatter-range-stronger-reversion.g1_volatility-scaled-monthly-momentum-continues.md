---
brief: 023_range-reversion-when-no-trend
source-idea: 023-03_flatter-range-stronger-reversion
line: 7.g patterns
backtest: 023-03_flatter-range-stronger-reversion_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 30-day return relative to its own 30-day volatility, the more its price continues in the same direction over the next 5 days, up after a strong rise and down after a strong fall.
Consequence: A trader should lean with a coin's volatility-scaled month-long move rather than fade it, and refuse to fade a coin pushed to an edge of its monthly range.
Why:
- F1: The tested reversion runs the other way: on the 5-day grid (2555 cases), where the close sits in its 30-day range predicts the coin's next 5-day return in the same direction (corr +0.054, t +2.75), and the strongest long-forecast quintile (close far below the middle) is followed by -1.33 % relative to drift (t -3.08, n 511), consistent with step 5's negative main mean (t -3.39, unusual move -0.40 % per case, about 2 times the 0.19 % cost of a trade in absolute size).
- F2: The same continuation shows in the plain 30-day return, and more sharply once scaled by the coin's own 30-day volatility: slopes on the next 5-day excess return have t +2.79 (raw) and t +3.04 (volatility-scaled), the top 30-day-return quintile being followed by +1.26 % (t +2.13, n 511) and the bottom four quintiles by -0.68 % to +0.25 %.
- F4: The continuation is not stable over time, which weakens its weight after this many angles: by year its 5-day slope is t +3.29 in 2020 and +2.47 in 2021 but -2.34 in 2022 and -0.71 in 2018, the w1-6 block is t -2.21 against +3.37 and +3.26 in w7-12 and w13-18, and leaving out 2020 drops the pooled t to +1.30 (2021: +1.67).
- F5: The pattern holds at 10 days too (range position t +2.24, 30-day return t +2.46, 1259 cases), and across coins it is positive in four of six (XRP t +2.50, ETH t +2.00 at 5 days; XMR -0.28, LTC +0.30).

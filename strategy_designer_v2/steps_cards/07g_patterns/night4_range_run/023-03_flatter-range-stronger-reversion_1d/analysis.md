---
line: 7.g patterns
backtest: 023-03_flatter-range-stronger-reversion_1d
idea tested: 023-03_flatter-range-stronger-reversion
step 5: rejected
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3270 USD
---
## Findings
- **F1:** The tested reversion runs the other way: on the 5-day grid (2555 cases), where the close sits in its 30-day range predicts the coin's next 5-day return in the same direction (corr +0.054, t +2.75), and the strongest long-forecast quintile (close far below the middle) is followed by -1.33 % relative to drift (t -3.08, n 511), consistent with step 5's negative main mean (t -3.39, unusual move -0.40 % per case, about 2 times the 0.19 % cost of a trade in absolute size).
- **F2:** The same continuation shows in the plain 30-day return, and more sharply once scaled by the coin's own 30-day volatility: slopes on the next 5-day excess return have t +2.79 (raw) and t +3.04 (volatility-scaled), the top 30-day-return quintile being followed by +1.26 % (t +2.13, n 511) and the bottom four quintiles by -0.68 % to +0.25 %.
- **F3:** Flatness does not strengthen the effect in either direction: the range-position slope is t +1.10 in the trendiest tercile, +2.20 in the middle and +1.52 in the flattest (about 850 cases each), and the flat-half extreme bottom quintile alone shows -2.28 % (t -2.94, n 158), the opposite of the brief's reversion.
- **F4:** The continuation is not stable over time, which weakens its weight after this many angles: by year its 5-day slope is t +3.29 in 2020 and +2.47 in 2021 but -2.34 in 2022 and -0.71 in 2018, the w1-6 block is t -2.21 against +3.37 and +3.26 in w7-12 and w13-18, and leaving out 2020 drops the pooled t to +1.30 (2021: +1.67).
- **F5:** The pattern holds at 10 days too (range position t +2.24, 30-day return t +2.46, 1259 cases), and across coins it is positive in four of six (XRP t +2.50, ETH t +2.00 at 5 days; XMR -0.28, LTC +0.30).
- **F6:** No other angle stood out: past 5-day return quintiles (largest |t| 1.27), 30-day volatility quintiles (largest |t| 1.15), short-to-long volatility ratio quintiles (largest |t| 1.28) and the book's weekday means show no grading beyond chance.

## Ideas
- `023-03_flatter-range-stronger-reversion.g1_volatility-scaled-monthly-momentum-continues` (from F1, F2, F4, F5): The larger a coin's 30-day return relative to its own 30-day volatility, the more its price continues in the same direction over the next 5 days, up after a strong rise and down after a strong fall.
- `023-03_flatter-range-stronger-reversion.g2_range-edge-continuation` (from F1, F3, F4): The farther a coin's close sits from the middle of its 30-day closing range, the more it moves further toward that edge over the next 5 days, down from near the bottom and up from near the top.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

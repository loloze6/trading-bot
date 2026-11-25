---
line: 7.b inconclusive
backtest: 040-01_falling-calm-scaled-fall-continuation_1d
idea tested: 040-01_falling-calm-scaled-fall-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.1961 USD
---
## Findings
- **F1:** The main measure is on the predicted side but just short of the bar: mean +0.91 % per case over 3 days with a day-clustered t of 1.93 (632 cases on 303 days). In the folds shown (B and C) the same cases give +1.62 % with t 2.39 (361 cases), so the effect is positive but too small for six coins to show clearly.
- **F2:** The continuation is present at every horizon in folds B and C, not only at the plan's 3 days. The sign-flipped drift-removed move is +0.82 % at 1 day (t 2.31), +1.62 % at 3 days (t 2.39), +1.80 % at 5 days (t 1.82) and +2.63 % at 10 days (t 2.24), with a strength of 0.14 to 0.17 of a usual move.
- **F3:** The effect is positive on all six coins but clear on only some. At 3 days it is +2.79 % on ETH (t 2.11), +2.01 % on LTC (t 2.42), +1.63 % on XRP (t 2.03) and +2.02 % on ZEC (t 1.85), against +0.39 % on BTC (t 0.45) and +0.42 % on XMR (t 0.42), with only 43 to 81 cases per coin.
- **F4:** The effect is mixed across periods. It is +2.56 % in 2018 (t 2.11, 163 cases) and +1.91 % in 2019 (t 2.02, 141 cases), but -3.28 % in 2020 (t -2.48, 28 cases) and +0.09 % in 2021 (40 cases). Windows w16 to w18 are negative (w16 -6.57 %, 8 cases).
- **F5:** The grading the idea claims is weak, which is why the supporting slope failed. By forecast quartile, from strongest to weakest, the 3-day move is +2.15 %, +0.90 %, +2.38 % and +1.04 %. By raw 3-day fall it is +1.64 %, +1.71 %, +2.81 % and +1.11 %. The slope is 0.0004 and not significant.
- **F6:** The size is too small to tell from zero, and the book barely pays its costs. The unusual move is +0.58 % (t 1.46 over 440 days) and the total move is +0.19 %, against a 0.19 % cost per trade. The book's Sharpe is 0.20, against holding's 0.57.

## Ideas
- `040-01.b1_calm-downtrend-falls-more-coins` (from F1, F2, F3, F6): In a falling, calm market, a coin that has fallen over the last 3 days keeps declining over the next 3 days, more so the larger that 3-day fall in units of its 30-day daily-return swing.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

---
line: 7.d not profitable
backtest: N2-03_deep-month-loss-rebound_1d
idea tested: N2-03_deep-month-loss-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3360 USD
---
## Findings
- **F1:** Fees are not why the book fails. Across 3297 trades, all long, the mean gross gain is -0.51% against a mean fee of 0.10%, so the trades already lose before costs.
- **F2:** Long holds make the loss. Trades held over 15 days (743) average -6.38% gross, while trades closed within 1.5 days (707) earn +2.30% and those of 1.5–3.5 days (693) earn +1.66%. The long holds lost most in 2018 (-24.0%, 145 trades) and 2022 (-14.7%, 137 trades).
- **F3:** The book is a long bet on falling coins. 75% of bars sit below the 100-day average, where the mean allocation is 0.52, against 0.08 above it. In 2018 the coins fell (mean daily return -0.35%) while the allocation averaged 0.60, and the book's summed daily return was -6.40, its only losing year.
- **F4:** Small forecasts lose and deep ones gain. Over non-overlapping 20-bar periods, forecasts between 0 and 2 are followed by -4.36% excess return (t -2.63, n=167), while forecasts of 5 or more are followed by +3.11% (t 2.06, n=216). The two lower forecast quartiles show -3.7% and -3.9% (t about -1.8 to -1.9, n=105 each).
- **F5:** The deep-fall rebound needs time. The excess return after forecasts of 5 or more rises with the horizon: +0.19% at 5 bars (t 0.50, n=814), +0.77% at 10 bars (t 1.11, n=414) and +3.11% at 20 bars (t 2.06, n=216).
- **F6:** Among deep falls, those still falling over the last 5 days do better. Their 10-bar excess return is +1.35% (t 1.62, n=302), against -0.79% (t -0.65, n=112) when the last 5 days were already up. Deep falls in the most volatile third of bars show -0.61% (t -0.54, n=146).
- **F7:** The largest entry forecasts lose. Trades entered at forecasts of 15–21 average -1.42% gross (1337 trades), while those entered at 8–15 earn +0.85% (792 trades).

## Ideas
- `N2-03_deep-month-loss-rebound.d1_only-extreme-falls-rebound` (from F4, F5, F1): A coin's 20-day fall is followed by further decline when the fall is only mild relative to its recent 20-day moves. Only a fall that is extreme against those recent moves is followed by an above-usual rise over the next 20 days.
- `N2-03_deep-month-loss-rebound.d2_bear-market-falls-keep-falling` (from F2, F3, F7): When a coin trades below its 100-day average and its 20-day decline keeps deepening, the decline continues and a long position held there loses. The rebound is concentrated in short bounces that resolve within a few days.
- `N2-03_deep-month-loss-rebound.d3_capitulation-in-calm-markets` (from F6, F4): A deep 20-day fall whose last 5 days are still down, in calm or ordinary volatility, is followed by an above-usual rise. This is a capitulation-type rebound.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

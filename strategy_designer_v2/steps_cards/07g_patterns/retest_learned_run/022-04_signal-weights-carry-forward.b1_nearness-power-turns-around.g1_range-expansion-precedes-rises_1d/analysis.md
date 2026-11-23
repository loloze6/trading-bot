---
line: 7.g patterns
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises_1d
idea tested: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4259 USD
---
## Findings
- **F1:** The tested range ratio carries the 5-day excess return pooled (slope t 2.66, 3131 non-overlapping cases), but not in an even grade: by quintile the means run -0.11 %, -1.32 % (t -3.55), -0.19 %, +0.68 %, +1.08 % (t 2.28), so the narrowest days do not lead to the lowest returns.
- **F2:** The range effect is uneven across coins and years. By coin the slope t is XRP 2.19, ZEC 2.13, ETH 1.73, BTC 0.27, XMR 0.09 and LTC -1.14. By year it runs from -2.11 in 2018 to +2.97 in 2024.
- **F3:** The book holds small positions on 99 % of coin-days (median allocation -0.035, standard deviation 0.17) and is short 55 % of the time, its daily returns correlate only 0.25 with the coins', and its best 1 % of days carry 204 % of its total gain, so its result rests on a handful of days.
- **F4:** The 20-day return predicts the 5-day excess return pooled (t 2.69, 2843 cases), but the top quintile (+0.65 %) is below the fourth (+0.91 %), and the effect sits in XRP (t 2.23) and ZEC (t 1.82), with BTC -0.04, LTC -0.65 and XMR -0.88.
- **F5:** Where the close sits in the day's range adds little.
- **F6:** The volatility level shows no grade: 20-day volatility t -0.05, and 20-day against 60-day volatility t 1.52 with no ordered quintiles.
- **F7:** Next-day returns averaged over the coins are highest after Friday bars (+0.44 %, t 2.98, 414 days) and Thursday bars (+0.37 %, t 1.90). The Thursday-Friday edge over other days comes from 2018-2019 (t 1.66 and 2.72) and is below t 0.91 in every year from 2020 to 2025.
- **F8:** The strongest single cell, narrow range with a close near the low (-1.94 % over 5 days, t -3.63, 308 cases), is one of nine cells cut from the same data and agrees with F1's uneven narrow-range quintiles.

## Ideas
- No ideas: I looked at about forty groupings (range, close place, 1-, 5- and 20-day returns, volatility level, weekday, range crossed with direction, trend and close place, by coin and by year). The few patterns near or above t 2 apart from the tested idea are carried by one or two coins (F4, F5), are no longer present after 2019 (F7), are not graded (F7), or are a single cell picked from several (F8), so none stands out from chance enough to found an idea.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

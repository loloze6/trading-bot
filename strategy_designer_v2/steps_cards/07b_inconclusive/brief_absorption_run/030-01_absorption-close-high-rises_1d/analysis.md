---
line: 7.b inconclusive
backtest: 030-01_absorption-close-high-rises_1d
idea tested: 030-01_absorption-close-high-rises
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.2107 USD
---
## Findings
- **F1:** The test's result is zero, not just short of the bar. Pooled over 369 cases, the slope of the 5-day unusual move on the forecast is -0.00016 (t -0.39). The size is +0.03 % per case, a strength of -0.012 of the coin's usual 10.60 % move. My own recomputation on 309 non-overlapping absorption days agrees: the slope on the close location has t -0.58, and the mean move signed by side is -0.05 % (t -0.06).
- **F2:** No horizon shows the predicted continuation. On absorption days the slope of the unusual move on the close location is negative at every horizon tested: t -1.88 at 1 day (341 cases), -0.87 at 3 days, -0.58 at 5 days, -0.31 at 10 days and -0.85 at 20 days (212 cases). Weighting by volume (close location × volume ratio) gives t between -1.48 and +0.02.
- **F3:** The 5-day move does not rise with close location. Mean unusual moves by close-location bin, from the low end to the high end, are +2.24 % (30 cases), -0.33 % (62), +1.51 % (79), +1.89 % (90) and -1.61 % (48). The closes nearest the high do worst, the opposite of the idea's gradient.
- **F4:** Heavier volume does not strengthen the effect. The mean signed 5-day move is -0.09 % for volume ratios of 2–2.5 (136 cases), -0.75 % for 2.5–3.5 (113) and +1.36 % for above 3.5 (60), with standard deviations of 11.5–20.0 %. These differences are far inside the noise.
- **F5:** No coin or side carries the effect.
- **F6:** The only sizeable departures are years whose signs flip. The signed 5-day move has t -3.42 in 2018 (44 cases), -2.89 in 2021 (37), +2.17 in 2022 (36) and +1.88 in 2024 (43). The opposite signs line up with neither bull nor bear years, so there is no stable regime where the idea holds.
- **F7:** The close location carries no information on ordinary days either. On days with volume under 2x the 20-day mean but a body of at most 30 % of the range, the slope has t between -1.18 and +0.31 at every horizon (641 to 4,522 cases). Heavy volume therefore adds nothing over a close location that is itself uninformative.
- **F8:** The book confirms the null. Its Sharpe is -0.009 and its yearly return -1.3 %. Per case, the total move of +0.12 % is 0.6 times the 0.19 % cost of a trade.

## Ideas
- No ideas: The 5-day result is zero (t -0.39 on 369 cases) at every horizon, coin, side, volume level and trend split (F1–F5, F7), and its only strong pieces are years of opposite sign (F6). No part of the data shows the effect clearly, and with no effect on the predicted side, more data would not give a clearer answer than this one, which is that the close location after heavy flat-result days does not predict the coin's next move.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

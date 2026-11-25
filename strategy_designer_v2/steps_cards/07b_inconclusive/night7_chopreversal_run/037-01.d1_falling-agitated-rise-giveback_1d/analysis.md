---
line: 7.b inconclusive
backtest: 037-01.d1_falling-agitated-rise-giveback_1d
idea tested: 037-01.d1_falling-agitated-rise-giveback
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3989 USD
---
## Findings
- **F1:** The tested rise does reverse. On the 495 bars in folds B and C where the regime picked the falling-agitated profile and a one-day rise of 0 to 1 usual swing, the next day's return beat the coin's drift on the short side by +1.06 % (t 4.04 unpooled; day-clustered t 2.56 over 231 days). Step 5's main measure is on the same side, +0.051 % per position bar with t 1.60, but falls short of the t of 2.
- **F2:** The book's sizing dilutes this. In B and C, 354 of the 763 active bars were held outside the rise regime (in chop or unknown). Their mean position was only 0.026 and they gained +0.002 % (t 0.23), against +0.167 % (t 2.43) on the 409 regime bars. Another 86 regime bars (17.5 %) had no position at all, yet carried the largest short-side move, +1.61 % (t 3.08). So the measure's 1,610 cases hold many near-empty bars.
- **F3:** Inside the tested band the give-back is a level, not a grade. The slope of the next-day return on the scaled rise is -0.010 % (t -0.01, n 432). The short-side move by quartile of the rise is +1.05 %, +1.08 %, +0.51 % and +1.38 %, and the smallest forecast quartile carries the largest move (+1.71 %, t 3.80). Across the whole profile the grade is clear: with |scaled return| up to 2, the slope is -1.20 % per swing (t -5.02, n 1,059).
- **F4:** Agitation is where the effect lives, as the brief says. In-profile rises of 0 to 0.33 and 0.33 to 0.66 swings were followed by -0.97 % (t -2.50) and -1.13 % (t -2.87). Out of profile the same buckets gave -0.32 % (t -2.08) and -0.13 % (t -0.81), with a slope of only -0.17 % per swing (t -2.04, n 5,523). The regime's rise bars beat the profile's other bars by -2.06 % (Welch t -6.12).
- **F5:** The give-back is a one-day move, so the plan's horizon is the right one. On the non-overlapping grid the short-side move is +1.06 % at 1 day (t 4.04, 495 cases), +0.61 % at 2 days (t 1.09, 264) and -0.27 % at 3 days (t -0.36, 177).
- **F6:** The effect is broad across coins but not every period. Five of six coins show a next-day fall after the regime's rises: BTC -1.14 % (t -2.48), LTC -1.41 % (t -2.55), ZEC -1.38 % (t -2.40), XMR -1.01 % (t -1.73) and ETH -0.75 % (t -1.30). XRP is weaker at -0.35 % (t -0.29). By year it holds in 2018 (-2.05 %, t -4.06), 2019 (-1.10 %, t -3.01) and 2021 (-1.19 %, t -1.69), but not in 2020 (-0.05 %, t -0.11). The case count per coin is what limits the test.
- **F7:** The move covers costs. The size is an unusual move of +0.56 % per case (t 1.99, 388 days) and a total move of +0.43 %, which are 2.9 and 2.2 times the 0.19 % cost of a trade. The idea is short on evidence, not on size, and more coins are available in every fold.

## Ideas
- `037-01.d1.b1_falling-agitated-rise-giveback-more-coins` (from F1, F2, F4, F5, F6, F7): In a falling, agitated market, the larger a coin's one-day rise relative to its 30-day daily swing, while staying within that usual swing, the larger its fall over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

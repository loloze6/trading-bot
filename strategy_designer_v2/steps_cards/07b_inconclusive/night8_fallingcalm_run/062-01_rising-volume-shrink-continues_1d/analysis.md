---
line: 7.b inconclusive
backtest: 062-01_rising-volume-shrink-continues_1d
idea tested: 062-01_rising-volume-shrink-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.2046 USD
---
## Findings
- **F1:** The test's result points the way the idea predicts but stays short of the bar: over all folds the slope is +0.00051 (t 0.87, 1345 in-profile cases) and the size is +0.89 % per case (t 1.34, on 353 days). On folds B and C alone the slope is +0.00156 (t 1.84, 746 cases), still under t 2.
- **F2:** The effect is broad across coins rather than carried by one. The h5 slope is positive in 5 of 6 coins: ETH t 0.34, LTC t 1.37, XMR t 1.68, XRP t 1.54, ZEC t 1.17. Only BTC goes against it (slope −0.0029, t −2.20). Each coin has only 107 to 154 cases, so on a few coins the effect shows as several weak positives.
- **F3:** The effect works more like a step than a grade. Shrinking-volume bars beat flat or growing-volume bars by +2.18 % over 5 days (+1.75 % against −0.43 %, Welch t 2.21, 327 against 419 cases). Inside the shrinking bars the four forecast quartiles earn +2.5 %, +2.5 %, −0.9 % and +2.8 %, with no rise across them. This flatness dilutes the slope that the test measures.
- **F4:** The effect varies by period. The h5 slope has t 2.80 in 2021 and t 1.45 in 2019, but −0.76 in 2018 and −0.82 in 2020. The market's own swings make the result unstable on this many cases.
- **F5:** Another horizon does not make it clearer. The slope has t 1.06 at 10 days (375 cases) and t 1.17 at 20 days (179 cases), against t 1.84 at 5 days. The plan's 5-day horizon is where the effect shows best.
- **F6:** No calm or agitated split can be read from these windows. 591 of the 746 in-profile cases cannot get a one-year agitation reading inside a window, so these results give no basis to narrow the idea to one profile. The theme is the same, positive (+0.89 % per case, 0.077 of a usual move) but too few cases. More coins are available: 13 more on 1d bars, mostly in folds A and D.

## Ideas
- `062-01.b1_rising-volume-shrink-more-coins` (from F1, F2, F5): In a rising market, the more a coin's trading volume over the past 30 days has shrunk against the 30 days before, the larger its rise over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

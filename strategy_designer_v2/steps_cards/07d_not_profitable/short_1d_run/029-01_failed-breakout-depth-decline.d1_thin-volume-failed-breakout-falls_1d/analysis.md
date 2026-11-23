---
line: 7.d not profitable
backtest: 029-01_failed-breakout-depth-decline.d1_thin-volume-failed-breakout-falls_1d
idea tested: 029-01_failed-breakout-depth-decline.d1_thin-volume-failed-breakout-falls
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3828 USD
---
## Findings
- **F1:** The move per case cannot cover a trade. The total short-side move is +0.10 % over 5 days, against a cost of 0.19 % per trade, because the coins' normal drift runs −0.59 % against the short. The 394 actual trades lost −1.84 % gross on average (t −4.26), with only 30 % winners, so the mean daily return was 5.2e-05 against the 0.0005 required.
- **F2:** The forecast does not keep the idea's grading. 442 of its 468 non-zero bars sit at exactly −20, so the book is short at full size whether the breakout volume was a little thin or very thin. It is also in the market only 2–9 % of bars per coin.
- **F3:** Across all 498 failed breakouts rebuilt from prices, only the thinnest quartile shows a fall. That quartile, with a mean thinness of 0.38 (volume about 38 % below its 20-day average), has a short-side unusual move of +1.15 % (t 1.42, 125 cases). The heavy-volume failures move −0.99 % (t −1.59, 303 cases). The near-average quartile (thinness 0.05) moves −1.09 %.
- **F4:** The losses gather where the coin was already depressed when the breakout failed. Trades entered in the lowest quartile of distance to the 50-day mean (−7 %) lost −5.0 % gross (t −3.95, 56 trades); the other quartiles lost −0.3 % to −2.6 %. Trades in the lowest 60-day-return quartile (−25 %) lost −4.45 % (t −2.97, 47 trades).
- **F5:** Among thin-volume failures, those after a falling 60 days (mean −18 %) rose: short-side unusual move −2.13 % (t −1.74, 60 cases). Those in the second and fourth 60-day quartiles fell: +2.63 % (t 2.17, 41 cases) and +1.87 % (t 1.17, 52 cases).
- **F6:** One market year carries much of the damage. In 2020 the failed-breakout cases moved −3.67 % against the short (t −3.48, 81 cases), and the trades lost −3.63 % gross (t −3.81, 46 trades). The book summed −11.4 % that year, while the coins averaged +0.42 % a day.
- **F7:** The book does better when the breakout came after a larger 20-day rise. Trade losses shrink steadily from −3.51 % (t −3.79) in the lowest 20-day-return quartile (+1 %) to −1.27 % (t −1.13) in the highest (+40 %). The failed-breakout cases in that highest quartile are the only 20-day quartile with a positive short-side unusual move (+0.41 %).

## Ideas
- `029-01_failed-breakout-depth-decline.d1_thin-volume-failed-breakout-falls.d1_thin-failure-above-trend` (from F1, F3, F4, F5, F6): When a coin's daily close moves above its prior 20-day high and then, within the next 3 days, closes back below that old high, the coin falls over the next 5 days. This holds only while the breakout day's volume was below its 20-day average and the coin's close stood above its 50-day average, and the lower that volume against its average, the larger the fall.
- `029-01_failed-breakout-depth-decline.d1_thin-volume-failed-breakout-falls.d2_thin-failure-after-extension` (from F1, F2, F3, F7): When a coin's daily close moves above its prior 20-day high and then, within the next 3 days, closes back below that old high, the coin falls over the next 5 days. The thinner the breakout day's volume against its 20-day average, and the larger the coin's 20-day rise into the breakout, the larger that fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

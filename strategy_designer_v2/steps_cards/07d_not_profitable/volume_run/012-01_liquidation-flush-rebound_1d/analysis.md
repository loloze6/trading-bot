---
line: 7.d not profitable
backtest: 012-01_liquidation-flush-rebound_1d
idea tested: 012-01_liquidation-flush-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.4894 USD
---
## Findings
- **F1:** The book earns a mean daily return of 0.000387, below the 0.0005 floor, against 0.00118 for holding the coins, with a deepest fall of -28.5% (Calmar 0.40), and it is in a position on only 18.0% of bars at a mean allocation of 0.84.
- **F2:** A lone flush gives no rebound and repeated flushes do: the 3-day excess return on grid flush bars is -0.0016 (t -0.33, n 329) with no flush in the prior 5 days, 0.0084 (t 1.88, n 352) after one, and 0.0210 (t 3.33, n 290) after two or more.
- **F3:** The book loses on the lone flush and gains on the repeated ones: the held daily gain is -0.0010 on 1029 bars with no prior flush in 5 days, against 0.0052 (n 1118), 0.0062 (n 704) and 0.0073 (n 302) after one, two and three or more.
- **F4:** The rebound sits in the extreme forecasts: the top forecast quartile has a 3-day excess of 0.0208 (t 3.09, n 243), while the other three quartiles give 0.0063, 0.0009 and 0.0069 with t between 0.19 and 1.31.
- **F5:** The rebound is strongest when the coin has already fallen over 5 days: the lowest 5-day-return tercile has a 3-day excess of 0.0159 (t 2.82, n 312), the middle tercile -0.0001 (t -0.02), and the held gain is 0.0080 in the deepest 5-day-fall quartile (median -16.8%) against 0.0015 to 0.0035 elsewhere.
- **F6:** Fees take a large share of the gain: 0.000257 per bar against a gross gain of 0.000651. Trades are short (median 1 day, 2655 trades), and the 603 trades lasting 1.5 to 3.5 days lose -3.58% net on average.
- **F7:** The losses gather in a few windows of falling markets. Held gain sums to -0.92 in w2, -0.35 in w24 and -0.20 in w14, with median 60-day returns of -13%, -20% and -47%. In those windows the mean count of prior flushes in 5 days is 1.2 to 1.5.

## Ideas
- `012-01_liquidation-flush-rebound.d1_repeated-flush-exhausts-cascade` (from F2, F3, F1, F6): When a bar closes sharply lower on volume far above its own 30-day average volume and leaves a long lower wick below its close, price rises over the next 3 days, only after earlier such flush bars in the preceding 5 days. The more flush bars the coin has had over those 5 days, and the more extreme the volume burst and the longer the wick, the larger that rise.
- `012-01_liquidation-flush-rebound.d2_flush-after-deep-weekly-fall` (from F5, F4, F1): When a bar closes sharply lower on volume far above its own 30-day average volume and leaves a long lower wick below its close, price rises over the next 3 days, the more so the deeper the coin's own 5-day fall into that bar. The more extreme the volume burst and the longer the wick, the larger that rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

---
line: 7.b inconclusive
backtest: 035-02_rising-market-narrowing-ranges-rise_1d
idea tested: 035-02_rising-market-narrowing-ranges-rise
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3704 USD
---
## Findings
- **F1:** Over all four folds the test's result is zero, not a near-miss. The top-minus-bottom-third difference in excess 3-day return is -0.055 % (Welch t -0.11, 741 cases per third), the top third's mean excess is -0.005 %, and the size is an unusual move of -0.02 % per case (t -0.05 over 508 days, strength 0.003). The same measure on folds B and C alone gives +1.05 % (t 1.50, 1,237 grid cases, Spearman 0.083, p 0.004), so folds A and D must point the other way.
- **F2:** In folds B and C the calm-range effect grows with the horizon. On each horizon's non-overlapping grid, the top-minus-bottom difference of the forecast is:
- **F3:** In folds B and C the idea's own ratio, before the plan's standardisation, ranks better at 3 days. The recorded raw range ratio gives a top-minus-bottom difference of +2.05 % (t 2.87, 1,237 cases), against +1.05 % (t 1.50) for the standardised forecast. At 5 and 7 days the two are similar: +3.82 % (t 3.21) and +5.36 % (t 2.98).
- **F4:** The effect is mixed across periods and coins.
- **F5:** Inside the rising profile at 3 days, in folds B and C, the effect lives in the strongest uptrends. On the 60-day-return terciles, the top-minus-bottom difference is:
- **F6:** The book pays mostly on the coin's drift. Its Sharpe is 0.92 against holding's 0.55 and its Calmar 0.70. The total move per case of +0.34 % is 1.8 times the 0.19 % cost, but the unusual move is -0.1 times the cost. At 7 days in folds B and C the top-minus-bottom gap of 5 % is many times the cost.

## Ideas
- `035-02.b1_narrowing-ranges-weekly-rise` (from F1, F2, F3, F6): In a rising market, a coin rises over the next 7 days, more so the lower its average daily high-to-low range over the last 14 days compared with its average daily range over the 90 days before them.
- `035-02.b2_strong-uptrend-narrowing-ranges-rise` (from F1, F4, F5): In a rising market, a coin rises over the next 3 days, more so the lower its average daily high-to-low range over the last 14 days compared with its average daily range over the 90 days before them, and more so the larger its 60-day return.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

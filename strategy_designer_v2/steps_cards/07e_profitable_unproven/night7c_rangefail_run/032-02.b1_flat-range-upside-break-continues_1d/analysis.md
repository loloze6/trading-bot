---
line: 7.e profitable but not proven
backtest: 032-02.b1_flat-range-upside-break-continues_1d
idea tested: 032-02.b1_flat-range-upside-break-continues
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4119 USD
---
## Findings
- **F1:** The book's gain is timing rather than the market's own rise: its mean daily return is 0.000482, of which the position times the coin's mean daily return accounts for only 0.000095, leaving 0.000387 of timing; its Sharpe on these folds is 1.08 against holding's 0.53.
- **F2:** The gain sits in the upside breaks and in the days just after them, at a horizon longer than the plan's 5 days. At the first bar of each break (138 cases), the unusual move is +0.42 % over 1 day (t 0.82), +2.69 % over 5 days (t 2.50), +4.87 % over 10 days (t 2.45) and +3.15 % over 20 days (t 1.37).
- **F3:** The plan's grading runs the wrong way. A larger break above the 60-day high does not bring a larger rise: break size has a Spearman of -0.11 with the 5-day move and -0.12 with the 10-day move. The middle third of breaks (raw 0.49 mean ranges) has a negative 10-day move (-1.28 %), while the smallest third (0.13) gains +10.5 %.
- **F4:** The size of the breaking day's own jump grades the follow-through inversely, with a Spearman of -0.27 against the 10-day move. The unusual 10-day move is +9.5 % (t 2.37, 48 cases) when the breaking day rose about 3.8 %, and +8.4 % (t 2.78, 47 cases) when it rose about 7.3 %. When it rose about 15.2 %, the move is -3.1 % (t -1.06, 47 cases).
- **F5:** The narrowness of the prior 60-day range grades the follow-through, with a Spearman of -0.22 between range width and the 10-day move. Breaks out of the narrowest ranges (width 24 % of price) gain +22.1 % over 10 days (t 2.82, 25 cases), against +2.6 % at 37 % width and +4.4 % at 50 % width.
- **F6:** The profit is concentrated by coin and by period:

## Ideas
- `032-02.b1.e1_quiet-breakouts-continue-longer` (from F2, F3, F4): In a coin that has gone nowhere over the past 60 days, a daily close above its prior 60-day high is followed by a rise over the next 10 days, and the smaller that day's own 1-day gain, the larger the rise.
- `032-02.b1.e2_tight-range-breakouts-continue` (from F2, F5): In a coin that has gone nowhere over the past 60 days, a daily close above its prior 60-day high is followed by a rise over the next 10 days, and the narrower that 60-day range was relative to the price, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

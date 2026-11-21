---
line: 7.g patterns
backtest: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.e2_breakout-in-falling-week-fails_4h
idea tested: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.e2_breakout-in-falling-week-fails
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.5550 USD
---
## Findings
- **F1:** When a 4h bar closes below the lowest low of the preceding two days after the deepest fifth of 7-day falls (measured against each coin's usual 7-day move), the coin over the next three days does +2.19 % better than its normal drift. That is t 5.77 over 934 cases, with 19 of 19 coins positive and a strength of 0.237, about 10 times the 0.22 % cost of a buy and a sell. Over all such breakdowns, the deeper the week's fall, the larger the rise (Spearman rho -0.105, p 7e-13).
- **F2:** The rebound in F1 grows with the horizon and holds in most years. It is +1.07 % (t 3.99) over one day, +2.19 % (t 5.77) over three days and +2.96 % (t 6.42, 924 cases) over six days. By year it is positive in 7 of 8 years (2021 t 3.7, 2024 t 4.96, 2025 t 4.65); 2018 is the exception at -0.81 % (t -1.0).
- **F3:** A deep falling week alone does not carry the rebound; the breakdown bar does. On all grid bars, the deepest tenth of coin-standardised 7-day returns is followed by only +0.50 % over three days (t 1.68, 1125 cases). After breakdowns in the deepest fifth of falling weeks the figure is +2.19 % (F1).
- **F4:** Against the brief, a narrow two-day range is followed by smaller and weaker moves, not larger ones. By quintile of the coin's two-day range against its 20-day average, from narrowest to widest:
- **F5:** The lag after a narrow range in F4 holds in both trends and in most years. It is -0.71 % (t -3.10) when the coin fell over the past 20 days and -0.58 % (t -2.00) when it rose. It is negative in 7 of 8 years; 2020 is the exception at +2.27 %. The same ordering shows in recent volatility against its 60-day level: the calmest fifth is followed by -0.71 % (t -3.70) and the most agitated fifth by +0.78 % (t 3.20, 15 of 19 coins positive).
- **F6:** The tested short of upside breakouts in a falling week is graded as the idea says. On raw cases it is -0.56 % against drift over three days (t -3.18, 2157 cases). By quintile of the week's fall the drift-adjusted returns run from -1.60 % for the deepest fall (t -3.50) to +0.73 % for the shallowest (t 2.07).
- **F7:** The book still earns almost nothing.
- **F8:** Hour-of-day effects are statistically strong but too small to trade. The bar starting 16:00 UTC returns +0.034 of a usual 4h move (t 6.7) and the 20:00 UTC bar returns -0.022 (t -4.1). Both are a few bps, far below the 22 bps round-trip cost (findings F2, F6).

## Ideas
- `019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.e2_breakout-in-falling-week-fails.g1_breakdown-after-deep-week-rebounds` (from F1, F2, F3): When a four-hour bar closes below the lowest low of the preceding two days after the coin has fallen over the past 7 days, the coin rises over the next three days, and the deeper the past week's fall against the coin's usual weekly move, the larger the rise.
- `019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.e2_breakout-in-falling-week-fails.g2_quiet-ranges-precede-underperformance` (from F4, F5): The narrower a coin's price range over the past two days compared with its usual two-day range over the past 20 days, the more the coin lags its normal drift over the next three days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

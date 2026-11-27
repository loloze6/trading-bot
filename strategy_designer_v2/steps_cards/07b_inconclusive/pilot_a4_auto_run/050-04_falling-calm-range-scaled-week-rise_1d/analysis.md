---
line: 7.b inconclusive
backtest: 050-04_falling-calm-range-scaled-week-rise_1d
idea tested: 050-04_falling-calm-range-scaled-week-rise
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.2146 USD
---
## Findings
- **F1:** The test's result is on the side the idea predicts but short of the bar: the forecast-weighted mean 3-day excess return is +0.70 % with t 1.26 (389 cases on 204 days), the supporting check passes (+0.58 % above minus below the median), and the unusual move is +0.54 % per case (t 1.31, 302 days), a strength of 0.058, the size real ideas usually show; so the effect is the usual size and lacks only the cases to show it.
- **F2:** The test's horizon is not the problem: on the explore half the weighted mean excess return is positive at every horizon, +0.25 % (1 day, t 0.69, 240 cases), +1.32 % (3 days, t 1.30, 80 cases), +1.90 % (5 days, t 1.27, 48 cases), +1.64 % (7 days, t 0.77, 32 cases) and +4.29 % (10 days, t 1.15, 24 cases); no horizon is clearly better than the plan's 3 days.
- **F3:** The effect is graded as the idea says but carried by its largest cases: at 3 days the top quarter of forecasts earns +2.45 % excess (t 1.46, 20 cases) against -0.46 % to +0.12 % in the three lower quarters, the top quarter of the raw range-scaled 7-day rise earns +2.25 % (t 1.89) against -1.45 % in the bottom quarter, and the Spearman correlation with the excess return is 0.15 for the forecast and 0.20 for the raw scaled rise.
- **F4:** The effect is mixed across coins and years, which adds noise to a small sample: at 3 days BTC loses -1.12 % (t -1.38, 30 cases) while XMR gains +2.47 % (t 1.66, 37 cases) and DOGE +2.62 % (t 1.12, 13 cases); by year the results are 2018 -0.23 % (27 cases), 2019 -1.28 % (24 cases) and 2021 +1.84 % (25 cases); no single coin or period holds the effect clearly enough to narrow the idea to it.
- **F5:** The depth of the downtrend does not decide the effect: the 3-day excess return is +0.59 % in the deepest third of 60-day falls, +0.07 % in the middle third and +0.49 % in the mildest, all with t under 0.5.
- **F6:** The sample is what holds the result back: the falling-calm profile with a 7-day rise is rare (the book is in a position on 12 % of coin-days), so the explore half has only 80 cases on 63 days at the 3-day grid, and the test used 6 of the 19 coins with data; another 13 coins (ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO) can add cases in folds A and D and part of B and C.
- **F7:** Cost does not rule the idea out: the total move per case, +0.75 %, is 2.2 times the 0.33 % cost of a trade, and the unusual move, +0.54 %, is 1.6 times it.

## Ideas
- `050-04.b1_range-scaled-week-rise-all-coins` (from F1, F3, F6, F7): In a falling, calm market, a coin that has risen over the last 7 days keeps rising over the next 3 days, and rises further the larger its 7-day rise is in units of its 30-day average daily range.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

---
line: 7.b inconclusive
backtest: 050-02_falling-calm-scaled-week-rise-continuation_1d
idea tested: 050-02_falling-calm-scaled-week-rise-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4114 USD
---
## Findings
- **F1:** Step 5's main measure lies on the side the idea predicts but falls short of the bar: a +0.64 % unusual 3-day move per case, 0.077 of the coin's usual 8.43 % move, t 1.89 over 503 cases on 341 days. This strength is in line with real ideas measured so far, about 0.05, so the effect looks small for this data rather than absent.
- **F2:** The effect is not tied to one coin, but it is mixed over time. On the explore half (101 cases) all four coins have a positive mean unusual 3-day move: BCH +0.47 %, ETH +1.01 %, XMR +0.73 %, ZEC +0.21 %, each with t under 1. By year the sign flips: 2019 is −0.68 % (t −0.96, 40 cases) against 2021 +2.61 % (t 2.12, 24 cases). So the market's own swings drown a small effect, which more cases would average out.
- **F3:** The grading fails at the plan's 3-day horizon, which is why the supporting check fails as well as the t. Step 5's size difference was −0.22 % (Welch t −0.38). On the explore half, the top forecast quartile (mean forecast 18.7) has −0.94 % against +2.28 % for the third quartile, with a Spearman correlation of −0.04 between forecast and the 3-day move.
- **F4:** The effect and its grading show more clearly over 5 days than over 3. On the explore half the mean unusual move is +1.48 % over 5 days (t 1.71, 95 cases) against +0.63 % over 3 days (t 1.01), and it fades to +1.06 % over 7 days and +0.67 % over 10 days. Over 5 days the raw scaled 7-day rise ranks the move positively (Spearman +0.13): its lowest quartile has −0.95 % against +2.57 %, +1.68 % and +2.23 % for the three larger quartiles.
- **F5:** More data is available than the test used. Thirteen more coins have daily bars in folds A and D, and partly in B and C: ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO and ONDO. This would add cases to an effect whose t of 1.89 is short only by its noise.

## Ideas
- `050-02.b1_calm-downtrend-week-rise-more-coins` (from F1, F2, F5): In a falling, calm market, a coin that has risen over the last 7 days keeps rising over the next 3 days, and rises further the larger its 7-day rise is in units of its 30-day daily-return swing.
- `050-02.b2_calm-downtrend-week-rise-five-days` (from F3, F4): In a falling, calm market, a coin that has risen over the last 7 days keeps rising over the next 5 days, and rises further the larger its 7-day rise is in units of its 30-day daily-return swing.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

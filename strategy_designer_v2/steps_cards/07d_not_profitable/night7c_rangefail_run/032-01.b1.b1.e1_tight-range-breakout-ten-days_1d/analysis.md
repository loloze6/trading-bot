---
line: 7.d confirmed, not profitable
backtest: 032-01.b1.b1.e1_tight-range-breakout-ten-days_1d
idea tested: 032-01.b1.b1.e1_tight-range-breakout-ten-days
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4324 USD
---
## Findings
- **F1:** Calmar fails on the depth of the falls, not on cost. On folds B and C the rebuilt book's deepest fall is -8.7%, running 573 days from w11 to w16, against a yearly return of +8.6%. The worst stretch is w12, where the book summed -2.7% and its 10 entries averaged a 10-day return of -15.7% with a mean worst point of -18.4%. Cost is small beside the move: the total move per case is +6.23%, 27.9 times the 0.22% a trade costs.
- **F2:** The losses sit in the wide-range breakouts.
- **F3:** Narrowness amplifies the break more than it acts alone.
- **F4:** Breakouts that close back below the broken 60-day high within 3 days (30 of 112) carry the falls.
- **F5:** Breakouts after quiet daily returns behave like the narrow ones (no separate check of this condition alone was made).

## Ideas
- `032-01.b1.b1.e1.d1_narrow-range-breakout-continuation` (from F1, F2, F3): In a coin whose price has gone nowhere over the past 60 days, a daily close above its prior 60-day high is followed by a further rise over the next 10 days, and the rise is carried by breaks out of narrow ranges. The rise grows steeply as the prior 60-day high-low range narrows against the price and nearly vanishes in the widest ranges.
- `032-01.b1.b1.e1.d2_breakout-held-above-level` (from F1, F4, F2): In a coin whose price has gone nowhere over the past 60 days, a daily close above its prior 60-day high is followed by a further rise over the next 10 days for as long as the daily close stays above that broken high. The further the close stays above the broken high, the larger the rise, while breaks whose close falls back under it give back their gain.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

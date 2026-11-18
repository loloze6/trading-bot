---
line: 7.d not profitable
backtest: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation_1d
idea tested: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3317 USD
---
## Findings
- **F1:** The book is long only on breakout bars, 5.5% of all bars, at a mean position of 0.57. Its mean daily return is 0.000103 against holding's 0.00118 (Sharpe 0.40 vs 0.55). Only 0.000038 per bar of its 0.000148 gross gain comes from the market's own rise, and fees take 0.000045 per bar.
- **F2:** The rise after a breakout comes mostly after the breakout bar, which the book has already left. The coin's excess daily return is 0.00183 on the breakout bar itself (t 0.96, n 967). It is 0.00393 on days 1–3 after it (t 2.99, n 1715), falls to 0.00049 on days 4–6 (t 0.35), and turns negative from day 11 on (−0.0016, t −1.19, n 1378).
- **F3:** Over the 404 non-overlapping breakout cases, the 10-day excess return over holding is +0.0229 (t 2.14, mean 10-day return 0.0347 against the coins' 0.0118). The book, which holds only the breakout bar, captures little of this. Its chained gain is 30% over 2898 days, with a deepest fall of −12.8%, so Calmar is 0.26.
- **F4:** The 20-day/100-day range width that sizes the position does not grade the outcome. The 10-day excess by width third is +0.017 (low), +0.027 (mid) and +0.024 (high), each with t of 1.4 or less. The slope t is 0.39.
- **F5:** Volume on the breakout bar, against its prior 20-day average, does grade the following rise. The mean 10-day return is 0.032, 0.047 and 0.075 across the low, mid and high volume-ratio thirds (259 overlapping breakout bars each).
- **F6:** The breakout effect differs by coin. The 10-day excess is +0.083 for XRP, +0.051 for ZEC and +0.024 for ETH, but −0.014 for LTC and −0.007 for XMR. LTC and XMR are also the two coins where the book's gross gain per bar is negative.

## Ideas
- `006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.d1_volume-surge-breakout-follow-through` (from F2, F3, F4, F5): When a coin closes above the high of its prior 20 days, the larger that day's volume against its prior 20-day average volume, the further price rises over the next 3 days.
- `006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.d2_breakout-rise-lasts-days` (from F1, F2, F3, F5): When a coin closes above the high of its prior 20 days, the wider its 20-day range was against its 100-day range, the further price rises over the next 10 days, with most of that rise coming over the 3 days after the breaking day, and more so the larger that day's volume against its prior 20-day average.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

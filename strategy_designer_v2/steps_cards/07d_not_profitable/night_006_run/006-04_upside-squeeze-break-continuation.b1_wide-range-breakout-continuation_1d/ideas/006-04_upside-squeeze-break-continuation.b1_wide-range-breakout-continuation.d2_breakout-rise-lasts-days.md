---
brief: 006_range-compression-precedes-expansion
source-idea: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation
line: 7.d not profitable
backtest: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes above the high of its prior 20 days, the wider its 20-day range was against its 100-day range, the further price rises over the next 10 days, with most of that rise coming over the 3 days after the breaking day, and more so the larger that day's volume against its prior 20-day average.
Consequence: A trader acting on this idea would hold upside breaks for several days rather than one bar, which is where the excess return that the book misses lies.
Why:
- F1: The book is long only on breakout bars, 5.5% of all bars, at a mean position of 0.57. Its mean daily return is 0.000103 against holding's 0.00118 (Sharpe 0.40 vs 0.55). Only 0.000038 per bar of its 0.000148 gross gain comes from the market's own rise, and fees take 0.000045 per bar.
- F2: The rise after a breakout comes mostly after the breakout bar, which the book has already left. The coin's excess daily return is 0.00183 on the breakout bar itself (t 0.96, n 967). It is 0.00393 on days 1–3 after it (t 2.99, n 1715), falls to 0.00049 on days 4–6 (t 0.35), and turns negative from day 11 on (−0.0016, t −1.19, n 1378).
- F3: Over the 404 non-overlapping breakout cases, the 10-day excess return over holding is +0.0229 (t 2.14, mean 10-day return 0.0347 against the coins' 0.0118). The book, which holds only the breakout bar, captures little of this. Its chained gain is 30% over 2898 days, with a deepest fall of −12.8%, so Calmar is 0.26.
- F5: Volume on the breakout bar, against its prior 20-day average, does grade the following rise. The mean 10-day return is 0.032, 0.047 and 0.075 across the low, mid and high volume-ratio thirds (259 overlapping breakout bars each).

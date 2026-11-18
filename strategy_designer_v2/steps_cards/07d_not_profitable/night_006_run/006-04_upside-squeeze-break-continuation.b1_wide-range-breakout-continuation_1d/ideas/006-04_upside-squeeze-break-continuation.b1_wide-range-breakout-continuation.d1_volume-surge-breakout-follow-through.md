---
brief: 006_range-compression-precedes-expansion
source-idea: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation
line: 7.d not profitable
backtest: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes above the high of its prior 20 days, the larger that day's volume against its prior 20-day average volume, the further price rises over the next 3 days.
Consequence: A trader would stay long for the few days after an upside break and size the position by the volume surge on the breaking day, instead of holding only the breaking bar and sizing by the prior range width.
Why:
- F2: The rise after a breakout comes mostly after the breakout bar, which the book has already left. The coin's excess daily return is 0.00183 on the breakout bar itself (t 0.96, n 967). It is 0.00393 on days 1–3 after it (t 2.99, n 1715), falls to 0.00049 on days 4–6 (t 0.35), and turns negative from day 11 on (−0.0016, t −1.19, n 1378).
- F3: Over the 404 non-overlapping breakout cases, the 10-day excess return over holding is +0.0229 (t 2.14, mean 10-day return 0.0347 against the coins' 0.0118). The book, which holds only the breakout bar, captures little of this. Its chained gain is 30% over 2898 days, with a deepest fall of −12.8%, so Calmar is 0.26.
- F4: The 20-day/100-day range width that sizes the position does not grade the outcome. The 10-day excess by width third is +0.017 (low), +0.027 (mid) and +0.024 (high), each with t of 1.4 or less. The slope t is 0.39.
- F5: Volume on the breakout bar, against its prior 20-day average, does grade the following rise. The mean 10-day return is 0.032, 0.047 and 0.075 across the low, mid and high volume-ratio thirds (259 overlapping breakout bars each).

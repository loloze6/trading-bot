---
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
source-idea: 021-03_thin-cloud-upward-breakout.d2_calm-breakout-lasts-longer
line: 7.g patterns
backtest: 021-03_thin-cloud-upward-breakout.d2_calm-breakout-lasts-longer_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's one-day fall relative to its usual daily move, the more the coin rises over the next 1 to 3 days.
Consequence: A trader would buy into a coin's sharpest daily falls, and refuse to sell it short right after them, expecting a rebound that grows with the depth of the fall.
Why:
- F1: On daily bars, a coin's next-day return runs against the size of its day's move. Over all days with |z| > 1 (z is the day's return standardised by the coin's own mean and standard deviation), the Spearman correlation of z with the next day's return is -0.129 (p < 0.0001, n = 3510). This is the strongest pattern of the angles examined, and the one that would most clearly survive the many angles looked at.
- F2: The rebound after falls is graded. The next day's mean return is:
- F3: The rebound after large falls (z ≤ -2) is spread across the sample, not carried by one place:

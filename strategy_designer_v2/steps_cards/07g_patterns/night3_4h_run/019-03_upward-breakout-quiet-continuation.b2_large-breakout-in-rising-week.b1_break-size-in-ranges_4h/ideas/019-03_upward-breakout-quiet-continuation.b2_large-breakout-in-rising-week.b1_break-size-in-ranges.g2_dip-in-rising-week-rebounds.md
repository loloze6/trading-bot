---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b1_break-size-in-ranges
line: 7.g patterns
backtest: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b1_break-size-in-ranges_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: While a coin's 7-day return is positive, the further its close has fallen over the past day, counted in its usual one-day move, the more it rises over the next one to three days.
Consequence: A trader would buy dips in a rising week, sized by how many usual daily moves the dip spans, and hold them a day or more.
Why:
- F1: Across the 6 coins, a coin's 1-day return counted in its usual 1-day move predicts the next day the other way. The bottom decile of that return is followed by an excess of +0.55 % over the next day (strength 0.105, t 3.64, 1638 independent cases) and the second decile by +0.28 % (strength 0.060, t 2.36, 1535 cases). Deciles 6 to 9 are followed by −0.19 % to −0.21 % (strength −0.040 to −0.049, t −1.4 to −2.1). The correlation of the 1-day z-return with the next day's z-move is negative on every coin (−0.019 BTC to −0.103 XMR). Before costs, then, the move is graded.
- F3: The same rebound is about 2.5 times larger while the coin's 7-day return is positive: +0.71 % over the next day (strength 0.142, t 5.03, 984 cases), against +0.28 % (strength 0.057, t 2.28, 2189 cases) when the 7-day return is negative. Measured over 3 days, the bottom decile of the 1-day z-return is followed by +1.18 % (strength 0.128, t 3.08, 538 cases).

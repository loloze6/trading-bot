---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g3_moderate-falls-keep-falling
line: 7.d not profitable
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g3_moderate-falls-keep-falling_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 14-day rise, the higher its return over the next 7 days, and the larger its 14-day fall, the lower its return over the next 7 days, with the strongest follow-through after the largest rises.
Consequence: A trader would lean long in proportion to a coin's two-week rise and short in proportion to its two-week fall, putting most of the risk on the rising side, where the market's own drift adds to the gain instead of taking it away.
Why:
- F1: The book earns 0.42 bp a day against 11.8 bp for holding the coins (Sharpe 0.22 against 0.55), so the yearly return is too small for the Calmar of 0.07; it is short on 55% of bars (9,676 of 17,524), long on only 6.4% (1,124), and flat on 38%, which gives a market part of −0.70 bp a day that eats most of its 1.5 bp of timing gain.
- F2: After 14-day rises, where the book is always flat, the excess 7-day return rises with the size of the rise, from +0.26% in the smallest fifth (n=171, t=0.29) to +3.76% in the largest fifth of rises scaled by volatility (n=171, t=2.55); this is the largest graded effect in the data, and the book takes none of it.
- F3: After 14-day falls the excess 7-day return is negative in five of the six fall-size sextiles, between −1.2% and −1.9% for the middle grades (t −1.3 to −1.9, about 145 cases each), so the short side's direction is right but its edge is about 1.5% a week.
- F5: Positions are small: the mean absolute allocation on active bars is 0.155 (median 0.144), so even the correct short edge turns into only 0.37 bp a day on short bars.

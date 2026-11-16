---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.g1_high-volatility-fall-rebound
line: 7.b inconclusive
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.g1_high-volatility-fall-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's 20-day volatility is high compared with its own past levels, the larger its one-day fall relative to its usual daily move over the past 20 days, the larger its rise over the next day, growing fastest among its largest falls.
Consequence: A trader in turbulent stretches would weight buys toward the most extreme vol-scaled falls, where the next-day rebound is concentrated.
Why:
- F1: Step 5's main measure is clearly on the predicted side: the next-day return minus the coin's mean, regressed on the forecast over 3447 regime bars, has a slope of 0.0011 with t 5.89. The result is inconclusive only because the supporting check failed: the slope where the volatility percentile is at least 0.9 is 0.00043 smaller than where it is between 0.8 and 0.9 (636 vs 242 bars).
- F4: Inside the regime, the gain sits in the largest falls. The top forecast quintile (mean forecast 16.3) is followed by a next-day excess return of +1.70% (t 4.25, n 204). The middle three quintiles are near zero (−0.03% to +0.16%, t at most 0.35).

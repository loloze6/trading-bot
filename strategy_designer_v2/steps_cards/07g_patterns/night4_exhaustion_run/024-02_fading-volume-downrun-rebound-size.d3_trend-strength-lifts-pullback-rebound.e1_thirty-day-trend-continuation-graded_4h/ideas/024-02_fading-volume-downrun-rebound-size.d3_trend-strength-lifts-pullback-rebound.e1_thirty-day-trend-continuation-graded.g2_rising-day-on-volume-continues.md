---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-02_fading-volume-downrun-rebound-size.d3_trend-strength-lifts-pullback-rebound.e1_thirty-day-trend-continuation-graded
line: 7.g patterns
backtest: 024-02_fading-volume-downrun-rebound-size.d3_trend-strength-lifts-pullback-rebound.e1_thirty-day-trend-continuation-graded_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: After a day on which the coin rose, the higher its volume over that day relative to its ten-day average volume, the more it keeps rising over the next three days beyond its normal drift.
Consequence: A trader adds to a long after a rising day in proportion to the volume behind it, and refuses to chase a rising day made on thin volume.
Why:
- F1: Volume predicts the 3-day move better than the tested 30-day return does. The log of a coin's last-day mean volume over its last-ten-day mean volume has a pooled slope on the 18-bar excess return of +0.0077 (t 3.81, 5148 non-overlapping cases), and the 3-day versus 20-day version has slope +0.0104 (t 4.00, 4716 cases). Excess return rises from -0.55 % in the lowest per-coin volume quintile to +0.79 % in the highest (t 2.64).
- F2: The volume effect holds broadly and is stronger over one day and after a rising day.

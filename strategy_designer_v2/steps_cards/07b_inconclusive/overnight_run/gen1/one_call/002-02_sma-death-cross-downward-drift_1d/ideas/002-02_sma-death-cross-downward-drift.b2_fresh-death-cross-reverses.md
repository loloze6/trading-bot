---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-02_sma-death-cross-downward-drift
line: 7.b inconclusive
backtest: 002-02_sma-death-cross-downward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's 50-day SMA has just crossed below its 200-day SMA, within the last 20 bars, the coin rises over the next 10 days by more than its average 10-day move.
Consequence: A trader would not open a short on a fresh death cross, and would treat the first weeks after it as prone to reversal.
Why:
- F6: Fresh death crosses tend to reverse rather than persist. Cases at most 20 bars after the cross give -0.026 (t -1.60, hit 41%). Cases 51 to 100 bars after give +0.016 (t 0.83).
- F2: The sign flips by period rather than by coin, so the pooled result cancels out. 2018 gives +0.037 (t 1.75) and 2019 gives +0.016 (t 1.87). 2020 gives -0.079 (t -4.44) and 2021 gives -0.063 (t -2.54). Every coin sits near zero, between t -0.57 and t 0.75.

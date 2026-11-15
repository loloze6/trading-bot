---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-01_sma-golden-cross-upward-drift
line: 7.b inconclusive
backtest: 002-01_sma-golden-cross-upward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In the first 30 days after a coin's 50-day SMA crosses above its 200-day SMA, the coin falls relative to its usual move over the next 10 days, and the fresher the cross, the larger the fall.
Consequence: A trader should not buy a fresh golden cross right away, because its early move tends to give back.
Why:
- F8: Fresh up-crosses tend to reverse rather than start a trend: in the first 30 days after the 50-day SMA turns above the 200-day, the 10-day excess is -0.021 (t -1.96, 147 cases), against +0.014 (t 0.89, 120) for 30 to 90 days after the cross.
- F6: The forecast's own grading is not monotone: the 10-day excess is -0.0085 in forecast 0-5, +0.0023 in 5-10, +0.0105 in 10-15 and +0.00004 in 15-20, and the widest raw-spread quintile gives -0.0049 against +0.012 in the middle one (t 1.47).

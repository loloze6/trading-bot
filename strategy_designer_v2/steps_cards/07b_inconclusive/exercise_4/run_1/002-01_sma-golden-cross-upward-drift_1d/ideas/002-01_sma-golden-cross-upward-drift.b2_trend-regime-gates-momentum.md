---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-01_sma-golden-cross-upward-drift
line: 7.b inconclusive
backtest: 002-01_sma-golden-cross-upward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The further a coin's 20-day return has risen, the more it rises over the next 10 days, only while its 50-day SMA is above its 200-day SMA.
Consequence: A short-term momentum long is worth taking only in the coin's long-term up-trend regime and should be refused below the 200-day average cross.
Why:
- F4: The same 20-day return carries no forward information while the 50-day SMA is below the 200-day SMA (slope -0.020, t -0.84, 681 cases). The up-minus-down 20-day-return split is -0.004 (t -0.40) there, against +0.039 (t 3.00; 361 vs 333 cases) in the up-trend. So the golden-cross state acts as a regime for short-term momentum, not as a signal by itself.
- F3: Within bars where the 50-day SMA is above the 200-day SMA, the coin's 20-day return grades the next 10 days clearly. Its slope on excess return is 0.069 with t 3.26 over 694 cases. The quartiles rise in order: q1 -0.029, q2 -0.001, q3 +0.010, q4 +0.034.

---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-01_sma-golden-cross-upward-drift
line: 7.b inconclusive
backtest: 002-01_sma-golden-cross-upward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's 50-day SMA is above its 200-day SMA, the higher its 20-day return, the more it rises over the next 10 days relative to its usual 10-day move.
Consequence: Within a golden-cross up-trend, a trader should weight longs by recent 20-day strength rather than by the width of the SMA spread, and stand aside on up-trend coins that have lagged.
Why:
- F3: Within bars where the 50-day SMA is above the 200-day SMA, the coin's 20-day return grades the next 10 days clearly. Its slope on excess return is 0.069 with t 3.26 over 694 cases. The quartiles rise in order: q1 -0.029, q2 -0.001, q3 +0.010, q4 +0.034.
- F4: The same 20-day return carries no forward information while the 50-day SMA is below the 200-day SMA (slope -0.020, t -0.84, 681 cases). The up-minus-down 20-day-return split is -0.004 (t -0.40) there, against +0.039 (t 3.00; 361 vs 333 cases) in the up-trend. So the golden-cross state acts as a regime for short-term momentum, not as a signal by itself.
- F5: The interaction of forecast and 20-day return is significant (slope 0.0031, t 2.87, 1375 cases). The 20-day effect is positive for 4 of 6 coins in the up-trend (ZEC t 1.78, XRP t 1.60). It is positive in 2019–2021 and 2024–2025 (t 2.47 in 2024, 2.24 in 2025) but negative in 2023 (t -2.66, 99 cases).
- F1: The plan's forecast slope on the coin's excess 10-day return is flat at every horizon (t 0.20, 0.37, 0.55 and -0.06 at 5, 10, 20 and 40 days; 3349, 1657, 811 and 388 non-overlapping cases), and inside the active bars the forecast buckets do not rise in order (0–5: -0.0085, 5–10: +0.0023, 10–15: +0.0105, 15–20: -0.0012, capped 20: +0.0009). So the spread's size grades nothing.

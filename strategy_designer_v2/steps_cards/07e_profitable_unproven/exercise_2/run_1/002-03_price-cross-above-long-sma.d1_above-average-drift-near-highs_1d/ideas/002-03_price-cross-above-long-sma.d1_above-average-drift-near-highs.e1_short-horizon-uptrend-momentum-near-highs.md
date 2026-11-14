---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs
line: 7.e profitable but not proven
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes above its long moving average, the nearer its close sits to the top of its recent range and the stronger its recent rise, the larger its return over the following days to two weeks. The effect fades by about a month.
Consequence: Hold momentum longs inside an uptrend for days to a couple of weeks, not a month, and size them by how close price is to its recent high.
Why:
- F1: The book's gain is mostly timing rather than the coins' own rise: its daily beta to holding is 0.15 with a daily alpha of 0.00039 (t 2.19, 2898 days), and the position's next-bar gain beats the coin's drift by 0.00039 per bar (t 2.94), while time-in-market × drift explains only 0.00022 of the 0.00062 mean gain.
- F2: The edge sits inside the above-200-day-average regime and is short-horizon. On non-overlapping grids, high-forecast bars minus trending bars with zero forecast give Welch t of 3.10 at 1 bar (3045 vs 2440 cases), 2.88 at 5 bars (600 vs 474) and 2.64 at 10 bars (299 vs 235), but only 0.94 at the plan's 20 bars (142 vs 124), which is why the verdict's 20-bar t was 0.61.
- F3: Being above the long average adds nothing by itself: next-day coin return is 0.001187 in the trending regime and 0.001193 in the unknown regime. The same momentum-near-high ranking separates returns only when the coin is trending (high minus low t 2.77 at 1 bar, 3.05 at 5 bars) and not when it is below the average (t 0.15 at 1 bar, −0.47 at 5 bars).
- F4: The response to forecast strength is graded. Next-day coin return rises monotonically across forecast quintiles: −0.00024, 0.0019, 0.0020, 0.0030, 0.0040 (1218 bars each).

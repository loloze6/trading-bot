---
brief: 012_liquidation-flush-partial-rebound
source-idea: 012-03_lower-wick-flush-recovery
line: 7.g patterns
backtest: 012-03_lower-wick-flush-recovery_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's volume on a down day relative to its prior 20-day median, the larger its excess rise over the next 3 days, whatever the size of that day's fall in units of its 20-day volatility.
Consequence: A trader can scale a 3-day long by the volume surge alone and need not wait for a sharp volatility-scaled fall or a long lower wick.
Why:
- F1: On down days, sampled on each window's 0,3,6,... grid, the coin's excess 3-day return rises with the log of the day's volume over its prior 20-day median: slope 0.0126, t 4.72, n 2245. The slope stays at t 4.44 once the day's volatility-scaled return is controlled for. It has the same sign in both halves (w1-12 t 2.79, w13-24 t 3.78) and in 7 of 8 years, and it is positive for all six coins (t from 0.36 for BTC to 2.55 for ZEC).
- F3: The tested wick share adds nothing among sharp falls on a volume burst. On grid events with z ≤ -1.5 and volume ratio ≥2, the slope of excess 3-day return on wick share is 0.0067 (t 0.16, n 109). With overlapping events, burst falls give +0.019 at the low-wick tercile and +0.0097 at the high-wick tercile. The rebound is carried by the volume, not the wick.

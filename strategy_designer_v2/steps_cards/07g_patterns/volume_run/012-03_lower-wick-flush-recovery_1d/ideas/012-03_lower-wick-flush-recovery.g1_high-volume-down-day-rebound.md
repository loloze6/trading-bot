---
brief: 012_liquidation-flush-partial-rebound
source-idea: 012-03_lower-wick-flush-recovery
line: 7.g patterns
backtest: 012-03_lower-wick-flush-recovery_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: On a day a coin closes lower, the larger that day's volume relative to its median over the prior 20 days, the larger the coin's rise over the next 3 days.
Consequence: A down day on heavy volume, even a modest fall, is a reason to buy the coin for a 3-day rebound in proportion to the volume surge, and a quiet down day is not.
Why:
- F1: On down days, sampled on each window's 0,3,6,... grid, the coin's excess 3-day return rises with the log of the day's volume over its prior 20-day median: slope 0.0126, t 4.72, n 2245. The slope stays at t 4.44 once the day's volatility-scaled return is controlled for. It has the same sign in both halves (w1-12 t 2.79, w13-24 t 3.78) and in 7 of 8 years, and it is positive for all six coins (t from 0.36 for BTC to 2.55 for ZEC).
- F2: The effect is graded in volume. Excess 3-day returns on down days are -0.0026 (t -1.10, n 1203) at volume ratio ≤1, +0.0014 (n 237) at 1.5–2, +0.022 (t 2.76, n 174) at 2–3, +0.035 (t 3.25, n 91) at 3–5 and +0.060 (t 2.33, n 34) above 5. On up days the slope is the other way and not significant: -0.0030, t -1.35, n 2466.
- F3: The tested wick share adds nothing among sharp falls on a volume burst. On grid events with z ≤ -1.5 and volume ratio ≥2, the slope of excess 3-day return on wick share is 0.0067 (t 0.16, n 109). With overlapping events, burst falls give +0.019 at the low-wick tercile and +0.0097 at the high-wick tercile. The rebound is carried by the volume, not the wick.
- F4: The book barely trades and loses. It is in position on about 1.5% of bars (522 of 17,524 coin-days), with a mean in-position daily return of -0.00014 and a Sharpe of -0.03. The trigger requires z ≤ -2 together with a volume burst, which leaves out most of the high-volume down days that carry F1.

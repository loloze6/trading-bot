---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.g1_next-day-rebound-after-sharp-falls
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.g1_next-day-rebound-after-sharp-falls_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's 20-day volatility is high against its own past 120 days, the larger its one-day return relative to that 20-day volatility, the lower its return over the next 1 day, on up days as well as down days.
Consequence: In high-volatility periods a trader can fade a coin's sharp one-day moves in both directions for one day, instead of trading only the down side.
Why:
- F4: In the high-volatility tercile the reversal holds on all bars, both sides: the slope of next-day excess return on the scaled one-day return is −0.0041 (t −4.38, n 2962), against 0.0009 (t 1.14) in the low tercile; moderate up days (z 0.5 to 1) are followed by −0.0023 (t −2.43, n 1987).
- F1: The rebound after down days lives in high volatility: on down days split by the coin's 20-day volatility rank within its own past 120 days, the slope of next-day excess return on the scaled fall is 0.0073 (t 3.45, n 1459) in the high tercile, 0.0007 (t 0.37) in the middle and −0.0011 (t −0.59) in the low; the fall × volatility-rank interaction has t 3.57, and fall alone has t −1.84.

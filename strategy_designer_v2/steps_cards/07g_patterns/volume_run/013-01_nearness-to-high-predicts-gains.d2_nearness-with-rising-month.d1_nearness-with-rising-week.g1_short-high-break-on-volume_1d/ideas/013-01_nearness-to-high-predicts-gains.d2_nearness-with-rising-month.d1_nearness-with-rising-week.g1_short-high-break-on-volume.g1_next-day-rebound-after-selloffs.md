---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g1_short-high-break-on-volume
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g1_short-high-break-on-volume_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The deeper a coin's one-day fall relative to its own 30-day daily volatility, the higher its return over the next 1 day.
Consequence: After a coin's sharp vol-scaled down day, lean long for the next day instead of following the drop, and refuse new shorts into it.
Why:
- F1: The day after a sharp fall reverses. Across all bars, the next-day excess return in the lowest decile of the day's return over its 30-day volatility is +0.584% (t 3.90, n 1450), and in the second-lowest decile +0.321% (t 2.72, n 1450). Deciles 3 to 10 sit between -0.215% and -0.003%, none with |t| above 1.9. The idea, which is about rising into the high, does not explain this.
- F6: The book's worst days follow market rises and are followed by rebounds. On the book's worst 2% of days, the mean coin return the day before is +1.65% and the book's next day is +0.134%. This fits with F1: the book is caught long into sharp one-day reversals.

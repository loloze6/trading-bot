---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal.g1_sunday-move-reverses-monday
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal.g1_sunday-move-reverses-monday_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 20-day volatility is high against its own past 120 days, a day's return measured in its 20-day standard deviations is reversed over the next 1 day. The reversal is larger the lower that day's volume is against its 20-day average.
Consequence: In turbulent periods, fade large daily moves made on light volume, and fade those made on heavy volume less.
Why:
- F4: The reversal sits in high-volatility periods. With 20-day volatility measured against its own 120-day median, the next-day slope is +0.00069 (t 0.74) in the lowest tercile, −0.00126 (t −1.32) in the middle and −0.00274 (t −2.32) in the highest. On the non-overlapping 3-day grid the highest tercile gives −0.00932 (t −2.64, n 621), against +0.00332 in the lowest.
- F5: Inside the high-volatility tercile, the reversal is stronger on light-volume days, which is the brief's original volume direction and the opposite of the plan's supporting check. Day volume is measured against its 20-day average. The slope is −0.00775 (t −2.64, n 742) in the lowest-volume tercile, −0.00510 (t −2.03) in the middle and −0.00144 (t −0.82) in the heaviest.

---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.d2_daily-move-continues-five-days
line: 7.d not profitable
backtest: 022-04_signal-weights-carry-forward.d2_daily-move-continues-five-days_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's move over the last day, the larger its move in the same direction over the next 5 days, only while that day's move goes the same way as the coin's 20-day return and the coin's 20-day volatility is low against its 120-day volatility.
Consequence: A trader would follow trend-extending days in calm markets and stand aside from them when volatility has risen.
Why:
- F3: The day's move continues only when it agrees with the coin's 20-day return. Then it earns +85 bps unusual move over 5 days (t 2.98, 1530 cases), about 4.4 times the cost. When it opposes the 20-day return it earns −3 bps (t −0.11, 1311 cases). The effect holds on both sides: +96 bps for longs (t 2.01) and +71 bps for shorts (t 1.68).
- F4: Calm volatility is where the move lives. Inside the agreeing cases, when 20-day volatility is low against its 120-day level (lowest tercile), the day's move is followed by +217 bps (t 4.09, 432 cases), about 11 times the cost. The middle tercile gives +64 bps (t 1.13) and the highest −45 bps (t −0.82).
- F6: The agreeing effect rests on the earlier years. It gives +165 to +295 bps per case in 2018 to 2021 (t up to 3.58 in 2019) and is negative in 2022 (−107), 2023 (−70) and 2025 (−84). It is also strongest on XRP (+225 bps, t 2.27) and ZEC (+120 bps). A test of it must survive the one-window-left-out check.

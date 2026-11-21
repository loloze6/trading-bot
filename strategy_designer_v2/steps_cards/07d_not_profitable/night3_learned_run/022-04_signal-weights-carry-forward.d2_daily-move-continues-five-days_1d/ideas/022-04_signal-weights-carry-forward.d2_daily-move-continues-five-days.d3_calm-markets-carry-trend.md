---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.d2_daily-move-continues-five-days
line: 7.d not profitable
backtest: 022-04_signal-weights-carry-forward.d2_daily-move-continues-five-days_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The lower a coin's 20-day volatility against its 120-day volatility, the larger its move over the next 5 days in the direction of its 20-day return.
Consequence: A trader would hold a short-horizon trend position more firmly the calmer the coin has become against its usual volatility.
Why:
- F4: Calm volatility is where the move lives. Inside the agreeing cases, when 20-day volatility is low against its 120-day level (lowest tercile), the day's move is followed by +217 bps (t 4.09, 432 cases), about 11 times the cost. The middle tercile gives +64 bps (t 1.13) and the highest −45 bps (t −0.82).
- F5: The 20-day return alone, signed, carries the same calm-volatility effect. It is followed by +133 bps over 5 days in the lowest volatility-ratio tercile (t 3.37, 756 cases), +49 bps in the middle (t 1.29) and −9 bps in the highest (t −0.24). It is not cleanly graded by the 20-day return's size: by quartile of its z-score it gives 32, 81, 82 and 37 bps.
- F6: The agreeing effect rests on the earlier years. It gives +165 to +295 bps per case in 2018 to 2021 (t up to 3.58 in 2019) and is negative in 2022 (−107), 2023 (−70) and 2025 (−84). It is also strongest on XRP (+225 bps, t 2.27) and ZEC (+120 bps). A test of it must survive the one-window-left-out check.

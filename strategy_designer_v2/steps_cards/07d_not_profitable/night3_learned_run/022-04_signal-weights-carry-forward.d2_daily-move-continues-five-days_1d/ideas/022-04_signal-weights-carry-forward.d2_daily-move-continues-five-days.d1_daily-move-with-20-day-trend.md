---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.d2_daily-move-continues-five-days
line: 7.d not profitable
backtest: 022-04_signal-weights-carry-forward.d2_daily-move-continues-five-days_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's move over the last day, the larger its move in the same direction over the next 5 days, only while that day's move goes the same way as the coin's 20-day return.
Consequence: A trader would follow a large day that extends the coin's 20-day trend and would refuse to follow one that goes against it, notably a large down day inside a rise.
Why:
- F1: The idea's move is about the size of a trade's cost and is not graded. Per case it moves +0.17 % in total against a 0.19 % round trip, a slope t of 1.46 over 3399 cases. By quintile of the forecast's size, the move after a day reads 19, 45, 83, 21 and 27 bps over 5 days, so the largest days carry no more than the smallest. No holding or sizing change can make this pay.
- F2: Large down days reverse rather than continue. After the largest days (|forecast| ≥ 15), the short bets earn −82 bps over 5 days (t −1.72, 377 cases), while the long bets earn +98 bps (t 1.58, 375 cases). In the book, short trades lose 3.33 % net on average over 4333 trades, and long trades gain 2.50 % over 3437.
- F3: The day's move continues only when it agrees with the coin's 20-day return. Then it earns +85 bps unusual move over 5 days (t 2.98, 1530 cases), about 4.4 times the cost. When it opposes the 20-day return it earns −3 bps (t −0.11, 1311 cases). The effect holds on both sides: +96 bps for longs (t 2.01) and +71 bps for shorts (t 1.68).
- F6: The agreeing effect rests on the earlier years. It gives +165 to +295 bps per case in 2018 to 2021 (t up to 3.58 in 2019) and is negative in 2022 (−107), 2023 (−70) and 2025 (−84). It is also strongest on XRP (+225 bps, t 2.27) and ZEC (+120 bps). A test of it must survive the one-window-left-out check.

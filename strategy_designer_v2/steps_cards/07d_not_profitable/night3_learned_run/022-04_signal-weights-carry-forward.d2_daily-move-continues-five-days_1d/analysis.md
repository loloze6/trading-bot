---
line: 7.d not profitable
backtest: 022-04_signal-weights-carry-forward.d2_daily-move-continues-five-days_1d
idea tested: 022-04_signal-weights-carry-forward.d2_daily-move-continues-five-days
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3160 USD
---
## Findings
- **F1:** The idea's move is about the size of a trade's cost and is not graded. Per case it moves +0.17 % in total against a 0.19 % round trip, a slope t of 1.46 over 3399 cases. By quintile of the forecast's size, the move after a day reads 19, 45, 83, 21 and 27 bps over 5 days, so the largest days carry no more than the smallest. No holding or sizing change can make this pay.
- **F2:** Large down days reverse rather than continue. After the largest days (|forecast| ≥ 15), the short bets earn −82 bps over 5 days (t −1.72, 377 cases), while the long bets earn +98 bps (t 1.58, 375 cases). In the book, short trades lose 3.33 % net on average over 4333 trades, and long trades gain 2.50 % over 3437.
- **F3:** The day's move continues only when it agrees with the coin's 20-day return. Then it earns +85 bps unusual move over 5 days (t 2.98, 1530 cases), about 4.4 times the cost. When it opposes the 20-day return it earns −3 bps (t −0.11, 1311 cases). The effect holds on both sides: +96 bps for longs (t 2.01) and +71 bps for shorts (t 1.68).
- **F4:** Calm volatility is where the move lives. Inside the agreeing cases, when 20-day volatility is low against its 120-day level (lowest tercile), the day's move is followed by +217 bps (t 4.09, 432 cases), about 11 times the cost. The middle tercile gives +64 bps (t 1.13) and the highest −45 bps (t −0.82).
- **F5:** The 20-day return alone, signed, carries the same calm-volatility effect. It is followed by +133 bps over 5 days in the lowest volatility-ratio tercile (t 3.37, 756 cases), +49 bps in the middle (t 1.29) and −9 bps in the highest (t −0.24). It is not cleanly graded by the 20-day return's size: by quartile of its z-score it gives 32, 81, 82 and 37 bps.
- **F6:** The agreeing effect rests on the earlier years. It gives +165 to +295 bps per case in 2018 to 2021 (t up to 3.58 in 2019) and is negative in 2022 (−107), 2023 (−70) and 2025 (−84). It is also strongest on XRP (+225 bps, t 2.27) and ZEC (+120 bps). A test of it must survive the one-window-left-out check.

## Ideas
- `022-04_signal-weights-carry-forward.d2_daily-move-continues-five-days.d1_daily-move-with-20-day-trend` (from F1, F2, F3, F6): The larger a coin's move over the last day, the larger its move in the same direction over the next 5 days, only while that day's move goes the same way as the coin's 20-day return.
- `022-04_signal-weights-carry-forward.d2_daily-move-continues-five-days.d2_trend-extending-day-in-calm-volatility` (from F3, F4, F6): The larger a coin's move over the last day, the larger its move in the same direction over the next 5 days, only while that day's move goes the same way as the coin's 20-day return and the coin's 20-day volatility is low against its 120-day volatility.
- `022-04_signal-weights-carry-forward.d2_daily-move-continues-five-days.d3_calm-markets-carry-trend` (from F4, F5, F6): The lower a coin's 20-day volatility against its 120-day volatility, the larger its move over the next 5 days in the direction of its 20-day return.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

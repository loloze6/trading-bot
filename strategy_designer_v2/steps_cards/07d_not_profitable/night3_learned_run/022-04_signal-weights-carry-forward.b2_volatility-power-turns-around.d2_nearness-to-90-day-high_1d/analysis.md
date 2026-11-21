---
line: 7.d not profitable
backtest: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around.d2_nearness-to-90-day-high_1d
idea tested: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around.d2_nearness-to-90-day-high
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.2469 USD
---
## Findings
- **F1:** The short side loses money: the book is short on 45 % of coin-bars, and those bars earn -0.000127 per bar, so shorts take -0.0000573 per bar off the book while longs add +0.000178; days with the book net short average -0.000118 against +0.000700 on net-long days.
- **F2:** The idea's effect sits only near the high. Over 3419 grid cases split by forecast quintile, the 5-day move above drift is +1.24 % in the top quintile (forecast +4.2), against -0.14 % in the bottom quintile (forecast -4.8), -0.60 % in the second and -0.42 % in the middle, so a close far below its 90-day high is not followed by a lower return.
- **F3:** Because the forecast is centred on its usual distance, the book is long about as often as short (44 % against 45 % of bars, mean positions +0.16 and -0.14), and it gets almost nothing from the coins' rise (gain from the market about 0.00001 per coin per bar). Its mean daily return of 0.000109 is about a tenth of holding's 0.00118, which is why it fails both the mean-return and the Sharpe-against-holding measures.
- **F4:** The deepest fall of the book was 16.9 % over 466 days across w2 to w6, while the coins chained +33.5 % over the same days at a mean position of only +0.007. In w4 the coins rose 33 % and the book lost 1.7 %, so the Calmar of 0.22 comes from betting against rising coins, not from crashes.
- **F5:** The slope is weaker in the coins' high-volatility tercile (t 0.53) than in the low and middle terciles (t 1.43 and 1.51), and weaker after a 30-day rise (t 0.45, 1324 cases) than after a 30-day fall (t 1.41, 2095 cases).
- **F6:** Cost is not the cause: the unusual move per case is +1.52 % over 5 days, 7.9 times the 0.19 % cost of a round trip, at 0.078 trades per day.

## Ideas
- `022-04_signal-weights-carry-forward.b2_volatility-power-turns-around.d2_nearness-to-90-day-high.d1_nearness-to-high-near-side` (from F1, F2, F3, F4, F6): The closer a coin's daily close sits to its highest close of the past 90 days, the higher its return over the next 5 days, only while the close is nearer its 90-day high than is usual for that coin, the rise growing as the close reaches a new 90-day high.
- `022-04_signal-weights-carry-forward.b2_volatility-power-turns-around.d2_nearness-to-90-day-high.d2_nearness-to-high-calm-coins` (from F2, F5, F6): The closer a coin's daily close sits to its highest close of the past 90 days, the higher its return over the next 5 days, and the more so the lower the coin's volatility over the past 30 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

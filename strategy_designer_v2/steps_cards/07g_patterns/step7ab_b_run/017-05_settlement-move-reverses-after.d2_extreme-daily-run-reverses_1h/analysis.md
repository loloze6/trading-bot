---
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.d2_extreme-daily-run-reverses_1h
idea tested: 017-05_settlement-move-reverses-after.d2_extreme-daily-run-reverses
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4040 USD
---
## Findings
- **F1:** The reversal of a coin's 24-hour run appears only when its past-week hourly volatility is high: after a run of more than one usual 24-hour move, the forecast-signed drift-adjusted return over the next 24 hours is +189 bps (t 6.32, 859 non-overlapping cases) in each coin's top volatility quintile, against -10 to +20 bps (|t| ≤ 1.12, about 856 cases each) in the four lower quintiles.
- **F2:** Inside the top volatility tercile the reversal is graded by the size of the run: by quartile of the absolute volatility-scaled 24-hour return, the signed 24-hour return is +6, +7, +63 (t 3.60) and +134 bps (t 6.52), about 1,389 cases each. The upper half is 3 to 7 times the round-trip cost of about 19 bps, while the idea as tested captured only 6 bps per case, 0.3 times that cost.
- **F3:** The high-volatility reversal holds on every coin: on the top tercile with absolute run above 1, it is +78 bps on BTC (t 2.50) and +115 to +184 bps on ETH, LTC, XMR, XRP and ZEC (t 2.19 to 3.08), 216 to 255 cases per coin. It is positive in all 8 years (+33 to +208 bps), with t above 2 in 4 of them (2018, 2019, 2021, 2023).
- **F4:** The reversal is stronger after falls than after rises. In the top volatility tercile, falls are followed by a rebound of +200 bps (t 6.45, 685 cases) and rises by a give-back of +67 bps (t 2.40, 677 cases). The book's trades show the same split: longs earned +0.32 % net (24,717 trades) and shorts lost -0.96 % net (23,093 trades).
- **F5:** The high-volatility rebound after falls lasts beyond a day: over the next 72 hours, top-tercile coins earn +253 bps above drift after falls beyond -1.5 usual moves (t 2.59, 100 cases) and +141 bps after falls of -0.5 to -1.5 (t 2.91, 379 cases).
- **F6:** In calm conditions the 24-hour run does not reverse, and after moderate falls it continues: in the bottom volatility tercile the excess return after a -0.5 to -1.5 run is -24 bps (t -2.31, 1,113 cases). Over all bars, the largest-rise decile gives back only -21 bps (t -1.71), against +70 bps after the largest-fall decile (t 4.73).
- **F7:** Hours 21 and 22 UTC rise more than other hours, by +4.9 and +3.8 bps per hour above each coin's mean (t 6.13 and 4.98). The effect is on every coin (t 2.61 to 4.04) and positive in 7 of 8 years. Hours 01 to 03 UTC fall by -2.1 to -3.6 bps (t -2.5 to -4.9). Both moves, about 9 bps over two hours, are below a round trip, as earlier runs' F2 predicts, so no idea is written from them.

## Ideas
- `017-05_settlement-move-reverses-after.d2_extreme-daily-run-reverses.g1_volatile-falls-rebound-next-day` (from F1, F2, F3, F4, F6): The higher a coin's hourly volatility over the past week, the more its 24-hour fall, measured in usual 24-hour moves, is followed by a rise over the next 24 hours: the larger the fall, the larger the rebound.
- `017-05_settlement-move-reverses-after.d2_extreme-daily-run-reverses.g2_turbulent-runs-fade-three-days` (from F1, F2, F4, F5): When a coin's hourly volatility over the past week is high, the larger its 24-hour run, measured in usual 24-hour moves, the more of that run it gives back over the next 3 days, more after falls than after rises.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

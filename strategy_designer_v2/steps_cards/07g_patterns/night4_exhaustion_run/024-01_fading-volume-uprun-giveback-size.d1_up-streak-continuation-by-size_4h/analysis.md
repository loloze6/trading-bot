---
line: 7.g patterns
backtest: 024-01_fading-volume-uprun-giveback-size.d1_up-streak-continuation-by-size_4h
idea tested: 024-01_fading-volume-uprun-giveback-size.d1_up-streak-continuation-by-size
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4159 USD
---
## Findings
- **F1:** A coin's 7-day return, measured in its usual moves, predicts its excess return over the next 3 days in the same direction. The pooled slope has t 3.85 on 5148 non-overlapping cases. The top quintile minus the bottom quintile is +0.122 standard deviations (Welch t 2.52), the top quintile alone is +0.098 (t 2.77), and the slope is positive in 5 of 6 coins (XRP t 3.33) and in 7 of 8 years (2022 t -1.45).
- **F2:** Down-streaks of at least two 4h bars where the last 8 hours' volume has faded against the last 24 hours fall further over the next 3 days, the reverse of the brief's give-back. Fading minus rising volume is -0.186 standard deviations (Welch t -3.09, n 1117). The slope on the size of the fade has t -2.85, and the fading half is lower in all 6 coins and in 6 of 8 years.
- **F3:** In up-streaks, fading volume makes no difference to the next 3 days: rising minus fading is +0.039 standard deviations (t 0.70, n 1323). The brief's give-back after up-runs on fading volume does not appear, and neither does the tested continuation: the main t is 1.21 and the unusual move is -0.09 % per case, -0.4 times the 0.19 % cost of a trade.
- **F4:** The larger a single 4h fall in usual moves, the larger the next day's excess return. The slope over falls has t -3.64. After falls of 3 or more usual moves, the next 4h bar's excess is +0.096 standard deviations (t 2.60, n 2406). Falls of 2 or more usual moves rebound in 4 of 6 coins, but 2020 shows -0.309 against +0.423 in 2018, so the effect varies by year.
- **F5:** The 4h bar from 20:00 to 24:00 UTC rises (+0.038 standard deviations, t 5.18, positive in all 6 coins) and the bar from 00:00 to 04:00 UTC falls (-0.036, t -4.65, negative in 5 of 6 coins). This holds in most years but is ungraded, so no idea is written on it.
- **F6:** The book moves with the coin rather than with any timing. Its worst decile of days averages -7.80 % against the coin's -7.69 %, and its best +8.69 % against +8.47 %. A Calmar of 0.37 matches a near-constant long holding, and the tested forecast's top-minus-bottom quintile of +0.092 (t 2.34) comes mostly from flat versus long bars.

## Ideas
- `024-01_fading-volume-uprun-giveback-size.d1_up-streak-continuation-by-size.g1_seven-day-run-continues-three-days` (from F1, F3): The larger a coin's 7-day return measured in its usual 4-hour moves over the past 30 days, the further it moves in the same direction over the next 3 days, beyond its normal drift.
- `024-01_fading-volume-uprun-giveback-size.d1_up-streak-continuation-by-size.g2_quiet-down-streak-keeps-falling` (from F2): When a coin falls in an unbroken streak of 4-hour periods while its volume over the last 8 hours shrinks against its last 24 hours, it keeps falling over the next 3 days, and the more the volume fades, the larger the further fall.
- `024-01_fading-volume-uprun-giveback-size.d1_up-streak-continuation-by-size.g3_sharp-drop-rebounds-next-day` (from F4): The larger a coin's single 4-hour fall measured in its usual 4-hour moves over the past 30 days, the larger its rebound over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

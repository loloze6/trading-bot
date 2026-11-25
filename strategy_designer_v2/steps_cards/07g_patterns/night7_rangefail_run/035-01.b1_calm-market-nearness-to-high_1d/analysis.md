---
line: 7.g patterns
backtest: 035-01.b1_calm-market-nearness-to-high_1d
idea tested: 035-01.b1_calm-market-nearness-to-high
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4027 USD
---
## Findings
- **F1:** The idea lives in calm bars. In calm bars, the 5-day excess return rises across the swing-scaled distance-from-high quintiles: −2.6 % (t −3.6, 197 cases), −2.9 % (t −3.9, 155), +0.1 %, +2.0 % (t 2.9, 197), +3.0 % (t 3.4, 197). In agitated bars the same quintiles go −0.6 %, 0.0 %, −0.9 %, +1.6 %, +1.2 %, with no t above 1.4 (with day clustering, 0.8 to 1.4).
- **F2:** The relation holds in every 60-day trend, and it is strongest in a choppy one. In choppy bars (calm and agitated pooled), the farthest-below-high tercile is followed by a 5-day excess of −9.9 % (t −4.5, 39 cases) and the nearest tercile by +4.0 % (t 2.0, 51). In falling bars the same terciles give −1.4 % against +2.4 % (t 2.4, 77). In rising bars they give −3.6 % against +2.5 % (t 2.5, 194).
- **F3:** Inside the calm nearest-to-high tercile, the size of the day's own move in units of the daily swing adds to the effect. The 5-day excess is +0.6 % (t_day 0.5) after the smallest one-day z-moves, +2.9 % (t_day 2.4) after middle ones and +5.8 % (t_day 2.4, 97 cases on 41 days) after the largest. In the farthest-below tercile there is no such grading (−2.3 %, −2.8 %, −2.8 %).
- **F4:** Over all calm bars, the one-day return quintiles alone give a graded 5-day excess of −1.4 %, −2.0 % (t −2.7), −0.3 %, +0.7 %, +2.9 % (t 2.9). In agitated bars the 1-day z-score quintiles give nothing (all |t_day| < 0.7).
- **F5:** The book earns mostly on its long side. Long bars earn a mean of 0.131 % per bar, summed 5.01, over 3837 bars; short bars earn 0.037 % per bar, summed 0.95, over 2568 bars. Long trades net a mean of +6.96 % (median +0.28 %, 1069 trades); short trades net +1.75 % (median −2.39 %, 469 trades).
- **F6:** The book's worst and best days are the coins' worst and best days, so its tails are market exposure. On the book's worst decile of days the book returns −0.90 % while the coins return −1.67 %; on its best decile the book returns +1.28 % while the coins return +1.58 %.
- **F7:** The weekday effect is chance. Raw next-day returns on Thursday and Friday look strong (t 3.6 and 4.3), but with day clustering they fall to t 0.95 and 1.44, and in 2021 the Thursday–Friday excess is 0.14 % (t 0.3). No weekday finding stands.

## Ideas
- `035-01.b1.g1_choppy-market-distance-from-high` (from F2, F1): In a choppy market, the further a coin's daily close sits below its 20-day high, measured in units of its 20-day daily swing, the more the coin falls over the next 5 days.
- `035-01.b1.g2_calm-breakout-day-size-continuation` (from F3, F4, F1): In a calm market, the larger a coin's one-day rise in units of its 20-day daily swing on a day its close sits near its 20-day high, the more the coin rises over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

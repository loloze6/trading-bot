---
line: 7.g patterns
backtest: 032-01.b1.b1.e2.d1.d3_aligned-continuation-inside-chop_1d
idea tested: 032-01.b1.b1.e2.d1.d3_aligned-continuation-inside-chop
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4420 USD
---
## Findings
- **F1:** On down days, the next day's excess return grows with the size of the fall counted in the coin's 30-day daily swings, and only when volatility is high: the slope on the scaled fall is -0.0136 (t -5.45, 1049 days) in the coin's top volatility tercile, -0.0046 (t -2.28) in the middle tercile and 0.0000 (t -0.01) in the bottom one; the tested 7-day idea does not explain this.
- **F2:** The down-day rebound holds on every coin, with slopes from -0.0032 (BTC, t -1.74) to -0.0087 (XRP, t -2.36), and in chop and trend alike (t -3.40 and -3.46), while up days show no graded next-day move (slope +0.0009, t 0.84, 3305 cases); falls of more than 2 daily swings are followed by a +1.90 % next-day excess (day-clustered t 2.13, 179 cases on 69 days).
- **F3:** The down-day rebound is uneven across years: t -0.58 in 2018, -2.95 in 2019, -5.33 in 2020 and -1.03 in 2021, so its strength depends on the period even though its sign never changes.
- **F4:** The 7-day continuation of the scaled weekly move depends on volatility more than on chop: on all grid cases the slope's t is 4.15, 1.57 and -0.55 from the low to the high volatility tercile, and 3.80, 3.42 and -0.97 from the low to the high tercile of 30-day against 90-day volatility (about 190 cases each); in the low-volatility tercile it continues in trends too (t 2.58, 86 cases) as well as in chop (t 2.71, 209 cases).
- **F5:** The book's short holdings lose and its long holdings carry the gain: trades under 7 days average -2.67 % net (1273 trades), while those of 7–14, 14–28 and over 28 days average +4.11 %, +8.61 % and +31.5 %; long trades average +4.86 % (1028) and short trades -1.59 % (1143), although on the grid both sides' signed excess is positive (long +4.1 %, t 3.70; short +3.4 %, t 3.23).
- **F6:** Weekday effects do not stand out once days are clustered: the largest next-day excesses (Friday +0.47 %, Saturday +0.39 %) have t 1.50 and 1.54, and the Friday–Saturday edge fades to -0.02 % in 2021.

## Ideas
- `032-01.b1.b1.e2.d1.d3.g1_volatile-down-day-next-day-rebound` (from F1, F2, F3): When a coin's daily swings over the past 30 days are large, a down day is followed by a rise over the next day, and the larger the day's fall measured in those 30-day daily swings, the larger the next day's rise.
- `032-01.b1.b1.e2.d1.d3.g2_calm-volatility-weekly-continuation` (from F4, F5): While a coin's daily swings over the past 30 days are no larger than over its past 90 days, its 7-day return counted in its 30-day daily swings is followed by a move the same way over the next 7 days, larger for a larger scaled move, in choppy and trending months alike.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

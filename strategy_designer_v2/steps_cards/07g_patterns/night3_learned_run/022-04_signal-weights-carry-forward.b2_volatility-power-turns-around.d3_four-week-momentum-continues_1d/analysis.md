---
line: 7.g patterns
backtest: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around.d3_four-week-momentum-continues_1d
idea tested: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around.d3_four-week-momentum-continues
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3851 USD
---
## Findings
- **F1:** The idea's gain sits in the top fifth of the forecast: the 5-day return above the coin's mean is +1.06 % (t 2.23, 684 cases) after the highest forecast quintile, while the other four quintiles are all at or below zero (-0.14 % to -0.38 %, t between -0.34 and -1.02).
- **F2:** Momentum works on the rising side only. On 5-day non-overlapping cases, the slope of the demeaned next-5-day return on the volatility-scaled 28-day return is 110 bps per unit with t 3.08 when the 28-day return is positive (1309 cases), and 32 bps with t 0.53 when it is negative (1246 cases); the short bets' signed demeaned return is +0.23 % with t 0.96 (1719 cases).
- **F3:** A large up day is followed by a further rise. After a 1-day return of 1 to 2 times the coin's 20-day volatility, the next 5 days run +1.55 % above the coin's mean (t 2.38, 286 cases), and above 2 times, +2.58 % (t 1.76, 94 cases). Large down days show no matching fall (+0.12 % and +0.02 %). The slope stays positive once the 28-day return is controlled for (z1 t 2.04, with r28z t 2.42, 2555 cases), and it is positive on all 6 coins (XRP t 2.24, ZEC t 1.70). Per case it is about 8 times the 0.19 % cost of a trade.
- **F4:** The momentum slope fades as the coin's 20-day volatility rises: t 2.68 in the calmest tercile, 1.97 in the middle one and 0.80 in the most volatile (about 860 cases each). The book's Sharpe is 0.91 and 0.98 in the two calmer market-volatility terciles and 0.38 in the most volatile.
- **F5:** The signal outlasts its 5-day horizon but not 20 days: the scaled 28-day return slope has t 2.87 at 5 days (2555 cases), 2.44 at 10 days (1259) and 0.62 at 20 days (539).
- **F6:** The book's failed Calmar comes from 2022 and 2023, when it earned -1.8 and -4.5 bps a day (Sharpe -0.19 and -0.54), while holding the coins had a Sharpe of 1.18 in 2023. In 2020 it earned 26 bps a day (Sharpe 1.99).
- **F7:** Friday and Saturday returns are higher than other days by 10 to 76 bps per coin (LTC t 3.88, XMR t 2.03). The effect is concentrated in 2018 and 2019 (t 3.37 and 5.82) and absent in 2021 and 2022. On the coin-average only Saturday stands out (t 2.24 of 7 weekdays tested), so I do not count this as separate from chance given the number of angles looked at.

## Ideas
- `022-04_signal-weights-carry-forward.b2_volatility-power-turns-around.d3_four-week-momentum-continues.g1_upside-four-week-momentum-continues` (from F1, F2, F5): The larger a coin's 28-day rise, the larger its return over the next 5 days above its normal drift.
- `022-04_signal-weights-carry-forward.b2_volatility-power-turns-around.d3_four-week-momentum-continues.g2_large-up-days-keep-rising` (from F3): The larger a coin's up day relative to its own 20-day volatility, the larger its return over the next 5 days.
- `022-04_signal-weights-carry-forward.b2_volatility-power-turns-around.d3_four-week-momentum-continues.g3_calm-market-four-week-momentum` (from F4, F6): When a coin's 20-day volatility is lower than usual, the larger its 28-day return, the larger its return over the next 5 days in the same direction.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

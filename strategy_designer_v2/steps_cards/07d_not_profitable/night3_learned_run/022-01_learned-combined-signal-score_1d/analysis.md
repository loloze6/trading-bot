---
line: 7.d not profitable
backtest: 022-01_learned-combined-signal-score_1d
idea tested: 022-01_learned-combined-signal-score
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3453 USD
---
## Findings
- **F1:** The learned weights do not carry forward from one year to the next. Across 40 coin-year pairs, a signal's rank correlation with the coin's excess 5-day return in one year correlates with the previous year's at -0.115 for the 28-day return, -0.196 for the 1-day return, -0.021 for nearness to the 90-day high and 0.133 for 30-day volatility. The sign repeats in only 35 % to 55 % of pairs. This matches the brief's own condition for the theory being wrong.
- **F2:** Because the weights look back over the past 365 days, the score ends up pointing against what follows. The forecast's rank correlation with the excess 5-day return is -0.037 pooled, and it is negative on 5 of 6 coins (BTC -0.073, ZEC -0.053) and in 7 of 8 years.
- **F3:** Both sides lose. Long cases earn -0.56 % excess per 5 days (t -2.10, 1535 cases) and short cases -0.49 % (t -1.83, 1743 cases). The two most negative forecast quintiles are followed by +0.67 % and +0.63 % excess moves, and the fourth quintile by -1.19 %.
- **F4:** The book's loss is timing, not exposure. Its gain before costs is -0.063 % per bar; -0.054 % of that is timing and -0.009 % comes from the market's own rise. It is short on 51 % of bars.
- **F5:** The book falls behind holding in every year the coins rose: in 2020, -0.17 % a day against +0.42 %; in 2021, -0.04 % against +0.41 %. It beats holding only in the two falling years, 2018 (+0.08 % against -0.39 %) and 2022 (+0.01 % against -0.18 %).
- **F6:** Taken alone, with its usual direction, the 28-day return is the largest single effect. Its top fifth is followed by a +1.11 % excess 5-day move (strength 0.104, t 1.98, 490 cases) and a +1.79 % total move, about 9 times the 0.19 % round-trip cost.
- **F7:** That momentum effect is not stable across years either. Its top-minus-bottom-fifth spread is positive in 4 of 8 years (2019 to 2021 and 2025, +2.3 % to +4.8 %) and negative in the other 4 (2018 -5.9 %, 2022 -2.8 %, 2023 -2.7 %, 2024 -0.1 %).
- **F8:** Days with the largest absolute move are followed by higher returns. The top fifth of the absolute 1-day return is followed by +0.93 % excess (strength 0.078, t 1.93, 628 cases) and +1.60 % total over 5 days. The second and third fifths are followed by -0.86 % and -0.99 % (t -2.2 and -2.4).

## Ideas
- `022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score` (from F1, F2, F3, F4): When a coin's four signals are combined into one score, the coin's return over the next 5 days is higher the higher that score is. The four signals are its 28-day return, minus its last 1-day return, its closeness to its 90-day high, and minus its 30-day volatility. Each signal is weighted equally in the direction its effect is known for, instead of by how well it predicted that coin's own 5-day returns over the past 365 days.
- `022-01_learned-combined-signal-score.d2_four-week-momentum-alone` (from F5, F6, F7): The higher a coin's 28-day return, the higher its return over the next 5 days.
- `022-01_learned-combined-signal-score.d3_large-day-precedes-rise` (from F8, F3): The larger a coin's absolute return over its last day, the higher its return over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

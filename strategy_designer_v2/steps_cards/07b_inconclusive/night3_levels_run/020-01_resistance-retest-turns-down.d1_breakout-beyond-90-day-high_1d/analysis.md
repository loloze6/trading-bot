---
line: 7.b inconclusive
backtest: 020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high_1d
idea tested: 020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5179 USD
---
## Findings
- **F1:** The test's result is on the side the idea predicts but far short of the bar: on 175 non-overlapping 5-day breakout cases, the slope of the drift-removed return on the forecast is positive with a t of 0.37, and the mean drift-removed return is +0.81 % (t 0.81). The median is −0.64 % and only 47 % of cases are positive, so a few large rises carry the mean.
- **F2:** The effect is not graded across the forecast. By forecast quartile, the 5-day drift-removed means are −1.45 %, −1.24 %, +5.38 % (sd 18 %) and +0.67 %, with 44, 44, 43 and 44 cases. On the raw distance above the high, the slope t is 1.83 at 5 days and 5.84 at 10 days. That 10-day t falls to 0.45 when both sides are winsorised and to −0.63 when the 5 largest moves are dropped, so it rests on a handful of extreme breakouts (ZEC's raw value reaches 61.9).
- **F3:** The effect is mixed across coins. The 5-day mean is +10.2 % on XRP (13 cases), +2.2 % on ETH (41) and +1.1 % on BTC (43), against −3.8 % on LTC (27), −0.9 % on XMR (26) and −0.1 % on ZEC (25). Within each coin, the correlation of the forecast with the move runs from −0.25 to +0.28.
- **F4:** The effect is mixed across periods. Breakouts are followed by +3.8 % in 2019 (24 cases) and +4.7 % in 2020 (31 cases), but by −9.6 % to +0.1 % in each year from 2021 to 2025 (5 to 34 cases a year).
- **F5:** Other horizons give no clearer graded answer. Over 1 day, breakout closes are followed by +0.56 % (t 2.59, 903 cases) against −0.03 % otherwise (Welch t 2.69), but the slope on the forecast is −0.67. Over 10 days the slope t is 2.02 on 96 cases, but it is fragile (F2). Over 20 days the mean is −3.5 % on 41 cases.
- **F6:** The brief's "more often held, stronger" grading does not show. The number of prior closes within 3 % of the 90-day high has a slope t of −0.81 on 140 cases. The means are +0.4 % at 0 touches, +3.0 % at 1 to 3, and −0.5 % above 3.
- **F7:** Cost is not what limits this idea. The unusual move is +3.17 % per case (strength 0.266, 260 cases), 16.4 times the 0.19 % cost of a round trip. The book's Sharpe of 0.82 beats holding by 0.26, but its mean daily return of 0.016 % and Calmar of 0.64 fail the bar because breakouts are rare (0.025 trades per day).

## Ideas
- `020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high.b1_90-day-breakout-more-coins` (from F1, F3, F7): The further a coin's daily close stands above its highest close of the previous 90 days, the more it rises over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

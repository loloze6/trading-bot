---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides
line: 7.g patterns
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: On days a coin closes lower, the further that day's high-low range exceeds the coin's average range over the past 30 days, the higher the coin's return over the next 3 days above its usual drift.
Consequence: A trader would lean long after a falling day that was unusually wide for the coin, more strongly the wider the day, holding for 3 days, and would not lean long after wide days that closed up.
Why:
- F1: The tested effect comes almost entirely from falling days. On the 3-day grid, a coin's 3-day excess return regressed on its range-versus-30-day-norm ratio has a slope of 0.0109 (t 4.62, 2524 cases) on days the coin closed down. On days it closed up the slope is 0.0043 (t 1.89, 2762 cases).
- F2: On down days the effect is graded and sits mostly in the widest days. By quintile of the range ratio, the excess 3-day return runs -0.57 %, -0.27 %, -0.09 %, -0.15 % and then +1.35 % in the widest quintile (t 3.29, 505 cases). That top quintile has a strength of 0.16 of the coin's usual 3-day move, about 3.6 times the tested idea's 0.045. On up days the five quintiles show no order (+0.26 %, -0.36 %, -0.15 %, -0.22 %, +0.20 %; top t 0.47).
- F3: The falling-day slope holds up across the sample. It is positive in all 6 coins (t from 0.91 for BTC to 3.26 for XMR, 2.70 for ZEC and 2.14 for XRP) and in all 8 years (t ≥ 2.1 in 2020, 2022, 2024 and 2025).
- F4: The split is also visible in coarser cuts. Wide-range days that closed down are followed by +0.80 % excess over 3 days (t 2.54, 854 cases), wide days that closed up by +0.05 % (t 0.17, 910 cases). The size of the fall itself predicts nothing: down-day quintiles of the return over its 30-day volatility show no order, with t between -1.23 and 1.54. It is the width of the day, not the size of the drop, that carries the move.
- F5: The book is diluted because it trades the whole signal on every day. Measured over the plan's 3466 cases, the idea's total move is +0.41 % against a 0.19 % trade cost. The book earns 0.0155 % a day on days in a position, against a 0.05 % requirement, while in a position on 99 % of coin-days. The wide-down-day cases move +1.35 % (F2), about 7 times the cost.

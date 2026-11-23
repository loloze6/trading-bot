---
line: 7.d confirmed, not profitable
backtest: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day_1h
idea tested: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4300 USD
---
## Findings
- **F1:** The book is long most of the time and mostly carries the coin's own moves rather than the settlement effect: it holds a position on 72 % of bars (mean allocation 0.38) with a median trade of 24 h and a mean of 40 h, because bets on two settlements a day overlap. On the coin's worst-day quintile it loses −1.91 % against the coin's −5.36 %, and on the best it gains +1.72 % against +5.34 %. Its Sharpe is 0.417 against holding's 0.554, and its deepest fall is −61 %, so Calmar is 0.14.
- **F2:** The effect is only in the strong falls; the weak falls lose. Over 24 h after the signal, the excess return is −0.13 % (t −1.46) and −0.13 % (t −1.42) in the two lowest forecast quintiles, against +0.17 % (t 1.70) and +0.29 % (t 2.60) in the two highest. The top quintile's total move is +0.44 %, 2.3 times the 0.19 % cost of a trade; the bottom two quintiles' total moves are +0.01 % and +0.02 %, below that cost.
- **F3:** The effect lives where the coin's last-7-day hourly volatility is high against its last-30-day volatility. On signals in the top half of the forecast, the excess return is +0.59 % (t 4.40, n 2338, total +0.74 %, 3.9 times the cost) in the hot third, against −0.05 % (calm) and +0.03 % (mid). As a check that this condition is not an effect of its own: on non-signal settlement bars the hot third earns −0.07 % (t −0.84), and on all 24-bar grid bars it earns +0.17 % (t 2.13), far below the +0.59 % where both hold.
- **F4:** Inside the hot third the effect is graded by the size of the fall: the bottom forecast half earns −0.12 % (t −0.98) and the top half +0.59 %. Across years the hot strong cases are positive in 2019 (+0.61 %, t 2.99), 2020 (+1.09 %, t 4.12) and 2024 (+0.92 %, t 4.44), but negative in 2022 (−0.72 %, t −3.05).
- **F5:** The 7-day trend sorts the signals as the brief's theory expects: falling into settlement after a run up, when longs should be the crowded, paying side. Signals with the 7-day return in its top third earn +0.20 % excess (t 2.51, total +0.35 %), against −0.01 % (down third) and −0.08 % (middle third). Non-signal settlement bars in the up third earn only +0.11 % (t 1.46), so the up trend alone carries about half of it.
- **F6:** The move is a 24-hour move and does not last. The excess return of all signals is +0.06 % at 24 h (t 1.27), −0.01 % at 48 h and −0.03 % at 72 h. For the top quintile it is +0.29 % at 24 h (t 2.60) and −0.02 % at 48 h, so holding the overlapping bets past a day (40 h on average) adds exposure and no gain.
- **F7:** The 15:00-stamped settlement (16:00 UTC) carries more than the 23:00 one: +0.065 % excess (t 1.17, n 8402) against +0.038 % (t 0.53, n 4246).

## Ideas
- `017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d1_settlement-fall-recovers-when-volatile` (from F1, F2, F3, F4, F6): The rise over the 24 hours after a 00:00 or 16:00 UTC funding settlement, following a fall over the 2 hours before it, grows with the size of that fall against the coin's usual 2-hour move. It grows more the higher the coin's hourly volatility over the last 7 days stands against its volatility over the last 30 days.
- `017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d2_settlement-fall-recovers-after-runup` (from F1, F2, F5, F6): The rise over the 24 hours after a 00:00 or 16:00 UTC funding settlement, following a fall over the 2 hours before it, grows with the size of that fall against the coin's usual 2-hour move. It grows more the larger the coin's 7-day return before the settlement, when longs are the crowded side paying funding.
- `017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d3_settlement-recovery-lasts-one-day` (from F1, F2, F6, F7): The rise over the 24 hours after a 00:00 or 16:00 UTC funding settlement grows with the size of the fall over the 2 hours before it against the coin's usual 2-hour move, and it is gone by the second day after settlement.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

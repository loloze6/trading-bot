---
line: 7.g patterns
backtest: 032-01.b1.b1.e2.d1_raw-scaled-weekly-continuation_1d
idea tested: 032-01.b1.b1.e2.d1_raw-scaled-weekly-continuation
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4025 USD
---
## Findings
- **F1:** The weekly continuation is confined to choppy bars, which is the tested idea itself. On the 7-day grid, the move in the signal's direction minus the drift is +1.71 % (t 1.59, 116 days, day-clustered) at a 30-day efficiency ratio of 0 to 0.15, and +2.58 % (t 2.30, 128 days) at 0.15 to 0.3. It is −0.51 % (t −0.32, 87 days) at 0.3 to 0.5 and −2.70 % (t −0.89, 24 days) above 0.5, so no reversal outside chop can be told from chance.
- **F2:** Inside chop the continuation grows with the scaled weekly move. Per case it is +1.66 % at |s| ≤ 0.5, +3.41 % at 1 to 1.5, +6.20 % at 1.5 to 2 (t 2.63, 40 cases) and +5.31 % above 2 (t 1.71, 22 cases), with t not day-clustered. It is the same after rises and falls: +2.10 % (t 2.48, 305 cases) and +2.28 % (t 2.88, 307 cases).
- **F3:** The book's gain comes from its longs. It earns +0.186 % a day on long coin-days (3703) and −0.029 % on short coin-days (3926). Short trades lose −2.54 % on average (median −3.38 %, 1743 trades), while long trades gain +3.23 % (1343 trades). The unusual move is symmetric (F2), so the shorts' losses come from the coins' own rise over folds B and C, not from the signal.
- **F4:** After a daily fall of 2 or more 30-day daily swings, the next day's return is +2.03 % (t 3.86, 154 cases). Day-clustered and net of each coin's mean, this shrinks to +1.22 % (t 1.58, 58 days). It is clearer only on XMR (+1.39 %, t 3.18) and ZEC (+1.21 %, t 2.48) out of six coins, and is absent on the 3-day grid (+0.39 %, t 0.32, 19 days).
- **F5:** Next-day returns by weekday are +0.58 % on Thursday (t 3.51) and −0.48 % on Wednesday (t −2.37) per case. Day-clustered they fall to t 1.50 and t −1.23, inside the range chance gives across seven weekdays.
- **F6:** Volatility level does not separate the continuation in chop once days are clustered. By 30-day volatility rank over 180 days, it is +3.30 % (t 1.02, 21 days) in the low third, +3.57 % (t 1.34, 23 days) in the middle and +0.51 % (t 0.19, 25 days) in the high third.

## Ideas
- No ideas: Beyond the tested idea's own choppy-regime continuation (F1, F2), I looked at efficiency-ratio levels, volatility ranks, coins, years, weekdays, daily shocks, trade sides and the book's extreme days, and every other pattern (F4, F5, F6) falls under t 2 once days are clustered or holds on only two of six coins, so none stands out from chance across that many angles.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

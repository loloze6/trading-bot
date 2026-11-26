---
line: 7.g patterns
backtest: 032-01.b1.b1.e2.d2.d1_chop-continuation-while-chop-lasts_1d
idea tested: 032-01.b1.b1.e2.d2.d1_chop-continuation-while-chop-lasts
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4368 USD
---
## Findings
- **F1:** When the coin's 30-day swings are calm against its own history, the tested continuation is much stronger than when they are agitated: on the 7-day grid with the week agreeing with the month, the slope of the next-7-day excess return on the scaled week is +0.047 (t 3.93, n 98) when 30-day daily volatility is below 0.75 of the coin's median, +0.013 (t 1.66, n 190) at 0.75–1.0, +0.010 (t 0.95, n 138) at 1.0–1.3, and −0.008 (t −0.54, n 110) above 1.3, which is the reverse of the brief's "agitated" premise.
- **F2:** Measured against the coin's own trailing 180-day volatility, the agreeing, choppy cases (efficiency below 0.3) show a signed next-7-day excess return of +10.8 % (day-clustered t 3.51, n 27) in the low third and +10.9 % (t 3.67, n 26) in the middle third, against +4.6 % (t 1.23, n 27) in the high third; these samples are small.
- **F3:** The follow-through sits in moderately choppy months: with the week agreeing with the month, the slope on the scaled week is +0.043 (t 4.24, n 173) at efficiency 0.15–0.3 and +0.030 (t 2.57, n 171) below 0.15, but +0.007 (t 0.62, n 130) at 0.3–0.45 and −0.008 (t −0.82, n 62) above 0.45.
- **F4:** The 30-day move scaled by 30-day swings predicts the next 7 days' excess return whatever the week does, in moderately choppy months: slope +0.037 (t 4.08, n 289) at efficiency 0.15–0.3, against +0.017 (t 0.73, n 323) below 0.15 and +0.003 (t 0.42, n 179) at 0.3–0.45; the weeks that disagree with the month in that band have a negative slope on the week (−0.029, t −1.65, n 116), so they follow the month and not the week.
- **F5:** After a large one-day fall the coin rises the next day, and the rise grows with the fall: the next-day excess return is +3.8 % after falls beyond 3 daily swings (n 48, 21 days, t 1.41), +1.2 % at 2–3 swings (n 131, t 1.73), +0.5 % at 1–2 swings (n 580, t 1.23) and +0.2 % at 0–1 swing; across all down days the slope of the next-day return on the scaled fall is −0.0062 (t −5.15, n 3146, not clustered).
- **F6:** The bounce after falls beyond 2 daily swings is positive in all 6 coins (from +1.3 % in XRP to +2.3 % in ZEC; t 0.87 to 2.12) and in all 4 years (from +0.7 % in 2018 to +5.0 % in 2020), whereas rises beyond 2 swings are followed by −0.6 % and −0.3 % (t −1.06 and −0.38).
- **F7:** The book's gain is very concentrated: its best 5 % of days sum to 233 % of its total summed daily gain, and on its worst 2 % of days it loses 5.0 % while the coins fall only 1.8 %, after a previous day of −1.8 % for the coins, which is what holds the Calmar at 0.59.

## Ideas
- `032-01.b1.b1.e2.d2.d1.g1_calm-chop-weekly-continuation` (from F1, F2, F3): When a coin's past 30 days are choppy and its daily swings over those 30 days are small compared with its own swings over the past six months, its 7-day move, scaled by its 30-day daily swings and pointing the same way as its 30-day move, is followed by a move the same way over the next 7 days. The calmer the month is against the coin's six-month swings, the larger the follow-through for a given scaled week.
- `032-01.b1.b1.e2.d2.d1.g2_moderate-chop-monthly-momentum` (from F4, F3): In a month whose net 30-day progress is moderate compared with the sum of its daily moves, a coin's 30-day return, scaled by its 30-day daily swings, is followed by a move the same way over the next 7 days, larger for a larger scaled 30-day move.
- `032-01.b1.b1.e2.d2.d1.g3_large-down-day-next-day-bounce` (from F5, F6, F7): The larger a coin's one-day fall, measured in its 30-day daily swings, the larger its rise over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

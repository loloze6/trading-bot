---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-03_weekend-reversal-exceeds-weekday.d1_sunday-move-reverses-early-week
line: 7.g patterns
backtest: 026-03_weekend-reversal-exceeds-weekday.d1_sunday-move-reverses-early-week_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's 24-hour return over Saturday is followed by a move in the same direction over Monday, the 24 hours from Monday 00:00 UTC: the larger Saturday's rise or fall, the larger Monday's move the same way.
Consequence: A trader would take Saturday's direction at Monday's open rather than fade the whole weekend, and would refuse an early-week fade that runs against Saturday's move.
Why:
- F1: Saturday's 24-hour move, read at the bar that closes Sunday 00:00 UTC, carries on over Monday. Regressed on Saturday's volatility-scaled move, Monday's move has t +7.30 pooled over 1936 coin-weeks, and t +4.25 with one case per week averaged across coins (375 weeks, slope 0.34). No other weekday's move predicts the day after its next day: those t lie between -0.70 and +1.55 on week averages.
- F2: The Saturday continuation into Monday is graded. Monday's mean return rises across Saturday's quintiles: -0.46 %, -0.09 %, +0.12 %, +0.23 %, +0.41 %, from the most negative quintile (z -0.83) to the most positive (z +1.20), with about 387 cases each. It is positive in 6 of 8 years, with t from +1.5 to +8.6. In 2021 and 2025 it reverses, with t -2.2 and -2.0.

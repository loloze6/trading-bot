---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-03_weekend-reversal-exceeds-weekday.d1_sunday-move-reverses-early-week
line: 7.g patterns
backtest: 026-03_weekend-reversal-exceeds-weekday.d1_sunday-move-reverses-early-week_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's 24-hour return over Saturday is followed by an opposite move over the next 24 hours, Sunday: the larger Saturday's rise, the larger Sunday's fall.
Consequence: A trader would fade Saturday's move through Sunday only, and close before Monday, when Saturday's direction returns.
Why:
- F3: On Sunday itself, Saturday's move is partly reversed. Sunday's move against Saturday's has t -4.17 pooled (1936 cases) and t -2.69 on week averages (375 weeks). Most of it sits in the top quintile: after Saturday's largest rises (z +1.20), Sunday averages -0.53 %, against +0.18 % to +0.34 % in the other quintiles.
- F1: Saturday's 24-hour move, read at the bar that closes Sunday 00:00 UTC, carries on over Monday. Regressed on Saturday's volatility-scaled move, Monday's move has t +7.30 pooled over 1936 coin-weeks, and t +4.25 with one case per week averaged across coins (375 weeks, slope 0.34). No other weekday's move predicts the day after its next day: those t lie between -0.70 and +1.55 on week averages.

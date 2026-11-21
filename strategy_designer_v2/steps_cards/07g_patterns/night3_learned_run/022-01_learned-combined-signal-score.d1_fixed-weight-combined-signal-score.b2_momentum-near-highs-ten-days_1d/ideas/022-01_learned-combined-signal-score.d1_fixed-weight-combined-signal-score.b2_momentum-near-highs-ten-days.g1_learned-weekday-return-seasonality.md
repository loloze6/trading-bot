---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.b2_momentum-near-highs-ten-days
line: 7.g patterns
backtest: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.b2_momentum-near-highs-ten-days_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The higher a coin's average next-day return on the same weekday over its past 52 weeks, the higher its return over the next day.
Consequence: A trader would lean into a coin on the weekdays that have recently been its strong ones, more so the stronger they have been, and away from it on its weak ones.
Why:
- F1: Next-day returns are higher on Thursdays and Fridays than on Mondays and Wednesdays, net of each coin's drift: Thursday +0.25 % (t 2.6), Friday +0.30 % (t 3.8), Monday −0.24 % (t −2.5), Wednesday −0.30 % (t −2.7), about 2,480 days each. The Thu+Fri minus Mon+Wed gap is positive on all 6 coins (+0.16 % to +0.36 % per day, t 1.7 to 3.1, about 1,657 days each) and in 6 of 8 years (2019 t 7.5, 2024 t 2.9), with 2022 slightly negative (t −0.5). It stands out among the roughly 15 angles looked at.

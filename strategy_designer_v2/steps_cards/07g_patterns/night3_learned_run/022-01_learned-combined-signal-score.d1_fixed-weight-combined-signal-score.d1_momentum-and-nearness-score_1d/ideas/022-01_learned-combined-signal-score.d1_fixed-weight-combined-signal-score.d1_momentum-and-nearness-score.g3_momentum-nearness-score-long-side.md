---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d1_momentum-and-nearness-score
line: 7.g patterns
backtest: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d1_momentum-and-nearness-score_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's 28-day return is positive and it sits near its 90-day closing high, its return over the next 5 days is higher the higher both are, measured against their usual levels.
Consequence: A trader would keep the combined score's long side, sized by its strength, and decline to take its short side.
Why:
- F1: The book's gain comes from its long side only. Bars held long earned a mean +0.085 % per bar (t 4.96, 8388 bars), and bars held short earned −0.008 % (t −0.67, 8796 bars). Long trades averaged +9.31 % net (1952 trades) and short trades −0.75 % (1598 trades). Short trades lost in 5 of 8 years.
- F2: The idea's slope is carried by its top fifth of forecasts. On 3419 non-overlapping 5-day cases, the top fifth ended +0.99 % above drift (t 2.04). The bottom fifth was only −0.16 % (t −0.41). The book shorts a side that does not fall.

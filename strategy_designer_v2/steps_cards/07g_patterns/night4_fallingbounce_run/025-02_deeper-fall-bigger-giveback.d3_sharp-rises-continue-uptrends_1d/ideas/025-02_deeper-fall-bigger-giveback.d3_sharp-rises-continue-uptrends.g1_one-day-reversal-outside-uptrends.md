---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-02_deeper-fall-bigger-giveback.d3_sharp-rises-continue-uptrends
line: 7.g patterns
backtest: 025-02_deeper-fall-bigger-giveback.d3_sharp-rises-continue-uptrends_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 90-day return is not positive, the larger a one-day move measured in usual daily moves, the larger the move in the opposite direction over the next day.
Consequence: In a coin that is not in an uptrend, a sharp up day is a reason to lean short and a sharp down day a reason to lean long for one day, rather than to follow the move.
Why:
- F1: Outside the rising regime (90-day return not positive), a one-day move in usual daily moves is partly reversed the next day: the regression of the next day's unusual return on the day's z gives slope -0.00319 with t -6.07 over 7,337 days, against slope -0.00072 with t -1.26 over 7,883 days in the rising regime.
- F2: That reversal is graded and occurs on both sides; outside the rising regime, days above +2 usual moves are followed by -0.67 % the next day (t -2.05, n 202, strength -0.138), days of +1 to +2 by -0.39 % (t -2.43, n 680), and days of -1 to -2 by +0.67 % (t 3.76, n 783, strength +0.137).
- F3: The F1 reversal holds in every coin, with slopes from -0.00175 to -0.00577 and t from -1.63 to -4.28, but it is concentrated in early years: t -3.45 in 2018, -8.53 in 2020 and -3.37 in 2021, against t between -0.38 and -1.31 from 2022 to 2025.

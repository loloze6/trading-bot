---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue
line: 7.g patterns
backtest: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's 24-hour return, measured against its usual 30-day 24-hour move, is followed over the next 24 hours by a move in the opposite direction. The reversal is larger the larger that move and the higher the coin's usual 24-hour move stands against its own longer past.
Consequence: A trader would fade large one-day moves on volatile coins and refuse to fade them in calm stretches.
Why:
- F1: A coin's 24-hour return, measured in its usual 30-day 24-hour move, is followed by an opposite move over the next 24 hours, and the effect grows with the coin's volatility level. On the 24-hour grid, the slope of the next 24-hour excess return on the past move, both in usual moves, runs from +0.026 (t 1.14) in the lowest volatility quintile through -0.089 (t -4.88) in the middle one to -0.150 (t -8.63) in the highest. Each quintile has about 2,990 independent cases.
- F2: In the higher-volatility 40 % of cases, the extreme quintiles reverse by more than a trade costs. After a mean past move of -1.70 usual moves the next 24 hours earn +1.10 % above drift (t 5.15, n 1196). After +1.84 usual moves they earn -0.63 % (t -3.40, n 1196). One trade costs 0.19 %.
- F4: The 24-hour reversal is persistent rather than one period's luck. The yearly slope is negative in 7 of 8 years, with t at or below -2 in 2018, 2019, 2020, 2021, 2023 and 2025, and near zero or positive only in 2022 (+0.001) and 2024 (+0.038, t 1.58). The coins agree in sign, from BTC at -0.009 (t -0.44) to XMR at -0.075 (t -3.63).
- F5: The reversal is not specific to the weekend, against the brief. The graded reversal after Saturday's 24 hours exceeds the other days' by only 0.080 (Welch t 1.48, n 2144 against 12847). The slope at the Sunday 00:00 anchor (-0.115, t -4.81) is close to the one at the Monday anchor (-0.104, t -3.45).

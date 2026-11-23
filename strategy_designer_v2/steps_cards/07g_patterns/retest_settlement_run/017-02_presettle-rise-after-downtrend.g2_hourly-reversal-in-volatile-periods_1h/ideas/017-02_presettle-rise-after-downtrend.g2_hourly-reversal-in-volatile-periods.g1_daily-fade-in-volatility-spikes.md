---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods
line: 7.g patterns
backtest: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Over the next 24 hours, a coin moves against its last 24-hour return, and the larger that return relative to its usual daily volatility, the larger the reversal, more strongly the higher its 24-hour volatility stands above its 30-day average.
Consequence: A trader would fade large one-day moves held for a day, mostly when volatility has just risen, trading about 24 times less often than the hourly fade, so each trade's move can cover its cost.
Why:
- F2: A full day's move also reverses over the next day, mostly when the coin's 24h volatility is high against its 30-day mean. On non-overlapping 24h cases, the slope of the next 24h excess return on the past 24h move (in volatility units) is -50.7 bp per unit with t -6.25 in the top tercile of that ratio (5221 cases). It is -8.1 bp (t -1.14) in the middle tercile and +9.1 bp (t +1.34) in the bottom tercile.
- F3: The 24h fade is graded and, for larger moves, bigger than the cost of a trade. The faded next-day move rises from -6.9 bp in the smallest-move quintile to +11.4 bp in the middle one, +39.5 bp (t 4.37) in the fourth and +19.0 bp (t 2.01) in the largest, against 0.19 % per trade. Over all 15662 cases it is +12.4 bp, a pure number of about 0.003 of the usual 497 bp daily move.
- F4: The 24h reversal is not uniform over time. Its slope is negative in every coin, with t from -1.1 (ZEC) to -3.2 (XMR). By year it is negative from 2018 to 2023 (t -3.4, -2.2, -0.9, -2.8, -1.8, -2.1) and absent in 2024 and 2025 (t +0.17, +0.28).
- F1: The tested hourly fade cannot pay. Its move is +0.01 % per case, a tenth of the 0.19 % a trade costs, and the book traded 20.42 times a day for a Sharpe of -11.93. The reversal itself is real only in the smaller coins: the 1h slope t is -5.0 for LTC, -6.2 for XMR, -5.9 for XRP and -7.8 for ZEC, against -1.1 for BTC and +0.1 for ETH.

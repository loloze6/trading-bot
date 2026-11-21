---
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
source-idea: 021-02_below-falling-cloud-continues-down.b1_slow-cloud-fall-continues
line: 7.d not profitable
backtest: 021-02_below-falling-cloud-continues-down.b1_slow-cloud-fall-continues_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes below its Ichimoku cloud and the cloud is falling, its return over the next 26 days is negative. It is more negative the more slowly the cloud has fallen over the past 26 days and the less the coin has already fallen over the past 52 days.
Consequence: A short below a gently falling cloud is worth taking after a moderate 52-day decline, and worth refusing after a deep one.
Why:
- F1: The book fails on its sign, not on its costs. Per case the unusual move is +2.49 % over 26 days, 12.9 times the 0.19 % cost of a trade. But the coins' normal drift against a short is -4.01 %, so the total move is -1.52 % per case. On the bars, the position's timing earns about +0.000195 a day, while being short 42 % of the time (mean position -0.156) costs -0.000185 a day of drift, leaving +0.00001.
- F2: The cases where the cloud collapsed fastest lose heavily as shorts. Across the four quartiles of the slow-fall value (mean 0.04, 0.08, 0.14, 0.39), the short's 26-day total return per case is -12.4 % (t -2.2, 39 cases), -5.6 % (t -1.2), +2.9 % (t 0.8) and +4.1 % (t 1.2). So the slow-fall dose has the stated direction, but only the slow half earns, and it earns weakly.
- F3: The short loses most where the coin has already fallen most over the past 52 days, and pays at moderate falls.
- F5: The result rests on one bear year. Short cases earned +16.0 % per 26 days in 2018 (t 3.9, 34 cases, hit rate 85 %), but lost -37 % in 2020 (t -3.4), -39 % in 2021 (t -3.1) and -16 % in 2023 (t -3.2). The book's mean daily return was +0.0015 in 2018 against -0.0004 to -0.0008 in 2020, 2023 and 2024. This is why it fails with one window left out (lowest Sharpe -0.43).

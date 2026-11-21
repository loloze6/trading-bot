---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends
line: 7.b inconclusive
backtest: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour return, read at an hourly close, falls by a large multiple of its 30-day average absolute daily return, the price rises over the next 4 days by more than the coin's usual 4-day drift, only while the coin's 30-day return is positive, and the larger that 30-day rise, the larger the rebound.
Consequence: A sharp hourly plunge in a coin that has risen over the past month is a reason to buy it for the next four days, and the stronger the month's rise, the stronger that reason.
Why:
- F1: The test came out inconclusive because its supporting check could not be computed, not because the effect was absent: 60.5 % of the 2345 cases entered at the forecast cap of 20, so the median entry forecast is 20.0 and no case lies strictly above it, while the main measure itself is +0.70 % per case with t 3.39.
- F2: Below the cap the effect is graded the way the idea predicts: by quintile of the raw fall-times-rise value, the top fifth (mean raw 36.4) earns an unusual 96-hour move of +1.85 % (t 3.01, 469 cases), against -0.19 % to +0.45 % for the middle three fifths; on all 701 non-overlapping 96-hour cells with a positive fall and a positive 30-day return, the cells above the product's median beat those below by 1.34 % (Welch t 1.96, 350 against 350), with Spearman rho 0.079 (p 0.035).
- F3: The effect is not spread evenly. It sits in 2020 (+2.04 %, t 4.42, 376 cases) and 2021 (+2.33 %, t 3.23, 320 cases), and is negative in 2018 (-1.14 %) and 2022 (-0.93 %). By coin it sits in ETH (+1.10 %, t 2.39), XRP (+1.44 %, t 2.01) and ZEC (+1.27 %, t 1.92), and is near zero in BTC (+0.06 %) and XMR (+0.09 %).
- F6: The idea is large enough to pay its costs. Its total move per case is 6.2 times the 0.19 % round trip and its unusual move 3.6 times; the book earns a Sharpe of 1.02, 0.47 above holding the coins.

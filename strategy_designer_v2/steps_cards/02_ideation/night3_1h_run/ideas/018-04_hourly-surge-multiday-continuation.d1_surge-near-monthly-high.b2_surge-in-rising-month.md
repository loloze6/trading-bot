---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high
line: 7.b inconclusive
backtest: 018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour return, read at an hourly close, first reaches several times its 30-day average absolute daily return on the upside, the price keeps rising over the next 10 days by more than the coin's usual 10-day return, only while the coin's 30-day return is positive: the larger the surge in usual daily moves, the larger the rise.
Consequence: A trader would hold an hourly-caught surge for about ten days when it comes inside a rising month, and refuse surges inside a falling month, which carried none of the move.
Why:
- F1: The tested result is on the side the idea predicts but short of the bar. The mean unusual move over 120 hours is +0.38 % per case (t 1.58, 2364 cases, strength 0.036), about 1.9 times the 0.19 % round-trip cost. At 240 hours the same cases show +0.79 % (t 2.15, 2270 cases, strength 0.050), so the plan's 5-day horizon cuts the move short; this matches the earlier finding that paying moves outlast their stated horizon.
- F2: The effect lives only in cases where the coin's 30-day return is positive, and is absent elsewhere. Those 843 cases show +0.97 % over 120 hours (t 2.30, strength 0.087) and +2.25 % over 240 hours (t 3.33, 803 cases, strength 0.141). The 1521 cases with a falling 30-day return show +0.05 % (t 0.17) and -0.00 % (t -0.01). The idea's own "near the 30-day high" weighting does not separate them: the 278 closest-to-high cases inside a falling month show +0.03 % (t 0.04).
- F3: The grading the idea states does not show inside the cases, so the effect is a regime effect rather than a graded one. The Spearman correlation of the 120-hour unusual move with the forecast is 0.013 (p 0.53) and with nearness to the high is -0.001 (p 0.97). Inside the rising-month cases these are -0.022 and -0.037. The forecast quintiles run +0.48 %, +0.12 %, -0.75 %, +1.18 %, +0.85 % at 120 hours, a passed upper-minus-lower check (+0.36 %) that is not monotone.
- F4: The effect depends heavily on the market's own year, even inside rising months. Over 120 hours it is +3.5 % in 2020 (t 3.45, 150 cases), +2.7 % in 2021 (t 2.28) and +2.3 % in 2024 (t 1.98). It is -7.4 % in 2018 (t -3.04, 32 cases), -1.8 % in 2022 (t -1.91) and -0.7 % in 2023. The book's shallow Calmar (0.57) sits with these shared falls.

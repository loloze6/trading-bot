---
line: 7.d not profitable
backtest: 021-02_below-falling-cloud-continues-down.b1_slow-cloud-fall-continues_1d
idea tested: 021-02_below-falling-cloud-continues-down.b1_slow-cloud-fall-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3663 USD
---
## Findings
- **F1:** The book fails on its sign, not on its costs. Per case the unusual move is +2.49 % over 26 days, 12.9 times the 0.19 % cost of a trade. But the coins' normal drift against a short is -4.01 %, so the total move is -1.52 % per case. On the bars, the position's timing earns about +0.000195 a day, while being short 42 % of the time (mean position -0.156) costs -0.000185 a day of drift, leaving +0.00001.
- **F2:** The cases where the cloud collapsed fastest lose heavily as shorts. Across the four quartiles of the slow-fall value (mean 0.04, 0.08, 0.14, 0.39), the short's 26-day total return per case is -12.4 % (t -2.2, 39 cases), -5.6 % (t -1.2), +2.9 % (t 0.8) and +4.1 % (t 1.2). So the slow-fall dose has the stated direction, but only the slow half earns, and it earns weakly.
- **F3:** The short loses most where the coin has already fallen most over the past 52 days, and pays at moderate falls.
- **F4:** The short loses when the coin has turned up over the past 26 days while still below the cloud. In the top quartile of the 26-day return (mean +3.2 %), the short's total is -15.4 % per case (t -2.2, 30 cases). The two middle quartiles (mean -16 % and -8 %) earn +8.7 % (t 2.6) and +4.4 %.
- **F5:** The result rests on one bear year. Short cases earned +16.0 % per 26 days in 2018 (t 3.9, 34 cases, hit rate 85 %), but lost -37 % in 2020 (t -3.4), -39 % in 2021 (t -3.1) and -16 % in 2023 (t -3.2). The book's mean daily return was +0.0015 in 2018 against -0.0004 to -0.0008 in 2020, 2023 and 2024. This is why it fails with one window left out (lowest Sharpe -0.43).
- **F6:** The book earns little on any coin. Mean daily book returns range from +0.00015 (BTC) to -0.00023 (XRP), against daily standard deviations of 1.2 to 1.4 %.

## Ideas
- `021-02_below-falling-cloud-continues-down.b1_slow-cloud-fall-continues.d1_slow-cloud-fall-shallow-decline` (from F1, F2, F3, F5): When a coin closes below its Ichimoku cloud and the cloud is falling, its return over the next 26 days is negative. It is more negative the more slowly the cloud has fallen over the past 26 days and the less the coin has already fallen over the past 52 days.
- `021-02_below-falling-cloud-continues-down.b1_slow-cloud-fall-continues.d2_collapsed-cloud-rebounds-up` (from F1, F2, F3): When a coin closes below its Ichimoku cloud and the cloud is falling, its return over the next 26 days is positive. It is larger the faster the cloud has fallen over the past 26 days.
- `021-02_below-falling-cloud-continues-down.b1_slow-cloud-fall-continues.d3_slow-fall-still-falling` (from F1, F2, F4, F5): When a coin closes below its Ichimoku cloud and the cloud is falling, its return over the next 26 days is negative. It is more negative the more slowly the cloud has fallen over the past 26 days and the more the coin has fallen over the past 26 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

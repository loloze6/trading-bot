---
brief: 023_range-reversion-when-no-trend
source-idea: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation
line: 7.g patterns
backtest: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's fall over the past day, relative to its usual daily move over the past 20 days, the larger its rise over the next day.
Consequence: A sharp down day measured against the coin's own recent volatility is a reason to be long for the following day rather than to follow the fall.
Why:
- F1: The day after a large fall the coin rises more than its drift. On a 1-day grid, a day whose return was 2 or more of its prior 20-day daily standard deviation below zero was followed by an excess next-day return of +0.67 % (t 2.52, 484 cases). A fall of 1 to 2 standard deviations was followed by +0.46 % (t 3.17, 1310 cases). A small rise of 0 to 1 standard deviation was followed by −0.22 % (t −3.56, 5317 cases).
- F2: This one-day reversal is negative and graded in every coin, with the slope of the next-day excess return on the day's standardised move ranging from −0.00040 (XRP, t −0.39) to −0.00372 (XMR, t −4.51; ETH t −2.26). It is strongest in 2018 (t −3.72), 2020 (t −4.18) and 2023 (t −2.94), but its sign flips in 2024 (t +0.71) and 2025 (t +0.48).

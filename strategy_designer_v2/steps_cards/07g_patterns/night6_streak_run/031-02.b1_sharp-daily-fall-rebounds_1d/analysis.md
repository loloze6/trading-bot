---
line: 7.g patterns
backtest: 031-02.b1_sharp-daily-fall-rebounds_1d
idea tested: 031-02.b1_sharp-daily-fall-rebounds
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3916 USD
---
## Findings
- **F1:** Up streaks keep going, and more so the longer they are: each extra consecutive up close adds +0.28 % to the coin's excess 2-day return (slope t 2.74 with each day's cases taken together, 3666 cases on 971 days); up streaks of 5 or more days are followed by +0.99 % (t 2.23, 182 cases) and a single up day by -0.32 % (t -2.28, 1966 cases), while down-streak length grades nothing (t 0.33, 3536 cases, 940 days).
- **F2:** The rebound after a fall grows with the coin's volatility: per unit of fall in usual moves, the slope is 0.36 % in the coin's lowest 60-day-volatility tercile (t 1.50, 487 days), 0.56 % in the middle (t 1.41, 556 days) and 1.34 % in the highest (t 1.97, 528 days); measured on the raw percentage fall, the slope is 0.20 per unit of return (t 2.40, 940 days), above the tested vol-scaled forecast's 2.28.
- **F3:** The rebound is in the 2-day horizon only: falls of 0.75 to 1.5 usual moves are followed by +0.80 % over 2 days (t 3.07, 847 cases), but over 5 days the fall slope is 0.21 % (t 0.35, 406 days) and that bucket is -0.38 % (t -0.82).
- **F4:** The book's gain is defensive rather than timed: it beat holding in the falling years (2018 -0.12 % against -0.35 % a day, 2022 -0.03 % against -0.19 %) and trailed it in every strong year (2020 +0.21 % against +0.42 %, 2021 +0.14 % against +0.41 %, 2024 +0.07 % against +0.24 %, 2025 +0.06 % against +0.20 %).
- **F5:** Weekday effects do not stand out once each day's cases are taken together: Friday's next-day excess of +0.30 % has t 2.09 (414 days), but only t 1.61 and 1.37 in the two halves of the period, and no other weekday reaches |t| 1.6. This is chance among the many angles looked at.

## Ideas
- `031-02.b1.g1_long-up-streaks-keep-rising` (from F1): The more consecutive days a coin has closed higher, the more it rises over the next 2 days beyond its normal drift.
- `031-02.b1.g2_volatile-falls-rebound-harder` (from F2, F3): The larger a coin's percentage fall on its latest day, the more it rises over the next 2 days, and this rebound is larger the higher the coin's volatility over the past 60 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

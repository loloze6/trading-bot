---
line: 7.g patterns
backtest: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation_1d
idea tested: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3958 USD
---
## Findings
- **F1:** The day after a large fall the coin rises more than its drift. On a 1-day grid, a day whose return was 2 or more of its prior 20-day daily standard deviation below zero was followed by an excess next-day return of +0.67 % (t 2.52, 484 cases). A fall of 1 to 2 standard deviations was followed by +0.46 % (t 3.17, 1310 cases). A small rise of 0 to 1 standard deviation was followed by −0.22 % (t −3.56, 5317 cases).
- **F2:** This one-day reversal is negative and graded in every coin, with the slope of the next-day excess return on the day's standardised move ranging from −0.00040 (XRP, t −0.39) to −0.00372 (XMR, t −4.51; ETH t −2.26). It is strongest in 2018 (t −3.72), 2020 (t −4.18) and 2023 (t −2.94), but its sign flips in 2024 (t +0.71) and 2025 (t +0.48).
- **F3:** Over 5 days, large up days continue instead of reversing. On the 5-day grid the top quintile of the day's move against its 20-day volatility was followed by a +1.63 % excess 5-day return (t 3.24, 570 cases). Days of +1 to +2 standard deviations were followed by +1.58 % (t 2.21, 255 cases), and days above +2 by +2.47 % (t 1.96, 110 cases). The 5-day slope is positive in 5 of 8 years (2019 t 2.79, 2023 t 2.22).
- **F4:** The tested momentum is lopsided and unstable. Its top forecast quintile earned +0.95 % excess over 5 days (t 2.00), but the bottom quintile earned only −0.10 % (t −0.26). The yearly slope was negative in 2018 (t −1.90), 2022 (t −1.45) and 2023 (t −1.42), and the slope fades in the highest-volatility tercile (t 0.32, against 2.27 and 2.62 in the lower two).
- **F5:** Long positions carry the book's gain. Long bars earned +0.174 % per bar (6633 bars) and short bars −0.015 % (6424 bars). Both the worst and the best deciles of bar gains come from large mostly-long positions after big 30-day rises (worst: mean |allocation| 0.86, 30-day return +13.3 %; best: 0.90, +16.1 %), which is where the Calmar-failing falls sit.
- **F6:** Saturdays stand out. Coins' daily returns averaged +0.45 % on Saturdays (t 5.53, 2484 coin-days), against −0.18 % to +0.33 % on the other weekdays. All six coins are higher on Saturdays than on other days (for example LTC +0.57 % against −0.02 %, XRP +0.57 % against +0.06 %), and the book's Saturday mean is its best weekday (+0.22 %).

## Ideas
- `023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.g1_one-day-fall-rebound` (from F1, F2): The larger a coin's fall over the past day, relative to its usual daily move over the past 20 days, the larger its rise over the next day.
- `023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.g2_strong-day-weekly-continuation` (from F3, F5): The larger a coin's rise over the past day, relative to its usual daily move over the past 20 days, the larger its further rise over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

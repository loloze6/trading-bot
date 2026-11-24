---
line: 7.g patterns
backtest: 031-02.b1.b1_strong-failed-rally-near-low_1d
idea tested: 031-02.b1.b1_strong-failed-rally-near-low
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3695 USD
---
## Findings
- **F1:** Nothing in the bars explains the tested idea. On the non-overlapping 20-day grid, bars in the near-low regime moved -1.22 % against their coin's drift (t -1.02, 319 cases), and bars outside it moved +0.98 % (t 0.60, 394 cases).
- **F2:** The gradient of nearness to the yearly low is not monotonic. By regime-score quintile, the 20-day excess moves are +0.27 %, -0.49 %, +3.54 %, -0.33 % and -3.00 %, with the nearest quintile at t -1.77 on 143 cases. Over 5 days the same quintiles give +0.95 % and -0.73 % at the two ends (t 1.73 and -1.75, 589 cases each).
- **F3:** Inside the regime, the recorded rally value does not grade the outcome in the idea's direction. The lowest tercile is followed by +2.96 % excess over 20 days (t 1.25), and the middle and top terciles by -3.61 % (t -1.85) and -2.98 % (t -1.66), about 106 cases each. That is a step after the lowest third, not a slope rising with the rally.
- **F4:** Past 20-day return, past 5-day volatility-scaled return and 20-day volatility level all show no separation in later excess returns, at either the 5-day or the 20-day horizon. Every quintile or tercile has |t| below 2: the largest is +0.94 % over 5 days after the fourth past-20-day quintile (t 1.94, 490 cases).
- **F5:** Daily excess returns by weekday give Saturday +0.37 % (t 4.14), Tuesday -0.28 % (t -2.88), Thursday -0.31 % (t -2.81) and Wednesday +0.25 % (t 2.11), about 2,140 coin-days each. These t's treat the six coins' same-day returns as independent. With their strong co-movement, the day-clustered t would be roughly half as large, which is not standing out across the roughly 15 tables examined. A weekday is also an on/off condition, not a graded situation.
- **F6:** The short-only book earned in the falling years and lost in the rising ones. Its mean daily return was +0.087 % in 2018 (t 2.78) and +0.066 % in 2022 (t 2.86), against -0.128 % in 2024 (t -2.90) and -0.098 % in 2025 (t -1.78). Its gain follows the coins' drift, not the idea's timing.

## Ideas
- No ideas: Across the forecast, the regime, the rally gradient, past returns, volatility, weekdays and years, nothing stood out from chance once the cross-coin clustering and the number of angles are accounted for. The only strong year pattern (F6) is the coins' own drift, and the strongest weekday pattern (F5) is neither robust to clustering nor graded.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

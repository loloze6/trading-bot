---
line: 7.g patterns
backtest: 031-03.g1_volume-surge-leads-two-week-drift_1d
idea tested: 031-03.g1_volume-surge-leads-two-week-drift
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3918 USD
---
## Findings
- **F1:** A coin's one-day return leans back the next day. The day-clustered t of its 1-day return against the next day's return is -3.05, over 17236 cases on 2874 days. The correlation is negative in every coin (from -0.026 for ZEC to -0.158 for XMR), in every year (from -0.004 in 2025 to -0.157 in 2020), and in both halves of the windows (t -1.85 for w1-12, t -2.51 for w13-24).
- **F2:** The lean is graded by the size of the day's move measured in the coin's usual daily moves, and is larger after falls than after rises. The next day's move beyond the coin's normal drift is:
- **F3:** The reversal sits in the high-volatility half of each coin's 20-day volatility. There, the day's return scaled by that volatility predicts the next day's with day-clustered t -3.09 (7253 cases, 1940 days); in the low-volatility half the t is +0.70 (7247 cases, 1865 days).
- **F4:** The reversal lasts about one day and is gone over longer horizons: the 1-day return against the next 3 days gives t -1.20 (5579 cases), and against the next 7 days t +1.93 (2299 cases).
- **F5:** The tested 14-day over 30-day volume ratio does not stand out as a finding.
- **F6:** The brief's medium-term reversal is absent. The 30-day return against the next 14 days gives t -0.38 (720 cases), the 60-day return t -0.33 (432 cases), and the quintiles of the 30-day return show no order (from -0.024 to +0.059 usual moves, all |t| < 0.7).
- **F7:** Most of the book's gain came from one year, and it does not move with the coins.

## Ideas
- `031-03.g1.g1_one-day-overreaction-reversal` (from F1, F2, F3, F4): The larger a coin's 1-day return measured against its usual daily move over the past 20 days, the more its price moves back the other way over the next day, and the more so the higher its 20-day volatility.
- `031-03.g1.g2_rebound-after-sharp-daily-falls` (from F2, F1, F4): The larger a coin's 1-day fall measured against its usual daily move over the past 20 days, the more its price rises over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

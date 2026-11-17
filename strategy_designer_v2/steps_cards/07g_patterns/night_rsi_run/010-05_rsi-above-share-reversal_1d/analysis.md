---
line: 7.g patterns
backtest: 010-05_rsi-above-share-reversal_1d
idea tested: 010-05_rsi-above-share-reversal
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.4142 USD
---
## Findings
- **F1:** In the most volatile third of each coin's days (20-day volatility), the next day's return ran against the day's own move scaled by its 20-day volatility, in both coins: BTC slope -0.0057 with t -3.96 and ETH slope -0.0084 with t -4.34, on 806 days each.
- **F2:** Inside that high-volatility third the reversal is graded across quintiles of the scaled move. The next day's coin-demeaned return falls from +0.0105 (t 3.45) after the largest falls (z -1.29), to +0.0064 (t 2.24), +0.0007, -0.0046 (t -1.88), and -0.0049 (t -2.21) after the largest rises (z +1.38), with about 322 days per quintile; on the raw daily return the slope is -0.149 with t -6.94 on 1612 days.
- **F3:** The high-volatility reversal holds in every year: the slope is negative in all eight years from 2018 to 2025, with t -2.69, -1.90, -3.37, -1.63, -1.61, -0.86, -2.63 and -3.02.
- **F4:** In the lowest-volatility third the sign turns slightly positive (BTC t 1.45, ETH t 1.58), and pooled over all days the slope is t -2.92 on 5794 days. Split by 20-day over 60-day volatility, the reversal sits only in the top third (slope -0.0047, t -3.29, n 972), against t 0.35 and t -0.88 in the other two thirds.
- **F5:** The reversal lasts one day only: in the high-volatility third, the day after next has slope +0.0014 with t 1.19 on 1602 days, and 7-day scaled-move slopes turn positive (t 2.41 on 815 cases).
- **F6:** The book lost mainly on its short side, which earned -0.00167 per day against -0.00039 on the long side. The coin rose 0.00245 more per day while the book was short than while it was long (Welch t 2.29, 2826 against 2800 days), because the 30-day RSI-above-50 share pointed weakly the other way at one day (t 2.20 on 5794 days, fading to t 1.49 at 7 days). The tested 14-day reversal slope was not significant (t 1.39 on 384 cases, quintiles not monotonic).

## Ideas
- `010-05_rsi-above-share-reversal.g1_high-volatility-one-day-reversal` (from F1, F2, F3, F4, F5): In a coin whose 20-day volatility is high relative to its own 60-day volatility, the larger the day's return measured in units of its 20-day volatility, the more the coin's return over the next 1 day runs the opposite way, with the reversal growing as that volatility ratio rises.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

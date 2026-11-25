---
line: 7.g patterns
backtest: 038-01_calm-swing-scaled-rise-continues_1d
idea tested: 038-01_calm-swing-scaled-rise-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4176 USD
---
## Findings
- **F1:** In the calm profile, the coin's next-5-day return minus its mean 5-day return rises with the 5-day move counted in 20-day daily swings, on both sides. The slope is +1.89 % per swing unit, with t 2.80 clustered by day (904 non-overlapping cases, 200 days). In the agitated profile the slope is -0.22 % with t -0.19 (718 cases, 186 days), so the effect lives in calm markets only.
- **F2:** The calm-profile response is graded and runs from falls to rises. Binned by the scaled 5-day move, the mean 5-day excess return goes -3.16 % (z ≤ -1.5, n 52), -3.25 % (t -2.80, n 93), -0.59 %, +0.06 %, +0.40 %, +1.75 %, +4.20 % (z > 1.5, t 1.84, n 80). The agitated bins show no order (-0.42 % to +1.43 %, every |t| < 0.7).
- **F3:** Taken one side at a time, neither half of the calm slope is sure on its own. Rises only: +2.24 % per unit, t 1.95 (471 cases). Falls only: +1.99 % per unit, t 1.33 (432 cases). Only the two-sided slope clears t 2 (F1), which fits the step-5 verdict on the rise-only idea (slope t 1.12, unusual move +0.17 %, t 0.47).
- **F4:** The calm continuation also holds on a 10-day horizon. The 10-day move in 10-day swing units predicts the next-10-day excess return with a slope of +2.91 % per unit, t 2.43 clustered by day (442 cases, 98 days). In the agitated profile the same slope is +0.67 % with t 0.39.
- **F5:** The calm slope points the same way across the sample, though no single slice is sure on its own.
- **F6:** Large calm falls are where the step-5 size misses most. In the bin z in (-1.5, -0.75], the 5-day excess is -3.25 % (t -2.80). In 2018, calm falls beyond -0.75 units lost a further -5.81 % (t -2.45, n 62). Against 0.22 % per trade, these moves are more than 10 times the cost, while the rise-only unusual move is 0.8 times.

## Ideas
- `038-01.g1_calm-two-sided-swing-continuation` (from F1, F2, F3, F6): In a calm market, the more of its 20-day daily swings a coin's 5-day move spans, the further the coin moves the same way over the next 5 days, for rises and falls alike.
- `038-01.g2_calm-swing-scaled-fall-continues` (from F2, F3, F6): In a calm market, the more of its 20-day daily swings a coin's 5-day fall spans, the more the coin falls over the next 5 days.
- `038-01.g3_calm-ten-day-swing-continuation` (from F4, F1): In a calm market, the more of its 20-day daily swings a coin's 10-day move spans, the further the coin moves the same way over the next 10 days.
- `038-01.g4_choppy-calm-break-continuation` (from F5, F1): In a choppy, calm market, the more of its 20-day daily swings a coin's 5-day move spans, the further the coin moves the same way over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

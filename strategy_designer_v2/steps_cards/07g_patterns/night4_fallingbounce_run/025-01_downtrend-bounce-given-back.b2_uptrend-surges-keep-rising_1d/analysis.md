---
line: 7.g patterns
backtest: 025-01_downtrend-bounce-given-back.b2_uptrend-surges-keep-rising_1d
idea tested: 025-01_downtrend-bounce-given-back.b2_uptrend-surges-keep-rising
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3996 USD
---
## Findings
- **F1:** In coins whose 90-day return is negative, an up-day is given back the next day, and more so the larger it is: the excess 1-day return falls by 0.576 % per unit of the up-day in 20-day standard deviations (t -2.73, 1051 non-overlapping cases). At 3 days the slope is -1.11 % per unit (t -1.86, 353 cases), and at 5 days it disappears (+0.33 %, t 0.29, 183 cases). In coins whose 90-day return is not negative, the same slope is positive: +0.40 % per unit at 1 day (t 2.02, 1146 cases) and +1.25 % at 3 days (t 1.98, 381 cases).
- **F2:** The tested idea's effect sits in the largest up-days of rising coins. With the recorded regime trending, up-days of 1 to 2 usual moves are followed by +1.83 % excess over 5 days (t 2.13, 170 cases), and those above 2 usual moves by +5.53 % (t 2.62, 59 cases). With the regime not trending, the slope on up-days is -0.35 % per unit (t -0.57, 641 cases).
- **F3:** The coin's 90-day direction persists over 5 days only when the coin is calm. In the lowest third of each coin's 20-day volatility, a non-negative 90-day return is followed by +0.90 % excess over 5 days (t 2.39, 505 cases), and a negative one by -0.76 % (t -2.03, 491 cases). In the middle and top thirds, every mean is between -0.47 % and -0.05 % with |t| ≤ 0.93.
- **F4:** The book earns only when it holds large positions, which under vol targeting means calm coins. Held bars in the top quartile of allocation have a next-day excess return of +0.226 % (t 2.40, 2214 bars). The two lowest quartiles have -0.197 % (t -1.74) and -0.173 % (t -1.64).
- **F5:** The book's losses come from a few crashes while it is long. The worst 1 % of position-bars (174 bars, mean allocation 1.14, mean coin move that day -9.55 %) carry 25 % of all its negative position gain. Its worst 2 % of days average -5.19 % against a coin move of -8.49 %, which is consistent with the Calmar of 0.53 failing.
- **F6:** Day-of-week returns look like a pattern but do not stand out from chance. Wednesday's excess 1-day return is negative in all 6 coins (-0.14 % to -0.40 %) and Thursday's is positive in all 6 (+0.11 % to +0.61 %). But averaged across coins per day the t-statistics are only -1.30 and +1.29, Friday's is 2.17, and the Thursday-and-Friday minus Monday-and-Wednesday gap shrinks from +0.18 to +1.76 % before 2022 to -0.13 to +0.63 % after. I propose no idea from it.

## Ideas
- `025-01_downtrend-bounce-given-back.b2_uptrend-surges-keep-rising.g1_downtrend-bounces-fade-overnight` (from F1): In a coin whose 90-day return is negative, a one-day rise is given back over the next day. The larger that rise in units of its 20-day standard deviation of daily returns, the larger the fall over the next day.
- `025-01_downtrend-bounce-given-back.b2_uptrend-surges-keep-rising.g2_calm-coins-keep-trending` (from F3, F4): In a coin whose 20-day standard deviation of daily returns is low against its own past, the direction of its 90-day return continues over the next 5 days. The calmer the coin, the larger the move in that direction.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

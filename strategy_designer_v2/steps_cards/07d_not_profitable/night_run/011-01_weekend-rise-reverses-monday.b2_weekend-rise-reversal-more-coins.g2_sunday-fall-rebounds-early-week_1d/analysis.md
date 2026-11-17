---
line: 7.d not profitable
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g2_sunday-fall-rebounds-early-week_1d
idea tested: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g2_sunday-fall-rebounds-early-week
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4000 USD
---
## Findings
- **F1:** The book barely earns because it holds a position on only 12.4% of days and with a small size (mean allocation 0.37 on the 2665 active Sundays), so its mean daily return is 0.00006 against 0.0015 for holding the coins, even though each active case gains 0.0017 per bar after a mean fee of 0.00043.
- **F2:** The weekend reversal in this data sits mostly on the side the book does not trade: after the 2589 Sunday rises, the next 2-day return is 1.09% below the coin's usual 2-day return (t -7.08), while after the 2665 Sunday falls it is only 0.23% above it (t 1.58).
- **F3:** The sizing puts its weight where the rebound is weakest. In the lowest-volatility tercile, Sunday falls are followed by a -0.25% excess 2-day return (t -1.20) while the allocation is at its highest, 0.51. In the highest-volatility tercile the excess is +1.69% (t 4.71, n 690) but the allocation is only 0.24.
- **F4:** The reversal is graded by weekend volume as the brief says: the slope of the excess 2-day return on the volatility-scaled Sunday return is -0.0183 (t -6.04, n 1302) in the lowest tercile of weekend volume against its 30-day average, -0.0090 (t -3.11) in the middle tercile and -0.0016 (t -0.82) in the highest.
- **F5:** Over all Sundays, the volatility-scaled Sunday return predicts the next 2 days with a slope of -0.0058 (t -4.39, n 4320), but the 2-day weekend return predicts nothing (slope 0.0001, t 0.09), so the information lies in the Sunday bar itself.
- **F6:** The fall side alone does not grow with the size of the fall: the forecast quartiles give excess 2-day returns of -0.34%, +0.23%, +0.76% and +0.28%, and the slope stays below t 1 inside every volatility tercile. The tested slope therefore had t of only 1.12.

## Ideas
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g2_sunday-fall-rebounds-early-week.d1_thin-weekend-sunday-move-reverses` (from F1, F2, F4, F5): A coin's Sunday return (Saturday close to Sunday close, measured against its own 20-day daily volatility) is reversed over the next 2 days, and the larger the Sunday move, the larger the reversal, the more so the lower its Saturday and Sunday volume was against its usual 30-day volume.
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g2_sunday-fall-rebounds-early-week.d2_sunday-rise-fades-early-week` (from F2, F5): A coin that rose on Sunday (its Saturday-close to Sunday-close return, measured against its own recent daily volatility) falls over the next 2 days, and the larger the Sunday rise, the larger the fall.
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g2_sunday-fall-rebounds-early-week.d3_sunday-fall-rebounds-when-volatile` (from F3, F6): A coin that fell on Sunday (its Saturday-close to Sunday-close return, measured against its own recent daily volatility) rises over the next 2 days, and the larger the Sunday fall, the larger the rise, only while the coin's 20-day daily volatility is high against its own past year.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

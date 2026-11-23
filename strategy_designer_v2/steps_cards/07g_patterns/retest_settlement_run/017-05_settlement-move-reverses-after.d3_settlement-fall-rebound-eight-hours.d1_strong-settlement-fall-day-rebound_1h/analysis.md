---
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound_1h
idea tested: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4420 USD
---
## Findings
- **F1:** The large 24-hour fall is what rebounds, whatever the hour. On the non-overlapping 24-bar grid, bars in the bottom decile of the 24-hour return (scaled by the mean absolute 24-hour move of the last 720 bars) are followed by a 24-hour return of +82.6 bp above the coin's normal drift (t 5.21, 1581 cases). The next decile gives only +19.8 bp (t 1.53). The middle and top deciles give between -4 and -26 bp, so the rebound sits in the deepest falls.
- **F2:** That rebound is much larger than the tested idea's. For the bottom two deciles of the 24-hour move, the strength is 0.102 of the coin's usual 24-hour move, against 0.031 for the settlement-fall cases. At +43 to +83 bp per case, the unusual move alone covers the 0.19 % cost of a trade.
- **F3:** The rebound after large 24-hour falls lives almost entirely in high-volatility stretches. When the 1-week hourly volatility over the 1-month volatility is above its median, it is +103.7 bp (t 6.17, 1277 cases); below the median it is -10.3 bp (t -0.74, 1278 cases).
- **F4:** The rebound after large 24-hour falls holds on every coin and in every part of the period:
- **F5:** The rebound after a 2-hour fall is not tied to the settlement clock, which is the brief's third falsifier. The 24-hour excess after a 2-hour fall of 1.5 usual moves or more is:
- **F6:** There is a clock pattern, but at 21:00–23:00 UTC rather than at settlement, and it is too small to trade:
- **F7:** The book earns on weekends: Saturday +15.9 bp (t 4.05) and Sunday +10.8 bp (t 3.25). Its year 2022 was -19.5 bp a day against the coins' -18.0 bp, so it did not shelter from the falling year.

## Ideas
- `017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound.g1_deep-daily-fall-rebounds` (from F1, F2, F4, F5): After a coin falls sharply over 24 hours, it rises over the next 24 hours, and the larger the fall against its usual 24-hour move, the larger the rise, at any hour of the day.
- `017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound.g2_turbulent-fall-rebound` (from F1, F3, F4): When a coin's hourly volatility over the past week is high against its past month, a sharp 24-hour fall is followed by a rise over the next 24 hours, and the larger the fall against its usual 24-hour move, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

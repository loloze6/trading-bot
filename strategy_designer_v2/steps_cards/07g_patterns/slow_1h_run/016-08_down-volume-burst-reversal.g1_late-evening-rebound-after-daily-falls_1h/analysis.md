---
line: 7.g patterns
backtest: 016-08_down-volume-burst-reversal.g1_late-evening-rebound-after-daily-falls_1h
idea tested: 016-08_down-volume-burst-reversal.g1_late-evening-rebound-after-daily-falls
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3979 USD
---
## Findings
- **F1:** Every coin drifts up in the late UTC evening, whatever its past 24 hours did. Hourly returns on bars closing at 21:00 and 22:00 UTC average +5.45bp (t 6.75, n 17403) and +4.36bp (t 5.66, n 17417); no other hour exceeds |t| 3.8. Over those two hours each coin averages +4.2 to +5.5bp (t 3.0 to 4.4), every weekday is positive (t 2.1 to 3.9), 7 of 8 years are positive (2022 is -2.2bp, t -1.4), and 83% of windows have a positive mean.
- **F2:** The book cannot turn the confirmed 2-hour edge into money. Its 7238 trades last 1.0 hour on median and lose 0.095% before fees (t -7.2) and 0.195% after; every coin is negative after fees (-0.11% to -0.27%). The position held over the bar closing at 21:00 gains only +1.87bp (t 2.38, n 7225), the second positive hour (22:00) is not held, and the round-trip fee of about 0.10% is larger than either.
- **F3:** Over a day, a large fall measured against the coin's own volatility is followed by a rebound. On a non-overlapping 24-hour grid, the 24-hour return in units of 30-day volatility has its lowest decile followed by +81.8bp excess over the next 24 hours (t 5.21, n 1596) and its second decile by +29.3bp (t 2.30); deciles 3 to 10 lie between -24 and -4bp. The slope is negative in all 6 coins (t -2.3 to -4.4) and in 7 of 8 years (t +0.54 in 2024).
- **F4:** Among 24-hour falls, how the fall was made matters beyond its size, but not the way the brief expects. Pooled over coins, a regression of the next-24-hour excess return on the fall's size, its log 24-hour/30-day volatility ratio and its largest single hour's share of the summed absolute hourly moves gives:
- **F5:** The negative hours closing at 03:00 UTC (-2.77bp, t -3.80) and 14:00 UTC (-3.56bp, t -3.80) do not hold up year by year. Hour 03 is positive in 2023 to 2025 and hour 14 is positive in 2022 and 2025, so I do not count either as a pattern.

## Ideas
- `016-08_down-volume-burst-reversal.g1_late-evening-rebound-after-daily-falls.g1_late-evening-drift-scaled-by-volatility` (from F1, F2): A coin rises over the 2 hours after the 20:00 UTC close, and the rise is larger the larger the coin's average absolute hourly return over its past 30 days.
- `016-08_down-volume-burst-reversal.g1_late-evening-rebound-after-daily-falls.g2_volatility-scaled-daily-fall-rebound` (from F3, F2): The larger a coin's fall over its past 24 hours, measured in units of its own 30-day volatility, the more the coin rises over the next 24 hours.
- `016-08_down-volume-burst-reversal.g1_late-evening-rebound-after-daily-falls.g3_turbulent-falls-rebound-harder` (from F4): After a 24-hour fall, the higher the coin's 24-hour volatility relative to its 30-day volatility, the more the coin rises over the next 24 hours.
- `016-08_down-volume-burst-reversal.g1_late-evening-rebound-after-daily-falls.g4_spread-out-falls-rebound-more` (from F4): After a 24-hour fall, the more evenly the fall is spread across its hours (the smaller its largest single hour's share of the hourly moves), the more the coin rises over the next 24 hours.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

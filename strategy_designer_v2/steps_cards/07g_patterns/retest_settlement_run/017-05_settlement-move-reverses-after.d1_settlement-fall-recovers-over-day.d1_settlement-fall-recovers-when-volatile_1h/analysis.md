---
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d1_settlement-fall-recovers-when-volatile_1h
idea tested: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d1_settlement-fall-recovers-when-volatile
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4283 USD
---
## Findings
- **F1:** The reversal after a settlement-time move is concentrated around 00:00 UTC and is absent at 16:00. The slope of the excess 24-hour return on the 2-hour fall, one case per day for each close hour, has t 5.2, 8.1 and 5.8 at close hours 0, 1 and 2, but only t 0.5 at hour 16, and stays within |t| 3.2 at every other hour.
- **F2:** At the 01:00 UTC close, the 3-hour move since 22:00 sorts the next 24 hours in a graded way. The deepest-fall decile gains +0.77 % in excess return (t 5.4, n 1653), the next +0.51 % (t 4.2), and the top-rise decile loses -0.42 % (t -3.2). The slope is positive in all six coins (t 2.3 to 5.9) and in 7 of 8 years; 2022 is the exception (t -0.2).
- **F3:** The tested book's forecast pays only at its extreme. Cases with forecast above 5 earn +0.15 % excess over 24 hours (t 2.6, n 8297), while the buckets from 1 to 5 are all negative (-0.14 % to -0.17 %). This matches the idea's whole size, an unusual move of +0.09 % per case, which is 0.4 times the 0.19 % cost of a trade.
- **F4:** A strong 72-hour rise keeps going over the next 72 hours.
- **F5:** A deep 24-hour fall reverses over the next 24 hours, but only in the tail.
- **F6:** The hours at the end of the UTC day carry a clock drift, but it is smaller than the cost of a trade. Hourly returns closing at 22:00 and 23:00 average +0.055 % (t 6.9) and +0.044 % (t 5.8). The 2 hours from 21:00 to 23:00 average +0.08 % to +0.11 %, positive in all six coins (t 3.1 to 4.7) and in 7 of 8 years.
- **F7:** Only the most volatile state shows an excess return. The top quintile of 7-day over 30-day volatility (ratio 1.37) earns +0.28 % excess over 24 hours (t 2.4), while the other four quintiles are between -0.18 % and +0.04 %.

## Ideas
- `017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d1_settlement-fall-recovers-when-volatile.g1_midnight-utc-move-reverses` (from F1, F2, F3): The deeper a coin's fall over the 3 hours into the 01:00 UTC close, measured against its usual 3-hour move, the more it rises over the next 24 hours; the larger its rise over those 3 hours, the more it lags over the next 24 hours.
- `017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d1_settlement-fall-recovers-when-volatile.g2_strong-three-day-run-continues` (from F4): The larger a coin's 72-hour return against its usual 72-hour move, the more it rises over the next 72 hours.
- `017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d1_settlement-fall-recovers-when-volatile.g3_deep-daily-fall-rebounds` (from F5, F7): The deeper a coin's 24-hour fall against its usual 24-hour move, the more it rises over the next 24 hours, and more so the higher its 7-day hourly volatility stands against its 30-day volatility.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

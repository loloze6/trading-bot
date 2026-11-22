---
line: 7.g patterns
backtest: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.b2_large-hourly-rise-continues-daylong_1h
idea tested: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.b2_large-hourly-rise-continues-daylong
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4083 USD
---
## Findings
- **F1:** Hourly returns between 20:00 and 22:00 UTC beat the coin's mean hourly return in both coins. Hour 20 averages +0.045 % (t 4.00) and hour 21 +0.040 % (t 3.69), about 5,840 hours each. These are the only two of 24 hours with a t above 3, so they stand out even after testing every hour. Pooled over both hours, BTC averages +0.037 % (t 3.81, 5,837 hours) and ETH +0.048 % (t 3.92, 5,837 hours).
- **F2:** The 20–22 UTC excess return holds outside any one period. It is positive in 7 of 8 years: from +0.028 % to +0.077 %, with t 1.2 to 3.7. The exception is 2022, at −0.031 % (t −1.45). It is positive on all 7 weekdays: from +0.034 % to +0.053 %, with t 1.5 to 2.8.
- **F3:** The 20–22 UTC excess return is largest after the coin fell over the prior 24 hours. By quartile of the prior 24-hour return it is +0.093 % (t 4.41) in the lowest quartile, +0.035 % (t 3.01) in the second, +0.003 % (t 0.22) in the third and +0.042 % (t 2.46) in the highest. The grading is clear across the lower three quartiles and breaks in the top one.
- **F4:** The opposite holds around the start of the UTC day. Hour 2 averages −0.032 % (t −3.35), hour 1 −0.023 % (t −2.22) and hour 0 −0.023 % (t −1.97). Only hour 2 clears the bar for 24 hours tested.
- **F5:** The tested idea's grading does not show in the bars, at either horizon tested:
- **F6:** Large hours on 2–4 times their usual volume are followed by a rise over 24 hours, whatever their direction:
- **F7:** The book is mostly the market's own exposure:

## Ideas
- `028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.b2_large-hourly-rise-continues-daylong.g1_late-us-hours-rebound-rise` (from F1, F2, F3): Each coin rises more than its usual hourly drift over the 20:00–22:00 UTC hours. The further the coin fell over the past 24 hours, the larger that rise.
- `028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.b2_large-hourly-rise-continues-daylong.g2_early-utc-hours-give-back` (from F4, F1): Each coin falls more than its usual hourly drift over the 00:00–03:00 UTC hours. The larger its rise over the preceding 20:00–00:00 UTC hours, the larger that fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

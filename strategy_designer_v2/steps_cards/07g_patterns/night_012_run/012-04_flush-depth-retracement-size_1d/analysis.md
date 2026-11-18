---
line: 7.g patterns
backtest: 012-04_flush-depth-retracement-size_1d
idea tested: 012-04_flush-depth-retracement-size
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3423 USD
---
## Findings
- **F1:** On down days (bar return below zero), the log of volume over its prior 20-day median predicts the next-day excess return with slope +0.0045 (t 5.28, n 7056 non-overlapping cases); on up days the same slope is +0.0002 (t 0.25, n 7300), so the volume effect sits only on falling days.
- **F2:** The same down-day effect holds over the next 3 days: slope +0.0126 per log unit of volume ratio (t 4.72, n 2245), while up days show −0.0030 (t −1.35, n 2470).
- **F3:** Among down days, next-day excess return rises with the volume-ratio quintile: from −0.05% (bottom quintile, n 1391) to +0.70% (top quintile, n 1400); up days stay flat or negative in every quintile (−0.14% in the top quintile).
- **F4:** The pooled volume slope is positive in every coin at one day (t from 0.69 in BTC to 2.82 in ZEC) but uneven by period: t 1.22 in w1–w12 and t 4.11 in w13–w24, so the effect is stronger in the later windows.
- **F5:** The tested flush filter adds little: sharp falls (z ≤ −2) with volume ≥ 2× and a lower wick ≥ 0.3 average +1.88% excess over 3 days (t 1.78, n 31) against +0.11% for other sharp falls (n 139), and −0.62% over the next day (t −1.06, n 85). The wick shape does not carry the rebound; the volume does.
- **F6:** The lower-wick quintiles do not rank the 3-day excess return in order (−0.02%, +0.31%, −0.50%, −0.35%, +0.53%), so wick length on its own shows no graded pattern.
- **F7:** The book traded on only 1.0% of days (175 active days) with a mean daily return of −0.45% on those days (t −1.46), so the strategy barely sampled the broader down-day volume effect.
- **F8:** Next-day excess return by weekday ranges from −0.30% on Wednesday (t −2.70) to +0.30% on Friday (t 3.76, n about 2480 each), but this is one of many angles examined and has no mechanism behind it.

## Ideas
- `012-04_flush-depth-retracement-size.g1_heavy-volume-down-day-rebound` (from F1, F3, F4, F5): On a day a coin closes lower, the higher that day's volume relative to its median over the prior 20 days, the larger the coin's rise over the next day.
- `012-04_flush-depth-retracement-size.g2_volume-graded-multi-day-selloff-reversal` (from F2, F3, F5): On a day a coin closes lower, the higher that day's volume relative to its median over the prior 20 days, the larger the coin's rise over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

---
line: 7.g patterns
backtest: 010-04_rsi-below-streak-continuation_1d
idea tested: 010-04_rsi-below-streak-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3171 USD
---
## Findings
- **F1:** The tested run length below 50 shows no grading of the coin's later returns. Across the signed run-length quintiles on the 14-day grid, the slope t is 0.49 (n=384). On the daily bars below 50, no run-length bucket has |t| above 1.0. On the 3-day grid none has |t| above 1.24. The short book earned a mean of 0.000108 per bar on 2286 short bars.
- **F2:** Where the pattern sits is the other side: the coin rises after its 14-day RSI has stayed above 50 for about one to four weeks. The next-day return is 0.0056 (t 3.80, n=693) after 6–15 days above 50 and 0.0031 (t 2.08, n=674) after 15–30 days. On the non-overlapping 3-day grid it is 0.0129 (t 2.57, n=231) and 0.0127 (t 2.85, n=223). The first 1–6 days above 50 give only 0.0043 (t 1.19, n=310) on that grid.
- **F3:** Beyond about 30 days above 50 the effect fades. The next-day return is 0.0015 (t 0.83, n=602) and the 3-day grid return is 0.0030 (t 0.56, n=198). At the 14-day horizon the above-50 run terciles are flat: slope t 0.95 and top tercile t 1.18 (n=67). So the pattern belongs to the next few days, not the next two weeks.
- **F4:** The next day's return falls steadily across the septiles of today's return scaled by 30-day volatility. It runs from 0.0046 (t 2.66, n=718) after the largest falls to −0.0013 (t −0.91) after the largest rises. On the 3-day grid the order flips: the top quintile is 0.0064 (t 1.97) and the bottom is 0.0017. I counted this as not standing out against the number of angles I looked at.
- **F5:** Saturday's mean coin return is 0.0028 (t 2.77, n=828). It comes almost entirely from the early years: 0.0051 (t 2.89) up to 2021 and 0.0004 (t 0.47) after. I treated this as a fading or chance pattern. The angles checked also included next-day return by volatility level (no monotone pattern) and the coin's moves around the book's worst and best 2% days (those days are simply the coin's ±7.5% days against the short; the day before and the day after show no |t| above 1.8).

## Ideas
- `010-04_rsi-below-streak-continuation.g1_rsi-above-50-short-horizon-continuation` (from F2, F3, F1): The longer a coin's 14-day RSI has stayed above 50 without a break, within its first month above 50, the higher the coin's return over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

---
line: 7.b inconclusive
backtest: 002-01_sma-golden-cross-upward-drift_1d
idea tested: 002-01_sma-golden-cross-upward-drift
step 5: inconclusive
step 6: not profitable enough
mode: analyst then deducer
explorations: 2
cost: 0.3441 USD
---
## Findings
- **F1:** Among blocks with forecast > 0, the coin's own past 30-day return splits the result in two: after a negative past 30 days the excess 10-bar return is -0.0264 (n=265, t=-3.32), and after a positive one it is +0.0173 (n=359, t=1.68); the two cancel to +0.0005 overall, against +/-0.158 dispersion, giving the flat pooled slope (t=0.37).
- **F2:** The split appears in every coin: within forecast > 0, the down30 mean excess return is negative for all six coins (-0.013 BTC to -0.034 ZEC, t -0.78 to -1.67), and the up30 mean is positive for all six (+0.003 LTC to +0.038 ZEC, t 0.12 to 1.43).
- **F3:** The split is monotonic in past momentum: across past-30-day quintiles within forecast > 0, the mean excess return runs -0.024 (t=-2.00), -0.031 (t=-2.73), +0.002, +0.019 (t=1.54) and +0.027 (t=1.14). The same sign split holds over other look-backs: past 60 days negative gives -0.041 (n=126, t=-3.64) against +0.011 (n=297, t=0.99), and past 10 days negative gives -0.020 (t=-2.57) against +0.016 (t=1.60).
- **F4:** The size of the forecast does not grade returns even where the effect lives: within forecast > 0 with a rising past 30 days, the slope on the forecast is 0.00079 (t=0.52), and the forecast buckets are not monotonic: 0-5 gives -0.0085, 5-10 gives +0.0023, 10-15 gives +0.0105, and 15-20 gives +0.0000.
- **F5:** The raw 50/200 spread does not order returns either: its quintiles give -0.005, -0.005, +0.012, +0.003 and -0.005, the best being the near-zero middle quintile (-31 to +30), and the raw spread's slope has t=-0.18.
- **F6:** The effect moves with the whole market rather than with single coins: 57% of the 10-bar return variance is shared with the cross-section, and relative to the same-day coin average, forecast > 0 blocks earn +0.0003 (t=0.06), with up30 at +0.0021 (t=0.27) and down30 at -0.0046 (t=-0.91).
- **F7:** The result changes by period: the pooled slope is negative in 2020 (t=-2.22) and 2022 (t=-2.42, only 25 active blocks), and the up30 active blocks earn +0.063 in 2021 (t=2.04) but -0.026 in 2023 (t=-2.47) and -0.113 in 2018 (t=-3.12).
- **F8:** Fresh up-crosses are too few to judge: only 52 active blocks follow an inactive one, with a mean excess return of +0.0077 (t=0.45), against +0.0001 for the 780 continuing blocks.

## Ideas
- `002-01_sma-golden-cross-upward-drift.b1_pullback-inside-uptrend-continues` (from F1, F2, F3, F6, F7): While a coin's 50-day SMA is above its 200-day SMA, if the coin's own close-to-close return over the past 30 days is negative, its next 10-day return comes in below its usual 10-day return.
- `002-01_sma-golden-cross-upward-drift.b2_longer-decline-under-golden-cross` (from F3, F1): While a coin's 50-day SMA is above its 200-day SMA, if the coin's return over the past 60 days is negative, its next 10-day return falls further below its usual 10-day return than after a negative past 30 days alone.
- `002-01_sma-golden-cross-upward-drift.b3_golden-cross-needs-momentum` (from F1, F2, F3, F7): While a coin's 50-day SMA is above its 200-day SMA, if the coin's return over the past 30 days is positive, its next 10-day return comes in above its usual 10-day return, and more so in the top quintile of past-30-day return.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

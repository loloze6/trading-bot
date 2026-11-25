---
line: 7.b inconclusive
backtest: 032-02_flat-range-downside-break-recovers_1d
idea tested: 032-02_flat-range-downside-break-recovers
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3963 USD
---
## Findings
- **F1:** Downside breaks in flat coins do not recover; they lean the other way at every horizon past one day. On closes below the prior 60-day low with a 60-day efficiency ratio at or below 0.3, the mean excess return is +1.23 % over 1 day (t 0.77, 81 cases on 35 days), -2.27 % over 5 days (t -0.76, 63 cases), -4.12 % over 10 days (t -1.01, 51 cases on 23 days) and -5.75 % over 20 days (t -0.78, 40 cases). The test's own -1.56 % (t -0.55) is this flat or negative effect, not a positive one too small to show.
- **F2:** The recovery is not graded by depth. On the recorded cases over 10 days, the shallow, mid and deep thirds earn -1.2 % (t -0.29), -3.2 % (t -1.05) and -1.3 % (t -0.22). Across all downside breaks the thirds are +0.7 %, -8.7 % (t -3.44) and -3.1 %. Depth does not order the outcome, which matches the step-5 slope t of 0.73.
- **F3:** The downside effect is mixed across periods and coins, with no part showing a clear recovery.
- **F4:** The mirror case, an upside break in a flat coin, keeps going instead of failing. Closes above the prior 60-day high with an efficiency ratio at or below 0.3 earn:
- **F5:** The upside continuation is graded by distance, but concentrated in time and coins.

## Ideas
- `032-02.b1_flat-range-upside-break-continues` (from F4, F5, F1): In a coin whose price has gone nowhere over the past 60 days, a daily close above the prior 60-day high is followed by a further rise over the next 5 days, and the further that close sits above the old high, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

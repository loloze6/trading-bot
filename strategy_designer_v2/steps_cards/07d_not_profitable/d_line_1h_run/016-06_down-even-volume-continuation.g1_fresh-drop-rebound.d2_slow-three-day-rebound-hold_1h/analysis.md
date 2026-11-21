---
line: 7.d not profitable
backtest: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold_1h
idea tested: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3250 USD
---
## Findings
- **F1:** Fees, not the forecast, sink the book: the positions earn 0.000107 a day before fees but pay 0.001195 a day in fees, on a turnover of 1.10 of the book a day, which leaves a mean daily book return of -0.001114 and a Sharpe of -1.44.
- **F2:** The book trades its signal hour by hour, not over the 3 days the idea is about: the forecast's on-runs last a median 3 hours (mean 8.5, 15930 runs), there are 0.91 new entries a day, and the 58401 trades last a median 5 hours with a mean of -0.386 % before fees and -0.486 % after.
- **F3:** Holding the position set at each non-overlapping 72-hour grid bar for the full 72 hours would have earned a mean allocation × 72-hour return of +0.0034 per case (t 3.48, n 1891 independent cases), so the rebound is real at the 3-day scale but is lost to hourly re-sizing.
- **F4:** The rebound sits only in the deepest 1-day falls: in the fall regime, forecasts of 15–20 are followed by a 72-hour excess of +0.0099 (n 739), while forecasts of 0–15 are followed by -0.0091 (n 1152; Welch t 4.98), and the 0–5, 5–10 and 10–15 buckets are all negative (-0.0088, -0.0054, -0.0142).
- **F5:** Most of the deep-fall rebound comes in the first day: for forecasts of 15–20 the excess is +0.0081 over the first 24 hours and only +0.0022 over hours 24–72, which is why the idea's supporting check failed (late slope 6.0e-05).
- **F6:** The depth of the 3-day fall also sorts what follows: within the regime, the deepest 3-day-fall quartile (below -7.6 %) is followed by a 72-hour excess of +0.0041, and the shallowest (0 to -1.65 %) by -0.0098; the lowest 1-day-return quintile (below -2.8 %) earns +0.0035 in the regime and +0.0122 even outside it (n 217).

## Ideas
- `016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold.d1_daily-set-three-day-drop-rebound` (from F1, F2, F3): When a coin has fallen over the past 3 days, the larger its fall over the last 1 day, the more it rises over the next 3 days, with that rebound set by the day's fall as it stands once the day is done, so that the expected rise stays the same through the hours that follow instead of changing from hour to hour.
- `016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold.d2_deep-drop-only-rebound` (from F4, F5, F1): When a coin has fallen over the past 3 days, the larger its fall over the last 1 day, the more it rises over the next 3 days, only among falls that are large against the coin's usual daily moves, and the rise grows steeply with the fall's size there, with most of it within the first day.
- `016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold.d3_three-day-fall-depth-rebound` (from F6, F3): The larger a coin's fall over the past 3 days, the more it rises over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

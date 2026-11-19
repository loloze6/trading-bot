---
line: 7.b inconclusive
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through_1h
idea tested: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3148 USD
---
## Findings
- **F1:** The main measure falls on the side the idea predicts but just short of the bar: the pooled 72-hour slope is +0.000469 with t 1.90 on 2,837 trending grid cases (1,190 with a positive forecast), and the supporting check passes (top third of positive forecasts minus forecast 0 = +0.0098), so the shortfall is about precision, not direction.
- **F2:** The effect is small against the market's own moves and uneven across slices: the 72-hour excess return has a standard deviation of 0.090; per-coin t runs from -0.78 (LTC) to 2.08 (ETH); per-year t runs from -0.78 (2018) to 3.10 (2020); and per-window t ranges from -1.66 to 3.73 with many near zero, so the six default coins alone give too few independent cases to clear t 2.
- **F3:** The plan's forecast throws away part of the signal: within positive forecasts the 72-hour slope is flat (+0.000015, t 0.04, n 1,190), yet the raw volume ratio predicts the 72-hour excess return with t 2.80 (n 2,837), and its quintiles rise in order (-0.0013, -0.0001, +0.0019, +0.0082, +0.0088), so the standardise-and-clip step dilutes a graded effect.
- **F4:** The effect is clearer at a shorter horizon: on a 24-hour grid the forecast slope has t 3.25 (n 8,577), positive in 62.5 % of windows; the high third of positive forecasts earns +0.0045 excess against -0.0005 at forecast 0; and the slope is positive on 5 of 6 coins (ETH t 2.49, XRP t 2.20, ZEC t 1.81), while at 168 and 336 hours t falls to 1.39 and 0.51.
- **F5:** The rising-month condition is not where the effect lives: the price-recomputed volume ratio predicts the 72-hour excess return about as well on non-trending grid cases (slope 0.0062, t 2.91, n 2,305) as the raw ratio does on trending ones (slope 0.0068, t 2.80), and at 24 hours it also holds off-regime (t 2.70, n 7,120).

## Ideas
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through.b1_heavy-volume-follow-through-more-coins` (from F1, F2): While a coin's 30-day return is positive, the higher its daily volume relative to its own 20-day average volume, the higher its return over the next 3 days.
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through.b2_heavy-volume-precedes-gains` (from F3, F5): The higher a coin's daily volume relative to its own 20-day average volume, the higher its return over the next 3 days, whether its 30-day return is rising or falling.
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through.b3_heavy-volume-next-day-follow-through` (from F4): While a coin's 30-day return is positive, the higher its daily volume relative to its own 20-day average volume, the higher its return over the next 1 day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
